import cv2 as cv
from tkinter import ttk, Tk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image


class ImageApp:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1366x768")
        self.image_labels = {}
        self.image_label_original = ttk.Label()
        self.image_label_averaging = ttk.Label()
        self.image_label_gaussian = ttk.Label()
        self.image_label_bernsen = ttk.Label()
        self.image_label_adaptive = ttk.Label()
        self.image_path = None
        self.create_interface()

    def ask_file(self):
        path = askopenfilename()
        self.image_path = path
        self.load_images()
        self.averaging_filter()
        self.gaussian_filter()
        self.bernsen_thresholding()
        self.adaptive_thresholding()

    def create_interface(self):
        label_original = ttk.Label(text="Original Image")
        label_averaging = ttk.Label(text="Averaging Filter")
        label_gaussian = ttk.Label(text="Gaussian Filter")
        label_bernsen = ttk.Label(text="Bernsen Method")
        label_adaptive = ttk.Label(text="Adaptive Thresholding")
        choose_button = ttk.Button(
            None,
            text='Choose file',
            command=self.ask_file)
        choose_button.grid(row=1, column=1, rowspan=1, columnspan=1)

        label_original.place(x=40, y=150)
        label_averaging.place(x=430, y=10)
        label_gaussian.place(x=810, y=10)
        label_bernsen.place(x=810, y=380)
        label_adaptive.place(x=430, y=380)

        self.image_label_original.place(x=40, y=170, width=350, height=350)
        self.image_label_averaging.place(x=430, y=30, width=350, height=350)
        self.image_label_gaussian.place(x=810, y=30, width=350, height=350)
        self.image_label_bernsen.place(x=810, y=400, width=350, height=350)
        self.image_label_adaptive.place(x=430, y=400, width=350, height=350)

    def load_images(self):
        image = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        image_tk = self.make_image(image)
        self.image_label_original.configure(image=image_tk)
        self.image_label_original.image = image_tk

    def make_image(self, image):
        return ImageTk.PhotoImage(Image.fromarray(image).resize((350, 350)))

    def averaging_filter(self):
        image = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        image_averaging = cv.blur(image, (5, 5))
        image_tk = self.make_image(image_averaging)
        self.image_label_averaging.configure(image=image_tk)
        self.image_label_averaging.image = image_tk

    def gaussian_filter(self):
        image = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        image_gaussian = cv.GaussianBlur(image, (5, 5), 0)
        image_tk = self.make_image(image_gaussian)
        self.image_label_gaussian.configure(image=image_tk)
        self.image_label_gaussian.image = image_tk

    def bernsen_thresholding(self):
        image_original = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        image_blurred = cv.GaussianBlur(image_original, (5, 5), 0)
        ret, th = cv.threshold(image_blurred, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        window_size = 15
        k = 0.15
        image_bernsen = image_original.copy()
        for i in range(0, image_original.shape[0] - window_size, window_size):
            for j in range(0, image_original.shape[1] - window_size, window_size):
                window = image_original[i:i + window_size, j:j + window_size]
                min_val = int(window.min() * (1 - k))
                max_val = int(window.max() * (1 + k))

                for x in range(i, i + window_size):
                    for y in range(j, j + window_size):
                        if image_original[x, y] < min_val or image_original[x, y] > max_val:
                            image_bernsen[x, y] = th[x, y]
        image_tk = self.make_image(image_bernsen)
        self.image_label_bernsen.configure(image=image_tk)
        self.image_label_bernsen.image = image_tk

    def adaptive_thresholding(self):
        image_original = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        image_adaptive = cv.adaptiveThreshold(
            image_original, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2
        )
        image_tk = self.make_image(image_adaptive)
        self.image_label_adaptive.configure(image=image_tk)
        self.image_label_adaptive.image = image_tk


app = ImageApp()
app.root.mainloop()
