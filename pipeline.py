import json
import os
import random

def generate_industrial_data():
    """生成 1984-2025 年工业级模拟监测数据"""
    os.makedirs('data/processed', exist_ok=True)
    center_lat, center_lon = 37.1174, -119.6043
    
    for year in range(1984, 2026):
        # 扩散逻辑：后期扩散速度加快，模拟生态灾害特征
        if year < 2000:
            num_points = max(2, (year - 1983)) 
            spread_range = 0.04 + (year - 1984) * 0.002
        else:
            num_points = 18 + (year - 2000) * 4 
            spread_range = 0.08 + (year - 2000) * 0.005
        
        locations = []
        for i in range(num_points):
            locations.append({
                "latitude": round(center_lat + random.uniform(-spread_range, spread_range), 6),
                "longitude": round(center_lon + random.uniform(-spread_range, spread_range), 6),
                "stress_score": round(random.uniform(0.35, 0.95), 4)
            })
        
        result = {
            "year": str(year),
            "outbreak_count": len(locations),
            "locations": locations
        }
        
        with open(f'data/processed/stress_{year}.json', 'w') as f:
            json.dump(result, f, indent=4)
    print(f"✅ Success: 42 years of spatial data generated.")

if __name__ == "__main__":
    generate_industrial_data()