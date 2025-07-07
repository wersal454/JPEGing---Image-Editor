import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import numpy as np
from io import BytesIO
import random
import cv2

class ComedyImageManipulator:
    def __init__(self, root):
        # Initialize main application window
        self.root = root
        self.root.title("JPEGing - Image Editor")
        self.root.geometry("1200x800")  # Set initial window size
        self.root.configure(bg="#2c3e50")  # Set background color
        
        # Language settings - supports English and Russian
        self.language = "English"
        self.translations = {
            "English": {
                "title": "🎭 JPEGing - Image Editor",
                "load_image": "Load Image",
                "save_image": "Save Result",
                "compress_tab": "JPEG Compression",
                "upscale_tab": "Upscaling",
                "original": "Original Image",
                "result": "Result",
                "placeholder": "Load an image to begin",
                "result_placeholder": "Apply an operation to see result",
                "status_ready": "Ready to work",
                "compress_quality": "Compression Quality:",
                "compress_passes": "Compression Passes:",
                "apply_compress": "Apply Compression",
                "compress_desc": "Creates JPEG compression artifacts",
                "upscale_scale": "Upscale Factor:",
                "upscale_noise": "Noise Level:",
                "color_shift": "Apply Color Distortions",
                "apply_upscale": "Apply Upscaling",
                "upscale_desc": "Image upscaling",
                "status_loading": "Loading: ",
                "status_compressing": "Applying compression...",
                "status_upscaling": "Applying upscaling...",
                "status_saving": "Saving: ",
                "error_load": "Error loading image: ",
                "error_compress": "Compression error: ",
                "error_upscale": "Upscaling error: ",
                "error_save": "Save error: ",
                "warning_no_image": "Please load an image first",
                "warning_no_result": "No result to save",
                "success_save": "Image saved successfully:\n"
            },
            "Russian": {
                "title": "🎭 JPEGing - Image Editor",
                "load_image": "Загрузить изображение",
                "save_image": "Сохранить результат",
                "compress_tab": "JPEG Сжатие",
                "upscale_tab": "Увеличение",
                "original": "Оригинальное изображение",
                "result": "Результат",
                "placeholder": "Загрузите изображение",
                "result_placeholder": "Примените операцию для просмотра результата",
                "status_ready": "Готов к работе",
                "compress_quality": "Качество сжатия:",
                "compress_passes": "Количество проходов:",
                "apply_compress": "Применить сжатие",
                "compress_desc": "Создает артефакты сжатия JPEG",
                "upscale_scale": "Масштаб увеличения:",
                "upscale_noise": "Уровень шума:",
                "color_shift": "Применять цветовые искажения",
                "apply_upscale": "Применить увеличение",
                "upscale_desc": "Увеличение изображения",
                "status_loading": "Загружено: ",
                "status_compressing": "Применение сжатия...",
                "status_upscaling": "Применение увеличения...",
                "status_saving": "Сохранение: ",
                "error_load": "Ошибка загрузки изображения: ",
                "error_compress": "Ошибка сжатия: ",
                "error_upscale": "Ошибка увеличения: ",
                "error_save": "Ошибка сохранения: ",
                "warning_no_image": "Пожалуйста, загрузите изображение",
                "warning_no_result": "Нет результата для сохранения",
                "success_save": "Изображение успешно сохранено:\n"
            }
        }
        
        # Configure ttk styles for themed widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme
        # Configure style for frames
        self.style.configure('TFrame', background='#2c3e50')
        # Configure style for labels
        self.style.configure('TLabel', background='#2c3e50', foreground='#ecf0f1', font=('Arial', 10))
        # Configure style for buttons
        self.style.configure('TButton', font=('Arial', 10), background='#3498db')
        # Configure button active state
        self.style.map('TButton', background=[('active', '#2980b9')])
        # Configure header label style
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        # Configure notebook (tab control) style
        self.style.configure('TNotebook', background='#2c3e50')
        # Configure notebook tab style
        self.style.configure('TNotebook.Tab', background='#34495e', foreground='#ecf0f1', font=('Arial', 10, 'bold'))
        # Configure selected tab style
        self.style.map('TNotebook.Tab', background=[('selected', '#3498db')])
        
        # Application state variables
        self.image_path = None    # Path to loaded image
        self.original_img = None  # Original PIL image object
        self.result_img = None    # Resulting image after processing
        
        # Build the user interface
        self.create_widgets()
    
    def tr(self, key):
        """Get translation for the current language"""
        return self.translations[self.language].get(key, key)
    
    def toggle_language(self):
        """Toggle between English and Russian languages"""
        self.language = "Russian" if self.language == "English" else "English"
        self.update_ui_text()
    
    def update_ui_text(self):
        """Update all UI text elements when language changes"""
        # Update title label
        self.title_label.config(text=self.tr("title"))
        # Update button texts
        self.load_btn.config(text=self.tr("load_image"))
        self.save_btn.config(text=self.tr("save_image"))
        # Update language button text
        self.lang_btn.config(text="RU" if self.language == "English" else "EN")
        
        # Update notebook tab names
        self.notebook.tab(0, text=self.tr("compress_tab"))
        self.notebook.tab(1, text=self.tr("upscale_tab"))
        
        # Update frame titles
        self.original_frame.config(text=self.tr("original"))
        self.result_frame.config(text=self.tr("result"))
        
        # Update placeholder texts
        self.original_placeholder.config(text=self.tr("placeholder"))
        self.result_placeholder.config(text=self.tr("result_placeholder"))
        
        # Update status bar
        self.status_var.set(self.tr("status_ready"))
        
        # Update compression tab elements
        self.compress_qlabel_title.config(text=self.tr("compress_quality"))
        self.compress_plabel_title.config(text=self.tr("compress_passes"))
        self.compress_btn.config(text=self.tr("apply_compress"))
        self.compress_desc.config(text=self.tr("compress_desc"))
        
        # Update upscale tab elements
        self.upscale_slabel_title.config(text=self.tr("upscale_scale"))
        self.upscale_nlabel_title.config(text=self.tr("upscale_noise"))
        self.color_shift_cb.config(text=self.tr("color_shift"))
        self.upscale_btn.config(text=self.tr("apply_upscale"))
        self.upscale_desc.config(text=self.tr("upscale_desc"))
    
    def create_widgets(self):
        """Create all UI elements and layout the application"""
        # Create header frame for title and buttons
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Application title
        self.title_label = ttk.Label(header_frame, text=self.tr("title"), style='Header.TLabel')
        self.title_label.pack(side=tk.LEFT)
        
        # Language toggle button
        self.lang_btn = ttk.Button(header_frame, text="RU", width=3, command=self.toggle_language)
        self.lang_btn.pack(side=tk.RIGHT, padx=5)
        
        # Load image button
        self.load_btn = ttk.Button(header_frame, text=self.tr("load_image"), command=self.load_image)
        self.load_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.X, padx=10, pady=5)
        
        # Create compression tab
        compress_frame = ttk.Frame(self.notebook)
        self.notebook.add(compress_frame, text=self.tr("compress_tab"))
        self.create_compress_tab(compress_frame)
        
        # Create upscaling tab
        upscale_frame = ttk.Frame(self.notebook)
        self.notebook.add(upscale_frame, text=self.tr("upscale_tab"))
        self.create_upscale_tab(upscale_frame)
        
        # Create frame for image display areas
        image_frame = ttk.Frame(self.root)
        image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
        
        # Original image frame
        self.original_frame = ttk.LabelFrame(image_frame, text=self.tr("original"))
        self.original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Result image frame
        self.result_frame = ttk.LabelFrame(image_frame, text=self.tr("result"))
        self.result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Placeholder for original image
        self.original_placeholder = ttk.Label(
            self.original_frame, 
            text=self.tr("placeholder"), 
            font=('Arial', 12), 
            anchor=tk.CENTER
        )
        self.original_placeholder.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder for result image
        self.result_placeholder = ttk.Label(
            self.result_frame, 
            text=self.tr("result_placeholder"), 
            font=('Arial', 12), 
            anchor=tk.CENTER
        )
        self.result_placeholder.pack(fill=tk.BOTH, expand=True)
        
        # Create status bar frame
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Save result button in status bar area
        self.save_btn = ttk.Button(status_frame, text=self.tr("save_image"), command=self.save_image)
        self.save_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=2)
        
        # Status bar variable and label
        self.status_var = tk.StringVar(value=self.tr("status_ready"))
        status_bar = ttk.Label(
            status_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
    
    def create_compress_tab(self, parent):
        """Create compression tab UI elements"""
        # Compression quality variable (1-95)
        self.compress_quality = tk.IntVar(value=5)
        # Number of compression passes variable (1-20)
        self.compress_passes = tk.IntVar(value=3)
        
        # Create parameter frame
        param_frame = ttk.Frame(parent)
        param_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Compression quality label
        self.compress_qlabel_title = ttk.Label(param_frame, text=self.tr("compress_quality"))
        self.compress_qlabel_title.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Compression quality slider
        quality_slider = ttk.Scale(
            param_frame, 
            from_=1, 
            to=95, 
            variable=self.compress_quality, 
            command=lambda v: self.compress_qlabel.config(text=f"{int(float(v))}")
        )
        quality_slider.grid(row=0, column=1, padx=5, sticky=tk.EW)
        
        # Compression quality value display
        self.compress_qlabel = ttk.Label(param_frame, text="5", width=3)
        self.compress_qlabel.grid(row=0, column=2, padx=5)
        
        # Compression passes label
        self.compress_plabel_title = ttk.Label(param_frame, text=self.tr("compress_passes"))
        self.compress_plabel_title.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Compression passes slider
        passes_slider = ttk.Scale(
            param_frame, 
            from_=1, 
            to=20, 
            variable=self.compress_passes, 
            command=lambda v: self.compress_plabel.config(text=f"{int(float(v))}")
        )
        passes_slider.grid(row=1, column=1, padx=5, sticky=tk.EW)
        
        # Compression passes value display
        self.compress_plabel = ttk.Label(param_frame, text="3", width=3)
        self.compress_plabel.grid(row=1, column=2, padx=5)
        
        # Apply compression button
        self.compress_btn = ttk.Button(
            param_frame, 
            text=self.tr("apply_compress"), 
            command=self.apply_compression
        )
        self.compress_btn.grid(row=0, column=3, rowspan=2, padx=10, sticky=tk.NS)
        
        # Description frame
        desc_frame = ttk.Frame(parent)
        desc_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Compression description label
        self.compress_desc = ttk.Label(desc_frame, text=self.tr("compress_desc"))
        self.compress_desc.pack(fill=tk.X)
        
        # Configure column weights
        param_frame.columnconfigure(1, weight=1)
    
    def create_upscale_tab(self, parent):
        """Create upscaling tab UI elements"""
        # Upscale factor variable (2x-8x)
        self.upscale_scale = tk.IntVar(value=4)
        # Noise level variable (0%-100%)
        self.upscale_noise = tk.IntVar(value=30)
        # Apply color shift checkbox variable
        self.apply_color_shift = tk.BooleanVar(value=True)
        
        # Create parameter frame
        param_frame = ttk.Frame(parent)
        param_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Upscale factor label
        self.upscale_slabel_title = ttk.Label(param_frame, text=self.tr("upscale_scale"))
        self.upscale_slabel_title.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Upscale factor slider
        scale_slider = ttk.Scale(
            param_frame, 
            from_=2, 
            to=8, 
            variable=self.upscale_scale, 
            command=lambda v: self.upscale_slabel.config(text=f"{int(float(v))}x")
        )
        scale_slider.grid(row=0, column=1, padx=5, sticky=tk.EW)
        
        # Upscale factor value display
        self.upscale_slabel = ttk.Label(param_frame, text="4x", width=5)
        self.upscale_slabel.grid(row=0, column=2, padx=5)
        
        # Noise level label
        self.upscale_nlabel_title = ttk.Label(param_frame, text=self.tr("upscale_noise"))
        self.upscale_nlabel_title.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Noise level slider
        noise_slider = ttk.Scale(
            param_frame, 
            from_=0, 
            to=100, 
            variable=self.upscale_noise, 
            command=lambda v: self.upscale_nlabel.config(text=f"{int(float(v))}%")
        )
        noise_slider.grid(row=1, column=1, padx=5, sticky=tk.EW)
        
        # Noise level value display
        self.upscale_nlabel = ttk.Label(param_frame, text="30%", width=5)
        self.upscale_nlabel.grid(row=1, column=2, padx=5)
        
        # Color shift checkbox
        self.color_shift_cb = ttk.Checkbutton(
            param_frame, 
            text=self.tr("color_shift"), 
            variable=self.apply_color_shift
        )
        self.color_shift_cb.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Apply upscaling button
        self.upscale_btn = ttk.Button(
            param_frame, 
            text=self.tr("apply_upscale"), 
            command=self.apply_upscale
        )
        self.upscale_btn.grid(row=0, column=3, rowspan=3, padx=10, sticky=tk.NS)
        
        # Description frame
        desc_frame = ttk.Frame(parent)
        desc_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Upscaling description label
        self.upscale_desc = ttk.Label(desc_frame, text=self.tr("upscale_desc"))
        self.upscale_desc.pack(fill=tk.X)
        
        # Configure column weights
        param_frame.columnconfigure(1, weight=1)
    
    def load_image(self):
        """Load an image file from disk"""
        # Open file dialog to select image
        file_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if not file_path:
            return
            
        try:
            self.image_path = file_path
            # Open image using PIL
            self.original_img = Image.open(file_path)
            
            # Display the original image
            self.show_image(self.original_img, self.original_frame, self.original_placeholder)
            
            # Reset result image
            self.result_img = None
            self.result_placeholder.pack(fill=tk.BOTH, expand=True)
            # Clear any existing result widgets
            for widget in self.result_frame.winfo_children():
                if isinstance(widget, (tk.Canvas, ttk.Label)) and widget != self.result_placeholder:
                    widget.destroy()
            
            # Update status bar
            filename = os.path.basename(file_path)
            status_text = f"{self.tr('status_loading')}{filename} ({self.original_img.width}x{self.original_img.height})"
            self.status_var.set(status_text)
        except Exception as e:
            # Show error message if loading fails
            messagebox.showerror("Error", f"{self.tr('error_load')}{str(e)}")
    
    def show_image(self, image, frame, placeholder):
        """Display an image in the specified frame"""
        # Hide placeholder text
        placeholder.pack_forget()
        # Clear any existing widgets in the frame
        for widget in frame.winfo_children():
            if isinstance(widget, (tk.Canvas, ttk.Label)) and widget != placeholder:
                widget.destroy()
        
        # Calculate display size while maintaining aspect ratio
        max_size = (600, 500)  # Max display dimensions
        img_width, img_height = image.size
        ratio = min(max_size[0] / img_width, max_size[1] / img_height)
        display_size = (int(img_width * ratio), int(img_height * ratio))
        
        # Create thumbnail for display
        display_img = image.copy()
        display_img.thumbnail(display_size, Image.LANCZOS)
        # Convert to Tkinter-compatible image
        tk_img = ImageTk.PhotoImage(display_img)
        
        # Create canvas for image display
        canvas = tk.Canvas(frame, bg="#34495e", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        # Display image on canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
        canvas.image = tk_img  # Keep reference to prevent garbage collection
        
        # Add image info label
        info_label = ttk.Label(frame, text=f"Size: {img_width}x{img_height}", anchor=tk.CENTER)
        info_label.pack(fill=tk.X, pady=5)
    
    def apply_compression(self):
        """Apply JPEG compression with artifacts to the image"""
        if not self.image_path or not self.original_img:
            messagebox.showwarning("Warning", self.tr("warning_no_image"))
            return
            
        try:
            # Update status and process UI events
            self.status_var.set(self.tr("status_compressing"))
            self.root.update()
            
            # Get compression parameters
            img = self.original_img.copy()
            quality = self.compress_quality.get()
            passes = self.compress_passes.get()
            
            # Convert to RGB if needed
            current_img = img.copy()
            if current_img.mode != 'RGB':
                current_img = current_img.convert('RGB')
            
            # Apply multiple compression passes
            for _ in range(passes):
                buffer = BytesIO()
                # Save with low quality to create artifacts
                current_img.save(buffer, format='JPEG', quality=quality, optimize=True)
                buffer.seek(0)
                current_img = Image.open(buffer)
            
            # Store and display result
            self.result_img = current_img
            self.show_image(current_img, self.result_frame, self.result_placeholder)
            
            # Calculate compression metrics
            buffer = BytesIO()
            current_img.save(buffer, format='JPEG', quality=quality)
            file_size = buffer.tell() / 1024  # Size in KB
            
            orig_size = os.path.getsize(self.image_path) / 1024
            # Avoid division by zero
            compression_ratio = orig_size / (file_size + 0.0001) if file_size > 0 else 0
            
            # Update status with compression results
            status_text = f"Compression complete! Size: {file_size:.1f} KB (Ratio: {compression_ratio:.1f}x)"
            self.status_var.set(status_text)
            
        except Exception as e:
            # Show compression error
            messagebox.showerror("Error", f"{self.tr('error_compress')}{str(e)}")
            self.status_var.set(self.tr("error_compress"))
    
    def apply_upscale(self):
        """Apply comedic upscaling effect to the image"""
        if not self.image_path or not self.original_img:
            messagebox.showwarning("Warning", self.tr("warning_no_image"))
            return
            
        try:
            # Update status and process UI events
            self.status_var.set(self.tr("status_upscaling"))
            self.root.update()
            
            # Convert PIL image to OpenCV format (BGR)
            img = np.array(self.original_img.convert('RGB'))
            img = img[:, :, ::-1].copy()  # Convert RGB to BGR
            
            # Get upscaling parameters
            scale = self.upscale_scale.get()
            noise_level = self.upscale_noise.get()
            
            # 1. Initial upscale using nearest neighbor for pixelation
            upscaled = cv2.resize(
                img, 
                (0, 0), 
                fx=scale, 
                fy=scale, 
                interpolation=cv2.INTER_NEAREST
            )
            
            # 2. Add pixelation artifacts by downscaling and upscaling
            # Downscale to half size
            pixelated = cv2.resize(
                upscaled, 
                (upscaled.shape[1]//2, upscaled.shape[0]//2), 
                interpolation=cv2.INTER_NEAREST
            )
            # Upscale back to original size
            pixelated = cv2.resize(
                pixelated, 
                (upscaled.shape[1], upscaled.shape[0]), 
                interpolation=cv2.INTER_NEAREST
            )
            
            # 3. Blend original upscale and pixelated version
            result = cv2.addWeighted(upscaled, 0.5, pixelated, 0.5, 0)
            
            # 4. Apply color distortions if enabled
            if self.apply_color_shift.get():
                # Split color channels
                b, g, r = cv2.split(result)
                
                # Random channel offsets for chromatic aberration effect
                offset_x = random.randint(-5, 5)
                offset_y = random.randint(-5, 5)
                # Shift blue channel
                b = np.roll(b, (offset_x, offset_y), (1, 0))
                # Shift green channel (half as much)
                g = np.roll(g, (offset_x//2, offset_y//2), (1, 0))
                
                # Enhance colors for comedic effect
                r = cv2.multiply(r, 1.2)  # Boost reds
                g = cv2.multiply(g, 0.9)  # Reduce greens
                
                # Merge channels back
                result = cv2.merge([b, g, r])
            
            # 5. Add noise if noise level > 0
            if noise_level > 0:
                # Generate random noise
                noise = np.random.randint(-noise_level, noise_level, result.shape, dtype=np.int16)
                # Add noise to image
                result = cv2.add(result.astype(np.int16), noise)
                # Clip values to valid range (0-255)
                result = np.clip(result, 0, 255).astype(np.uint8)
            
            # 6. Apply slight blur to blend artifacts
            result = cv2.GaussianBlur(result, (3, 3), 0)
            
            # Convert back to PIL Image (RGB format)
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            self.result_img = Image.fromarray(result_rgb)
            
            # Display the result
            self.show_image(self.result_img, self.result_frame, self.result_placeholder)
            
            # Update status with processing results
            orig_size = f"{self.original_img.width}x{self.original_img.height}"
            new_size = f"{result.shape[1]}x{result.shape[0]}"
            color_status = "with color distortions" if self.apply_color_shift.get() else "without color distortions"
            noise_status = f", noise: {noise_level}%" if noise_level > 0 else ""
            status_text = f"Upscaling complete! {orig_size} → {new_size} ({color_status}{noise_status})"
            self.status_var.set(status_text)
            
        except Exception as e:
            # Show upscaling error
            messagebox.showerror("Error", f"{self.tr('error_upscale')}{str(e)}")
            self.status_var.set(self.tr("error_upscale"))
    
    def save_image(self):
        """Save the processed image to disk"""
        if not self.result_img:
            messagebox.showwarning("Warning", self.tr("warning_no_result"))
            return
            
        # Open save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            # Update status and process UI events
            filename = os.path.basename(file_path)
            self.status_var.set(f"{self.tr('status_saving')}{filename}")
            self.root.update()
            
            # Save the image
            self.result_img.save(file_path)
            # Show success message
            messagebox.showinfo("Success", f"{self.tr('success_save')}{file_path}")
            # Update status
            self.status_var.set(f"Saved: {filename}")
        except Exception as e:
            # Show save error
            messagebox.showerror("Error", f"{self.tr('error_save')}{str(e)}")

if __name__ == "__main__":
    # Create main application window
    root = tk.Tk()
    
    # Set application icon (if available)
    try:
        root.iconbitmap("app_icon.ico")
    except:
        # Continue without icon if not found
        pass
        
    # Create application instance
    app = ComedyImageManipulator(root)
    # Start main event loop
    root.mainloop()