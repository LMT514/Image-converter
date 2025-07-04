import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import re
import subprocess
from pydub import AudioSegment
from pydub.utils import which

class VideoConverter:
    def __init__(self, root, main_root):
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
    
        ffmpeg_path = os.path.join(bundle_dir, "ffmpeg.exe")
        if os.path.isfile(ffmpeg_path):
            AudioSegment.converter = ffmpeg_path

        self.root = root
        self.main_root = main_root
        self.root.title("Video Converter")
        self.root.geometry("700x650")
        self.center_window()
        self.set_app_icon()
        
        # Verify FFmpeg installation
        if not which("ffmpeg"):
            messagebox.showerror(
                "FFmpeg Missing",
                "FFmpeg is required for video conversion. Please install FFmpeg and add it to your PATH."
            )
            self.root.destroy()
            return
        
        # Supported formats
        self.source_formats = [
            "MP4", "AVI", "MOV", "MKV", "FLV", "WMV", "WEBM", "MPEG", "MPG",
            "AUDIO (Extract from Video)"  # Added audio extraction option
        ]
        self.target_formats = [
            ("MP4", "mp4"),
            ("AVI", "avi"),
            ("MOV", "mov"),
            ("MKV", "mkv"),
            ("FLV", "flv"),
            ("WMV", "wmv"),
            ("WEBM", "webm"),
            ("MPEG", "mpeg"),
            ("MPG", "mpg")
        ]
        self.input_paths = []
        self.output_path = ""
        self.MAX_FILES = 20
        
        self.create_widgets()
    
    def center_window(self):
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
        converters = ["Main Menu", "Image Converter", "Audio Converter", "Video Converter"]
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
        self.nav_buttons[3].configure(style="ActiveNav.TButton")
        
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
        ttk.Label(conversion_frame, text="Source Type:").pack(side=tk.LEFT)
        self.source_format_var = tk.StringVar()
        self.source_combo = ttk.Combobox(
            conversion_frame,
            textvariable=self.source_format_var,
            values=self.source_formats,
            state="readonly",
            width=18
        )
        self.source_combo.current(0)
        self.source_combo.pack(side=tk.LEFT, padx=5)
        
        # Target format selection
        ttk.Label(conversion_frame, text="Convert to:").pack(side=tk.LEFT, padx=(5, 0))
        self.target_format_var = tk.StringVar()
        target_names = [fmt[0] for fmt in self.target_formats]
        self.target_combo = ttk.Combobox(
            conversion_frame,
            textvariable=self.target_format_var,
            values=target_names,
            state="readonly",
            width=15
        )
        self.target_combo.current(1)
        self.target_combo.pack(side=tk.LEFT, padx=5)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="STEP 2: SELECT FILES", style="Section.TFrame")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Browse button
        self.upload_btn = ttk.Button(
            input_frame, 
            text="Browse Files", 
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
        self.folder_var = tk.StringVar(value="Converted Videos")
        self.folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.folder_var,
            width=20,
            state="disabled"
        )
        self.folder_entry.pack(side=tk.LEFT, padx=5)
        
        # Convert button
        self.convert_btn = ttk.Button(
            main_frame,
            text="CONVERT",
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
        elif converter_name == "Audio Converter":
            self.root.destroy()
            converter_window = tk.Toplevel(self.main_root)
            from audio_converter import AudioConverter
            AudioConverter(converter_window, self.main_root)
        elif converter_name != "Video Converter":
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
        source_type = self.source_format_var.get()
        
        # Map formats to file extensions
        format_extensions = {
            "MP4": ("*.mp4",),
            "AVI": ("*.avi",),
            "MOV": ("*.mov",),
            "MKV": ("*.mkv",),
            "FLV": ("*.flv",),
            "WMV": ("*.wmv",),
            "WEBM": ("*.webm",),
            "MPEG": ("*.mpeg",),
            "MPG": ("*.mpg",),
            "AUDIO (Extract from Video)": ("*.mp3 *.wav *.aac *.m4a *.ogg *.wma *.flac",)
            
        }
        
        # Get extensions for selected source format
        extensions = format_extensions.get(source_type, ("*.*",))
        filetypes = [
            (f"{source_type} files", ";".join(extensions)),
            ("All files", "*.*")
        ]
        
        file_paths = filedialog.askopenfilenames(filetypes=filetypes)
        if not file_paths:
            return
            
        # Filter files by selected source format
        valid_paths = []
        for path in file_paths:
            ext = os.path.splitext(path)[1].lower()
            if source_type == "AUDIO (Extract from Video)":
                # Allow all video formats for audio extraction
                if ext in ['.mp3', '.wav', '.aac', '.m4a', '.ogg', '.wma', '.flac', '.mpeg', '.mpg']:
                    valid_paths.append(path)
            else:
                # For specific formats, filter by selected source type
                allowed_exts = [e.replace("*", "") for e in extensions]
                if ext in allowed_exts:
                    valid_paths.append(path)
        
        if not valid_paths:
            messagebox.showerror(
                "Format Error", 
                f"No valid {source_type} files selected!"
            )
            return
            
        # Add new files to existing selection
        new_paths = list(set(self.input_paths + valid_paths))
        
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
        try:
            source_type = self.source_format_var.get()
            file_type = "video"
            
            if source_type == "AUDIO (Extract from Video)":
                file_type = "video (audio extraction)"
            
            self.files_label.config(text=f"{len(self.input_paths)} {file_type} files selected")
            self.convert_btn.config(state="normal" if self.input_paths else "disabled")
            self.status_var.set(f"Loaded {len(self.input_paths)} files")
            
            # Show previews for all files
            self.show_previews()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load files:\n{str(e)}")
            self.status_var.set(f"Error loading files: {str(e)}")
    
    def clear_previews(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def show_previews(self):
        try:
            # Clear existing previews
            self.clear_previews()
            
            # Only show if there are files
            if not self.input_paths:
                # Add placeholder text when no files
                placeholder = ttk.Label(
                    self.scrollable_frame,
                    text="No files selected. Click 'Browse Files' to add files.",
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
                    command=lambda f=file_path: self.remove_file(f)
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
    
    def remove_file(self, file_path):
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
    
    def get_format_extension(self, display_name):
        """Get file extension from display name"""
        for fmt in self.target_formats:
            if fmt[0] == display_name:
                return fmt[1]
        return display_name.lower()
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        return re.sub(r'[<>:"/\\|?*]', '', filename)
    
    def convert_files(self):
        if not self.input_paths:
            messagebox.showerror("Error", "No files selected!")
            return
        
        if not self.output_path:
            messagebox.showerror("Error", "Please select an output folder!")
            return
        
        target_display = self.target_format_var.get()
        if not target_display:
            messagebox.showerror("Error", "Please select target format!")
            return
        
        # Get actual file extension
        target_format = self.get_format_extension(target_display)
        
        # Determine output directory
        if self.create_folder_var.get():
            folder_name = self.folder_var.get().strip() or "Converted Videos"
            output_dir = os.path.join(self.output_path, folder_name)
        else:
            output_dir = self.output_path
        
        # Create output folder if needed
        if self.create_folder_var.get() and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.status_var.set(f"Created folder: {folder_name}")
        
        # Convert files
        success_count = 0
        error_count = 0
        total_files = len(self.input_paths)
        ffmpeg_path = which("ffmpeg")
        
        for i, input_path in enumerate(self.input_paths):
            # Sanitize filename and create output path
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            clean_name = self.sanitize_filename(base_name)
            output_file = os.path.join(output_dir, f"{clean_name}.{target_format}")
            
            self.status_var.set(f"Converting {i+1}/{total_files}: {base_name}")
            self.root.update()
            
            try:
                if target_format in ["mp3", "wav", "aac", "m4a", "ogg", "wma", "flac"]:
                    # Extract audio from video
                    audio = AudioSegment.from_file(input_path)
                    
                    # Handle special formats
                    if target_format == "aac":
                        audio.export(output_file, format="adts", codec="aac")
                    elif target_format == "m4a":
                        audio.export(output_file, format="ipod", codec="aac")
                    elif target_format == "wma":
                        audio.export(output_file, format="asf", codec="wmav2")
                    elif target_format == "flac":
                        audio.export(output_file, format="flac", codec="flac", 
                                    parameters=["-compression_level", "8"])
                    else:
                        audio.export(output_file, format=target_format)
                else:
                    # Video-to-video conversion
                    command = [
                        ffmpeg_path,
                        "-i", input_path,
                        "-y",  # Overwrite without asking
                        output_file
                    ]
                    
                    # Run FFmpeg command
                    subprocess.run(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True,
                        text=True
                    )
                
                success_count += 1
                
            except Exception as e:
                error_count += 1
                self.status_var.set(f"Error converting {base_name}: {str(e)}")
                # Log detailed error
                with open("conversion_errors.log", "a") as log_file:
                    log_file.write(f"Error converting {input_path} to {target_format}: {str(e)}\n")
        
        # Show summary
        source_type = self.source_format_var.get()
        if source_type == "AUDIO (Extract from Video)":
            message_text = f"Processed {total_files} video files (audio extracted)\n\n"
        else:
            message_text = f"Processed {total_files} video files\n\n"
            
        messagebox.showinfo(
            "Conversion Complete", 
            message_text +
            f"Success: {success_count}\n"
            f"Errors: {error_count}\n\n"
            f"Files saved to: {output_dir}\n\n"
            "You can convert the same files again or remove them individually."
        )
        
        # Update status
        self.status_var.set(f"Converted {success_count} files to {target_display}")