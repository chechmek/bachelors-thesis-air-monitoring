import numpy as np

def compute_aqi_from_pm25(pm25_value):
    if pm25_value < 0:
        return 0
    
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.0, 35.4, 51, 100),
        (35.4, 55.4, 101, 150),
        (55.4, 150.4, 151, 200),
        (150.4, 250.4, 201, 300),
        (250.4, 350.4, 301, 400),
        (350.4, 500.4, 401, 500),
    ]

    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= pm25_value <= c_high:
            return round((i_high - i_low) / (c_high - c_low) * (pm25_value - c_low) + i_low)
    return None

def calculate_metrics(data_points_list):
    if len(data_points_list) != 12:
        raise ValueError("Expected exactly 12 data points")

    pm2_5_values = [point['pm2_5'] for point in data_points_list]
    temp_values = [point['temp'] for point in data_points_list]
    humidity_values = [point['humidity'] for point in data_points_list]

    avg_pm2_5 = float(np.mean(pm2_5_values))
    avg_temp = float(np.mean(temp_values))
    avg_humidity = float(np.mean(humidity_values))
    aqi = compute_aqi_from_pm25(avg_pm2_5)

    return {
        'avg_temp': avg_temp,
        'avg_humidity': avg_humidity,
        'avg_pm2_5': avg_pm2_5,
        'aqi': aqi
    } 