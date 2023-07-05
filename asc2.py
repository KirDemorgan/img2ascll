from tkinter import Tk, Button, filedialog, scrolledtext, messagebox, Label
from PIL import Image, ImageTk
import tkinter.font as tkfont
import tkinter.messagebox as messagebox
import ctypes
from tkinter import ttk

ASCII_CHARS = '@%#*+=-:. '

ART_WIDTH = 80
ART_HEIGHT = 30

def get_screen_height():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(1)

def resize_image(image, new_width=ART_WIDTH, new_height=ART_HEIGHT):
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        index = int(pixel_value / (256 / len(ASCII_CHARS)))
        if index >= len(ASCII_CHARS):
            index = len(ASCII_CHARS) - 1
        ascii_str += ASCII_CHARS[index]
    return ascii_str

def convert_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        try:
            image = Image.open(file_path)
            image = resize_image(image)
            image = grayify(image)
            ascii_str = pixels_to_ascii(image)
            ascii_text.delete("1.0", "end")
            ascii_text.insert("1.0", ascii_str)
            adjust_art_size() 
            update_art_resolution(image.width, image.height) 
        except Exception as e:
            ascii_text.delete("1.0", "end")
            ascii_text.insert("1.0", f"Ошибка: {str(e)}")

def adjust_art_size():
    art_height = ascii_text.get("1.0", "end").count('\n') + 1
    screen_height = get_screen_height()
    if art_height > screen_height:
        new_height = max(screen_height - 4, ART_HEIGHT)
        ascii_text.config(height=new_height)
    else:
        ascii_text.config(height=ART_HEIGHT)

def copy_ascii_art():
    ascii_art = ascii_text.get("1.0", "end-1c")
    formatted_ascii_art = ascii_art.replace('\n', '\r\n')
    root.clipboard_clear()
    root.clipboard_append(formatted_ascii_art)
    messagebox.showinfo("Скопировано", "ASCII-арт скопирован в буфер обмена.")

def update_art_resolution(width, height):
    resolution_label.config(text=f"Разрешение: {width}x{height}")

root = Tk()
root.title("Конвертер изображения в ASCII-арт by demorganbtw")

logo_path = "E:/1/converter.png"
logo_image = Image.open(logo_path)
logo_tk = ImageTk.PhotoImage(logo_image)
root.iconphoto(True, logo_tk)

style = ttk.Style()
style.configure("TButton", font=("Arial", 12))

select_button = ttk.Button(root, text="Выбрать изображение", command=convert_image)
select_button.pack(pady=10)

font = tkfont.Font(family="Courier New", size=8) 
ascii_text = scrolledtext.ScrolledText(root, width=ART_WIDTH, height=ART_HEIGHT, font=font)
ascii_text.pack()

copy_button = ttk.Button(root, text="Копировать", command=copy_ascii_art)
copy_button.pack(pady=10)

resolution_label = Label(root, text="Разрешение: ", font=("Arial", 12))
resolution_label.pack()

root.mainloop()
