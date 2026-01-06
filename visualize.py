import requests
import folium
from folium.plugins import SideBySideLayers

def get_data(month):
    # 从你的后端 API 获取指定月份的数据
    url = f"http://127.0.0.1:8000/analyze/{month}"
    return requests.get(url).json()

# 1. 创建基础地图
m = folium.Map(location=[37.11, -119.74], zoom_start=11)

# 2. 创建左侧图层 (5月 - 爆发初期)
left_layer = folium.FeatureGroup(name="May 2025")
may_data = get_data("05")
for loc in may_data["locations"]:
    folium.CircleMarker(
        [loc["latitude"], loc["longitude"]],
        radius=8, color="green", fill=True,
        popup=f"May Stress: {loc['stress_score']}"
    ).add_to(left_layer)

# 3. 创建右侧图层 (10月 - 扩散期)
right_layer = folium.FeatureGroup(name=" October 2025")
oct_data = get_data("10")
for loc in oct_data["locations"]:
    folium.CircleMarker(
        [loc["latitude"], loc["longitude"]],
        radius=8, color="red", fill=True,
        popup=f"Oct Stress: {loc['stress_score']}"
    ).add_to(right_layer)

# 4. 把图层添加到地图
left_layer.add_to(m)
right_layer.add_to(m)

# 5. 加上那个酷炫的滑动条
SideBySideLayers(left_layer, right_layer).add_to(m)

m.save("comparison_map.html")
print("🔥 搞定！对比地图已生成：comparison_map.html")