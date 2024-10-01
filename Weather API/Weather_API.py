import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import io

# Function to get weather data
def get_weather():
    city = city_entry.get()
    api_key = "5432234971d6c2bbad7196777064aeb4"  # Your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        data = response.json()

        # Check if the response contains the necessary data
        if "weather" in data and "main" in data and "wind" in data:
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            icon = data['weather'][0]['icon']

            # Update the weather information
            weather_info = f"Weather: {weather_desc.capitalize()}\n"
            weather_info += f"Temperature: {temp}\u00B0C\n"  # Using Unicode for degree symbol
            weather_info += f"Wind Speed: {wind_speed} m/s\n"
            
            weather_label.config(text=weather_info)

            # Load weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            icon_response = requests.get(icon_url)
            img_data = Image.open(io.BytesIO(icon_response.content))
            img = img_data.resize((100, 100), Image.ANTIALIAS)  # Resize image for better fit
            weather_icon.config(image=ImageTk.PhotoImage(img))
            weather_icon.image = ImageTk.PhotoImage(img)  # Keep a reference
        else:
            messagebox.showerror("Error", "No weather data available. Please check the city name.")
    
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")

# Set up the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.configure(bg='#e0f7fa')  # Light cyan background color

# City Entry
city_entry = tk.Entry(root, font=("Helvetica", 14), width=20, bd=2, relief='solid')
city_entry.pack(pady=20)

# Get Weather Button
get_weather_button = tk.Button(root, text="Get Weather", command=get_weather, font=("Helvetica", 14), bg='#ffab40', fg='white', bd=0)
get_weather_button.pack(pady=10)

# Weather Label
weather_label = tk.Label(root, text="", font=("Helvetica", 14), bg='#e0f7fa', fg='black')
weather_label.pack(pady=10)

# Weather Icon
weather_icon = tk.Label(root, bg='#e0f7fa')
weather_icon.pack(pady=10)

# Run the app
root.mainloop()
