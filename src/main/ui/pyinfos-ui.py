import tkinter as tk
from tkinter import ttk, messagebox
import requests
import xml.etree.ElementTree as ET

def get_weather(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo = requests.get(geo_url).json()
    if "results" not in geo:
        messagebox.showerror("Erreur", "Ville non trouvée ❌")
        return None
    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather = requests.get(weather_url).json()
    temp = weather["current_weather"]["temperature"]
    wind = weather["current_weather"]["windspeed"]
    return f"🌤️ {city}\n🌡️ Température : {temp}°C\n💨 Vent : {wind} km/h"

def get_news():
    url = "https://news.google.com/rss?hl=fr&gl=FR&ceid=FR:fr"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    news_list = []
    for item in root.findall(".//item")[:5]:
        title = item.find("title").text
        news_list.append(f"👉 {title}")
    return "\n".join(news_list)

def update_dashboard():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Attention", "Veuillez entrer une ville")
        return
    weather_text = get_weather(city)
    news_text = get_news()
    if weather_text:
        weather_label.config(text=weather_text)
    news_label.config(text=news_text)

root = tk.Tk()
root.title("🌍 PyInfos - UI v1.0")
root.geometry("600x500")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Arial", 12))

frame = tk.Frame(root)
frame.pack(pady=10)

city_entry = tk.Entry(frame, font=("Arial", 14), width=30)
city_entry.pack(side=tk.LEFT, padx=5)

search_button = ttk.Button(frame, text="Rechercher", command=update_dashboard)
search_button.pack(side=tk.LEFT)

weather_label = tk.Label(root, text="", font=("Arial", 14), justify=tk.LEFT)
weather_label.pack(pady=20)

news_label = tk.Label(root, text="", font=("Arial", 12), justify=tk.LEFT, wraplength=550)
news_label.pack(pady=10)

root.mainloop()