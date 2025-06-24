import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from pydub import AudioSegment

class AudioConverter:
    def __init__(self, root, main_root):
        self.root = root
        self.main_root = main_root
        self.root.title("Audio Converter")
        self.root.geometry("700x650")  # Adjusted height
        self.center_window()
        self.set_app_icon()
        
        # Supported formats
        self.formats = ["MP3", "WAV", "AAC", "M4A", "OGG", "WMA"]
        self.input_paths = []
        self.output_path = ""
        self.MAX_FILES = 20
        
        self.create_widgets()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def set_app_icon(self):
        try:
            self.root.iconbitmap("convert-icon.ico")
        except:
            try:
                base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
                icon_path = os.path.join(base_path, "convert-icon.ico")
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
            except:
                pass
    
    def create_widgets(self):
        # Configure style
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Section.TFrame", background="#ffffff", relief="solid", borderwidth=1)
        style.configure("Nav.TButton", font=("Arial", 10, "bold"), padding=5)
        style.configure("Preview.TFrame", background="#ffffff", relief="groove", borderwidth=1)
        
        # Navigation bar
        nav_frame = ttk.Frame(self.root, height=40)
        nav_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Nav buttons
        converters = ["Main Menu", "Image Converter", "Audio Converter", "Video Converter", "Document Converter"]
        self.nav_buttons = []
        for converter in converters:
            btn = ttk.Button(
                nav_frame,
                text=converter,
                style="Nav.TButton",
                command=lambda c=converter: self.navigate(c)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.nav_buttons.append(btn)
        
        # Highlight current converter
        self.nav_buttons[2].configure(style="ActiveNav.TButton")
        
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
        self.target_combo.current(1)
        self.target_combo.pack(side=tk.LEFT, padx=5)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="STEP 2: SELECT AUDIO FILES", style="Section.TFrame")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Browse button
        self.upload_btn = ttk.Button(
            input_frame, 
            text="Browse Audio Files", 
            command=self.browse_files
        )
        self.upload_btn.pack(pady=10, padx=10)
        
        # Preview frame with scrollbar
        preview_frame = ttk.Frame(input_frame)
        preview_frame.pack(fill=tk.X, pady=(5, 10))
        
        # Create container for preview with scrollable canvas
        preview_container = ttk.Frame(preview_frame)
        preview_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(preview_container, bg="#f0f0f0", height=150)
        scrollbar = ttk.Scrollbar(preview_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Preview.TFrame")
        
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
        self.files_label.pack(pady=(0, 10))
        
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
        self.folder_var = tk.StringVar(value="Converted Audio")
        self.folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.folder_var,
            width=20
        )
        self.folder_entry.pack(side=tk.LEFT, padx=5)
        
        # Convert button
        self.convert_btn = ttk.Button(
            main_frame,
            text="CONVERT AUDIO",
            command=self.convert_files,
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
    
    def navigate(self, converter_name):
        if converter_name == "Main Menu":
            self.root.destroy()
            self.main_root.deiconify()
        elif converter_name == "Image Converter":
            self.root.destroy()
            converter_window = tk.Toplevel(self.main_root)
            from image_converter import ImageConverter
            ImageConverter(converter_window, self.main_root)
        elif converter_name != "Audio Converter":
            messagebox.showinfo(
                "Coming Soon", 
                f"{converter_name} will be available in the next version!"
            )
    
    def toggle_folder_entry(self):
        if self.create_folder_var.get():
            self.folder_entry.config(state="normal")
        else:
            self.folder_entry.config(state="disabled")
    
    def browse_files(self):
        filetypes = [
            ("Audio Files", "*.mp3 *.wav *.aac *.m4a *.ogg *.wma"),
            ("All Files", "*.*")
        ]
        
        file_paths = filedialog.askopenfilenames(filetypes=filetypes)
        if not file_paths:
            return
            
        # Add new files to existing selection
        new_paths = list(set(self.input_paths + list(file_paths)))
        
        # Limit to MAX_FILES
        if len(new_paths) > self.MAX_FILES:
            new_paths = new_paths[:self.MAX_FILES]
            messagebox.showwarning(
                "File Limit", 
                f"Maximum {self.MAX_FILES} files allowed. Only first {self.MAX_FILES} will be processed."
            )
        
        self.input_paths = new_paths
        self.process_files()
    
    def process_files(self):
        """Process the selected files and show previews"""
        try:
            self.files_label.config(text=f"{len(self.input_paths)} files selected")
            self.convert_btn.config(state="normal" if self.input_paths else "disabled")
            self.status_var.set(f"Loaded {len(self.input_paths)} audio files")
            
            # Show previews for all audio files
            self.show_previews()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load files:\n{str(e)}")
            self.status_var.set(f"Error loading files: {str(e)}")
    
    def clear_previews(self):
        """Clear existing previews"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def show_previews(self):
        """Display preview for all audio files with remove buttons"""
        try:
            # Clear existing previews
            self.clear_previews()
            
            # Only show if there are files
            if not self.input_paths:
                # Add placeholder text when no files
                placeholder = ttk.Label(
                    self.scrollable_frame,
                    text="No files selected. Click 'Browse Audio Files' to add files.",
                    foreground="#888888",
                    font=("Arial", 9)
                )
                placeholder.pack(pady=20)
                return
            
            # Configure for file list
            for i, file_path in enumerate(self.input_paths):
                # Create file container
                file_frame = ttk.Frame(
                    self.scrollable_frame,
                    padding=5,
                    relief="groove",
                    borderwidth=1
                )
                file_frame.pack(fill=tk.X, padx=5, pady=2)
                file_frame.file_path = file_path  # Store file path in frame
                
                # Filename with remove button
                filename = os.path.basename(file_path)
                
                # Filename and remove button container
                bottom_frame = ttk.Frame(file_frame)
                bottom_frame.pack(fill=tk.X, expand=True)
                
                # Filename label
                ttk.Label(
                    bottom_frame,
                    text=filename,
                    width=50,
                    anchor=tk.W
                ).pack(side=tk.LEFT, padx=(0, 5))
                
                # Remove button
                remove_btn = ttk.Button(
                    bottom_frame,
                    text="X",
                    width=6,
                    command=lambda f=file_path: self.remove_audio(f)
                )
                remove_btn.pack(side=tk.RIGHT)
            
            # Update canvas scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            # Create error label if preview fails
            error_label = ttk.Label(
                self.scrollable_frame,
                text=f"Preview Error: {str(e)}",
                foreground="red"
            )
            error_label.pack()
    
    def remove_audio(self, file_path):
        """Remove a specific audio file from the selection"""
        if file_path in self.input_paths:
            self.input_paths.remove(file_path)
            self.status_var.set(f"Removed: {os.path.basename(file_path)}")
            self.process_files()  # Update previews and file count
    
    def set_output_path(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path = path
            self.path_var.set(path)
            self.status_var.set(f"Output path set to: {path}")
    
    def convert_files(self):
        if not self.input_paths:
            messagebox.showerror("Error", "No audio files selected!")
            return
        
        if not self.output_path:
            messagebox.showerror("Error", "Please select an output folder!")
            return
        
        target_format = self.target_format_var.get().lower()
        if not target_format:
            messagebox.showerror("Error", "Please select target format!")
            return
        
        # Determine output directory
        if self.create_folder_var.get():
            folder_name = self.folder_var.get().strip() or "Converted Audio"
            output_dir = os.path.join(self.output_path, folder_name)
        else:
            output_dir = self.output_path
        
        # Create output folder if needed
        if self.create_folder_var.get() and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.status_var.set(f"Created folder: {folder_name}")
        
        # Convert audio files
        success_count = 0
        error_count = 0
        total_files = len(self.input_paths)
        
        for i, input_path in enumerate(self.input_paths):
            filename = os.path.splitext(os.path.basename(input_path))[0]
            output_file = os.path.join(output_dir, f"{filename}.{target_format}")
            
            self.status_var.set(f"Converting {i+1}/{total_files}: {filename}")
            self.root.update()
            
            try:
                # Load audio file
                audio = AudioSegment.from_file(input_path)
                
                # Export to target format
                audio.export(output_file, format=target_format)
                success_count += 1
                
            except Exception as e:
                error_count += 1
                self.status_var.set(f"Error converting {filename}: {str(e)}")
        
        # Show summary
        messagebox.showinfo(
            "Conversion Complete", 
            f"Processed {total_files} audio files\n\n"
            f"Success: {success_count}\n"
            f"Errors: {error_count}\n\n"
            f"Files saved to: {output_dir}\n\n"
            "You can convert the same files again or remove them individually."
        )
        
        # Update status
        self.status_var.set(f"Converted {success_count} audio files to {target_format.upper()}")