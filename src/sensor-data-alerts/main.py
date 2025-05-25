import json
import os
from kafka import KafkaConsumer

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)
    
config = load_config()

bootstrap_servers = config['kafka']['bootstrap_servers']
metrics_topic = config['kafka']['topics']['metrics']

def create_alert_message(data):
    aqi = data.get("aqi")
    pm2_5 = data.get("avg_pm2_5")
    temperature = data.get("avg_temp")
    humidity = data.get("avg_humidity")
    window_end_time = data.get("window_end_time")

    if aqi is None or pm2_5 is None or temperature is None or humidity is None or window_end_time is None:
        return None

    if aqi <= 150:
        return None

    message = f"🚨 **Air Quality Alert** 🚨\n"
    message += f"🕒 Time: {window_end_time}\n\n"

    if aqi <= 50:
        message += f"🌬️ AQI: {aqi:.2f} (Good) - Air quality is considered satisfactory, and air pollution poses little or no risk.\n"
    elif aqi <= 100:
        message += f"😐 AQI: {aqi:.2f} (Moderate) - Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.\n"
    elif aqi <= 150:
        message += f"😟 AQI: {aqi:.2f} (Unhealthy for Sensitive Groups) - Members of sensitive groups may experience health effects. The general public is not likely to be affected.\n"
    elif aqi <= 200:
        message += f"😷 AQI: {aqi:.2f} (Unhealthy) - Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.\n"
    elif aqi <= 300:
        message += f"🤢 AQI: {aqi:.2f} (Very Unhealthy) - Health warnings of emergency conditions. The entire population is more likely to be affected.\n"
    else:
        message += f"☠️ AQI: {aqi:.2f} (Hazardous) - Health alert: everyone may experience more serious health effects.\n"

    message += f"💨 PM2.5: {pm2_5:.2f} µg/m³ - "
    if pm2_5 <= 12:
        message += "Levels are good.\n"
    elif pm2_5 <= 35.4:
        message += "Levels are moderate.\n"
    elif pm2_5 <= 55.4:
        message += "Levels are unhealthy for sensitive groups.\n"
    elif pm2_5 <= 150.4:
        message += "Levels are unhealthy.\n"
    elif pm2_5 <= 250.4:
        message += "Levels are very unhealthy.\n"
    else:
        message += "Levels are hazardous.\n"

    message += f"🌡️ Temperature: {temperature:.1f}°C - "
    if temperature < 0:
        message += "Freezing! Bundle up. 🥶\n"
    elif temperature < 10:
        message += "Chilly weather. A warm jacket is a good idea. 🧥\n"
    elif temperature < 20:
        message += "Cool and pleasant. Perfect for a walk. 🚶\n"
    elif temperature < 30:
        message += "Warm and sunny. Enjoy the outdoors! ☀️\n"
    elif temperature < 35:
        message += "Hot! Stay hydrated and find some shade. 🥵\n"
    else:
        message += "Very hot! Avoid prolonged outdoor activity. 🔥\n"

    message += f"💧 Humidity: {humidity:.1f}% - "
    if humidity < 30:
        message += "Dry air. You might need some moisturizer.🧴\n"
    elif humidity < 60:
        message += "Comfortable humidity levels. 😊\n"
    elif humidity < 80:
        message += "A bit humid. Can feel a little sticky. 💦\n"
    else:
        message += "Very humid. Feels muggy. 😥\n"

    return message

if __name__ == "__main__":
    consumer = KafkaConsumer(
        metrics_topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        group_id='alert-script-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print(f"Listening to Kafka topic: {metrics_topic}")

    for message in consumer:
        data = message.value

        alert = create_alert_message(data)
        if alert:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alert.txt'), 'w', encoding='utf-8') as f:
                f.write(alert)