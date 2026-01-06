import rasterio
from rasterio.warp import transform as warp_transform
import numpy as np
import pandas as pd
import os

# === 路径配置 (保持不变) ===
# 注意：在 API 模式下，我们通常使用相对路径或环境变量，这里暂时保持相对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMG_DIR = os.path.join(BASE_DIR, "data", "images")
OUT_DIR = os.path.join(BASE_DIR, "data", "outputs")

# 5月数据
MAY_NIR  = os.path.join(IMG_DIR, "SJER_2024-05-10_B08_10m.jp2")
MAY_SWIR = os.path.join(IMG_DIR, "SJER_2024-05-10_B11_20m.jp2")
MAY_RED  = os.path.join(IMG_DIR, "SJER_2024-05-10_B04_10m.jp2") 

# 10月数据
OCT_NIR  = os.path.join(IMG_DIR, "SJER_B08_10m.jp2") 
OCT_SWIR = os.path.join(IMG_DIR, "SJER_B11_20m.jp2")
OCT_RED  = os.path.join(IMG_DIR, "SJER_B04_10m.jp2") 

# === 帮助函数 ===
def read_band(path, match_shape=None):
    if not os.path.exists(path): 
        print(f"❌ 警告: 找不到文件 {path}")
        return None, None, None
        
    with rasterio.open(path) as src:
        from rasterio.enums import Resampling
        if match_shape:
            data = src.read(1, out_shape=match_shape, resampling=Resampling.bilinear).astype('float32')
        else:
            data = src.read(1).astype('float32')
        
        # 归一化处理
        if np.nanmax(data) > 1.0:
            data = data / 10000.0
            
        return data, src.transform, src.crs

# === ⭐️ 核心改造点：封装成可调用的函数 ===
def analyze_region(target_lat=37.11, target_lon=-119.74, radius_km=15.0):
    """
    供 API 调用的主函数。
    返回: List[Dict] (包含受压树木的列表)
    """
    print(f"🚀 [Core Engine] 启动分析: Lat={target_lat}, Lon={target_lon}, Radius={radius_km}km")

    # 1. 加载数据
    nir_may, transform, crs = read_band(MAY_NIR)
    # 如果主文件读不到，直接返回空列表
    if nir_may is None: return []

    swir_may, _, _ = read_band(MAY_SWIR, match_shape=nir_may.shape)
    red_may, _, _  = read_band(MAY_RED, match_shape=nir_may.shape)
    nir_oct, _, _ = read_band(OCT_NIR)
    swir_oct, _, _ = read_band(OCT_SWIR, match_shape=nir_may.shape)
    red_oct, _, _ = read_band(OCT_RED, match_shape=nir_may.shape)

    if red_may is None or red_oct is None:
        print("❌ 错误: 缺少必要的波段文件")
        return []

    # 2. 计算指标
    with np.errstate(divide='ignore', invalid='ignore'):
        ndwi_may = (nir_may - swir_may) / (nir_may + swir_may)
        ndvi_may = (nir_may - red_may) / (nir_may + red_may)
        ndwi_oct = (nir_oct - swir_oct) / (nir_oct + swir_oct)
        ndvi_oct = (nir_oct - red_oct) / (nir_oct + red_oct)
        
        # 填充 NaN
        ndwi_may = np.nan_to_num(ndwi_may, nan=-1)
        ndvi_may = np.nan_to_num(ndvi_may, nan=-1)
        ndwi_oct = np.nan_to_num(ndwi_oct, nan=-1)
        ndvi_oct = np.nan_to_num(ndvi_oct, nan=-1)

    # 3. 地理围栏 (使用传入的 lat, lon, radius)
    center_x_list, center_y_list = warp_transform({'init': 'EPSG:4326'}, crs, [target_lon], [target_lat])
    center_row, center_col = ~transform * (center_x_list[0], center_y_list[0])
    center_row, center_col = int(center_row), int(center_col)
    
    height, width = ndwi_may.shape
    Y, X = np.ogrid[:height, :width]
    dist_from_center = np.sqrt((X - center_col)**2 + (Y - center_row)**2)
    # 将 km 转为像素距离 (Sentinel-2 10m 分辨率)
    roi_mask = dist_from_center <= ((radius_km * 1000) / 10.0)

    # 4. 应用过滤器 (保持你调教好的完美参数)
    is_vegetation = (ndvi_may > 0.45) & (red_may < 0.18)
    structure_exists = (ndvi_oct > 0.30)
    not_water = (ndwi_may < 0.25)
    not_sand_ndwi = (ndwi_may > 0.0) 
    not_bright_soil = (swir_may < 0.25)
    
    candidate_mask = roi_mask & is_vegetation & structure_exists & not_water & not_sand_ndwi & not_bright_soil
    
    # 5. 计算压力
    delta_ndwi = ndwi_may - ndwi_oct
    valid_range_mask = candidate_mask & (delta_ndwi > 0.05) & (delta_ndwi < 0.40)
    valid_deltas = delta_ndwi[valid_range_mask]
    
    results_list = []

    if valid_deltas.size > 0:
        mean_val = np.nanmean(valid_deltas)
        std_val = np.nanstd(valid_deltas)
        
        # 阈值逻辑
        dynamic_threshold = mean_val + (2 * std_val)
        final_threshold = max(dynamic_threshold, 0.08)
        final_threshold = min(final_threshold, 0.3)
        
        outbreak_mask = valid_range_mask & (delta_ndwi > final_threshold)
        rows, cols = np.where(outbreak_mask)
        
        # 坐标转换与结果打包
        if len(rows) > 0:
            xs, ys = rasterio.transform.xy(transform, rows, cols, offset='center')
            lons, lats = warp_transform(crs, {'init': 'EPSG:4326'}, xs, ys)
            
            for r, c, lon, lat in zip(rows, cols, lons, lats):
                # 构造符合 JSON 格式的字典
                results_list.append({
                    "latitude": round(lat, 6),
                    "longitude": round(lon, 6),
                    "stress_score": round(float(delta_ndwi[r, c]), 4),
                    "condition": "Water Stressed"
                })

    print(f"✅ 分析完成，发现 {len(results_list)} 个风险点。")
    return results_list

# === 保持脚本可独立运行 (方便调试) ===
if __name__ == "__main__":
    # 手动运行时，还是把结果存成 CSV
    results = analyze_region()
    
    if results:
        print("🔄 [手动模式] 正在导出 CSV...")
        df = pd.DataFrame(results)
        # 将 key 转换为 CSV 友好的列名
        df.columns = ["Latitude", "Longitude", "Stress_Score", "Condition"]
        csv_path = os.path.join(OUT_DIR, "PineGuard_Local_Outbreak.csv")
        df.to_csv(csv_path, index=False)
        print(f"📄 CSV 已保存: {csv_path}")
        print(df.head())
    else:
        print("✅ 森林健康，无风险点。")