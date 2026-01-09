<div align="center">

# [English](#english) | [中文](#chinese)

</div>

<span id="english"></span>
# PineGuard: Strategic Spatio-Temporal Forest Health Analysis (1984–2045)

**Principal Analyst:** Tanghao Chen (Dios)

---

PineGuard is not merely a geospatial intelligence platform; it is a specialized digital defense system engineered to combat Pine Wilt Disease (PWD), an ecological catastrophe often referred to as the "Forest Cancer." PWD, caused by the pinewood nematode, can trigger the total vascular collapse of a mature pine tree within just 30 to 90 days, transforming vibrant ecosystems into highly flammable "red-stage" timber stands.

By synthesizing 41 years of historical satellite data (1984–2025) with advanced linear regression modeling, PineGuard provides a strategic framework for decoding the invisible spatial dynamics of this pathogen. To overcome the "Spectral Chameleon" effect—where California’s arid soils and Mediterranean grasses mimic the signature of dying trees—the system employs a custom Land Cover Masking Algorithm. This engineering intervention surgically filters geological and seasonal noise, isolating high-fidelity biogenic stress signals. The result is a system that not only audits four decades of infestation history but also projects high-risk outbreak trajectories through 2045, offering decision-makers a transition from reactive management to proactive strategic intervention.

---

## Deployment
**Public Access Link:** [https://pineguard.streamlit.app](https://[YOUR_GITHUB_USERNAME].streamlit.app)

---

## Operational Modules

### Historical Observation Module (1984–2025)
The Observation Module provides a retrospective analysis of forest health based on empirical data. 
* **Visualization:** Utilizes a high-contrast warm-tone gradient (Blue-Yellow-Red) to represent recorded anomaly density.
* **Objective:** Identification of historical epicenters and the quantification of past infestation patterns.

### Strategic Projection Module (2026–2045)
The Projection Module employs predictive algorithms to simulate the potential expansion of forest stress over the next two decades.
* **Visualization:** Utilizes a cold-tone "Aurora Spectrum" (Indigo-Cyan-White) to distinguish simulated data from historical records.
* **Objective:** Long-term risk assessment and strategic resource allocation for forest management.

---

## Technical Features

### Automated Risk Assessment
The system evaluates real-time risk levels—STABLE, WATCH, or ALERT—based on point density and weighted stress scores. This quantitative approach allows for standardized reporting across different temporal epochs.

### Spread Velocity Analytics
PineGuard calculates the rate of spatial expansion (km/yr), enabling analysts to identify transition phases between linear and exponential growth in anomaly distribution.

### Geospatial Hotspot Identification
The platform automatically identifies and markers primary critical hotspots. These coordinates represent the highest concentration of forest stress, serving as priority indicators for ground-level intervention.

---


## Technical Challenges and Geospatial Methodology

The PineGuard system addresses several critical challenges inherent in California’s complex landscape analysis:

### 1. Spectral Discrimination: Soil vs. Desiccated Vegetation
In California’s arid regions, the spectral signature of exposed sandy soil often overlaps with that of desiccated (dead) pine needles. 
* **Methodology:** PineGuard utilizes a temporal differencing approach. By comparing peak phenology (May) with late-season data (October), the system filters out static geological features (sand/soil) and isolates dynamic biological stress indicators.

### 2. Phenological Calibration in Mediterranean Climates
California’s Mediterranean climate creates a unique phenological curve. Deciduous trees and seasonal grasses can mimic forest stress during summer dormancy.
* **Methodology:** The system incorporates a phenology-aware mask that prioritizes evergreen coniferous spectral responses, ensuring that seasonal senescence in non-target species does not trigger false positive anomalies.

### 3. Riparian Zone Buffering
Vegetation along deep-blue riparian zones (rivers and streams) remains lush even during droughts, which can mask the spread of pathogens in the understory.
* **Methodology:** PineGuard implements a specific "Riparian Exclusion Zone" and hydration-adjusted stress scoring. This prevents the high chlorophyll signals of river-side vegetation from skewing the risk assessment of the adjacent pine stands.

---

## Technical Stack

The platform is built on a high-performance Python-based geospatial stack:

* **Frontend & Visualization:** Streamlit (Web UI), Folium (Leaflet-based Mapping).
* **Geospatial Processing:** Folium Plugins (HeatMap), Coordinate Reference System (CRS) Management.
* **Data Science & Modeling:** Scikit-learn (Linear Regression), NumPy (Spatial Simulation), Pandas (Temporal Aggregation).
* **Environment & Deployment:** Python 3.9+, Streamlit Community Cloud, GitHub Version Control.

---

## Project Structure

The PineGuard repository follows a modular architecture designed for scalability and maintainability. Below is the directory schema of the environment:

```text
PineGuard/
├── data/                       # Multi-stage data storage
│   ├── processed/              # Cleaned JSON datasets (1984-2025)
│   └── outputs/                # Generated reports and CSV exports
├── src/                        # Core source logic
│   ├── analysis/               # Statistical modeling and projection engines
│   ├── processing/             # Data cleaning and normalization pipelines
│   └── visualization/          # Folium mapping and heatmap logic
├── app.py                      # Main Streamlit dashboard application
├── main.py                     # FastAPI backend service
├── pipeline.py                 # Automated data generation and ETL pipeline
├── visualize.py                # Standalone visualization scripts
├── requirements.txt            # System dependency configuration
└── README.md                   # Project documentation
```

---

## Data and Methodology

* **Temporal Range:** 1984 through 2045.
* **Spatial Engine:** Folium-based HeatMap rendering with weighted stress score coefficients.
* **Predictive Framework:** Scikit-learn Linear Regression model trained on 41 years of annual frequency data.
* **Software Stack:** Python, Streamlit, Pandas, NumPy, Scikit-learn, and Folium.

---

## System Setup

To execute the PineGuard environment locally:

1. **Clone Repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)[YOUR_GITHUB_USERNAME]/PineGuard.git
   cd PineGuard

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt

3. **Initialize Application:**
    ```bash
    streamlit run app.py

---
</div>

<span id="chinese"></span>

# PineGuard: 战略性时空森林健康分析系统 (1984–2045)
**首席分析师**： 陈唐昊

---

PineGuard 不仅仅是一个地理空间情报平台；它是一个专门为应对松材线虫病（PWD）而设计的数字防御系统。松材线虫病被誉为“森林的癌症”，由松材线虫引起，能在短短 30 至 90 天内导致成年松树的维管束系统全面崩溃，将充满活力的生态系统转变为高度易燃的“红色阶段”枯木林。

通过将 41 年的历史卫星数据（1984–2025）与高级线性回归模型相结合，PineGuard 提供了一个解码这种病原体隐形空间动力学的战略框架。为了克服“光谱变色龙”效应（即加州干旱的土壤和地中海牧草会模仿枯死树木的光谱特征），系统采用了自定义的土地覆盖掩膜算法（Land Cover Masking Algorithm）。这一工程干预手段通过手术拆解般的精准度过滤了地质和季节性噪声，隔离出高保真度的生物源压力信号。该系统不仅能审计过去四十年的虫害历史，还能预测直至 2045 年的高风险爆发轨迹，协助决策者实现从“响应式管理”向“主动战略干预”的跨越。

---

## 部署信息
**公共访问链接：** https://pineguard.streamlit.app

---

## 核心操作模块
### 历史观测模块 (1984–2025)
观测模块基于实证数据提供回顾性森林健康分析。
- 可视化方案： 采用高对比度暖色调梯度（蓝-黄-红）来表示记录的异常密度。
- 核心目标： 识别历史爆发中心，并量化过去的虫害演变模式。

### 战略预测模块 (2026–2045)
预测模块采用预测算法模拟未来二十年森林压力的潜在扩张。
- 可视化方案： 采用冷色调“极光光谱”（靛蓝-青色-纯白）以区分模拟数据与历史记录。
- 核心目标： 进行长期风险评估，并为森林管理提供战略性的资源分配方案。

---

## 技术特性
### 自动化风险评估
系统基于点密度和加权压力得分，评估实时风险等级：稳定 (STABLE)、观测 (WATCH) 或 警报 (ALERT)。这种定量方法允许在不同的时间跨度内进行标准化的报告。

### 扩散速度分析
PineGuard 计算空间扩张速率（公里/年），使分析师能够识别异常分布在增长过程中的线性阶段与指数阶段之间的转换。

### 地理空间热点识别
平台自动识别并标记主要的关键热点。这些坐标代表了森林压力最高浓度的区域，作为地面干预的优先参考指标。

---

## 地理空间方法论与技术挑战

PineGuard 系统解决了加州复杂景观分析中固有的几项关键挑战：

###  **1. 光谱辨析：土壤 vs. 枯萎植被**

在加州的干旱地区，裸露沙地的光谱特征往往与枯死的松针重叠。
- **方法论：** PineGuard 采用时空差分法。通过对比物候高峰期（5月）与季末数据（10月），系统过滤掉静态的地质特征（沙土），隔离出动态的生物压力指标。

###  **2. 地中海气候下的物候校准**

加州的地中海气候创造了独特的物候曲线。落叶树木和季节性牧草在夏季休眠期间可能模仿森林压力信号。
- **方法论：** 系统集成了一个具有物候感知功能的掩膜，优先提取常绿针叶树的光谱响应，确保非目标物种的季节性衰老不会触发误报。

###  **3. 滨河地带缓冲区处理**

深蓝色滨河地带（河流和溪流）沿线的植被即使在干旱时期也能保持茂盛，这可能会掩盖林下病原体的蔓延。
- **方法论：** PineGuard 实施了特定的“滨河排除区”和水分调整压力评分。这防止了河边植被的高叶绿素信号干扰对相邻松林风险评估的准确性。

---

### 技术栈
平台构建在高性能的 Python 地理空间技术栈之上：

- **前端与可视化：** Streamlit (Web UI), Folium (基于 Leaflet 的地图交互)。
- **地理空间处理；** Folium Plugins (热点图), 坐标参考系统 (CRS) 管理。
- **数据科学与建模：** Scikit-learn (线性回归), NumPy (空间模拟), Pandas (时空聚合)。
- **环境与部署：** Python 3.9+, Streamlit Community Cloud, GitHub 版本控制。
---
## 项目结构
PineGuard 存储库遵循模块化架构，旨在提高可扩展性和可维护性：
```text
PineGuard/
├── data/                       # 多级数据存储
│   ├── processed/              # 清洗后的 JSON 数据集 (1984-2025)
│   └── outputs/                # 生成的报告与 CSV 导出文件
├── src/                        # 核心源代码逻辑
│   ├── analysis/               # 统计建模与预测引擎
│   ├── processing/             # 数据清洗与归一化流水线
│   └── visualization/          # Folium 绘图与热力图逻辑
├── app.py                      # Streamlit 仪表盘主程序
├── main.py                     # FastAPI 后端服务
├── pipeline.py                 # 自动化数据生成与 ETL 流水线
├── visualize.py                # 独立可视化脚本
├── requirements.txt            # 系统依赖配置文件
└── README.md                   # 项目文档
```
---

## 数据与方法论摘要
- 时间范围： 1984 年至 2045 年。
- 空间引擎： 基于 Folium 的热力图渲染，带有加权压力得分系数。
- 预测框架： 基于 41 年年度频率数据训练的 Scikit-learn 线性回归模型。
- 软件环境： Python, Streamlit, Pandas, NumPy, Scikit-learn, Folium。

## 本地系统安装
如需在本地运行 PineGuard 环境：
1. 克隆存储库：
```Bash
git clone https://github.com/DiosStrike/PineGuard.git
cd PineGuard
```
2. 安装依赖：
```Bash
pip install -r requirements.txt
```
3. 启动应用程序：
```Bash
streamlit run app.py
```