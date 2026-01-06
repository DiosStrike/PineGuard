import folium
import pandas as pd
import os
import math

# === 配置 ===
CSV_PATH = "data/outputs/PineGuard_Local_Outbreak.csv"
OUT_HTML = "data/outputs/PineGuard_Stress_Map.html"

# SJER 区域中心
CENTER_LAT = 37.11
CENTER_LON = -119.74
DEFAULT_RADIUS = 15000  # 默认分析半径 (米)

def get_color(score):
    if score > 0.28:
        return 'red'
    else:
        return 'orange'

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    计算两点间的地球表面距离 (单位: 米)
    用于自动计算最远的点离中心有多远
    """
    R = 6371000  # 地球半径 (米)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def main():
    print("🗺️ 正在生成 [自动适配版] 压力分布图...")
    
    if not os.path.exists(CSV_PATH):
        print("❌ 找不到 CSV 文件。")
        return

    df = pd.read_csv(CSV_PATH)
    print(f"📊 加载了 {len(df)} 个受压点。")

    # 1. 计算最大距离，决定圈要画多大
    max_dist = 0
    for _, row in df.iterrows():
        dist = haversine_distance(CENTER_LAT, CENTER_LON, row['Latitude'], row['Longitude'])
        if dist > max_dist:
            max_dist = dist
            
    print(f"📏 最远的点距离中心: {max_dist:.2f} 米")
    
    # 设定视觉半径：取 (最大距离 + 1000米缓冲) 和 (默认15km) 中的较大者
    # 这样保证圈永远够大，能包住所有的点
    visual_radius = max(DEFAULT_RADIUS, max_dist + 1000)
    print(f"🎨 动态调整绿圈半径为: {visual_radius:.2f} 米")

    # 2. 创建地图
    m = folium.Map(location=[CENTER_LAT, CENTER_LON], zoom_start=11, tiles=None)

    # 卫星底图
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite (Esri)',
        overlay=False,
        control=True
    ).add_to(m)

    # 街道底图
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='Street Map',
        overlay=False,
        control=True
    ).add_to(m)

    # 3. 标记地理围栏 (使用动态半径)
    folium.Circle(
        location=[CENTER_LAT, CENTER_LON],
        radius=visual_radius, 
        color='#00ff00', # 亮绿色
        weight=2,
        fill=False,
        popup=f'Analysis Boundary (Auto-Fit: {visual_radius/1000:.1f}km)'
    ).add_to(m)

    # 4. 撒点
    outbreak_group = folium.FeatureGroup(name="Stressed Trees")
    
    for _, row in df.iterrows():
        lat = row['Latitude']
        lon = row['Longitude']
        score = row['Stress_Score']
        
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin: 0; color: orange;">⚠️ Water Stress Signal</h4>
            <hr>
            <b>Stress Score:</b> {score:.4f}<br>
            <b>Status:</b> Needs Inspection<br>
            <br>
            <i>Lat: {lat}<br>Lon: {lon}</i>
        </div>
        """
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=get_color(score),
            fill=True,
            fill_color=get_color(score),
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(outbreak_group)
    
    outbreak_group.add_to(m)
    folium.LayerControl().add_to(m)

    m.save(OUT_HTML)
    print(f"✅ 最终地图已生成: {OUT_HTML}")
    print("👉 这次绿圈会自动变大，绝对能包住那个点！")

if __name__ == "__main__":
    main()