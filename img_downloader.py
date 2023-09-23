import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import requests
from bs4 import BeautifulSoup
import urllib.parse
import webbrowser

def convert_to_icon(input_image, output_icon):
    try:
        image = Image.open(input_image)
        # Resize the image to 512x512 pixels with the Lanczos filter
        image = image.resize((512, 512), Image.LANCZOS)
        icon_path = os.path.splitext(input_image)[0] + ".ico"  # Save in the same folder with the same name as the PNG file
        image.save(icon_path, format="ICO")
        return icon_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def browse_button_click():
    folder_paths = []
    while True:
        folder_path = filedialog.askdirectory()
        if not folder_path:
            break  # Exit the loop if no more folders are selected
        folder_paths.append(folder_path)
    if folder_paths:
        for folder_path in folder_paths:
            convert_folder(folder_path)

def convert_folder(folder_path):
    png_files = [file for file in os.listdir(folder_path) if file.endswith('.png')]
    if png_files:
        for png_file in png_files:
            png_file_path = os.path.join(folder_path, png_file)
            icon_path = convert_to_icon(png_file_path, "")
            if icon_path:
                # Delete the original PNG file
                os.remove(png_file_path)
                status_label.config(text=f"Icon created and PNG file deleted: {icon_path}")
    else:
        status_label.config(text=f"No PNG files found in {folder_path}")

def on_hover_enter(event):
    browse_button.config(bg="green", fg="white")  # Change background to green and text color to white

def on_hover_leave(event):
    browse_button.config(bg="SystemButtonFace", fg="black")  # Reset background and text color to default

def search_google_images(query):
    query_encoded = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={query_encoded}&tbm=isch"
    webbrowser.open(search_url)

def display_images(image_links):
    if not image_links:
        status_label.config(text="No images found on Google Images.")
        return

    # Clear any previous image buttons
    for button in image_buttons:
        button.destroy()

    # Display image buttons for user selection
    for i, image_link in enumerate(image_links):
        image_button = tk.Button(window, text=f"Image {i + 1}", command=lambda link=image_link: select_and_convert_image(link))
        image_button.config(font=("Arial", 14), bg="SystemButtonFace")
        image_button.pack()
        image_buttons.append(image_button)

def select_and_convert_image(selected_image_url):
    # Download the selected image
    image_filename = os.path.join(selected_folder_path, "selected_image.jpg")
    download_image(selected_image_url, image_filename)

    # Convert the downloaded image to an icon
    icon_path = convert_to_icon(image_filename, "")

    # Display the status
    status_label.config(text=f"Icon created from selected image: {icon_path}")

# Create a Tkinter window
window = tk.Tk()
window.title("Hassan Icon Changer")

# Set the window size, background color, and center content
window.geometry("1200x500")
window.configure(bg="#021b3b")

# Create a label for instructions with specified font size and bold
label = tk.Label(window, text="Browse to select folders containing PNG files.", font=("Arial", 40, "bold"))
label.pack(pady=(100, 20))  # Add padding (margin) at the top

# Create a browse button with the specified style
browse_button = tk.Button(window, text="Browse", command=browse_button_click, width=25, height=2)
browse_button.config(font=("Arial", 14), bg="SystemButtonFace")
browse_button.pack()

# Bind hover events to change button style
browse_button.bind("<Enter>", on_hover_enter)
browse_button.bind("<Leave>", on_hover_leave)

# Create a label for status messages
status_label = tk.Label(window, text="")
status_label.pack()

# Create an entry field for the user to input the Google Images search query
query_entry = tk.Entry(window, font=("Arial", 14), width=40)
query_entry.pack(pady=10)

# Create a button for searching Google Images for "folder icon"
search_button = tk.Button(window, text="Search Folder Icons", command=lambda: display_images(search_google_images(query_entry.get() + " folder icon")))
search_button.config(font=("Arial", 14), bg="SystemButtonFace")
search_button.pack()

# Create a list to store image buttons
image_buttons = []

# Create a folder path to store selected images
selected_folder_path = ""

# Center the window in the middle of the screen
window.eval('tk::PlaceWindow . center')
# Function to paste clipboard contents into an entry field
def paste_from_clipboard():
    try:
        clipboard_text = window.clipboard_get()
        query_entry.delete(0, tk.END)  # Clear the current entry text
        query_entry.insert(0, clipboard_text)  # Insert clipboard content into the entry field
    except tk.TclError:
        # Handle the case where clipboard is empty or inaccessible
        messagebox.showerror("Error", "Unable to access clipboard.")

# Create a button for pasting clipboard contents
paste_button = tk.Button(window, text="Paste", command=paste_from_clipboard, width=10, height=1)
paste_button.config(font=("Arial", 12), bg="SystemButtonFace")
paste_button.pack(pady=5)

# Start the Tkinter main loop
window.mainloop()
