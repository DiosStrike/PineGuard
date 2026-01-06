# PineGuard: Strategic Spatio-Temporal Forest Health Analysis (1984–2045)

**Principal Analyst:** Tanghao Chen (Dios)

PineGuard is a geospatial intelligence platform engineered for the monitoring, analysis, and projection of forest health anomalies. By synthesizing 41 years of historical data with linear regression modeling, the system provides a strategic framework for understanding the spatial dynamics of forest stress and predicting future risk trajectories.

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

