import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import threading

from encryptor import (
    load_image, save_image,
    encrypt_shift, decrypt_shift,
    encrypt_swap, decrypt_swap
)

class ImageEncryptorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ Image Encryption Tool")
        self.root.configure(bg="#121212")
        self.root.geometry("900x500")
        self.original_image = None
        self.current_image = None

        self.setup_widgets()

    def setup_widgets(self):
        title = tk.Label(self.root, text="Image Encryption Tool", font=("Arial", 18, "bold"), fg="#00ff99", bg="#121212")
        title.pack(pady=10)

        controls = tk.Frame(self.root, bg="#121212")
        controls.pack(pady=10)

        tk.Button(controls, text="📂 Load Image", command=self.load_image, bg="#1e1e1e", fg="#00ffaa", width=15).grid(row=0, column=0, padx=10)
        tk.Button(controls, text="🔐 Encrypt (Shift)", command=lambda: self.run_thread(self.encrypt_shift), bg="#1e1e1e", fg="#ffaa00", width=18).grid(row=0, column=1, padx=10)
        tk.Button(controls, text="🔐 Encrypt (Swap)", command=lambda: self.run_thread(self.encrypt_swap), bg="#1e1e1e", fg="#ffaa00", width=18).grid(row=0, column=2, padx=10)
        tk.Button(controls, text="🔓 Decrypt (Shift)", command=lambda: self.run_thread(self.decrypt_shift), bg="#1e1e1e", fg="#00ffff", width=18).grid(row=0, column=3, padx=10)
        tk.Button(controls, text="🔓 Decrypt (Swap)", command=lambda: self.run_thread(self.decrypt_swap), bg="#1e1e1e", fg="#00ffff", width=18).grid(row=0, column=4, padx=10)
        tk.Button(controls, text="💾 Save Result", command=self.save_result, bg="#1e1e1e", fg="#ffffff", width=15).grid(row=0, column=5, padx=10)

        self.status_label = tk.Label(self.root, text="", fg="#888888", bg="#121212")
        self.status_label.pack()

        self.preview_frame = tk.Frame(self.root, bg="#121212")
        self.preview_frame.pack(pady=10)

        self.original_label = tk.Label(self.preview_frame, text="Original Image", fg="white", bg="#121212")
        self.original_label.grid(row=0, column=0, padx=20)
        self.result_label = tk.Label(self.preview_frame, text="Result Image", fg="white", bg="#121212")
        self.result_label.grid(row=0, column=1, padx=20)

        self.original_canvas = tk.Label(self.preview_frame, bg="#1e1e1e")
        self.original_canvas.grid(row=1, column=0, padx=20)
        self.result_canvas = tk.Label(self.preview_frame, bg="#1e1e1e")
        self.result_canvas.grid(row=1, column=1, padx=20)

    def run_thread(self, func):
        threading.Thread(target=self.safe_call, args=(func,), daemon=True).start()

    def safe_call(self, func):
        self.set_status("⏳ Processing...")
        try:
            func()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.set_status("✅ Done.")

    def load_image(self):
       file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
       if file_path:
            self.original_image = load_image(file_path).convert("RGB")
            self.current_image = self.original_image.copy()
            self.display_image(self.original_image, self.original_canvas)
            self.result_canvas.config(image="")  # Clear the result image
            self.result_canvas.image = None


    def display_image(self, image, canvas):
        resized = image.resize((250, 250))
        tk_image = ImageTk.PhotoImage(resized)
        canvas.image = tk_image
        canvas.configure(image=tk_image)

    def encrypt_shift(self):
        if self.current_image:
            self.current_image = encrypt_shift(self.current_image, shift=50)
            self.display_image(self.current_image, self.result_canvas)

    def decrypt_shift(self):
        if self.current_image:
            self.current_image = decrypt_shift(self.current_image, shift=50)
            self.display_image(self.current_image, self.result_canvas)

    def encrypt_swap(self):
        if self.current_image:
            self.current_image = encrypt_swap(self.current_image, seed=42)
            self.display_image(self.current_image, self.result_canvas)

    def decrypt_swap(self):
        if self.current_image:
            self.current_image = decrypt_swap(self.current_image, seed=42)
            self.display_image(self.current_image, self.result_canvas)

    def save_result(self):
        if self.current_image:
            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if path:
                save_image(self.current_image, path)
                messagebox.showinfo("Saved", f"Image saved to {path}")

    def set_status(self, msg):
        self.status_label.config(text=msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorGUI(root)
    root.mainloop()