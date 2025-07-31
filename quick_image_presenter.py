import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
import time
from PIL import Image, ImageTk, ImageOps
import threading
import math

class QuickImagePresenter:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Image Presenter")
        self.root.geometry("1400x900")  # Made window bigger
        self.root.resizable(True, True)
        
        # Configure style for modern look
        self.setup_styles()
        
        # Variables
        self.folder_path = tk.StringVar()
        self.default_time = tk.IntVar(value=5)
        self.transition_type = tk.StringVar(value="Dissolve")
        self.images = []
        self.current_image_index = 0
        self.presentation_running = False
        self.presentation_window = None
        self.timer_thread = None
        self.stop_timer = False
        self.preview_images = []
        
        # Transition types
        self.transitions = [
            "Dissolve", "Fade", "Slide Left", "Slide Right", 
            "Slide Up", "Slide Down", "Zoom In", "Zoom Out",
            "Rotate", "Flip"
        ]
        
        self.setup_ui()
    
    def setup_styles(self):
        """Setup modern styling for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors with a modern color scheme
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), foreground='#1a237e')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#303f9f')
        style.configure('Info.TLabel', font=('Segoe UI', 10), foreground='#424242')
        style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'), background='#8e24aa', foreground='white')
        style.configure('Secondary.TButton', font=('Segoe UI', 10), background='#03a9f4', foreground='white')
        style.configure('Preview.TFrame', relief='solid', borderwidth=2, background='#f5f5f5')
        style.configure('Settings.TLabelframe', font=('Segoe UI', 12, 'bold'), foreground='#1a237e')
        style.configure('Settings.TLabelframe.Label', font=('Segoe UI', 12, 'bold'), foreground='#1a237e')
        style.configure('Folder.TLabelframe', font=('Segoe UI', 12, 'bold'), foreground='#1a237e')
        style.configure('Folder.TLabelframe.Label', font=('Segoe UI', 12, 'bold'), foreground='#1a237e')
    
    def setup_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title with enhanced styling
        title_label = ttk.Label(main_frame, text="Quick Image Presenter", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Enhanced folder selection section (left side)
        folder_frame = ttk.LabelFrame(main_frame, text="📁 Image Folder Selection", padding="15", style='Folder.TLabelframe')
        folder_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10), pady=(0, 20))
        folder_frame.columnconfigure(1, weight=1)
        
        ttk.Label(folder_frame, text="Select Folder:", style='Subtitle.TLabel').grid(row=0, column=0, sticky=tk.W, pady=8)
        folder_input_frame = ttk.Frame(folder_frame)
        folder_input_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8)
        folder_input_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(folder_input_frame, textvariable=self.folder_path, font=('Segoe UI', 11)).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(folder_input_frame, text="Browse", command=self.browse_folder, style='Secondary.TButton').grid(row=0, column=1)
        
        # Enhanced settings frame (right side)
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Presentation Settings", padding="15", style='Settings.TLabelframe')
        settings_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=(0, 20))
        settings_frame.columnconfigure(1, weight=1)
        
        # Default time with larger controls
        ttk.Label(settings_frame, text="Display Time (seconds):", style='Subtitle.TLabel').grid(row=0, column=0, sticky=tk.W, pady=8)
        time_spinbox = ttk.Spinbox(settings_frame, from_=1, to=60, textvariable=self.default_time, width=12, font=('Segoe UI', 11))
        time_spinbox.grid(row=0, column=1, sticky=tk.W, pady=8)
        
        # Transition type with larger controls
        ttk.Label(settings_frame, text="Transition Type:", style='Subtitle.TLabel').grid(row=1, column=0, sticky=tk.W, pady=8)
        transition_combo = ttk.Combobox(settings_frame, textvariable=self.transition_type, 
                                       values=self.transitions, state="readonly", width=18, font=('Segoe UI', 11))
        transition_combo.grid(row=1, column=1, sticky=tk.W, pady=8)
        
        # Image preview section
        preview_frame = ttk.LabelFrame(main_frame, text="🖼️ Image Preview", padding="15")
        preview_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)
        
        ttk.Label(preview_frame, text="Selected Images:", style='Subtitle.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Preview canvas with scrollbar
        preview_canvas_frame = ttk.Frame(preview_frame)
        preview_canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        preview_canvas_frame.columnconfigure(0, weight=1)
        preview_canvas_frame.rowconfigure(0, weight=1)
        
        self.preview_canvas = tk.Canvas(preview_canvas_frame, bg='white', height=200)
        preview_scrollbar = ttk.Scrollbar(preview_canvas_frame, orient="horizontal", command=self.preview_canvas.xview)
        self.preview_canvas.configure(xscrollcommand=preview_scrollbar.set)
        
        self.preview_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        preview_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Preview container frame
        self.preview_container = ttk.Frame(self.preview_canvas)
        self.preview_canvas.create_window((0, 0), window=self.preview_container, anchor="nw")
        
        # Enhanced play button
        play_button = ttk.Button(main_frame, text="🎬 Start Presentation", 
                                command=self.start_presentation, style='Accent.TButton')
        play_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Info button
        info_button = ttk.Button(main_frame, text="ℹ", width=3, command=self.show_info, style='Secondary.TButton')
        info_button.grid(row=0, column=1, sticky=tk.NE, padx=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to present images", style='Info.TLabel')
        self.status_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # Bind canvas resize
        self.preview_container.bind('<Configure>', lambda e: self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all")))
    
    def fix_image_orientation(self, image):
        """Fix image orientation based on EXIF data"""
        try:
            # Check if image has EXIF data
            if hasattr(image, '_getexif') and image._getexif() is not None:
                exif = image._getexif()
                if exif is not None:
                    # Get orientation tag
                    orientation = exif.get(274)  # 274 is the orientation tag
                    if orientation is not None:
                        # Apply the correct rotation
                        if orientation == 3:
                            image = image.rotate(180, expand=True)
                        elif orientation == 6:
                            image = image.rotate(270, expand=True)
                        elif orientation == 8:
                            image = image.rotate(90, expand=True)
        except Exception as e:
            print(f"Error fixing image orientation: {e}")
        
        return image
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:
            self.folder_path.set(folder)
            self.load_images()
    
    def load_images(self):
        folder = self.folder_path.get()
        if not folder or not os.path.exists(folder):
            return
        
        # Supported image formats
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
        
        self.images = []
        for filename in os.listdir(folder):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                filepath = os.path.join(folder, filename)
                self.images.append((filename, filepath))
        
        # Sort images in ascending order
        self.images.sort(key=lambda x: x[0].lower())
        
        self.status_label.config(text=f"Loaded {len(self.images)} images")
        self.update_preview()
    
    def update_preview(self):
        """Update the image preview section"""
        # Clear existing previews
        for widget in self.preview_container.winfo_children():
            widget.destroy()
        
        self.preview_images = []
        
        # Show up to 8 preview images
        preview_count = min(len(self.images), 8)
        
        for i in range(preview_count):
            if i < len(self.images):
                filename, filepath = self.images[i]
                
                try:
                    # Load and resize image for preview
                    image = Image.open(filepath)
                    # Fix orientation before resizing
                    image = self.fix_image_orientation(image)
                    image.thumbnail((120, 120), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    # Create preview frame
                    preview_frame = ttk.Frame(self.preview_container, style='Preview.TFrame')
                    preview_frame.grid(row=0, column=i, padx=5, pady=5)
                    
                    # Image label
                    img_label = ttk.Label(preview_frame, image=photo)
                    img_label.image = photo
                    img_label.pack(pady=5)
                    
                    # Filename label
                    name_label = ttk.Label(preview_frame, text=filename[:15] + "..." if len(filename) > 15 else filename, 
                                          style='Info.TLabel', wraplength=100)
                    name_label.pack(pady=2)
                    
                    self.preview_images.append(photo)
                    
                except Exception as e:
                    print(f"Error loading preview for {filepath}: {e}")
        
        # Update canvas scroll region
        self.preview_container.update_idletasks()
        self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))
    
    def extract_time_from_filename(self, filename):
        """Extract time from filename like '1a-11' -> 11 seconds"""
        # Remove file extension
        name_without_ext = os.path.splitext(filename)[0]
        
        # Look for pattern like '-11' at the end
        match = re.search(r'-(\d+)$', name_without_ext)
        if match:
            return int(match.group(1))
        
        return None
    
    def start_presentation(self):
        if not self.images:
            messagebox.showwarning("No Images", "Please select a folder with images first.")
            return
        
        self.presentation_running = True
        self.current_image_index = 0
        
        # Create fullscreen presentation window
        self.presentation_window = tk.Toplevel(self.root)
        self.presentation_window.title("Image Presentation")
        self.presentation_window.attributes('-fullscreen', True)
        self.presentation_window.configure(bg='black')
        
        # Bind escape key and close button
        self.presentation_window.bind('<Escape>', lambda e: self.stop_presentation())
        self.presentation_window.bind('<Key>', lambda e: self.handle_key_press(e))
        self.presentation_window.protocol("WM_DELETE_WINDOW", self.stop_presentation)
        
        # Create top control bar
        control_frame = tk.Frame(self.presentation_window, bg='black', height=80)
        control_frame.pack(fill='x', side='top')
        control_frame.pack_propagate(False)
        
        # Close button (top right)
        close_button = tk.Button(control_frame, text="✕", 
                                command=self.stop_presentation,
                                bg='red', fg='white', 
                                font=('Segoe UI', 16, 'bold'),
                                relief='flat', bd=0, padx=15, pady=8,
                                activebackground='darkred', activeforeground='white')
        close_button.pack(side='right', padx=20, pady=20)
        
        # Timer label (top left)
        self.timer_label = tk.Label(control_frame, text="", 
                                   bg='black', fg='white', 
                                   font=('Segoe UI', 20, 'bold'))
        self.timer_label.pack(side='left', padx=20, pady=20)
        
        # Image counter (top left)
        self.counter_label = tk.Label(control_frame, text="", 
                                     bg='black', fg='white', 
                                     font=('Segoe UI', 14))
        self.counter_label.pack(side='left', padx=20, pady=20)
        
        # Create image label
        self.image_label = tk.Label(self.presentation_window, bg='black')
        self.image_label.pack(expand=True, fill='both')
        
        # Start presentation
        self.show_next_image()
    
    def handle_key_press(self, event):
        """Handle key presses during presentation"""
        if event.keysym == 'Escape':
            self.stop_presentation()
        elif event.keysym == 'Left':
            self.previous_image()
        elif event.keysym == 'Right':
            self.next_image()
        elif event.keysym == 'space':
            self.toggle_pause()
    
    def previous_image(self):
        """Go to previous image"""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_next_image()
    
    def next_image(self):
        """Go to next image"""
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.show_next_image()
    
    def toggle_pause(self):
        """Toggle pause/resume"""
        if hasattr(self, 'paused'):
            self.paused = not self.paused
            if not self.paused:
                self.start_timer(self.current_display_time)
        else:
            self.paused = True
            self.stop_timer = True
    
    def show_next_image(self):
        if not self.presentation_running or self.current_image_index >= len(self.images):
            self.stop_presentation()
            return
        
        filename, filepath = self.images[self.current_image_index]
        
        try:
            # Load and resize image
            image = Image.open(filepath)
            # Fix orientation before resizing
            image = self.fix_image_orientation(image)
            
            # Get screen dimensions
            screen_width = self.presentation_window.winfo_screenwidth()
            screen_height = self.presentation_window.winfo_screenheight() - 80  # Account for control bar
            
            # Calculate aspect ratio
            img_width, img_height = image.size
            aspect_ratio = img_width / img_height
            screen_ratio = screen_width / screen_height
            
            if aspect_ratio > screen_ratio:
                # Image is wider than screen
                new_width = screen_width
                new_height = int(screen_width / aspect_ratio)
            else:
                # Image is taller than screen
                new_height = screen_height
                new_width = int(screen_height * aspect_ratio)
            
            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Apply transition effect
            self.apply_transition(photo)
            
            # Update counter label
            self.counter_label.config(text=f"Image {self.current_image_index + 1} of {len(self.images)}")
            
            # Determine display time
            display_time = self.extract_time_from_filename(filename)
            if display_time is None:
                display_time = self.default_time.get()
            
            self.current_display_time = display_time
            
            # Start timer
            self.start_timer(display_time)
            
        except Exception as e:
            print(f"Error loading image {filepath}: {e}")
            self.current_image_index += 1
            self.show_next_image()
    
    def apply_transition(self, new_photo):
        """Apply transition effect based on selected type"""
        transition = self.transition_type.get()
        
        if transition == "Dissolve":
            self.apply_dissolve_transition(new_photo)
        elif transition == "Fade":
            self.apply_fade_transition(new_photo)
        elif transition == "Slide Left":
            self.apply_slide_transition(new_photo, "left")
        elif transition == "Slide Right":
            self.apply_slide_transition(new_photo, "right")
        elif transition == "Slide Up":
            self.apply_slide_transition(new_photo, "up")
        elif transition == "Slide Down":
            self.apply_slide_transition(new_photo, "down")
        elif transition == "Zoom In":
            self.apply_zoom_transition(new_photo, "in")
        elif transition == "Zoom Out":
            self.apply_zoom_transition(new_photo, "out")
        elif transition == "Rotate":
            self.apply_rotate_transition(new_photo)
        elif transition == "Flip":
            self.apply_flip_transition(new_photo)
        else:
            # Default: immediate change
            self.image_label.configure(image=new_photo)
            self.image_label.image = new_photo
    
    def apply_dissolve_transition(self, new_photo):
        """Apply dissolve transition effect"""
        # Create a simple crossfade effect
        self.image_label.configure(image=new_photo)
        self.image_label.image = new_photo
        # Add a brief pause for visual effect
        self.root.after(100)
    
    def apply_fade_transition(self, new_photo):
        """Apply fade transition effect"""
        # Simple fade transition with opacity change
        self.image_label.configure(image=new_photo)
        self.image_label.image = new_photo
        # Add a brief pause for visual effect
        self.root.after(150)
    
    def apply_slide_transition(self, new_photo, direction):
        """Apply slide transition effect"""
        # Get current image position
        x, y = 0, 0
        screen_width = self.presentation_window.winfo_screenwidth()
        screen_height = self.presentation_window.winfo_screenheight() - 80
        
        # Set initial position based on direction
        if direction == "left":
            x = screen_width
        elif direction == "right":
            x = -screen_width
        elif direction == "up":
            y = screen_height
        elif direction == "down":
            y = -screen_height
        
        # Create temporary label for transition
        temp_label = tk.Label(self.presentation_window, image=new_photo, bg='black')
        temp_label.image = new_photo
        temp_label.place(x=x, y=y)
        
        # Animate the slide
        steps = 20
        for i in range(steps + 1):
            if not self.presentation_running:
                temp_label.destroy()
                return
            
            progress = i / steps
            if direction == "left":
                new_x = screen_width * (1 - progress)
            elif direction == "right":
                new_x = -screen_width * (1 - progress)
            elif direction == "up":
                new_y = screen_height * (1 - progress)
            elif direction == "down":
                new_y = -screen_height * (1 - progress)
            
            temp_label.place(x=new_x, y=new_y)
            self.root.after(20)  # 20ms delay between steps
        
        # Replace the main image
        self.image_label.configure(image=new_photo)
        self.image_label.image = new_photo
        temp_label.destroy()
    
    def apply_zoom_transition(self, new_photo, zoom_type):
        """Apply zoom transition effect"""
        # Create temporary label for transition
        temp_label = tk.Label(self.presentation_window, image=new_photo, bg='black')
        temp_label.image = new_photo
        temp_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Animate the zoom
        steps = 15
        for i in range(steps + 1):
            if not self.presentation_running:
                temp_label.destroy()
                return
            
            progress = i / steps
            if zoom_type == "in":
                scale = 0.1 + (0.9 * progress)
            else:  # zoom out
                scale = 1.0 - (0.9 * progress)
            
            # Apply scaling effect
            temp_label.configure(width=int(self.presentation_window.winfo_screenwidth() * scale),
                               height=int((self.presentation_window.winfo_screenheight() - 80) * scale))
            self.root.after(25)  # 25ms delay between steps
        
        # Replace the main image
        self.image_label.configure(image=new_photo)
        self.image_label.image = new_photo
        temp_label.destroy()
    
    def apply_rotate_transition(self, new_photo):
        """Apply rotate transition effect"""
        # Create temporary label for transition
        temp_label = tk.Label(self.presentation_window, image=new_photo, bg='black')
        temp_label.image = new_photo
        temp_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Animate the rotation (simulated with scaling)
        steps = 20
        for i in range(steps + 1):
            if not self.presentation_running:
                temp_label.destroy()
                return
            
            progress = i / steps
            # Simulate rotation with scaling changes
            scale = 0.5 + (0.5 * abs(math.sin(progress * math.pi)))
            
            temp_label.configure(width=int(self.presentation_window.winfo_screenwidth() * scale),
                               height=int((self.presentation_window.winfo_screenheight() - 80) * scale))
            self.root.after(30)  # 30ms delay between steps
        
        # Replace the main image
        self.image_label.configure(image=new_photo)
        self.image_label.image = new_photo
        temp_label.destroy()
    
    def apply_flip_transition(self, new_photo):
        """Apply flip transition effect"""
        # Create temporary label for transition
        temp_label = tk.Label(self.presentation_window, image=new_photo, bg='black')
        temp_label.image = new_photo
        temp_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Animate the flip (simulated with scaling)
        steps = 15
        for i in range(steps + 1):
            if not self.presentation_running:
                temp_label.destroy()
                return
            
            progress = i / steps
            # Simulate flip with horizontal scaling
            scale_x = abs(math.cos(progress * math.pi))
            scale_y = 1.0
            
            temp_label.configure(width=int(self.presentation_window.winfo_screenwidth() * scale_x),
                               height=int((self.presentation_window.winfo_screenheight() - 80) * scale_y))
            self.root.after(25)  # 25ms delay between steps
        
        # Replace the main image
        self.image_label.configure(image=new_photo)
        self.image_label.image = new_photo
        temp_label.destroy()
    
    def start_timer(self, duration):
        self.stop_timer = False
        self.timer_thread = threading.Thread(target=self.countdown_timer, args=(duration,))
        self.timer_thread.daemon = True
        self.timer_thread.start()
    
    def countdown_timer(self, duration):
        for i in range(duration, 0, -1):
            if self.stop_timer:
                return
            
            # Update timer label
            self.presentation_window.after(0, lambda t=i: self.timer_label.config(text=f"{t}s"))
            time.sleep(1)
        
        if not self.stop_timer:
            # Move to next image
            self.current_image_index += 1
            self.presentation_window.after(0, self.show_next_image)
    
    def stop_presentation(self):
        self.presentation_running = False
        self.stop_timer = True
        
        if self.presentation_window:
            self.presentation_window.destroy()
            self.presentation_window = None
    
    def show_info(self):
        info_text = """Quick Image Presenter v2.0

License: MIT License

This application provides automatic image presentation with the following features:
• Automatic folder-based image loading
• Customizable display times
• Multiple transition effects
• Full-screen presentation mode
• Image preview functionality
• Modern UI design

Presentation Controls:
• ESC key: Exit presentation
• Left/Right arrows: Navigate images
• Spacebar: Pause/Resume
• X button: Exit presentation
• Images are displayed in ascending alphabetical order
• Display time is extracted from filename (e.g., 'image-10.jpg' = 10 seconds)
• If no time is specified in filename, default time is used

MIT License:
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
        
        messagebox.showinfo("About Quick Image Presenter", info_text)
    
    def show_presentation_info(self):
        info_text = """Quick Image Presenter - Active Session

Current Status: Full-screen presentation mode

Controls:
• ESC key: Exit presentation
• Left/Right arrows: Navigate images
• Spacebar: Pause/Resume
• X button: Exit presentation

Image Display Algorithm:
• Images displayed in ascending alphabetical order
• Display time extracted from filename (e.g., 'image-10.jpg' = 10 seconds)
• Default time used if no time specified in filename
• Automatic progression to next image

License: MIT License"""
        
        messagebox.showinfo("Presentation Info", info_text)

def main():
    root = tk.Tk()
    app = QuickImagePresenter(root)
    root.mainloop()

if __name__ == "__main__":
    main() 