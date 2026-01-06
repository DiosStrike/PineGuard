import rasterio
from rasterio.warp import transform as warp_transform
import numpy as np
import matplotlib.pyplot as plt
import os

# === 路径配置 ===
IMG_DIR = "data/images"
OUT_DIR = "data/outputs"
MAY_NIR = os.path.join(IMG_DIR, "SJER_2024-05-10_B08_10m.jp2")
MAY_SWIR = os.path.join(IMG_DIR, "SJER_2024-05-10_B11_20m.jp2")
MAY_RED = os.path.join(IMG_DIR, "SJER_2024-05-10_B04_10m.jp2") # 5月红光波段
OCT_NIR = os.path.join(IMG_DIR, "SJER_B08_10m.jp2") 
OCT_SWIR = os.path.join(IMG_DIR, "SJER_B11_20m.jp2")
OCT_RED = os.path.join(IMG_DIR, "SJER_B04_10m.jp2") # 10月红光波段 (请确认文件名是否存在)

# 如果你没有下载 B04，脚本会自动处理
# 修正：我们之前的 downloader 好像只保存了 B04, B08, B11，所以应该都有！

# === 🎯 嫌疑犯坐标 (你刚刚查的那个点) ===
TARGET_LAT = 37.135799
TARGET_LON = -119.752751
WINDOW_SIZE = 40 # 查看周围 40x40 像素 (约400x400米)

def get_crop(nir_path, red_path, swir_path, label):
    """读取并裁剪出目标点周围的小图"""
    if not os.path.exists(nir_path) or not os.path.exists(red_path):
        print(f"❌ 缺少波段文件: {label}")
        return None

    with rasterio.open(nir_path) as src:
        # 1. 坐标转换：Lat/Lon -> 像素行列
        from rasterio.warp import transform as warp_transform
        xs, ys = warp_transform({'init': 'EPSG:4326'}, src.crs, [TARGET_LON], [TARGET_LAT])
        row, col = src.index(xs[0], ys[0])
        
        # 2. 定义窗口
        r_start = max(0, row - WINDOW_SIZE // 2)
        r_end = r_start + WINDOW_SIZE
        c_start = max(0, col - WINDOW_SIZE // 2)
        c_end = c_start + WINDOW_SIZE
        
        window = rasterio.windows.Window(c_start, r_start, WINDOW_SIZE, WINDOW_SIZE)
        
        # 3. 读取数据 (归一化到 0-1)
        nir = src.read(1, window=window).astype('float32') / 4000.0 # 4000是一个经验亮度值
        
    with rasterio.open(red_path) as src:
        red = src.read(1, window=window).astype('float32') / 4000.0
        
    # 构建假彩色图像 (NIR, Red, Green_substitute)
    # 通常假彩色标准是: R=NIR, G=Red, B=Green
    # 但我们没下载 Green，可以用 Red 代替 B，或者全黑
    # 更好的方案：R=NIR (植被强), G=Red (土壤), B=Red (土壤) -> 植被会变红，土会变灰
    
    img = np.dstack((nir, red, red)) 
    
    # 简单的亮度增强
    img = np.clip(img * 1.5, 0, 1)
    
    return img

def main():
    print(f"🕵️‍♂️ 正在调取卫星监控录像: {TARGET_LAT}, {TARGET_LON}")

    # 1. 生成 5月 图像
    img_may = get_crop(MAY_NIR, MAY_RED, MAY_SWIR, "May")
    
    # 2. 生成 10月 图像
    img_oct = get_crop(OCT_NIR, OCT_RED, OCT_SWIR, "Oct")

    if img_may is None or img_oct is None:
        print("❌ 无法生成对比图，缺文件。")
        return

    # 3. 可视化对比
    plt.figure(figsize=(10, 5))
    
    # 十字准星位置
    center = WINDOW_SIZE // 2
    
    plt.subplot(1, 2, 1)
    plt.imshow(img_may)
    plt.scatter([center], [center], c='yellow', marker='+', s=100, linewidth=2) # 标记中心
    plt.title("2024-05-10 (Wet Season)\nRed = Healthy Vegetation")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(img_oct)
    plt.scatter([center], [center], c='yellow', marker='+', s=100, linewidth=2)
    plt.title("2024-10-12 (Dry Season)\nGrey/Dark = Dead/Soil")
    plt.axis('off')
    
    save_path = os.path.join(OUT_DIR, "PineGuard_Visual_Verification.png")
    plt.savefig(save_path, dpi=150)
    print(f"✅ 视觉验证图已生成: {save_path}")
    print("💡 读图指南: 左图如果中心是亮红色的，说明那时候绝对有植物！右图如果变灰暗，说明确实消失了。")

if __name__ == "__main__":
    main()