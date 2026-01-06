import os
import requests
import zipfile

# 1. 配置参数
# 这是你之前成功下载的 2024-10-12 数据链接
DATA_URL = "https://zipper.dataspace.copernicus.eu/v1/Products(1190457d-60a3-4835-80da-33161c699912)/$value"
RAW_DIR = "data/raw"
IMG_DIR = "data/images"
ZIP_PATH = os.path.join(RAW_DIR, "scene.zip")

# 定义我们需要提取的目标波段及其所在的分辨率文件夹
TARGET_BANDS = {
    "B04": "R10m",  # Red (10m)
    "B08": "R10m",  # NIR (10m)
    "B11": "R20m"   # SWIR (20m) - 用于计算 NDWI
}

def download_data():
    os.makedirs(RAW_DIR, exist_ok=True)
    if os.path.exists(ZIP_PATH):
        print(f"📦 {ZIP_PATH} 已存在，跳过下载。")
        return

    print(f"📥 正在启动全量下载 (约 1.1GB)...")
    # 注意：在实际工程中，这里通常需要 CDSE 的 Access Token
    # 如果链接失效，脚本会报错，届时需更新 Token
    response = requests.get(DATA_URL, stream=True)
    if response.status_code == 200:
        with open(ZIP_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ ZIP 包已下载至: {ZIP_PATH}")
    else:
        print(f"❌ 下载失败，状态码: {response.status_code}。请检查 Token 是否过期。")

def extract_bands():
    os.makedirs(IMG_DIR, exist_ok=True)
    print(f"🔓 正在扫描 ZIP 内部结构并提取核心波段...")

    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        all_files = zip_ref.namelist()
        
        for band, res_folder in TARGET_BANDS.items():
            # 搜索匹配特定波段和分辨率路径的文件
            # 例如搜索包含 'IMG_DATA/R10m/' 和 '_B04_10m.jp2' 的路径
            match = [f for f in all_files if f"{res_folder}/" in f and f"_{band}_{res_folder[1:]}.jp2" in f]
            
            if match:
                source_path = match[0]
                # 统一重命名为简单格式：SJER_Bxx_xxm.jp2
                target_name = f"SJER_{band}_{res_folder[1:]}.jp2"
                target_path = os.path.join(IMG_DIR, target_name)
                
                with zip_ref.open(source_path) as source, open(target_path, 'wb') as target:
                    target.write(source.read())
                print(f"✨ 已提取 {band}: {target_name}")
            else:
                print(f"⚠️ 未找到波段 {band} 在文件夹 {res_folder} 中。")

if __name__ == "__main__":
    # 执行下载（如果已存在则跳过）
    download_data()
    # 执行精准提取
    extract_bands()
    print("\n🎊 PineGuard 数据准备就绪！包含 NDVI 和 NDWI 所需的全部波段。")