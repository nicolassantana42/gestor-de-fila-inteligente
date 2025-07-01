import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from src.utils.visualization import MarketApp

if __name__ == "__main__":
    root = tk.Tk()
    app = MarketApp(root)
    root.mainloop()