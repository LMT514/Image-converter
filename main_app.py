import tkinter as tk
import os
import sys
from tkinter import ttk
from image_converter import ImageConverter
from audio_converter import AudioConverter
from video_converter import VideoConverter

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Converter")
        self.root.geometry("700x650")
        self.center_window()
        self.set_app_icon()
        
        self.create_widgets()
    
    def set_app_icon(self):
        """Set application icon with PyInstaller support"""
        try:
            # First try directly in working directory
            self.root.iconbitmap("convert-icon.ico")
        except:
            try:
                # Handle PyInstaller bundled executable
                base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
                icon_path = os.path.join(base_path, "convert-icon.ico")
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
            except:
                pass  # Fail silently if icon can't be loaded
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def create_widgets(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Converter.TButton", font=("Arial", 12), padding=10)
        
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20)
        
        ttk.Label(
            header_frame, 
            text="Advanced File Converter",
            style="Title.TLabel"
        ).pack()
        
        # Converter buttons
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=30)
        
        converters = [
            ("Image Converter", self.open_image_converter),
            ("Audio Converter", self.open_audio_converter),
            ("Video Converter", self.open_video_converter),
        ]
        
        for text, command in converters:
            btn = ttk.Button(
                buttons_frame,
                text=text,
                command=command,
                style="Converter.TButton",
                width=20
            )
            btn.pack(pady=10)
    
    def open_image_converter(self):
        self.root.withdraw()
        converter_window = tk.Toplevel()
        ImageConverter(converter_window, self.root)
    
    def open_audio_converter(self):
        self.root.withdraw()
        converter_window = tk.Toplevel()
        AudioConverter(converter_window, self.root)

    def open_video_converter(self):
        self.root.withdraw()
        converter_window = tk.Toplevel()
        VideoConverter(converter_window, self.root)
    
    def open_converter(self):
        tk.messagebox.showinfo(
            "Coming Soon", 
            "This converter will be available in the next version!"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()