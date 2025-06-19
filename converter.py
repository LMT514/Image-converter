import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Scrollbar
from PIL import Image, ImageTk
import os
import sys

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Converter")
        self.root.geometry("600x700")  # Increased window height for thumbnail grid
        
        self.set_app_icon()
        
        # Supported formats
        self.formats = ["PNG", "JPG", "JPEG", "ICO", "BMP"]
        self.input_paths = []
        self.output_path = ""
        self.preview_images = []  # Store references to all preview images
        self.MAX_FILES = 20
        
        # Create UI elements
        self.create_widgets()
    
    def set_app_icon(self):
        """Set application icon if available"""
        try:
            if os.path.exists("convert-icon.ico"):
                self.root.iconbitmap("convert-icon.ico")
            else:
                base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
                icon_path = os.path.join(base_path, "convert-icon.ico")
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
        except Exception:
            pass
    
    def create_widgets(self):
        # Configure style
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Section.TFrame", background="#ffffff", relief="solid", borderwidth=1)
        
        # Main container frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Conversion format section
        format_frame = ttk.LabelFrame(main_frame, text="STEP 1: SELECT CONVERSION", style="Section.TFrame")
        format_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Format selection frame
        conversion_frame = ttk.Frame(format_frame)
        conversion_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Source format selection
        ttk.Label(conversion_frame, text="Convert from:").pack(side=tk.LEFT)
        self.source_format_var = tk.StringVar()
        self.source_combo = ttk.Combobox(
            conversion_frame,
            textvariable=self.source_format_var,
            values=self.formats,
            state="readonly",
            width=8
        )
        self.source_combo.current(0)
        self.source_combo.pack(side=tk.LEFT, padx=5)
        
        # Target format selection
        ttk.Label(conversion_frame, text="to:").pack(side=tk.LEFT, padx=(5, 0))
        self.target_format_var = tk.StringVar()
        self.target_combo = ttk.Combobox(
            conversion_frame,
            textvariable=self.target_format_var,
            values=self.formats,
            state="readonly",
            width=8
        )
        self.target_combo.current(0)
        self.target_combo.pack(side=tk.LEFT, padx=5)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="STEP 2: SELECT INPUT", style="Section.TFrame")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Browse button
        self.upload_btn = ttk.Button(
            input_frame, 
            text="Browse Images", 
            command=self.browse_images
        )
        self.upload_btn.pack(pady=(10, 5), padx=10)
        
        # Preview frame with scrollbar
        preview_frame = ttk.Frame(input_frame)
        preview_frame.pack(fill=tk.X, pady=(5, 10))
        
        # Create container for preview with scrollable canvas
        preview_container = ttk.Frame(preview_frame)
        preview_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(preview_container, bg="#f0f0f0", height=200)
        scrollbar = ttk.Scrollbar(preview_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Selected files label
        self.files_label = ttk.Label(
            input_frame, 
            text="No files selected",
            foreground="#555555"
        )
        self.files_label.pack(pady=(0, 5))
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="STEP 3: CONFIGURE OUTPUT", style="Section.TFrame")
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Output path selection
        path_frame = ttk.Frame(output_frame)
        path_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        ttk.Label(path_frame, text="Save to:").pack(side=tk.LEFT)
        
        self.path_var = tk.StringVar(value="Select output folder")
        self.path_label = ttk.Label(
            path_frame, 
            textvariable=self.path_var,
            foreground="#333333",
            width=30
        )
        self.path_label.pack(side=tk.LEFT, padx=5)
        
        self.path_btn = ttk.Button(
            path_frame, 
            text="Browse...", 
            width=8,
            command=self.set_output_path
        )
        self.path_btn.pack(side=tk.RIGHT)
        
        # Create folder options frame
        folder_frame = ttk.Frame(output_frame)
        folder_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        # Create folder checkbox
        self.create_folder_var = tk.BooleanVar(value=False)
        create_folder_cb = ttk.Checkbutton(
            folder_frame,
            text="Create output folder:",
            variable=self.create_folder_var,
            command=self.toggle_folder_entry
        )
        create_folder_cb.pack(side=tk.LEFT)
        
        # Folder name entry
        self.folder_var = tk.StringVar(value="Converted Images")
        self.folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.folder_var,
            width=20
        )
        self.folder_entry.pack(side=tk.LEFT, padx=5)
        
        # Convert button
        self.convert_btn = ttk.Button(
            main_frame,
            text="CONVERT IMAGES",
            command=self.convert_images,
            state="disabled"
        )
        self.convert_btn.pack(pady=20)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def toggle_folder_entry(self):
        """Enable/disable folder name entry based on checkbox state"""
        if self.create_folder_var.get():
            self.folder_entry.config(state="normal")
        else:
            self.folder_entry.config(state="disabled")
    
    def browse_images(self, event=None):
        """Open file dialog to select multiple images of the selected source format"""
        source_format = self.source_format_var.get().lower()
        
        # Map formats to file extensions
        format_extensions = {
            "png": ("*.png",),
            "jpg": ("*.jpg", "*.jpeg"),
            "jpeg": ("*.jpg", "*.jpeg"),
            "ico": ("*.ico",),
            "bmp": ("*.bmp",)
        }
        
        # Get extensions for selected source format
        extensions = format_extensions.get(source_format, ("*.*",))
        filetypes = [
            (f"{source_format.upper()} files", ";".join(extensions)),
            ("All files", "*.*")
        ]
        
        file_paths = filedialog.askopenfilenames(filetypes=filetypes)
        if not file_paths:
            return
            
        # Filter files by selected source format
        valid_paths = []
        for path in file_paths:
            ext = os.path.splitext(path)[1].lower()
            if ext in [e.replace("*", "") for e in extensions]:
                valid_paths.append(path)
        
        if not valid_paths:
            messagebox.showerror(
                "Format Error", 
                f"No valid {source_format.upper()} files selected!"
            )
            return
            
        # Limit to MAX_FILES
        if len(valid_paths) > self.MAX_FILES:
            valid_paths = valid_paths[:self.MAX_FILES]
            messagebox.showwarning(
                "File Limit", 
                f"Maximum {self.MAX_FILES} files allowed. Only first {self.MAX_FILES} will be processed."
            )
        
        self.process_files(valid_paths)
    
    def process_files(self, file_paths):
        """Process the selected files and show previews"""
        try:
            # Add new files to existing selection
            self.input_paths = list(set(self.input_paths + list(file_paths)))
            
            # Limit to MAX_FILES
            if len(self.input_paths) > self.MAX_FILES:
                self.input_paths = self.input_paths[:self.MAX_FILES]
                messagebox.showwarning(
                    "File Limit", 
                    f"Maximum {self.MAX_FILES} files allowed. Only first {self.MAX_FILES} will be processed."
                )
            
            self.files_label.config(text=f"{len(self.input_paths)} files selected")
            self.convert_btn.config(state="normal" if self.input_paths else "disabled")
            self.status_var.set(f"Loaded {len(self.input_paths)} images")
            
            # Show previews for all images
            self.show_previews(self.input_paths)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load images:\n{str(e)}")
            self.status_var.set(f"Error loading images: {str(e)}")
    
    def clear_previews(self):
        """Clear existing preview thumbnails"""
        # Clear existing previews
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.preview_images = []
    
    def show_previews(self, file_paths):
        """Display preview thumbnails for all images with remove buttons"""
        try:
            # Clear existing previews
            self.clear_previews()
            
            # Configure grid for thumbnails
            max_columns = 4
            row, col = 0, 0
            
            for i, file_path in enumerate(file_paths):
                # Create thumbnail container with a border
                thumb_frame = ttk.Frame(
                    self.scrollable_frame,
                    padding=2,
                    relief="groove",
                    borderwidth=1
                )
                thumb_frame.grid(row=row, column=col, padx=5, pady=5)
                thumb_frame.file_path = file_path  # Store file path in frame
                
                # Open and resize image for thumbnail
                try:
                    img = Image.open(file_path)
                    img.thumbnail((100, 100))  # Create thumbnail
                    
                    # Convert to PhotoImage for Tkinter
                    photo = ImageTk.PhotoImage(img)
                    self.preview_images.append(photo)  # Keep reference
                    
                    # Create thumbnail label
                    thumb_label = tk.Label(
                        thumb_frame,
                        image=photo,
                        bg="#f0f0f0"
                    )
                    thumb_label.image = photo  # Keep reference
                    thumb_label.pack(pady=(0, 5))
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    thumb_label = tk.Label(
                        thumb_frame,
                        text=error_msg,
                        fg="red",
                        wraplength=100
                    )
                    thumb_label.pack(pady=(0, 5))
                
                # Filename with remove button
                filename = os.path.basename(file_path)
                if len(filename) > 15:
                    filename = filename[:12] + "..."
                
                # Filename and remove button container
                bottom_frame = ttk.Frame(thumb_frame)
                bottom_frame.pack(fill=tk.X, expand=True)
                
                # Filename label
                ttk.Label(
                    bottom_frame,
                    text=filename,
                    width=10,
                    wraplength=80
                ).pack(side=tk.LEFT, padx=(0, 5))
                
                # Remove button
                remove_btn = ttk.Button(
                    bottom_frame,
                    text="X",
                    width=2,
                    command=lambda f=file_path: self.remove_image(f)
                )
                remove_btn.pack(side=tk.RIGHT)
                
                # Update grid position
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1
            
            # Update canvas scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            # Create error label if preview fails
            error_label = ttk.Label(
                self.scrollable_frame,
                text=f"Preview Error: {str(e)}",
                foreground="red"
            )
            error_label.grid(row=0, column=0)
    
    def remove_image(self, file_path):
        """Remove a specific image from the selection"""
        if file_path in self.input_paths:
            self.input_paths.remove(file_path)
            self.status_var.set(f"Removed: {os.path.basename(file_path)}")
            
            # Update UI
            self.files_label.config(text=f"{len(self.input_paths)} files selected")
            if not self.input_paths:
                self.convert_btn.config(state="disabled")
                self.files_label.config(text="No files selected")
            
            # Refresh previews
            self.show_previews(self.input_paths)
    
    def set_output_path(self):
        """Set custom output path"""
        path = filedialog.askdirectory()
        if path:
            self.output_path = path
            self.path_var.set(path)
            self.status_var.set(f"Output path set to: {path}")
    
    def convert_images(self):
        """Convert multiple images to selected format"""
        if not self.input_paths:
            messagebox.showerror("Error", "No images selected!")
            return
        
        if not self.output_path:
            messagebox.showerror("Error", "Please select an output folder!")
            return
        
        output_format = self.target_format_var.get().lower()
        if not output_format:
            messagebox.showerror("Error", "Please select output format!")
            return
        
        try:
            # Determine final output directory
            if self.create_folder_var.get():
                folder_name = self.folder_var.get().strip()
                if not folder_name:
                    folder_name = "Converted Images"
                output_dir = os.path.join(self.output_path, folder_name)
            else:
                output_dir = self.output_path
            
            # Create output folder if needed
            if self.create_folder_var.get() and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                self.status_var.set(f"Created folder: {os.path.basename(output_dir)}")
            
            # Convert images
            success_count = 0
            error_count = 0
            total_files = len(self.input_paths)
            
            for i, input_path in enumerate(self.input_paths):
                filename = os.path.splitext(os.path.basename(input_path))[0]
                output_file = os.path.join(output_dir, f"{filename}.{output_format}")
                
                self.status_var.set(f"Processing {i+1}/{total_files}: {filename}")
                self.root.update()  # Update UI for progress
                
                try:
                    img = Image.open(input_path)
                    
                    # Handle transparency for formats that don't support it
                    if output_format in ["jpg", "jpeg", "bmp"] and img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # Save image
                    img.save(output_file)
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    self.status_var.set(f"Error converting {filename}: {str(e)}")
            
            # Show summary
            messagebox.showinfo(
                "Conversion Complete", 
                f"Processed {total_files} images\n\n"
                f"Success: {success_count}\n"
                f"Errors: {error_count}\n\n"
                f"Files saved to: {output_dir}"
            )
            
            # Reset UI
            self.status_var.set(f"Converted {success_count} images to {output_format.upper()}")
            if success_count > 0:
                self.convert_btn.config(state="disabled")
                self.input_paths = []
                self.files_label.config(text="No files selected")
                self.clear_previews()
            
        except Exception as e:
            messagebox.showerror("Conversion Error", f"An error occurred:\n{str(e)}")
            self.status_var.set(f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()