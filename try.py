'''import os 

path = "D:\dionigi\Documents\Python scripts\WavArt\\assets"
paths=[]
for elem in os.listdir(path):
    if os.path.isfile(os.path.join(path,elem)):
        paths.append(os.path.join("assets",elem))
print(paths)'''

import tkinter as tk
from PIL import Image, ImageTk

# Main Tkinter window
root = tk.Tk()
root.geometry("400x400")

# Load or create an initial image
initial_image = Image.new("RGB", (200, 200), color="blue")  # Create a blank blue image
img_tk = ImageTk.PhotoImage(initial_image)

# Label to display the image
image_panel = tk.Label(root, image=img_tk)
image_panel.pack(pady=20)

# Function to dynamically update the image
def update_image():
    # Create or modify a new image (for demonstration, make a red image here)
    new_image = Image.new("RGB", (200, 200), color="red")
    
    # Convert the new image to ImageTk format
    new_img_tk = ImageTk.PhotoImage(new_image)
    
    # Update the panel with the new image
    image_panel.config(image=new_img_tk)
    image_panel.image = new_img_tk  # Keep a reference to avoid garbage collection

# Button to update the image
update_button = tk.Button(root, text="Update Image", command=update_image)
update_button.pack(pady=10)

root.mainloop()