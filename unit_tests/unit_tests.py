import unittest
import os
import re


def tag_adder(dir, add_tag):
    count = 0
    add_tag = re.split('[,;./?<>~`]', add_tag)
    add_tag = [word.strip() for word in add_tag if word]  # removes comma only entries

    # while self.root_directory is None:
    #   print("Select a folder first!")

    for filename in os.listdir(dir):
        with open(os.path.join(dir, filename), 'r') as file:
            contents = file.read()
            for tag in add_tag:
                if contents.find(tag) != -1:  # tag to be added already exists in file
                    continue
                with open(os.path.join(dir, filename), 'w') as file:
                    file.write(contents)
                    file.write(", " + tag)  # write tag to the end of txt file
                    count += 1

    if count == 0:
        print("Tag already existed in every txt file.")
    else:
        print("You added {} instances of tag(s).".format(count))

class TestTagManager(unittest.TestCase):
    def test_add_tags(self):
        dir = r"C:\Users\iamth\Desktop\Python Programs\GOATED\TagManager\unit_tests\test_add_tags"
        text1 = "eastern dragon, sky, 1boy"
        tag = "dog"
        with open(os.path.join(dir, "test.txt"), 'w') as file:
            file.write(text1)
        text2 = "eastern dragon, sky, 1boy, dog"

        tag_adder(dir, tag)
        with open(os.path.join(dir, "test.txt"), 'r') as file:
            contents = file.read()
            self.assertEqual(text2,contents)

    def test_activation_tag(self):
        pass

    def test_remove_tags(self):
        pass

    def test_replace_tags(self):
        pass
