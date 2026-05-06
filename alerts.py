def generate_alerts(temp, humidity, rain_prob):
    alerts = []

    if temp > 40:
        alerts.append("🔥 High Temperature Alert")

    if humidity > 80:
        alerts.append("💧 High Humidity Alert")

    if rain_prob > 60:
        alerts.append("🌧️ Rain Alert")

    return alerts