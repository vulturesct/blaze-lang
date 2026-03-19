import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
import os

root = tk.Tk()
root.withdraw()

file = filedialog.askopenfilename(
    title="Open a Blaze file 🔥",
    filetypes=[("Blaze Files", "*.blz"), ("All Files", "*.*")]
)

if file:
    blaze = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blaze.py')
    subprocess.run([sys.executable, blaze, file])
else:
    messagebox.showinfo("Blaze", "No file selected!")

root.destroy()