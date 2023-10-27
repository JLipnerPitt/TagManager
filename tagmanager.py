import os
import tkinter as tk
import shutil
import cv2
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk


class TagManager:
    def __init__(self):
        self.directory = None  # main dataset location
        self.img_directory = None  # created folder location to store only images from dataset
        self.txt_directory = None  # created folder location to store only txt files from dataset

    def set_directory(self, dir):
        self.directory = dir

    def get_main_directory(self):
        return self.directory

    def get_img_directory(self):
        return self.img_directory

    def get_txt_directory(self):
        return self.txt_directory

    def create_folder(self, folder_name, directory=None):
        if directory is None:
            directory = self.directory

        folder_path = os.path.join(directory, folder_name)  # joins creates directory/folder_name path
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # delete folder if it already exists
        os.makedirs(folder_path)  # creates folder in specified directory
        return folder_path

    def separate_images(self):
        images_path = self.create_folder("dataset_images")
        for filename in os.listdir(self.directory):  # checks each file in directory
            if filename.endswith(".jpg"):
                imgfile = os.path.join(self.directory, filename)
                shutil.copy(imgfile, images_path)

        self.img_directory = images_path


    def separate_txt_files(self):
        txt_path = self.create_folder("dataset_tags")
        for filename in os.listdir(self.directory):  # checks each file in directory
            if filename.endswith(".txt"):
                txtfile = os.path.join(self.directory, filename)
                shutil.copy(txtfile, txt_path)

        self.txt_directory = txt_path

    def tag_searcher(self, tag, choice=None, folder_name=None):
        #  creates folder located in the datasets path
        if folder_name is None:
            directory2 = self.create_folder(os.path.dirname(self.directory), "tag_manager")
        else:
            directory2 = self.create_folder(os.path.dirname(self.directory), folder_name)

        if choice is None:  # searches for txt files with tag by default
            choice = "with"

        if choice == "without":
            condition = lambda x: tag not in x
            message = "without"
        else:  # choice == "with"
            condition = lambda x: tag in x
            message = "with"

        count = 0
        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):  # Ensure we're only looking at .txt files
                with open(os.path.join(self.directory, filename), 'r') as file:
                    contents = file.read()
                    if condition(contents):
                        txtfile = os.path.join(self.directory, filename)
                        imgfile = os.path.join(self.directory, filename.replace('.txt', '.jpg'))
                        shutil.copy(txtfile, directory2)
                        shutil.copy(imgfile, directory2)
                        count += 1

        print("There are {} images {} the '{}' tag.".format(count, message, tag))
        os.startfile(directory2)  # opens folder the files were moved to
        return directory2

    def tag_adder(self, new_tag, search_dir=None):
        count = 0
        if search_dir is None:
            search_dir = self.directory

        for filename in os.listdir(search_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(search_dir, filename), 'a+') as file:  # a+ appends to end of string
                    file.write(", " + new_tag)
                    count += 1
        print("You added the '{}' tag to {} txt files.".format(new_tag, count))

    def activation_tag(self, act_tag):
        count = 0
        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):
                with open(os.path.join(self.directory, filename), 'r') as old_file:
                    contents = old_file.read()
                with open(os.path.join(self.directory, filename), 'w') as new_file:
                    new_file.write(act_tag + ", ")  # Write new data to new file
                    new_file.write(contents)  # Append old content to new file
                count += 1
        print("You added the '{}' tag to {} txt files.".format(act_tag, count))

    def tag_replacer(self, old_tag, new_tag, search_dir=None):
        count = 0
        if search_dir is None:
            search_dir = self.directory

        for filename in os.listdir(search_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(search_dir, filename), 'r') as old_file:
                    contents = old_file.read()
                with open(os.path.join(search_dir, filename), 'w') as old_file:
                    old_file.write(contents.replace(old_tag, new_tag))  # replace old tag with new tag
                count += 1
        print("You replaced {} copies of '{}' with {} copies of '{}'.".format(count, old_tag, count, new_tag))

    def tag_remover(self, rem_tag, search_dir=None):
        count = 0
        if search_dir is None:
            search_dir = self.directory

        if isinstance(rem_tag, list) == False:
            for filename in os.listdir(self.directory):
                if filename.endswith(".txt"):
                    with open(os.path.join(self.directory, filename), 'r') as old_file:
                        contents = old_file.read()
                    new_contents = contents.replace(rem_tag + ", ", "")  # try to replace old tag with new tag

                    if contents != new_contents:  # if contents have changed, the tag was removed
                        with open(os.path.join(search_dir, filename), 'w') as file:
                            file.write(new_contents)
                        count += 1
            print("You removed {} copies of '{}'.".format(count, rem_tag))

        else:
            for filename in os.listdir(self.directory):
                if filename.endswith(".txt"):
                    with open(os.path.join(self.directory, filename), 'r') as old_file:
                        contents = old_file.read()
                    old_contents = contents
                    for tag in rem_tag:
                        if not contents.find(tag):
                            continue
                        contents = contents.replace(", " + tag, "")  # try to replace old tag with new tag

                    if contents != old_contents:  # if contents have changed, the tag was removed
                        with open(os.path.join(search_dir, filename), 'w') as file:
                            file.write(contents)

    def convert_image_type(self, old, new, path=None):
        if path is None:
            path = self.directory

        files = os.listdir(path)
        images = []
        [images.append(file) for file in files if file.endswith(old)]

        for img in images:
            if os.path.exists(os.path.join(path, img.replace(old, new))):
                continue
            os.rename(os.path.join(path, img), os.path.join(path, img.replace(old, new)))

    def rename_txt_and_img_pairs(self, path=None):
        if path is None:
            path = self.directory

        files = os.listdir(path)  # stores all files in directory
        txt_files = []  # stores all txt paths
        jpg_files = []  # stores all jpg paths

        [txt_files.append(file) for file in files if file.endswith(".txt")]
        [jpg_files.append(file) for file in files if file.endswith(".jpg")]

        #  sorting txt and jpg files numerically
        txt_files = sorted(txt_files, key=lambda f: int(f.split(".")[0]))
        jpg_files = sorted(jpg_files, key=lambda f: int(f.split(".")[0]))
        n = int(len(files)/2)  # number of txt and jpg files are the same

        #  renaming txt and jpg files
        for i in range(n):
            if os.path.exists(os.path.join(path, "{}.jpg".format(i+1))) == True:
                i += 1
                continue
            os.rename(os.path.join(path, jpg_files[i]), os.path.join(path, "{}.jpg".format(i+1)))
            os.rename(os.path.join(path, txt_files[i]), os.path.join(path, "{}.txt".format(i+1)))

    def upscale(self):
        if self.img_directory is None:
            self.create_folder("dataset_images")

        for img in self.img_directory:
            im = cv2.imread(img)
            if im[0] or img[1] < 2000:
                pass

        #  if folder doesn't exist, create it, and make a copy
           #  else check size of each image in folder
              #  if img width or height is < 2000 pixels, upscale

        # after all images have been upscaled, show old and upscaled image side by side
        # if satisfied with upscaled image results, overwrite that image in the main folder


class Interface:
    def __init__(self):
        self.folder = "Select Folder"
        self.root = tk.Tk()  # main parent window
        self.root.title("Tag Manager")
        self.root.geometry('1080x1920')
        self.image_window = tk.PhotoImage(file='')
        self.tm = TagManager()  # for calling tagmanager functions
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
        self.directory_frame.configure(text=dir)  # updates the text label on the directory frame
        self.tm.setDirectory(dir)
        self.image_window = self.tm.getDirectory()


    def select_folder_widget(self):
        # Create frames for each functionality
        self.directory_frame = ttk.LabelFrame(self.root, text="Select Folder", width=25, height=25)
        self.directory_frame.grid(row=0, column=0)
        self.directory_frame.grid_propagate(False)
        self.directory_frame.pack(padx=10, pady=10)
        self.directory_frame.place(x=0, y=0)
        # Select Directory
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="white")
        self.search_button = ttk.Button(self.directory_frame, text="Search", width=15,
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


#gui = Interface()
tm = TagManager()
tm.set_directory(filedialog.askdirectory())
tm.separate_images()
tm.separate_txt_files()

