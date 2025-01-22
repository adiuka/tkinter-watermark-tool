import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from function import img_watermark, text_watermark


class WatermarkApp(tk.Tk): # We inherit the Tk class from tkinter
    def __init__(self, *args, **kwargs): # We specify the inheritance
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvatica', size=18, weight='bold')
        self.image_path = None
        self.logo_path = None

        # The technique used containers that we will stack on top of each other.
        # Then the want we want visible will be brought to the top. 
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ImageWaterMark, TextWaterMark):
            page_name = F.__name__ # We take the name of the Class as a page name
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame # We create the dictionary entries based on the Page Name

            # We then put all of the pages in the same location
            # The one one the top will be the one that is visible!
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")


    def show_frame(self, page_name): # Once a page name is received will show that page
        frame = self.frames[page_name] # Targets our dictionary
        frame.tkraise() # Brings our frame to the top of the window


    def upload_action_img(self):
        self.image_path = fd.askopenfilename(
            title="Select a File",
            filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*"))
        )
        if self.image_path:
            # Validate file Extension:
            valid_extensions = (".png", ".jpg", ".jpeg")
            if not self.image_path.lower().endswith(valid_extensions):
                mb.showerror("Invalid File", "Please select a valid image file (PNG, JPG, JPEG).")
                self.image_path = None
            print(f"File selected: {self.image_path}")
        else:
            print("Wrong format selected, please choose a png or jpeg.")
        return self.image_path
    

    def upload_action_logo(self):
        self.image_path = fd.askopenfilename(
            title="Select a File",
            filetypes=(("Image Files", "*.png"), ("All Files", "*.*"))
        )
        if self.image_path:
            # Validate file Extension:
            valid_extensions = (".png")
            if not self.image_path.lower().endswith(valid_extensions):
                mb.showerror("Invalid File", "Please select a valid image file (PNG, JPG, JPEG).")
                self.image_path = None
            print(f"File selected: {self.image_path}")
        else:
            print("Wrong format selected, please choose a png or jpeg.")
        return self.image_path


    def choose_directory(self):
        self.file_path = fd.askdirectory(
            title="Select Directory"
        )
        return self.file_path


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Please choose if you want to add an image watermark to an image \n" 
                         "or a text watermark to an image",
                         font=controller.title_font)
        label.pack(side='top', fill='x', pady=10)
        # CANVAS CONFIG #
        canvas = tk.Canvas(self, width=256, height=275, highlightthickness=0)
        self.start_image = tk.PhotoImage(file='./assets/watermark funny_modified.png')
        canvas.create_image(128, 137, image=self.start_image)
        canvas.pack(padx=10, pady=10)
        # BUTTONS #
        image_watermark_button = tk.Button(self, text='Create Img Watermark',
                                           command=lambda: controller.show_frame("ImageWaterMark")) # The button to create an image watermark
                       # The lambda button initialises an annonymous function. In this case the controller 
        text_watermark_button = tk.Button(self, text='Create Text Watermark',
                                          command=lambda: controller.show_frame("TextWaterMark")) # The button to create a text watermark
        image_watermark_button.pack(padx=10, pady=10)
        text_watermark_button.pack(padx=10, pady=10)

        
class ImageWaterMark(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.image_path = None
        self.logo_path = None
        # Labels
        top_label = tk.Label(self, text="Upload your image and watermark!",
                         font=controller.title_font)
        top_label.pack(side='top', fill='x', pady=10)
        self.img_path_label = tk.Label(self, text="No Image Selected", fg='red', font='Helvatica 10')
        self.logo_path_label = tk.Label(self, text="No Logo Selected",fg='red', font='Helvatica 10')
        # Add functionality that shows where it will be saved based on choice:
        self.save_path_label = tk.Label(self, text="Current FilePath is : Tkinter-build/created_images", font='Helvatica 10') # Work in Progress

        # Buttons
        open_img_button = tk.Button(self, text='Open Image',
                                command=lambda: self.set_image_path(controller.upload_action_img())) # The button to create a text watermark        
        open_logo_button = tk.Button(self, text='Open Logo',
                                command=lambda: self.set_logo_path(controller.upload_action_logo())) # The button to create a text watermark       
        # open_file_path_button = tk.Button(self, text='Select Save Directory',
                                          # command=lambda: controller.choose_directory()) # To implement
        process_button = tk.Button(self, text='Process',
                                command=lambda: img_watermark(self.image_path, self.logo_path))
        back_button = tk.Button(self, text='Gack to Start', # The button to go back to the start page
                                command=lambda: controller.show_frame("StartPage"))
        
        self.img_path_label.pack()
        open_img_button.pack(padx=10, pady=10)
        self.logo_path_label.pack()
        open_logo_button.pack(padx=10, pady=10)
        self.save_path_label.pack()
        process_button.pack(padx=10, pady=10)
        # open_file_path_button.pack(padx=10, pady=10)
        back_button.pack(padx=20, pady=20)


    def set_image_path(self, path):
        if path:
            self.image_path = path
            self.img_path_label.config(text=f"Chosen img: {self.image_path}", fg='green')
            print(f"Image path set: {self.image_path}")


    def set_logo_path(self, path):
        if path:
            self.logo_path = path
            self.logo_path_label.config(text=f"Chosen logo: {self.logo_path}", fg='green')
            print(f"Logo path set: {self.logo_path}")


class TextWaterMark(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.image_path = None
        self.text = ""

        top_label = tk.Label(self, text="Upload your image and watermark!",
                         font=controller.title_font)
        top_label.pack(side='top', fill='x', pady=10)
        self.img_path_label = tk.Label(self, text="No Image Selected", fg='red', font='Helvatica 10')
        self.confirmation_label = tk.Label(self,text='No Text Confirmed', fg='red', font='Helvatica 10')
        # Configure text Entry
        self.text_entry = tk.Entry(self, width=21)
        
        # Add functionality that shows where it will be saved based on choice:
        self.save_path_label = tk.Label(self, text="Current FilePath is : Tkinter-build/created_images", font='Helvatica 10') # Work in Progress

        # Buttons
        open_img_button = tk.Button(self, text='Open Image',
                                command=lambda: self.set_image_path(controller.upload_action_img())) # The button to create a text watermark
        set_text_button = tk.Button(self, text='Confirm Text',
                                    command=lambda: self.set_text())
        process_button = tk.Button(self, text='Process',
                                command=lambda: text_watermark(self.image_path, self.text))

        back_button = tk.Button(self, text='Gack to Start', # The button to go back to the start page
                                command=lambda: controller.show_frame("StartPage"))
                            
        self.img_path_label.pack()
        open_img_button.pack(padx=10, pady=10)
        self.confirmation_label.pack()
        self.text_entry.pack()
        set_text_button.pack(padx=10, pady=10)
        self.save_path_label.pack()
        process_button.pack(padx=10, pady=10)
        back_button.pack(padx=20, pady=20)


    def set_image_path(self, path):
        if path:
            self.image_path = path
            self.img_path_label.config(text=f"Chosen img: {self.image_path}", fg='green')
            print(f"Image path set: {self.image_path}")


    def set_text(self):
        self.text = self.text_entry.get()
        self.confirmation_label.config(text="Text Confirmed", fg='green')



if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()