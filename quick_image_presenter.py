import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
import time
from PIL import Image, ImageTk
import threading

class QuickImagePresenter:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Image Presenter")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
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
        
        # Transition types
        self.transitions = [
            "Dissolve", "Fade", "Slide Left", "Slide Right", 
            "Slide Up", "Slide Down", "Zoom In", "Zoom Out",
            "Rotate", "Flip"
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Quick Image Presenter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Folder selection
        ttk.Label(main_frame, text="Image Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(folder_frame, textvariable=self.folder_path, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Default time
        ttk.Label(main_frame, text="Default Display Time (seconds):").grid(row=2, column=0, sticky=tk.W, pady=5)
        time_spinbox = ttk.Spinbox(main_frame, from_=1, to=60, textvariable=self.default_time, width=10)
        time_spinbox.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Transition type
        ttk.Label(main_frame, text="Transition Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        transition_combo = ttk.Combobox(main_frame, textvariable=self.transition_type, 
                                       values=self.transitions, state="readonly", width=15)
        transition_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Play button
        play_button = ttk.Button(main_frame, text="Play Presentation", 
                                command=self.start_presentation, style="Accent.TButton")
        play_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Info button
        info_button = ttk.Button(main_frame, text="ℹ", width=3, command=self.show_info)
        info_button.grid(row=0, column=2, sticky=tk.NE, padx=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to present images", 
                                     font=("Arial", 10))
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(20, 0))
    
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
        self.presentation_window.protocol("WM_DELETE_WINDOW", self.stop_presentation)
        
        # Create close button
        close_button = tk.Button(self.presentation_window, text="✕", 
                                command=self.stop_presentation,
                                bg='red', fg='white', font=('Arial', 16, 'bold'),
                                relief='flat', bd=0, padx=10, pady=5)
        close_button.place(x=self.presentation_window.winfo_screenwidth()-50, y=10)
        
        # Create info button
        info_button = tk.Button(self.presentation_window, text="ℹ", 
                               command=self.show_presentation_info,
                               bg='blue', fg='white', font=('Arial', 16, 'bold'),
                               relief='flat', bd=0, padx=10, pady=5)
        info_button.place(x=self.presentation_window.winfo_screenwidth()-100, y=10)
        
        # Create timer label
        self.timer_label = tk.Label(self.presentation_window, text="", 
                                   bg='black', fg='white', font=('Arial', 24, 'bold'))
        self.timer_label.place(x=self.presentation_window.winfo_screenwidth()-150, y=60)
        
        # Create image label
        self.image_label = tk.Label(self.presentation_window, bg='black')
        self.image_label.pack(expand=True, fill='both')
        
        # Start presentation
        self.show_next_image()
    
    def show_next_image(self):
        if not self.presentation_running or self.current_image_index >= len(self.images):
            self.stop_presentation()
            return
        
        filename, filepath = self.images[self.current_image_index]
        
        try:
            # Load and resize image
            image = Image.open(filepath)
            
            # Get screen dimensions
            screen_width = self.presentation_window.winfo_screenwidth()
            screen_height = self.presentation_window.winfo_screenheight()
            
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
            
            # Update image label
            self.image_label.configure(image=photo)
            self.image_label.image = photo  # Keep a reference
            
            # Determine display time
            display_time = self.extract_time_from_filename(filename)
            if display_time is None:
                display_time = self.default_time.get()
            
            # Start timer
            self.start_timer(display_time)
            
        except Exception as e:
            print(f"Error loading image {filepath}: {e}")
            self.current_image_index += 1
            self.show_next_image()
    
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
        info_text = """Quick Image Presenter v1.0

License: MIT License

This application provides automatic image presentation with the following features:
• Automatic folder-based image loading
• Customizable display times
• Multiple transition effects
• Full-screen presentation mode

Presentation Controls:
• No mouse or keyboard controls during presentation
• Press ESC key or click the X button to exit
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
• X button: Exit presentation
• No other controls available during presentation

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