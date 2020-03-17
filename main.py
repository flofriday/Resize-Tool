import tkinter as tk
from tkinter import filedialog as fd, messagebox as mb
import os
from PIL import Image
import platform
from shutil import rmtree
import subprocess
from pathlib import Path


# Return a list of all filenames in that folder that are images
def get_images(folder):
    files = os.listdir(folder)
    images = []
    for file in files:
        # A helper variable containing the full path of the file
        abs_file = os.path.join(folder, file)

        # Ignore all folders
        if os.path.isdir(abs_file):
            continue

        # Asume the file is an image and open it, if it fails we won't
        # add it to the images list
        try:
            im = Image.open(abs_file)
            im.verify()
            im.close
            images.append(file)
        except Exception:
            pass

    # Return the list of confirmed images
    return images


# Open the file dialog and ask the user for a folder. Then also set the notify
# text to tell the user how many images are found int that folder
def open_folder_dialog():
    folder.set(fd.askdirectory(initialdir=str(Path.home()), title="Selecte a folder"))
    images = get_images(folder.get())
    text.set(f"{len(images)} images found")


# Open the OS filemanager (explorer on windows, finder on macOS) with the
# path provided. This function works on linux, macOS and windows.
def open_filemanager(path):
    system = platform.system()
    if system == "Linux":
        subprocess.call(["xdg-open", path])
    elif system == "Darwin":
        subprocess.call(["open", path])
    elif system == "Windows":
        os.startfile(path)


# Resize an image in folder with the name in file to size. The longer of both
# sides will be resized to size and the other side will be shortend accordingly
# so that the aspect remains
def resize_image(folder, file, size):
    # Calculate the input and output paths
    infile = os.path.join(folder, file)
    outfile = os.path.join(folder, "Resized Images", file)

    # Open the image and read the width and height
    im = Image.open(infile)
    width = im.size[0]
    height = im.size[1]
    new_width = size
    new_height = size

    # Exit if the image is small enough
    if width < size and height < size:
        im.save(outfile)
        return

    # Calculate the new dimensions for the image
    if width > height:
        new_height = int(size * height / width)
    else:
        new_width = int(size * width / height)

    # Resize the image
    im = im.resize((new_width, new_height), Image.ANTIALIAS)
    im.save(outfile)


# Resize all images in the selected folder
def resize():
    # Exit if there is no folder selected
    if folder.get() == "":
        text.set("You need to select a folder first")
        return

    # Exit if size is too small
    if size.get() < 10:
        text.set("Size musst at least be 10")
        return

    # Create the folder to put the resized images in. If the folder already
    # exists, delete it and then recreate it to ensure it is empty.
    outpath = os.path.join(folder.get(), "Resized Images")
    if os.path.exists(outpath):
        rmtree(outpath)
    os.makedirs(outpath)

    # Get all images form the folder, loop over them and resize each one
    images = get_images(folder.get())
    error_images = []
    for i, image in enumerate(images):
        text.set(f"Resizing image {i+1} of {len(images)}")
        w.update()
        try:
            resize_image(folder.get(), image, size.get())
        except Exception:
            error_images.append(image)

    # Check if therer were any errors
    if len(error_images) != 0:
        # Display a message box to the user
        message = (
            f"An error occoured with the following {len(error_images)}"
            + " files (all other images should have worked tough):"
            + ", ".join(error_images)
        )
        mb.showerror("Error", message)
        text.set(f"{len(images) - len(error_images)} images resized")
    else:
        text.set(f"All {len(images)} images are resized :)")

    # Open the folder with the resized images in the filemanager
    open_filemanager(outpath)


# Create the window
w = tk.Tk()
w.title("Resize Images")

# Create the global state variables
folder = tk.StringVar()
size = tk.IntVar()
size.set(640)
text = tk.StringVar()
text.set("Select a folder")

# Size selection
size_frame = tk.Frame(w)
size_frame.pack()
size_label = tk.Label(size_frame, text="Size (Pixel)", fg="#000")
size_entry = tk.Entry(size_frame, textvariable=size)
size_label.pack(side=tk.LEFT)
size_entry.pack(side=tk.LEFT)

# Folder selection
folder_frame = tk.Frame(w)
folder_frame.pack()
folder_entry = tk.Entry(folder_frame, textvariable=folder)
folder_button = tk.Button(
    folder_frame, text="Browse...", fg="#000", command=open_folder_dialog
)
folder_entry.pack(side=tk.LEFT)
folder_button.pack(side=tk.LEFT)

# Text to communicate with the user
text_label = tk.Label(w, textvariable=text, fg="#000")
text_label.pack()

# Resize button
resize_button = tk.Button(w, text="Resize", fg="#000", command=resize)
resize_button.pack()

# Start the app
w.mainloop()
