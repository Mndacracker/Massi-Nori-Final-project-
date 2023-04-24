import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import os
import inspect
import urllib
import requests
import json
from PIL import Image, ImageTk
import io

downloaded_files = []

# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
# apod_desktop.init_apod_cache(script_dir)

# Create the main window
root = tk.Tk()
root.title("Image Viewer")
root.geometry("800x600")

# Create a tab control
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Image Viewer")
tab_control.pack(expand=1, fill="both")

# Create a label and an image widget for the main picture
label = tk.Label(tab1, text="Image Text")
label.pack(pady=10)
image = tk.PhotoImage(file="nasa_logo.png")
image_widget = tk.Label(tab1, image=image)
image_widget.pack()

tab1.grid_propagate(False)

# Create a frame for the "View Cached Images" box
frame1 = ttk.Frame(tab1)
frame1.pack(pady=10)

# Create a label and a dropdown menu for selecting the cached images
label1 = ttk.Label(frame1, text="View Cached Images")
label1.pack(side="left")
view_options = ttk.Combobox(frame1, values=downloaded_files)
view_options.pack(side="left", padx=10)

# Create a button for setting the selected image as desktop background
button1 = ttk.Button(frame1, text="Set as Desktop")
button1.pack(side="left", padx=10)

# Create a frame for the "Get More Images" box
frame2 = ttk.Frame(tab1)
frame2.pack(pady=10)

# Create a label and a calendar dropdown widget for selecting the date
label2 = ttk.Label(frame2, text="Select Date")
label2.pack(side="left")
date_entry = DateEntry(frame2, width=12, background='darkblue', foreground='white', borderwidth=2)
date_entry.pack(side="left", padx=10)

def download_image():
     # Get the selected date
    selected_date = date_entry.get_date()

    # Construct the API URL with the selected date as a parameter
    api_url = f"https://api.nasa.gov/planetary/apod?date={selected_date}&api_key=A34XmIKhgiFEERsIDpSUIxGuNThWYMsNCSARb9wV"

    # Make a GET request to the API
    response = requests.get(api_url)

    # Parse the JSON response
    data = json.loads(response.text)

    # Get the image URL and download the image
    image_url = data["url"]
    response = requests.get(image_url)
    img_data = response.content

    # Create the "images" folder if it does not exist
    if not os.path.exists("images"):
        os.makedirs("images")

    # Open the image data using PIL and save it as a PNG file in the "images" folder
    image_url = data["url"]
    image_filename = image_url.split("/")[-1]
    image_filename = image_filename.split(".jpg")[0]
    img = Image.open(io.BytesIO(img_data))
    img = img.resize((400, 400))
    img_path = os.path.join("images", f"{image_filename}.png")
    img.save(img_path, "PNG")

    # Update the image widget
    image = ImageTk.PhotoImage(img)
    image_widget.configure(image=image)
    image_widget.image = image

    downloaded_files.append(image_filename)

    # Update the options in the "View Cached Images" drop-down menu
    view_options.set(downloaded_files)
    view_options['values'] = downloaded_files

    # Update the label with the image description
    label.configure(text=data["explanation"])

# Create a button for downloading the selected image
button2 = ttk.Button(frame2, text="Download Image", command=download_image)
button2.pack(side="left", padx=10)

# Start the main loop
root.mainloop()
