import tkinter as tk
import tagmanager
from tkinter import filedialog
from tkinter import ttk


class Interface:
    def __init__(self):
        self.folder = "Select Folder"
        self.root = tk.Tk()  # main parent window
        self.root.title("Tag Manager")
        self.root.geometry('1080x1920')
        self.image_window = tk.PhotoImage(file='')
        self.tm = tagmanager.TagManager()  # for calling tagmanager functions
        self.widgets()
        self.root.mainloop()

    def widgets(self):
        self.select_folder_widget()
        self.tag_search_widget()
        self.add_tag_widget()
        self.remove_tag_widget()
        self.image_widget()

    def select_directory(self):
        dir = filedialog.askdirectory()
        if dir == "":
            return
        self.root_directory_frame.configure(text=dir)  # updates the text label on the directory frame
        self.tm.set_directory(dir)
        #self.image_window = self.tm.get_directory()


    def select_folder_widget(self):
        # Create frames for each functionality
        self.root_directory_frame = ttk.LabelFrame(self.root, text="Select Folder", width=25, height=25)
        self.root_directory_frame.grid(row=0, column=0)
        self.root_directory_frame.grid_propagate(False)
        self.root_directory_frame.pack(padx=10, pady=10)
        self.root_directory_frame.place(x=0, y=0)
        # Select Directory
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="white")
        self.search_button = ttk.Button(self.root_directory_frame, text="Search", width=15,
                                       command=lambda: self.select_directory())
        self.search_button.pack(padx=4, pady=4)
        #self.search_button.place(x=0, y=0)

    def tag_search_widget(self):
        self.tag_search_frame = ttk.LabelFrame(self.root, text="Tag Searcher")
        self.tag_search_frame.pack(padx=10, pady=10)
        self.tag_search_frame.place(x=0, y=55)

        # Tag Searcher
        self.search_entry1 = ttk.Entry(self.tag_search_frame)
        self.search_entry1.pack(padx=10, pady=5)

        self.search_button = ttk.Button(self.tag_search_frame, text="Search",
                                       command=lambda: self.tm.tag_searcher(self.search_entry1.get(), self.radio_var.get()))
        self.search_button.pack(pady=5)

        self.radio_var = tk.StringVar(value="with") # shows neither being clicked
        self.with_radio = ttk.Radiobutton(self.tag_search_frame, text="with", variable=self.radio_var, value="with")
        self.without_radio = ttk.Radiobutton(self.tag_search_frame, text="without", variable=self.radio_var, value="without")
        self.with_radio.pack(pady=10) # displays the actual clickable button for with
        self.without_radio.pack(pady=10)

    def add_tag_widget(self):
        self.add_tag_frame = ttk.LabelFrame(self.root, text="Add Tags")
        self.add_tag_frame.pack(padx=10, pady=10)
        self.add_tag_frame.place(x=0, y=235)

        # Tag Adder
        self.add_entry = ttk.Entry(self.add_tag_frame)
        self.add_entry.pack(padx=10, pady=5)
        self.add_button = ttk.Button(self.add_tag_frame, text="Add Tag",
                                    command=lambda: self.tm.tag_adder(self.add_entry.get()))
        self.add_button.pack(pady=5)

        # Add Activation Tag
        self.add_activation = ttk.Entry(self.add_tag_frame)
        self.add_activation.pack(padx=10, pady=5)
        self.add_acti_button = ttk.Button(self.add_tag_frame, text="Add Activation Tag",
                                    command=lambda: self.tm.activation_tag(self.add_activation.get()))
        self.add_acti_button.pack(pady=5)

    def remove_tag_widget(self):
        self.tag_remove_frame = ttk.LabelFrame(self.root, text="Remove Tags")
        self.tag_remove_frame.pack(padx=10, pady=10)
        self.tag_remove_frame.place(x=0, y=390)

        # Tag Remover
        self.remove_entry = ttk.Entry(self.tag_remove_frame)
        self.remove_entry.pack(padx=10, pady=5)
        self.remove_button = ttk.Button(self.tag_remove_frame, text="Remove",
                                       command=lambda: self.tm.tag_remover(self.remove_entry.get()))
        self.remove_button.pack(pady=5)

    def image_widget(self):
        self.image_frame = ttk.LabelFrame(self.root, text="Image")
        self.image_frame.pack(padx=25, pady=25)
        self.image_frame.place(x=500, y=250)

    def upscale_widget(self):
        pass