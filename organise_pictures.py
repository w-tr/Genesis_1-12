# %%
from MyPictureClass import MyPicture 
import pathlib
import os
import glob
# find all *.jpg
base = (pathlib.Path(__file__).parent)

src = "src/merge"
dst = "image_organised"
basesrc = os.path.join(base, src)
basedst = os.path.join(base, dst)

jpg_list = glob.glob(basesrc+"/**.jpg", recursive=True)
jpeg_list = glob.glob(basesrc+"/**.jpeg", recursive=True)
img_list = jpg_list + jpeg_list

for src_file in img_list:
    inst = MyPicture(src_file, dst)
    inst.move_file()

# %%
