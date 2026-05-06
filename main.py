import pandas as pd
from src.weather_api import get_weather
from src.alerts import generate_alerts
from src.simulation import simulate_weather

mode = input("Enter mode (api/sim): ").lower()
city = input("Enter city: ")

records = []

try:
    if mode == "api":
        data = get_weather(city)

        temp = data["current_weather"]["temperature"]
        humidity = data["hourly"]["relativehumidity_2m"][0]
        rain_prob = data["hourly"]["precipitation_probability"][0]

    else:
        sim = simulate_weather()
        temp = sim["temp"]
        humidity = sim["humidity"]
        rain_prob = sim["rain_prob"]

    alerts = generate_alerts(temp, humidity, rain_prob)

    print("\n--- WEATHER REPORT ---")
    print("Temperature:", temp)
    print("Humidity:", humidity)
    print("Rain Probability:", rain_prob)

    print("\n--- ALERTS ---")
    if alerts:
        for a in alerts:
            print(a)
    else:
        print("No alerts")

    # Save report
    df = pd.DataFrame([{
        "temp": temp,
        "humidity": humidity,
        "rain_prob": rain_prob
    }])

    df.to_csv("reports/weather_report.csv", index=False)

    print("\nReport saved to reports/weather_report.csv")

except Exception as e:
    print("Error:", e)