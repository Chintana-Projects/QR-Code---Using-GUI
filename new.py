import qrcode
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox

class QRCodeGenerator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("QR Code Generator")

        # Data type
        self.data_type = tk.StringVar()
        self.data_type.set("1")

        tk.Label(self.window, text="Choose QR code type:").grid(row=0, column=0, padx=5, pady=5)
        tk.Radiobutton(self.window, text="Text", variable=self.data_type, value="1").grid(row=0, column=1, padx=5, pady=5)
        tk.Radiobutton(self.window, text="URL", variable=self.data_type, value="2").grid(row=0, column=2, padx=5, pady=5)
        tk.Radiobutton(self.window, text="Phone Number", variable=self.data_type, value="3").grid(row=0, column=3, padx=5, pady=5)
        tk.Radiobutton(self.window, text="Email", variable=self.data_type, value="4").grid(row=0, column=4, padx=5, pady=5)

        # Data
        tk.Label(self.window, text="Enter data:").grid(row=1, column=0, padx=5, pady=5)
        self.data_entry = tk.Entry(self.window, width=50)
        self.data_entry.grid(row=1, column=1, columnspan=4, padx=5, pady=5)

        # Save location
        tk.Label(self.window, text="Save location (e.g., qr_code.png):").grid(row=2, column=0, padx=5, pady=5)
        self.save_location_entry = tk.Entry(self.window, width=50)
        self.save_location_entry.grid(row=2, column=1, columnspan=4, padx=5, pady=5)

        # Fill color
        self.fill_color = tk.StringVar()
        self.fill_color.set("1")
        tk.Label(self.window, text="Fill color:").grid(row=3, column=0, padx=5, pady=5)
        tk.Radiobutton(self.window, text="Black", variable=self.fill_color, value="1").grid(row=3, column=1, padx=5, pady=5)
        tk.Radiobutton(self.window, text="Red", variable=self.fill_color, value="2").grid(row=3, column=2, padx=5, pady=5)
        tk.Radiobutton(self.window, text="Blue", variable=self.fill_color, value="3").grid(row=3, column=3, padx=5, pady=5)

        # Background color
        self.back_color = tk.StringVar()
        self.back_color.set("1")
        tk.Label(self.window, text="Background color:").grid(row=4, column=0, padx=5, pady=5)
        tk.Radiobutton(self.window, text="Yellow", variable=self.back_color, value="1").grid(row=4, column=1, padx=5, pady=5)
        tk.Radiobutton(self.window, text="Pink", variable=self.back_color, value="2").grid(row=4, column=2, padx=5, pady=5)
        tk.Radiobutton(self.window, text="White", variable=self.back_color, value="3").grid(row=4, column=3, padx=5, pady=5)

        # Size
        tk.Label(self.window, text="QR box size (5-30):").grid(row=5, column=0, padx=5, pady=5)
        self.size_entry = tk.Entry(self.window, width=10)
        self.size_entry.grid(row=5, column=1, padx=5, pady=5)

        # Shape
        self.shape = tk.StringVar()
        self.shape.set("1")
        tk.Label(self.window, text="Shape style:").grid(row=6, column=0, padx=5, pady=5)
        tk.Radiobutton(self.window, text="Square", variable=self.shape, value="1").grid(row=6, column=1, padx=5, pady=5)
        tk.Radiobutton(self.window, text="Circle", variable=self.shape, value="2").grid(row=6, column=2, padx=5, pady=5)

        # Generate button
        tk.Button(self.window, text="Generate QR Code", command=self.generate_qr).grid(row=7, column=1, columnspan=3, padx=5, pady=5)

    def generate_qr(self):
        data_type = self.data_type.get()
        data = self.data_entry.get()
        if not data:
            messagebox.showerror("Error", "Please enter data")
            return
        if data_type == "3":
            data = f"tel:{data}"
        elif data_type == "4":
            data = f"mailto:{data}"
        save_location = self.save_location_entry.get()
        if not save_location:
            messagebox.showerror("Error", "Please enter a save location")
            return
        fill_color = self.fill_color.get()
        if fill_color == "1":
            fill_color = (0, 0, 0)
        elif fill_color == "2":
            fill_color = (255, 0, 0)
        elif fill_color == "3":
            fill_color = (0, 0, 255)
        else:
            fill_color = (0, 0, 0)
        back_color = self.back_color.get()
        if back_color == "1":
            back_color = (255, 255, 0)
        elif back_color == "2":
            back_color = (255, 192, 203)
        elif back_color == "3":
            back_color = (255, 255, 255)
        else:
            back_color = (255, 255, 255)
        try:
            size = int(self.size_entry.get())
        except ValueError:
            size = 10
        shape = "circle" if self.shape.get() == "2" else "square"
        self.generate_qr_code(data, save_location, fill_color, back_color, size, shape)

    def generate_qr_code(self, data, save_location, fill_color, back_color, size, shape):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=size,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_matrix = qr.get_matrix()
        modules_count = len(qr_matrix)
        img_size = modules_count * size
        img = Image.new("RGBA", (img_size, img_size), back_color)
        draw = ImageDraw.Draw(img)
        for row in range(modules_count):
            for col in range(modules_count):
                if qr_matrix[row][col]:
                    x1 = col * size
                    y1 = row * size
                    x2 = x1 + size
                    y2 = y1 + size
                    if shape == "circle":
                        draw.ellipse((x1, y1, x2, y2), fill=fill_color)
                    else:
                        draw.rectangle((x1, y1, x2, y2), fill=fill_color)
        if not save_location.lower().endswith(".png"):
            save_location += ".png"
        img.save(save_location, format="PNG")
        messagebox.showinfo("Success", f"QR Code saved successfully at {save_location}!")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    generator = QRCodeGenerator()
    generator.run()