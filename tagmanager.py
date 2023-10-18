import os
import tkinter as tk
import shutil
from tkinter import filedialog
from PIL import Image, ImageTk


class TagManager:
    def __init__(self):
        self.directory = None

    def setDirectory(self, dir):
        self.directory = dir

    def getDirectory(self):
        return self.directory

    def create_folder(self, directory, folder_name):
        folder_path = os.path.join(directory, folder_name)  # joins creates directory/folder_name path
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # delete folder if it already exists
        os.makedirs(folder_path)  # create folder since it doesn't exist
        return folder_path

    def remove_tag_button(self):
        root = tk.Tk()
        # The command parameter is used to specify the function that will be called when the button is clicked
        button = tk.Button(root, text="Remove tags?", command=self.tag_remover)
        button.pack()
        root.mainloop()

    def tag_searcher(self, tag, choice=None, folder_name=None):
        #  creates folder located in the datasets path
        if folder_name is None:
            directory2 = self.create_folder(os.path.dirname(self.directory), "tag_manager")
        else:
            directory2 = self.create_folder(os.path.dirname(self.directory), folder_name)

        if choice is None:
            choice = "with"

        count = 0
        if choice == "without":
            condition = lambda x: tag not in x
            message = "without"
        else:  # choice == "with"
            condition = lambda x: tag in x
            message = "with"

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

    def activation_tag(self, act_tag, search_dir=None):
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
                        if contents.find(tag) == False:
                            continue
                        contents = contents.replace(", " + tag, "")  # try to replace old tag with new tag

                    if contents != old_contents:  # if contents have changed, the tag was removed
                        with open(os.path.join(search_dir, filename), 'w') as file:
                            file.write(contents)


class Interface:
    def __init__(self):
        self.folder = "Select Folder"
        self.root = tk.Tk()
        self.root.title("Tag Manager")
        self.tm = TagManager()
        self.select_folder_widget()
        self.tag_search_widget()
        self.add_tag_widget()
        self.remove_tag_widget()
        self.root.mainloop()

    def select_directory(self):
        dir = filedialog.askdirectory()
        if dir == "":
            return
        self.directory_frame.configure(text=dir)  # updates the text label on the directory frame
        self.tm.setDirectory(dir)


    def select_folder_widget(self):
        # Create frames for each functionality
        self.directory_frame = tk.LabelFrame(self.root, text="Select Folder")
        self.directory_frame.pack(padx=10, pady=10, fill=tk.X)

        # Select Directory
        self.search_button = tk.Button(self.directory_frame, text="Search",
                                       command=lambda: self.select_directory())
        self.search_button.pack(pady=5)

    def tag_search_widget(self):
        self.tag_search_frame = tk.LabelFrame(self.root, text="Tag Searcher")
        self.tag_search_frame.pack(padx=10, pady=10, fill=tk.X)
        self.on_radio_change()

        # Tag Searcher
        self.search_entry1 = tk.Entry(self.tag_search_frame)
        self.search_entry1.pack(padx=10, pady=5)

        self.search_button = tk.Button(self.root, text="Search",
                                       command=lambda: self.tm.tag_searcher(self.search_entry1.get(), self.radio_var.get()))
        self.search_button.pack(pady=5)

    def add_tag_widget(self):
        self.tag_add_frame = tk.LabelFrame(self.root, text="Add Tags")
        self.tag_add_frame.pack(padx=10, pady=10, fill=tk.X)

        # Tag Adder
        self.add_entry = tk.Entry(self.tag_add_frame)
        self.add_entry.pack(padx=10, pady=5)
        self.add_button = tk.Button(self.tag_add_frame, text="Add Tag",
                                    command=lambda: self.tm.tag_adder(self.add_entry.get()))
        self.add_button.pack(pady=5)

        # Add Activation Tag
        self.add_activation = tk.Entry(self.tag_add_frame)
        self.add_activation.pack(padx=10, pady=5)
        self.add_acti_button = tk.Button(self.tag_add_frame, text="Add Activation Tag",
                                    command=lambda: self.tm.activation_tag(self.add_activation.get()))
        self.add_button.pack(pady=5)

    def remove_tag_widget(self):
        self.tag_remove_frame = tk.LabelFrame(self.root, text="Remove Tags")
        self.tag_remove_frame.pack(padx=10, pady=10, fill=tk.X)

        # Tag Remover
        self.remove_entry = tk.Entry(self.tag_remove_frame)
        self.remove_entry.pack(padx=10, pady=5)
        self.remove_button = tk.Button(self.tag_remove_frame, text="Remove",
                                       command=lambda: self.tm.tag_remover(self.remove_entry.get()))
        self.remove_button.pack(pady=5)

    def on_radio_change(self):
        self.radio_var = tk.StringVar(value="with") # shows neither being clicked
        with_radio = tk.Radiobutton(self.root, text="with", variable=self.radio_var, value="with")
        without_radio = tk.Radiobutton(self.root, text="without", variable=self.radio_var, value="without")
        with_radio.pack(pady=10) # displays the actual clickable button for with
        without_radio.pack(pady=10)

gui = Interface()
