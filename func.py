import os
import subprocess
import barcode
from barcode.writer import SVGWriter, ImageWriter
from PIL import Image, ImageTk
import io
import tkinter as tk
import logging
import settings as conf
import svgwrite

class BarcodeManager:
    def generate_barcode(data):
        """
           Generates a barcode for the given data and saves it as an image file.

           :param data: The data you want to encode in the barcode.
           """

        barcode_class = barcode.get_barcode_class(conf.barcode_standard)

        # Save the barcode as a SVG (for printing)
        my_barcode = barcode_class(data, writer=SVGWriter())
        my_barcode.save("temp")
        # Save the barcode as a PNG image (for preview)
        my_barcode_png = barcode_class(data, writer=ImageWriter())
        my_barcode_png.save("temp")
        EventLogger.log_event('info', 'Generated barcode.')

    def preview_temp_png(image_label):
        """
        Opens and displays the specified image in a given Tkinter label widget.

        Parameters:
            image_label (tk.Label): The Tkinter label widget to display the image.
        """
        # Open the image using Pillow
        img = Image.open("temp.png")

        # Convert image for Tkinter usage
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        EventLogger.log_event('info', 'Preview updated.')

    def print_barcode():
        # THIS I HAVE NOT TESTED AT ALL IF IT PRINTS! But it does open in default app or Edge!
        """Prints barcode."""
        try:
            # Try opening with the default application
            os.startfile("temp.svg")
        except OSError as e:
            if e.winerror == 1155: # "No application is associated with the specified file for this operation."
                # Fallback to open with Microsoft Edge
                print("Default application not set. Fallback to open with Microsoft Edge.")
                subprocess.run(['start', 'msedge', "temp.svg"], shell=True)
            else:
                # Handle other exceptions
                print("An unexpected error occurred:", e)
        EventLogger.log_event('info', 'Print job successful')

    def flush_temp_images():
        # Makes blank rectangles. (Security? I'm sure there's a better way to deal with temporary files.)
        """Creates a blank PNG file."""
        image = Image.new('RGBA', (200, 200), (255, 255, 255, 0))  # White background with full transparency
        image.save("temp.png")
        """Creates a blank SVG file."""
        dwg = svgwrite.Drawing("temp.svg", size=(200, 200))
        dwg.add(dwg.rect(insert=(0, 0), size=(200, 200), fill='white', fill_opacity=0))
        dwg.save()
        EventLogger.log_event('info', 'Temporary images flushed.')


class EventLogger:

    # Configure (should I use __init__? )
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level
        format='%(asctime)s - %(levelname)s - %(message)s',  # message format
        handlers=[
            logging.FileHandler("application.log"),  # Logs to file
            logging.StreamHandler()  # log to console
        ]
    )

    def log_event(level, message):
        """
        Logs an event with the specified level and message.

        Args:
            level (str): The level of the log ('info', 'warning', 'error').
            message (str): The log message.
        """
        if level == 'info':
            logging.info(message)
        elif level == 'warning':
            logging.warning(message)
        elif level == 'error':
            logging.error(message)
        else:
            logging.debug(message)