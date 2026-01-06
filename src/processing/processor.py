import rasterio
from rasterio.enums import Resampling
import numpy as np
import os
import matplotlib.pyplot as plt

# 1. 路径配置
DATA_DIR = "data/images"
OUTPUT_DIR = "data/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

B04_PATH = os.path.join(DATA_DIR, "SJER_B04_10m.jp2")  # Red
B08_PATH = os.path.join(DATA_DIR, "SJER_B08_10m.jp2")  # NIR
B11_PATH = os.path.join(DATA_DIR, "SJER_B11_20m.jp2")  # SWIR

def load_and_align_band(target_meta, file_path):
    """重采样并对齐波段"""
    with rasterio.open(file_path) as src:
        data = src.read(
            out_shape=(target_meta['count'], target_meta['height'], target_meta['width']),
            resampling=Resampling.bilinear
        )
        return data[0].astype('float32') / 10000.0

def process_eco_indices():
    print("🧪 启动 PineGuard 多维特征提取器 (优化显示版)...")

    with rasterio.open(B04_PATH) as b04_src:
        meta_10m = b04_src.meta.copy()
        red = b04_src.read(1).astype('float32') / 10000.0
        nir = load_and_align_band(meta_10m, B08_PATH)
        swir = load_and_align_band(meta_10m, B11_PATH)

    # 2. 核心指数计算
    print("🧮 计算物理指标...")
    np.seterr(divide='ignore', invalid='ignore')
    
    # NDVI = (NIR - Red) / (NIR + Red)
    ndvi = (nir - red) / (nir + red)
    # NDWI = (NIR - SWIR) / (NIR + SWIR)
    ndwi = (nir - swir) / (nir + swir)

    # 清理无效值
    ndvi = np.nan_to_num(ndvi, nan=0.0)
    ndwi = np.nan_to_num(ndwi, nan=0.0)

    # 3. 保存地理空间矩阵 (用于后续 AI 训练)
    meta_10m.update(dtype=rasterio.float32, count=1, driver='GTiff')
    with rasterio.open(os.path.join(OUTPUT_DIR, "SJER_NDVI.tif"), 'w', **meta_10m) as dst:
        dst.write(ndvi, 1)
    with rasterio.open(os.path.join(OUTPUT_DIR, "SJER_NDWI.tif"), 'w', **meta_10m) as dst:
        dst.write(ndwi, 1)

    # 4. 优化可视化 (针对 10 月加州干旱季进行拉伸)
    print("🖼️ 生成针对性风险对比图...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # --- 左图：NDVI (植被活力) ---
    # 针对你测出的 0.24 均值，我们将 0.5 设为“最绿”，让细节浮现
    im1 = ax1.imshow(ndvi, cmap='RdYlGn', vmin=0.1, vmax=0.5)
    ax1.set_title('Forest Vitality (NDVI)\n[Optimized for Dry Season]')
    plt.colorbar(im1, ax=ax1, label='Vegetation Index')

    # --- 右图：NDWI (含水量) ---
    # NDWI 在干旱季通常较低，我们将 0.4 设为深蓝上限
    im2 = ax2.imshow(ndwi, cmap='Blues', vmin=0, vmax=0.4)
    ax2.set_title('Water Content (NDWI)\n[Drought Stress Level]')
    plt.colorbar(im2, ax=ax2, label='Moisture Index')

    vis_path = os.path.join(OUTPUT_DIR, "SJER_Risk_Dual_Analysis.png")
    plt.savefig(vis_path, dpi=300, bbox_inches='tight')
    print(f"✅ 处理完成！请查看: {vis_path}")

if __name__ == "__main__":
    process_eco_indices()