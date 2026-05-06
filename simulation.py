import random

def simulate_weather():
    return {
        "temp": random.randint(20, 45),
        "humidity": random.randint(30, 90),
        "rain_prob": random.randint(0, 100)
    }