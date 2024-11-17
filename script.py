#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import requests
from dotenv import load_dotenv
import logging
from PIL import Image, ImageDraw, ImageFont
import traceback

# Load environment variables from .env file
load_dotenv()

# Configuration
API_KEY = os.getenv("APIKEY")
LAT = os.getenv("LAT")
LON = os.getenv("LON")
url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=imperial"

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Paths for fonts and images
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
font_path = os.path.join(picdir, 'Font.ttc')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


from waveshare_epd import epd2in13_V4

try:
    # Fetch weather data
    response = requests.get(url)
    response.raise_for_status()
    weather_data = response.json()
    temperature = round(weather_data["main"]["temp"])
    temperature_text = f"{temperature}°F"

    # Initialize the e-Paper display
    logging.info("epd2in13_V4 Demo")
    epd = epd2in13_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    # Create a blank image for drawing
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    # Load the font
    font24 = ImageFont.truetype(font_path, 48)

    # Draw the temperature text
    draw.text((10, 50), temperature_text, font=font24, fill=0)

    # Display the image on the e-Paper
    epd.display(epd.getbuffer(image))
    logging.info("Displayed temperature on e-Paper")

    # Put the display to sleep
    epd.sleep()

except requests.exceptions.RequestException as e:
    logging.error(f"Error fetching weather data: {e}")
except KeyError:
    logging.error("Error: Unexpected response format from the API.")
except IOError as e:
    logging.error(e)
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
