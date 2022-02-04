
# ? How to implement
# ? 1. Create a class for capturing all the potential info bits I want to pump out.
# ? 2. Inspect the json
# ? 3. Filter the saved info to look for inital bits i can use to remove Duplication.
# ?  . a. Check timestamp.
# ?  . b. Check image hash.
# ?  . c. Check via filecmp or image hash.



# %% 
# Find the Files
import os
import pathlib
import time
import filecmp
import time
import glob
import json
# %% 
# Find the Files
from PIL import Image
import imagehash
x = PicOrganiser();
# %%
# Find the Files
for filename in glob.glob('path'):
    x.name = x
    x.time = os.path.getctime(filename)

# %%
# Make directories
pathlib.Path(__file__).parent.resolved()
new_dir = os.path.join(sorted_pictures,/,str(year),/str(mount))
os.makedirs("path/"+str(year)/str(month))



# %%
file1 = "file1.jpg"
file2 = "file2.jpg"
file3 = "file3.jpg"
file4 = "file4.jpg"
file5 = "file5.jpg"
print(time.ctime(os.path.getctime("file1.jpg")))
print(os.path.getctime("file2.jpg"))
print(time.ctime(os.path.getctime("file3.jpg")))
print(filecmp.cmp(file1, file2))
print(filecmp.cmp(file1, file3))

hash1 = imagehash.average_hash(Image.open(file1))
hash2 = imagehash.average_hash(Image.open(file2))
hash3 = imagehash.average_hash(Image.open(file3))
hash4 = imagehash.average_hash(Image.open(file4))
hash5 = imagehash.average_hash(Image.open(file5))
# %% 
print(hash1)
print(hash2)
print(hash3)
print(hash4)
print(hash5)
print("delta from 4 to 5 : ", abs(hash4-hash5))
print("delta from 1 to 5 : ", abs(hash1-hash5))
# %%
import cv2

class CompareImage(object):

    def __init__(self, image_1_path, image_2_path):
        self.minimum_commutative_image_diff = 1
        self.image_1_path = image_1_path
        self.image_2_path = image_2_path

    def compare_image(self):
        image_1 = cv2.imread(self.image_1_path, 0)
        image_2 = cv2.imread(self.image_2_path, 0)
        commutative_image_diff = self.get_image_difference(image_1, image_2)

        if commutative_image_diff < self.minimum_commutative_image_diff:
            print("Matched")
            return commutative_image_diff
        return 10000 #random failure value

    @staticmethod
    def get_image_difference(image_1, image_2):
        first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

        img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
        img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
        img_template_diff = 1 - img_template_probability_match

        # taking only 10% of histogram diff, since it's less accurate than template method
        commutative_image_diff = (img_hist_diff / 10) + img_template_diff
        return commutative_image_diff

# %%

    if __name__ == '__main__':
        compare_image = CompareImage('image1/path', 'image2/path')
        image_difference = compare_image.compare_image()
        print(image_difference)

# %%
import os
import pathlib
import time
from datetime import datetime
from PIL import Image
import imagehash
import shutil

class MyPictures():


    def __init__(self, src_, dst_):
        # Don't test the validity of path, its coming from a glob search, so must exit
        self.src = str(src_)
        # ----------------------------------------
        # Extract pre-processing information
        # ----------------------------------------
        temp = pathlib.Path(src_)
        self.file_parent = temp.parent
        self.file_name = temp.name
        self.file_extension = temp.suffix
        # Subject to manipulation, find min of creation, access and modified date for file, then
        # turn the c time number into a time structure.
        self.build_time = min(os.path.getctime(src_), os.path.getatime(src_), os.path.getmtime(src_))
        self.build_year = time.gmtime(self.build_time).tm_year
        self.build_month = time.gmtime(self.build_time).tm_mon
        # Create destination path
        self.dst = os.path.join(dst_, str(self.build_year), f"{self.build_month:02}")
        # ----------------------------------------
        # Extract post-processing information
        # ----------------------------------------
        self.imghash = imagehash.average_hash(Image.open(src_))

    def name_file_to_timestamp(self):
        # self.build_time
        # return filename
        #self.dst = os.path.join(root, self.build_year, self.build_month)
        timestamp =  time.strftime("%Y_%m_%d-%H%M%S", time.gmtime(self.build_time))
        return timestamp + self.file_extension

    def move_file(self):
        filename = self.name_file_to_timestamp()
        os.makedirs(self.dst, exist_ok=True)
        isCopied = False;
        files_of_dir = os.listdir(self.dst)
        while not isCopied:
            if filename in files_of_dir:
                #overwrite filename
                new_name = filename.split("-(#")
                if (len(new_name) < 2): #instance where this is first iteration.
                    new_name = filename.split(".")
                    filename = new_name[0] + "-(#1)" + self.file_extension
                else: # instance where this delimiter is encountered
                    inst = ''.join(filter(lambda i: i.isdigit(), new_name[1]))
                    print(inst)
                    print(type(inst))
                    iteration = int(inst) + 1
                    print(iteration)
                    print(type(iteration))
                    filename = new_name[0] + self.add_duplication_tag(iteration) + self.file_extension
            else:
                shutil.move(self.src, os.path.join(self.dst, filename))
                isCopied = True

    def add_duplication_tag(self, num):
        return "-(#" + str(num) + ")"

# %%
# Test
a1 = MyPictures("bob.jpg", "./dump")
a2 = MyPictures("bob2.jpg", "./dump")
# %%
a3 = MyPictures("bob3.jpg", "./dump")
# %%
a1.move_file()
# %%
a2.move_file()
# %%
a3.move_file()
# %%
b1 = MyPictures("rob.jpg", "./dump")
b2 = MyPictures("rob2.jpg", "./dump")
    # %%
a = MyPictures("file1.jpg", ".")
b = MyPictures("file2.jpg", ".")
c = MyPictures("file3.jpg", ".")
d = MyPictures("file4.jpg", ".")
e = MyPictures("bob.jpg", ".")
f = MyPictures("rob.jpg", ".")
print(a.name_file())
print(b.name_file())
print(c.name_file())
print(d.name_file())
print(e.name_file())
print(f.name_file())
print(a.dst)
print(b.dst)
print(c.dst)
print(d.dst)
print(e.dst)
print(f.dst)


#datetime.strftime



# %%

os.replace
if os.path.exists(filename):
    while True:
        new_filename = 
        str(string).split


 for files in os.listdir(uploadPath):
        if not os.listdir(dirPath):
            shutil.move(uploadPath+files, dirPath+files)
            print('no need to rename, so i moved it ...', files)
        else:
            for files in os.listdir(uploadPath):
                addOne=0
                for dirFile in os.listdir(dirPath):
                    if files in dirFile:
                        newName = os.rename(uploadPath+files, dirPath+files+str(addOne))
                        addOne+=1
                        print('renamed in '+str(newName))
                shutil.move(uploadPath+files, dirPath+files)
