import tkinter as tk
import metadata as meta
from func import BarcodeManager as bm
from func import EventLogger as el


def on_button_click_generate():
    barcode_value = str(entry_barcode.get()).upper()
    if len(barcode_value) == 0:
        pass
        # append_to_console("Barcode cannot be empty.")
    else:
        bm.generate_barcode(barcode_value)
        bm.preview_temp_png(image_label) # Preview the updated image
        root.update_idletasks() # Refresh the window to reflect changes
def on_button_click_print():
    bm.print_barcode()

def on_closing():
    bm.flush_temp_images()
    root.destroy()  # Ensure the Tkinter application closes

bm.flush_temp_images()
# Initialize the main window
root = tk.Tk()
root.title(meta.__title__)
root.resizable(width=False, height=False)

# Initial preview of the image
image_label = tk.Label(root)
bm.preview_temp_png(image_label)

# Create the elements
label_barcode_text = tk.Label(root, text="Enter your text:")
entry_barcode = tk.Entry(root, width=30)
button_gen = tk.Button(root, text="Generate", command=on_button_click_generate)
button_print = tk.Button(root, text="Print", command=on_button_click_print)

# Position the elements
label_barcode_text.grid(row=0, column=0, padx=5, pady=10)
entry_barcode.grid(row=0, column=1, padx=5, pady=10)
button_gen.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky='ew')
image_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky='ew')
button_print.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky='ew')

entry_barcode.focus_set()

# Will bind and work on print when I can test it properly. (no printer)
entry_barcode.bind('<Return>', lambda event: on_button_click_generate())
# Bind the function to the application close event
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
