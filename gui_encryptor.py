import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import os

def swap_pixels(img):
    pixels = list(img.getdata())
    total_pixels = len(pixels)
    shuffled_indices = list(range(total_pixels))
    random.shuffle(shuffled_indices)
    shuffled_pixels = [pixels[i] for i in shuffled_indices]
    img.putdata(shuffled_pixels)
    return img, shuffled_indices

def reverse_swap(img, indices):
    shuffled_pixels = list(img.getdata())
    original_pixels = [None] * len(shuffled_pixels)
    for i, index in enumerate(indices):
        original_pixels[index] = shuffled_pixels[i]
    img.putdata(original_pixels)
    return img

def apply_math_op(img, key=20):
    pixels = list(img.getdata())
    new_pixels = [((r + key) % 256, (g + key) % 256, (b + key) % 256) for r, g, b in pixels]
    img.putdata(new_pixels)
    return img

def reverse_math_op(img, key=20):
    pixels = list(img.getdata())
    new_pixels = [((r - key) % 256, (g - key) % 256, (b - key) % 256) for r, g, b in pixels]
    img.putdata(new_pixels)
    return img

class ImageEncryptorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Image Encryption Tool")
        self.root.geometry("640x640")
        self.root.resizable(False, False)
        self.dark_mode = False
        self.img_full = None
        self.tk_img_preview = None
        self.image_path = None
        self.set_theme()
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)

        self.label = tk.Label(root, text="🖼️ No image loaded", font=("Segoe UI", 12, "bold"), bg=self.bg_color, fg=self.fg_color)
        self.label.pack(pady=8)

        self.canvas = tk.Canvas(root, width=300, height=300, bg=self.canvas_bg, highlightthickness=1, highlightbackground=self.canvas_border)
        self.canvas.pack()

        self.status = tk.Label(root, text="Status: Waiting for image...", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 10))
        self.status.pack(pady=10)

        btn_frame = tk.Frame(root, bg=self.bg_color)
        btn_frame.pack(pady=10)

        self.btn_load = ttk.Button(btn_frame, text="📁 Load Image", command=self.load_image)
        self.btn_encrypt = ttk.Button(btn_frame, text="🔒 Encrypt", command=self.encrypt_image)
        self.btn_decrypt = ttk.Button(btn_frame, text="🔓 Decrypt", command=self.decrypt_image)
        self.btn_save = ttk.Button(btn_frame, text="💾 Save", command=self.save_image)
        self.btn_theme = ttk.Button(btn_frame, text="🌙 Toggle Mode", command=self.toggle_theme)

        self.btn_load.grid(row=0, column=0, padx=5, pady=5)
        self.btn_encrypt.grid(row=0, column=1, padx=5, pady=5)
        self.btn_decrypt.grid(row=1, column=0, padx=5, pady=5)
        self.btn_save.grid(row=1, column=1, padx=5, pady=5)
        self.btn_theme.grid(row=2, column=0, columnspan=2, pady=10)

        self.apply_theme()

    def set_theme(self):
        if self.dark_mode:
            self.bg_color = "#1e1e1e"
            self.fg_color = "#ffffff"
            self.canvas_bg = "#2a2a2a"
            self.canvas_border = "#444"
        else:
            self.bg_color = "#f0f0f0"
            self.fg_color = "#000000"
            self.canvas_bg = "#ffffff"
            self.canvas_border = "#aaa"

    def apply_theme(self):
        self.root.configure(bg=self.bg_color)
        self.label.config(bg=self.bg_color, fg=self.fg_color)
        self.status.config(bg=self.bg_color, fg=self.fg_color)
        self.canvas.config(bg=self.canvas_bg, highlightbackground=self.canvas_border)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()
        self.apply_theme()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            return
        self.image_path = file_path
        self.img_full = Image.open(file_path).convert("RGB")
        self.display_preview(self.img_full)
        self.status.config(text="Status: Image loaded.")
        self.label.config(text=os.path.basename(file_path))

    def display_preview(self, img):
        preview = img.copy()
        preview.thumbnail((300, 300))
        self.tk_img_preview = ImageTk.PhotoImage(preview)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img_preview)

    def encrypt_image(self):
        if self.img_full is None or not self.image_path:
            messagebox.showerror("Error", "No image loaded.")
            return
        self.img_full, shuffled_indices = swap_pixels(self.img_full)
        self.img_full = apply_math_op(self.img_full, key=20)

        # Save key file with same base name
        key_path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key files", "*.key")])
        if not key_path:
            return
        self.save_key_file(shuffled_indices, key_path)

        self.display_preview(self.img_full)
        self.status.config(text="Status: Image encrypted and key saved.")

    def decrypt_image(self):
        if self.img_full is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        key_path = filedialog.askopenfilename(title="Select Key File", filetypes=[("Key Files", "*.key")])
        if not key_path or not os.path.exists(key_path):
            messagebox.showerror("Error", "No valid key file selected.")
            return

        indices = self.load_key_file(key_path)
        if indices is None:
            messagebox.showerror("Error", "Failed to read key file.")
            return

        self.img_full = reverse_math_op(self.img_full, key=20)
        self.img_full = reverse_swap(self.img_full, indices)
        self.display_preview(self.img_full)
        self.status.config(text=f"Status: Image decrypted using selected key.")

    def save_image(self):
        if self.img_full is None:
            messagebox.showerror("Error", "No image to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in [".jpg", ".jpeg"]:
                self.img_full.save(file_path, format="JPEG", quality=85)
            else:
                self.img_full.save(file_path, format="PNG", optimize=True)
            self.status.config(text=f"Status: Image saved as {os.path.basename(file_path)}.")

    def save_key_file(self, indices, path):
        with open(path, "w") as f:
            f.write(",".join(map(str, indices)))

    def load_key_file(self, path):
        try:
            with open(path, "r") as f:
                return list(map(int, f.read().split(",")))
        except Exception as e:
            print("Key file load error:", e)
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorGUI(root)
    root.mainloop()