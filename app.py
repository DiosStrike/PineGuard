import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import time

# 1. 页面配置
st.set_page_config(page_title="PineGuard Strategic Analysis", layout="wide")

# 工业级 CSS 注入
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    .signature { position: absolute; top: 10px; right: 10px; color: #8B949E; font-family: 'Courier New', monospace; font-size: 0.9rem; z-index: 999; }
    .metric-container { display: flex; justify-content: space-between; margin-bottom: 25px; gap: 15px; }
    .metric-card { background-color: #161B22; border: 1px solid #30363D; padding: 20px; border-radius: 6px; flex: 1; }
    .status-light { height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 8px; }
    .metric-label { color: #8B949E; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { color: #C9D1D9; font-size: 1.8rem; font-weight: 700; font-family: 'Courier New', monospace; }
    </style>
    <div class="signature">Author: Tanghao Chen (Dios)</div>
    """, unsafe_allow_html=True)

st.title("PineGuard: Strategic Spatio-Temporal Analysis")
st.markdown("---")

# --- 侧边栏 ---
st.sidebar.header("Operational Module")
module = st.sidebar.radio("Select System Mode", ["Historical Observation", "Strategic Projection"])

if 'obs_year' not in st.session_state: st.session_state.obs_year = 1984
if 'proj_year' not in st.session_state: st.session_state.proj_year = 2026
if 'playing' not in st.session_state: st.session_state.playing = False

# 配色配置
if module == "Historical Observation":
    st.sidebar.subheader("Observation Control")
    year = st.sidebar.slider("Historical Year", 1984, 2025, value=st.session_state.obs_year)
    st.session_state.obs_year = year
    point_color = "#E63946"
    heatmap_gradient = {0.2: '#0000FF', 0.4: '#00FFFF', 0.6: '#FFFF00', 0.9: '#FF0000'}
    mode_tag = "OBSERVATION"
else:
    st.sidebar.subheader("Projection Settings")
    year = st.sidebar.slider("Projection Year", 2026, 2045, value=st.session_state.proj_year)
    st.session_state.proj_year = year
    point_color = "#00D4FF"
    heatmap_gradient = {0.1: '#01012b', 0.3: '#0000FF', 0.6: '#00D4FF', 1.0: '#FFFFFF'}
    mode_tag = "STRATEGIC PROJECTION"

# Play 逻辑：点击必重置
btn_col1, btn_col2 = st.sidebar.columns(2)
if btn_col1.button("Play"):
    if module == "Historical Observation": st.session_state.obs_year = 1984
    else: st.session_state.proj_year = 2026
    st.session_state.playing = True
    st.rerun()

if btn_col2.button("Pause"):
    st.session_state.playing = False

show_heatmap = st.sidebar.checkbox("Enable Heatmap", value=True)
map_style = st.sidebar.selectbox("Base Layer", ["Satellite (Google)", "Terrain (OSM)"])

try:
    # 模型训练
    stats_res = requests.get("http://127.0.0.1:8000/stats/annual_outbreak_counts").json()
    df_stats = pd.DataFrame(stats_res)
    model = LinearRegression().fit(df_stats[['year']], df_stats['outbreak_count'])
    
    center = [37.1174, -119.6043]
    display_year = st.session_state.obs_year if module == "Historical Observation" else st.session_state.proj_year

    # 数据获取/预测逻辑
    if module == "Historical Observation":
        data = requests.get(f"http://127.0.0.1:8000/analyze/{display_year}").json()
        locations = data["locations"]
        count = data["outbreak_count"]
    else:
        count = int(model.predict([[display_year]])[0])
        np.random.seed(display_year)
        spread = 0.08 + (display_year - 2025) * 0.005
        lats = np.random.uniform(center[0]-spread, center[0]+spread, count)
        lons = np.random.uniform(center[1]-spread, center[1]+spread, count)
        scores = np.random.uniform(0.4, 0.9, count)
        locations = [{"latitude": lat, "longitude": lon, "stress_score": score} for lat, lon, score in zip(lats, lons, scores)]

    # --- 新增分析逻辑 ---
    # 1. 核心爆发点检测 (Hotspot Detection)
    hotspot = max(locations, key=lambda x: x['stress_score']) if locations else None
    # 2. 扩散速度评估 (Spread Velocity)
    velocity = 1.2 + (display_year - 1984) * 0.05 if display_year > 1984 else 0.0

    # 风险判定
    if count < 15: risk_lvl, risk_col = "STABLE", "#28A745"
    elif count < 80: risk_lvl, risk_col = "WATCH", "#FFC107"
    else: risk_lvl, risk_col = "ALERT", "#DC3545"

    # 指标卡
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-card"><div class="metric-label">Observation Year</div><div class="metric-value">{display_year}</div></div>
            <div class="metric-card"><div class="metric-label">Anomalies Detected</div><div class="metric-value">{count}</div></div>
            <div class="metric-card"><div class="metric-label">Spread Velocity</div><div class="metric-value">{velocity:.1f} km/yr</div></div>
            <div class="metric-card">
                <div class="metric-label">Security Status</div>
                <div class="metric-value"><span class="status-light" style="background-color:{risk_col};"></span>{risk_lvl}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_map, col_data = st.columns([3, 1.2])

    with col_map:
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}' if map_style == "Satellite (Google)" else 'OpenStreetMap'
        m = folium.Map(location=center, zoom_start=10, tiles=tiles, attr='PineGuard GIS')
        
        heat_data = [[l["latitude"], l["longitude"], l["stress_score"]] for l in locations]
        if show_heatmap and heat_data:
            HeatMap(heat_data, radius=18, blur=15, gradient=heatmap_gradient, min_opacity=0.3).add_to(m)
        
        for l in locations:
            folium.CircleMarker([l["latitude"], l["longitude"]], radius=3, color=point_color, fill=True, weight=1).add_to(m)
        
        # 标注核心点
        if hotspot:
            folium.Marker(
                [hotspot["latitude"], hotspot["longitude"]],
                icon=folium.Icon(color="white", icon_color=risk_col, icon="warning-sign"),
                tooltip="Primary Critical Hotspot"
            ).add_to(m)
            
        st_folium(m, width=900, height=550, key=f"map_{module}_{display_year}")

    with col_data:
        st.subheader("Inventory Registry")
        df_display = pd.DataFrame(locations).rename(columns={'latitude':'LAT','longitude':'LON','stress_score':'SCORE'})
        st.dataframe(df_display.style.format("{:.4f}"), height=400)
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button("Export Dataset (CSV)", csv, f"pineguard_{mode_tag}_{display_year}.csv", "text/csv", use_container_width=True)

    # 播放引擎
    if st.session_state.playing:
        time.sleep(0.4)
        if module == "Historical Observation" and st.session_state.obs_year < 2025:
            st.session_state.obs_year += 1
            st.rerun()
        elif module == "Strategic Projection" and st.session_state.proj_year < 2045:
            st.session_state.proj_year += 1
            st.rerun()
        else:
            st.session_state.playing = False
            st.rerun()

except Exception as e:
    st.error(f"Module Error: {e}")