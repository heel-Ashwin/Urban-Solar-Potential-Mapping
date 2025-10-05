from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load dataset on startup
df = pd.read_csv("solar_predictions.csv")

def calculate_solar_suitability_index(solar_potential, elevation, precipitation):
    """Calculate Solar Suitability Index (0-100)"""
    # Normalize factors
    solar_score = min(solar_potential / 20000 * 50, 50)  # Max 50 points
    elev_score = max(20 - (elevation / 2000 * 20), 0)  # Lower elevation better, max 20 points
    prec_score = max(30 - (precipitation / 100 * 30), 0)  # Lower precipitation better, max 30 points
    
    return round(solar_score + elev_score + prec_score, 1)

def recommend_system_type(solar_potential, area=100):
    """Recommend solar system type based on potential"""
    if solar_potential < 14000:
        return "Small Rooftop System"
    elif solar_potential < 17000:
        return "Community Solar Installation"
    else:
        return "Utility-Scale Solar Farm"

def calculate_energy_yield(solar_potential, area=100, efficiency=0.18):
    """Calculate annual energy yield in kWh/year"""
    # solar_potential is in Wh/m²/year (from mean of 12 months)
    # Convert to kWh/m²/year and multiply by area and efficiency
    annual_yield = (solar_potential / 1000) * area * efficiency * 365
    return round(annual_yield, 2)

def calculate_roi(annual_yield, system_cost_per_kw=1000):
    """Calculate ROI metrics"""
    system_size_kw = annual_yield / 1200  # Approximate system size
    total_cost = system_size_kw * system_cost_per_kw
    annual_savings = annual_yield * 0.08  # $0.08 per kWh
    payback_period = total_cost / annual_savings if annual_savings > 0 else 0
    lifetime_savings = annual_savings * 25  # 25-year lifetime
    
    return {
        "system_size_kw": round(system_size_kw, 2),
        "total_cost": round(total_cost, 2),
        "annual_savings": round(annual_savings, 2),
        "payback_period": round(payback_period, 1),
        "lifetime_savings": round(lifetime_savings, 2)
    }

def recommend_infrastructure(system_size_kw):
    """Recommend infrastructure components"""
    panel_capacity = 0.4  # 400W panels
    num_panels = int(system_size_kw / panel_capacity)
    inverter_capacity = round(system_size_kw * 1.2, 1)  # 120% of system size
    battery_capacity = round(system_size_kw * 4, 1)  # 4 hours storage
    
    return {
        "num_panels": num_panels,
        "panel_wattage": 400,
        "inverter_capacity_kw": inverter_capacity,
        "battery_capacity_kwh": battery_capacity,
        "estimated_area_sqm": num_panels * 2  # ~2 sqm per panel
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    input_lat = float(data.get("latitude"))
    input_lon = float(data.get("longitude"))
    area = float(data.get("area", 100))  # Default 100 sqm

    # Calculate Euclidean distance from all grid points
    df['distance'] = np.sqrt((df['lat'] - input_lat)**2 + (df['lon'] - input_lon)**2)

    nearest_row = df.loc[df['distance'].idxmin()]

    # Extract values
    current_solar = nearest_row['srad_mean']
    future_solar = nearest_row['predicted_solar_future']
    elevation = nearest_row['elev']
    precipitation = nearest_row['prec_mean']
    
    # Calculate metrics
    ssi = calculate_solar_suitability_index(current_solar, elevation, precipitation)
    system_type = recommend_system_type(current_solar, area)
    annual_yield = calculate_energy_yield(current_solar, area)
    roi_metrics = calculate_roi(annual_yield)
    infrastructure = recommend_infrastructure(roi_metrics['system_size_kw'])
    
    # Calculate future projections
    future_annual_yield = calculate_energy_yield(future_solar, area)
    solar_change = round(((future_solar - current_solar) / current_solar) * 100, 2)

    return jsonify({
        "input_latitude": input_lat,
        "input_longitude": input_lon,
        "grid_latitude": float(nearest_row['lat']),
        "grid_longitude": float(nearest_row['lon']),
        
        # Current solar data
        "solar_potential_current": round(current_solar, 2),
        "solar_potential_future": round(future_solar, 2),
        "solar_change_percent": solar_change,
        
        # Environmental factors
        "elevation": float(elevation),
        "precipitation": float(precipitation),
        "temp_min": float(nearest_row['tmin_mean']),
        "temp_max": float(nearest_row['tmax_mean']),
        
        # Analysis metrics
        "solar_suitability_index": ssi,
        "system_type": system_type,
        "annual_energy_yield": annual_yield,
        "future_annual_yield": future_annual_yield,
        
        # ROI metrics
        "roi": roi_metrics,
        
        # Infrastructure recommendations
        "infrastructure": infrastructure
    })

if __name__ == "__main__":
    app.run(debug=True)