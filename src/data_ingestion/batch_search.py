import os  # <--- 刚才漏掉的罪魁祸首在此
import requests
import json

# SJER 站点的中心坐标
SJER_COORDS = "-119.74 37.11" 

def search_sentinel_data(start_date, end_date):
    print(f"🔍 正在搜索 SJER 站点影像 ({start_date} 至 {end_date})...")
    base_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
    
    query_filter = (
        f"Collection/Name eq 'SENTINEL-2' and "
        f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/Value eq 'S2MSI2A') and "
        f"OData.CSC.Intersects(area=geography'SRID=4326;POINT({SJER_COORDS})') and "
        f"ContentDate/Start gt {start_date}T00:00:00.000Z and "
        f"ContentDate/Start lt {end_date}T00:00:00.000Z and "
        f"Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/Value lt 5.0)"
    )
    
    params = {"$filter": query_filter, "$top": 10, "$orderby": "ContentDate/Start asc"}

    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"❌ 搜索失败: {response.text}")
            return []

        data = response.json()
        products = data.get('value', [])
        
        if not products:
            print("📭 未找到高质量影像。")
            return []

        print(f"✨ 找到 {len(products)} 个高质量时间点数据！\n")
        search_results = []
        for p in products:
            p_id = p['Id']
            p_date = p['ContentDate']['Start'].split('T')[0]
            print(f"📅 捕获日期: {p_date} | ID: {p_id[:8]}...")
            search_results.append({"id": p_id, "date": p_date})
        return search_results

    except Exception as e:
        print(f"💥 错误: {e}")
        return []

if __name__ == "__main__":
    results = search_sentinel_data("2024-05-01", "2024-11-30")
    if results:
        # 现在 os 已经 import 了，不会再报错了
        os.makedirs("data", exist_ok=True)
        with open("data/search_results.json", "w") as f:
            json.dump(results, f, indent=4)
        print(f"\n💾 搜索结果已成功保存至 data/search_results.json")