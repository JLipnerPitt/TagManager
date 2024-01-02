import os
import shutil
#import cv2


class TagManager:
    def __init__(self):
        self.root_directory = None  # parent folder of dataset location
        self.img_directory = None  # created folder location to store only images from dataset
        self.txt_directory = None  # created folder location to store only txt files from dataset

    def set_directory(self, dir):
        self.root_directory = dir

    def get_main_directory(self):
        return self.root_directory

    def get_img_directory(self):
        return self.img_directory

    def get_txt_directory(self):
        return self.txt_directory

    def create_folder(self, folder_name, directory=None):
        if directory is None:
            directory = self.root_directory

        folder_path = os.path.join(directory, folder_name)  # joins creates directory/folder_name path
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # delete folder if it already exists
        os.makedirs(folder_path)  # creates folder in specified directory
        return folder_path

    def separate_images(self):
        images_path = self.create_folder("dataset_images")
        for filename in os.listdir(self.root_directory):  # checks each file in directory
            if filename.endswith(".jpg"):
                imgfile = os.path.join(self.root_directory, filename)
                shutil.copy(imgfile, images_path)

        self.img_directory = images_path


    def separate_txt_files(self):
        txt_path = self.create_folder("dataset_tags")
        for filename in os.listdir(self.root_directory):  # checks each file in directory
            if filename.endswith(".txt"):
                txtfile = os.path.join(self.root_directory, filename)
                shutil.copy(txtfile, txt_path)

        self.txt_directory = txt_path

    def tag_searcher(self, tag, choice=None, folder_name=None):
        #  creates folder located in the datasets path
        if folder_name is None:
            directory2 = self.create_folder("tag_manager", os.path.dirname(self.root_directory))
        else:
            directory2 = self.create_folder(folder_name, os.path.dirname(self.root_directory))

        if choice is None:  # searches for txt files with tag by default
            choice = "with"

        if choice == "without":
            condition = lambda x: tag not in x
            message = "without"
        else:  # choice == "with"
            condition = lambda x: tag in x
            message = "with"

        count = 0
        for filename in os.listdir(self.root_directory):
            if filename.endswith(".txt"):  # Ensure we're only looking at .txt files
                with open(os.path.join(self.root_directory, filename), 'r') as file:
                    contents = file.read()
                    if condition(contents):
                        txtfile = os.path.join(self.root_directory, filename)
                        imgfile = os.path.join(self.root_directory, filename.replace('.txt', '.jpg'))
                        shutil.copy(txtfile, directory2)
                        shutil.copy(imgfile, directory2)
                        count += 1

        print("There are {} images {} the '{}' tag.".format(count, message, tag))
        os.startfile(directory2)  # opens folder the files were moved to
        return directory2

    def tag_adder(self, new_tag, search_dir=None):
        count = 0
        if search_dir is None:
            search_dir = self.root_directory

        for filename in os.listdir(search_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(search_dir, filename), 'a+') as file:  # a+ appends to end of string
                    file.write(", " + new_tag)
                    count += 1
        print("You added the '{}' tag to {} txt files.".format(new_tag, count))

    def activation_tag(self, act_tag):
        count = 0
        for filename in os.listdir(self.root_directory):
            if filename.endswith(".txt"):
                with open(os.path.join(self.root_directory, filename), 'r') as old_file:
                    contents = old_file.read()
                with open(os.path.join(self.root_directory, filename), 'w') as new_file:
                    new_file.write(act_tag + ", ")  # Write new data to new file
                    new_file.write(contents)  # Append old content to new file
                count += 1
        print("You added the '{}' tag to {} txt files.".format(act_tag, count))

    def tag_replacer(self, old_tag, new_tag, search_dir=None):
        count = 0
        if search_dir is None:
            search_dir = self.root_directory

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
            search_dir = self.root_directory

        if isinstance(rem_tag, list) == False:
            for filename in os.listdir(self.root_directory):
                if filename.endswith(".txt"):
                    with open(os.path.join(self.root_directory, filename), 'r') as old_file:
                        contents = old_file.read()
                    new_contents = contents.replace(rem_tag + ", ", "")  # try to replace old tag with new tag

                    if contents != new_contents:  # if contents have changed, the tag was removed
                        with open(os.path.join(search_dir, filename), 'w') as file:
                            file.write(new_contents)
                        count += 1
            print("You removed {} copies of '{}'.".format(count, rem_tag))

        else:
            for filename in os.listdir(self.root_directory):
                if filename.endswith(".txt"):
                    with open(os.path.join(self.root_directory, filename), 'r') as old_file:
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
            path = self.root_directory

        files = os.listdir(path)
        images = []
        [images.append(file) for file in files if file.endswith(old)]

        for img in images:
            if os.path.exists(os.path.join(path, img.replace(old, new))):
                continue
            os.rename(os.path.join(path, img), os.path.join(path, img.replace(old, new)))

    def rename_txt_and_img_pairs(self, path=None):
        if path is None:
            path = self.root_directory

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
        #if self.img_directory is None:
         #   self.create_folder("dataset_images")

        upscale_directory = self.create_folder("images to be upscaled")

        for img in os.listdir(self.root_directory):
            if img.endswith(".jpg"):
                im = cv2.imread(os.path.join(self.root_directory, img))
                height, width = im.shape[:2]
                if (width or height) < 2000:
                    shutil.copy(os.path.join(self.root_directory, img), upscale_directory)

        #  if folder doesn't exist, create it, and make a copy
           #  else check size of each image in folder
              #  if img width or height is < 2000 pixels, upscale

        # after all images have been upscaled, show old and upscaled image side by side
        # if satisfied with upscaled image results, overwrite that image in the main folder

