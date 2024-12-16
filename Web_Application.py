from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

# OpenWeatherMap API Key
API_KEY = "9816248933c6ca1f0593ec77fa0d0735"  

def getWeather():
    city = textfield.get()

    if city == "":
        messagebox.showerror("Input Error", "Please enter a city name")
        return
    
    
    geolocator = Nominatim(user_agent="WeatherApp")  
    location = geolocator.geocode(city)

    if location is None:
        messagebox.showerror("City Not Found", f"Could not find information for {city}")
        return

    # Get timezone of the city
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    name.config(text="CURRENT WEATHER")

    # Fetch weather data using OpenWeatherMap API
    complete_url = f"http://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={API_KEY}&units=metric"
    weather_data = requests.get(complete_url).json()

    if weather_data["cod"] != "404":
        main_data = weather_data["main"]
        weather_desc = weather_data["weather"][0]["description"]
        wind_data = weather_data["wind"]
        
        # Extract data
        temperature = main_data["temp"]
        humidity = main_data["humidity"]
        pressure = main_data["pressure"]
        wind_speed = wind_data["speed"]

        # Update labels with weather data
        t.config(text=f"{temperature}°C")
        c.config(text=weather_desc.capitalize())
        w.config(text=f"{wind_speed} m/s")
        h.config(text=f"{humidity}%")
        d.config(text=weather_desc.capitalize())
        p.config(text=f"{pressure} hPa")
    else:
        messagebox.showerror("Weather Error", "City not found in OpenWeatherMap database")


# Search Box
search_image = PhotoImage(file="search.png")
myimage = Label(image=search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

search_icon = PhotoImage(file="search_icon.png")
myimage_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=34)

# Logo
logo_image = PhotoImage(file="logo.png")
Logo = Label(image=logo_image)
Logo.place(x=150, y=100)

# Button Box
Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Time 
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# Label for weather data
label1 = Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=125, y=430)

h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)

d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)

p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()
