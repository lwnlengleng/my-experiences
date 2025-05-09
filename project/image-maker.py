import cv2
import numpy as np
from PIL import Image
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread

class ImageMaker:
    def __init__(self):
        self.edge_thickness = 1
        self.saturation_intensity = 1.4
        self.max_size = (370, 320)
        self.filter_type = 'classic'
        self.brightness = 1.0
        self.contrast = 1.0
    
    def _adjust_colors(self, img):
        """Adjust brightness, contrast and saturation"""
        # Brightness and contrast
        img = cv2.convertScaleAbs(img, alpha=self.contrast, beta=self.brightness * 50)
        
        # Saturation
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv2.split(img_hsv)
        s = s * self.saturation_intensity
        s = np.clip(s, 0, 255)
        img_hsv = cv2.merge([h, s, v])
        return cv2.cvtColor(img_hsv.astype("uint8"), cv2.COLOR_HSV2BGR)

    def _apply_classic_anime(self, img):
        """Classic effect"""
        img_color = cv2.bilateralFilter(img, 5, 100, 100)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.medianBlur(img_gray, 5)
        img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                       cv2.ADAPTIVE_THRESH_MEAN_C,
                                       cv2.THRESH_BINARY, 9, 5)
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2BGR)
        img_color = self._reduce_colors(img_color, 7)
        return cv2.bitwise_and(img_color, 255 - img_edge)

    def _apply_watercolor_anime(self, img):
        """Watercolor-style effect"""
        # Apply bilateral filter with large parameters for painting effect
        img_color = cv2.bilateralFilter(img, 9, 150, 150)
        # Reduce colors more dramatically
        img_color = self._reduce_colors(img_color, 5)
        return img_color

    def _apply_sketch_anime(self, img):
        """Sketch-style effect"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Laplacian(gray_blur, cv2.CV_8U, ksize=5)
        edges = 255 - edges
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return cv2.bitwise_and(img, edges)

    def _reduce_colors(self, img, num_colors):
        data = np.float32(img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        _, labels, centers = cv2.kmeans(data, num_colors, None, criteria, 10,
                                      cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        result = centers[labels.flatten()]
        return result.reshape(img.shape)

    def _resize_image(self, img):
        height, width = img.shape[:2]
        ratio = min(self.max_size[0]/width, self.max_size[1]/height)
        if ratio < 1:
            new_size = (int(width * ratio), int(height * ratio))
            img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
        return img

    def create_sticker(self, input_path, output_folder="OUTPUT_PATH"):
        try:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            img = cv2.imread(input_path)
            if img is None:
                raise ValueError(f"Could not read image: {input_path}")

            # Resize image
            img = self._resize_image(img)

            # Apply color adjustments
            img = self._adjust_colors(img)

            # Apply selected filter
            if self.filter_type == 'classic':
                anime = self._apply_classic_anime(img)
            elif self.filter_type == 'watercolor':
                anime = self._apply_watercolor_anime(img)
            elif self.filter_type == 'sketch':
                anime = self._apply_sketch_anime(img)

            # Convert to PIL for transparency
            anime_pil = Image.fromarray(cv2.cvtColor(anime, cv2.COLOR_BGR2RGB))
            anime_pil = anime_pil.convert('RGBA')

            # Make white/light pixels transparent
            data = anime_pil.getdata()
            new_data = []
            for item in data:
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            
            anime_pil.putdata(new_data)

            # Save sticker
            filename = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_folder, f"{filename}_image_maker.png")
            anime_pil.save(output_path, "PNG")

            return output_path

        except Exception as e:
            raise Exception(f"Error creating sticker: {str(e)}")

class StickerMakerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Maker")
        self.window.geometry("400x600")
        
        self.sticker_maker = ImageMaker()
        self.setup_gui()

    def setup_gui(self):
        ttk.Label(self.window, text="สร้างรูปภาพแบบใหม่", font=('TH Sarabun New', 20, 'bold')).pack(pady=10)
        
        # เลือกไฟล์ภาพ
        ttk.Button(self.window, text="เลือกรูปภาพ", command=self.select_files).pack(pady=5)
        
        # เลือก Filter
        ttk.Label(self.window, text="เลือกฟิลเตอร์:").pack(pady=5)
        self.filter_var = tk.StringVar(value='classic')
        filters = [
            ("คลาสสิก", 'classic'),
            ("สีน้ำ", 'watercolor'),
            ("สเก็ตช์", 'sketch')
        ]
        for text, value in filters:
            ttk.Radiobutton(self.window, text=text, value=value, 
                           variable=self.filter_var).pack()

        # Color adjustments
        ttk.Label(self.window, text="ปรับแต่งสี:", font=('TH Sarabun New', 16)).pack(pady=5)
        
        # Brightness
        ttk.Label(self.window, text="ความสว่าง:").pack()
        self.brightness_scale = ttk.Scale(self.window, from_=0.1, to=2.0, 
                                        orient='horizontal', length=200)
        self.brightness_scale.set(1.0)
        self.brightness_scale.pack()
        
        # Contrast
        ttk.Label(self.window, text="คอนทราสต์:").pack()
        self.contrast_scale = ttk.Scale(self.window, from_=0.1, to=2.0, 
                                      orient='horizontal', length=200)
        self.contrast_scale.set(1.0)
        self.contrast_scale.pack()
        
        # Saturation
        ttk.Label(self.window, text="ความอิ่มตัวของสี:").pack()
        self.saturation_scale = ttk.Scale(self.window, from_=0.1, to=2.0, 
                                        orient='horizontal', length=200)
        self.saturation_scale.set(1.4)
        self.saturation_scale.pack()

        # Progress
        self.progress = ttk.Progressbar(self.window, length=300, mode='determinate')
        self.progress.pack(pady=10)
        
        # Status
        self.status_label = ttk.Label(self.window, text="")
        self.status_label.pack(pady=5)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="เลือกรูปภาพ",
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if files:
            self.process_images(files)

    def process_images(self, files):
        def process():
            try:
                total = len(files)
                self.progress['maximum'] = total
                
                for i, file in enumerate(files):
                    self.status_label['text'] = f"กำลังประมวลผลรูปที่ {i+1}/{total}"
                    self.progress['value'] = i
                    self.window.update()

                    # Update sticker maker settings
                    self.sticker_maker.filter_type = self.filter_var.get()
                    self.sticker_maker.brightness = self.brightness_scale.get()
                    self.sticker_maker.contrast = self.contrast_scale.get()
                    self.sticker_maker.saturation_intensity = self.saturation_scale.get()

                    # Create sticker
                    output_path = self.sticker_maker.create_sticker(file)

                self.progress['value'] = total
                self.status_label['text'] = "เสร็จสิ้น!"
                messagebox.showinfo("สำเร็จ", 
                                  f"สร้างรูปภาพเสร็จแล้ว {total} รูป")
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.status_label['text'] = "เกิดข้อผิดพลาด"

        Thread(target=process).start()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = StickerMakerGUI()
    app.run()
