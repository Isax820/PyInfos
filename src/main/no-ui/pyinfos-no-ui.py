import requests
import xml.etree.ElementTree as ET

def get_weather(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo = requests.get(geo_url).json()

    if "results" not in geo:
        print("❌ Ville non trouvée")
        return

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather = requests.get(weather_url).json()

    temp = weather["current_weather"]["temperature"]
    wind = weather["current_weather"]["windspeed"]

    print(f"\n🌤️  Météo à {city} :")
    print(f"🌡️  Température : {temp}°C")
    print(f"💨 Vent : {wind} km/h")

def get_news():
    url = "https://news.google.com/rss?hl=fr&gl=FR&ceid=FR:fr"
    response = requests.get(url)

    root = ET.fromstring(response.content)

    print("\n📰 Actualités :\n")

    for item in root.findall(".//item")[:5]:
        title = item.find("title").text
        print(f"👉 {title}")

def main():
    print("===== 🌍 PyInfos - NO UI - v1.0 =====")
    city = input("🏙️  Entrez une ville : ")
    get_weather(city)
    get_news()

if __name__ == "__main__":
    main()