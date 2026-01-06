import os
import json
import requests
import zipfile
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

SEARCH_RESULTS = "data/search_results.json"
RAW_DIR = "data/raw"
IMG_DIR = "data/images"
TARGET_BANDS = {"B04": "R10m", "B08": "R10m", "B11": "R20m"}

def get_access_token():
    username = os.getenv("CDSE_USERNAME")
    password = os.getenv("CDSE_PASSWORD")

    if not username or not password:
        print(f"❌ 错误: .env 文件中缺少 CDSE_USERNAME 或 CDSE_PASSWORD")
        return None

    print(f"🔐 正在验证账号: {username} ...")
    
    # 认证服务器不需要 /odata
    token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    try:
        r = requests.post(token_url, data=data)
        if r.status_code == 200:
            return r.json()["access_token"]
        else:
            print(f"❌ 认证失败: {r.status_code}")
            return None
    except Exception as e:
        print(f"❌ 网络错误: {e}")
        return None

def download_baseline_data():
    if not os.path.exists(SEARCH_RESULTS):
        print("❌ 找不到 search_results.json")
        return

    with open(SEARCH_RESULTS, 'r') as f:
        products = json.load(f)
    
    # 锁定 5月10日 数据
    baseline_prod = products[0] 
    p_id = baseline_prod['id']
    p_date = baseline_prod['date']
    
    print(f"🎯 目标数据: {p_date} (ID: {p_id})")
    
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)

    zip_name = f"SJER_{p_date}.zip"
    zip_path = os.path.join(RAW_DIR, zip_name)
    
    if os.path.exists(zip_path):
        print(f"📦 文件已存在: {zip_path}")
    else:
        token = get_access_token()
        if not token:
            return

        print(f"📥 开始下载 (修正 URL 版)...")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 👇 核心修复：加上了 /odata
        url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({p_id})/$value"
        
        try:
            with requests.get(url, headers=headers, stream=True) as r:
                if r.status_code == 200:
                    total_size = int(r.headers.get('content-length', 0))
                    downloaded = 0
                    print(f"   文件大小: {total_size / (1024*1024):.2f} MB")
                    
                    with open(zip_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024*1024): 
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if downloaded % (50 * 1024 * 1024) < 1024*1024: 
                                    print(f"   ... {downloaded // (1024*1024)} MB / {total_size // (1024*1024)} MB")
                    print("✅ 下载完成！")
                else:
                    print(f"❌ 下载失败 (HTTP {r.status_code})")
                    print(f"   服务器返回: {r.text[:200]}") # 打印错误详情
                    return
        except Exception as e:
            print(f"❌ 下载中断: {e}")
            if os.path.exists(zip_path):
                os.remove(zip_path) # 删除坏文件
            return

    # 解压提取
    print(f"🔓 提取波段中...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            all_files = zip_ref.namelist()
            count = 0
            for band, res in TARGET_BANDS.items():
                match = [f for f in all_files if f"{res}/" in f and f"_{band}_{res[1:]}.jp2" in f]
                if match:
                    target_name = f"SJER_{p_date}_{band}_{res[1:]}.jp2"
                    target_path = os.path.join(IMG_DIR, target_name)
                    if not os.path.exists(target_path):
                        with zip_ref.open(match[0]) as source, open(target_path, 'wb') as target:
                            target.write(source.read())
                        print(f"   ✨ 已提取: {target_name}")
                        count += 1
                    else:
                        print(f"   ⏩ 已存在: {target_name}")
                        count += 1
            
            if count == 0:
                print("⚠️  警告: ZIP 包里没找到对应的波段文件！可能是 Level-1C 格式而非 Level-2A。")

    except zipfile.BadZipFile:
        print("❌ ZIP 文件损坏。")

if __name__ == "__main__":
    download_baseline_data()