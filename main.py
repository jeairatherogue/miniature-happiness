import tkinter as tk
import metadata as meta
from func import BarcodeManager as bm
from func import EventLogger as el


def on_button_click_generate():
    barcode_value = str(entry_barcode.get()).upper()
    if len(barcode_value) == 0:
        append_to_console("Barcode cannot be empty.")
    else:
        bm.generate_barcode(barcode_value)
        # Preview the updated image
        bm.preview_temp_png(image_label)
        # Refresh the window to reflect changes
        root.update_idletasks()
def on_button_click_print():
    bm.print_barcode()

def append_to_console(text):
    console.config(state=tk.NORMAL)
    console.insert(tk.END, text + '\n')
    console.see(tk.END)
    console.config(state=tk.DISABLED)

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
console = tk.Text(root, height=7, width=50, state=tk.DISABLED)

# Position the elements
label_barcode_text.grid(row=0, column=0, padx=5, pady=10)
entry_barcode.grid(row=0, column=1, padx=5, pady=10)
button_gen.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky='ew')
image_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky='ew')
button_print.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky='ew')
console.grid(row=4, column=0, columnspan=3, padx=5, pady=10, sticky='ew')

entry_barcode.focus_set()
# Will bind and work on print when I can test it properly. (no printer)
entry_barcode.bind('<Return>', lambda event: on_button_click_generate())
append_to_console(r"""
 /\_/\
( o.o )
 > ^ <
 cat.
""")
el.log_event('info', 'Cat printed. Application loaded.')
# Bind the function to the application close event
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
