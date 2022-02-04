# %%
import os
import pathlib
import time
import glob
# from PIL import Image
# import imagehash
import hashlib
import shutil

class TimestampFilename():
    """Create a class that can be used to move file, according to time stamp."""

    def __init__(self, src_, dst_):
        """On creating an object. Extract meaningful information."""
        # Don't test the validity of path, its coming from a glob search
        # Garbage in Garbage out
        self.src_ = str(src_)
        self.dst_ = str(dst_)
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
        # ----------------------------------------
        # Create processed information
        # ----------------------------------------
        # Create time related destination path
        self.dst = os.path.join(dst_, str(self.build_year), f"{self.build_month:02}")
        # Create hash
        md5hash = hashlib.md5()
        with open(src_, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5hash.update(byte_block)
        self.hash = md5hash.hexdigest()

    def get_timestamp_name(self):
        """Create a timestamp name for picture."""
        timestamp =  time.strftime("%Y%m%d-%H%M%S", time.gmtime(self.build_time))
        return timestamp + self.file_extension

    def add_duplication_tag(self, num):
        """Wrap int into duplication string identifier."""
        return "-(#" + str(num) + ")"

    def move_file(self):
        """Move picture from source to the distination.
        
        If the picture has identical timestamp then iterate instance of name."""
        filename = self.get_timestamp_name()
        os.makedirs(self.dst, exist_ok=True)
        isCopied = False;
        files_of_dir = os.listdir(self.dst)
        while not isCopied:
            if filename in files_of_dir:
                #overwrite filename
                print("Found Duplicated timestamp")
                new_name = filename.split("-(#")
                # instance where this is first iteration.
                if (len(new_name) < 2):
                    new_name = filename.split(".")
                    filename = new_name[0] + "-(#1)" + self.file_extension
                else:  # instance where this delimiter is encountered
                    inst = ''.join(
                        filter(lambda i: i.isdigit(), new_name[1]))
                    iteration = int(inst) + 1
                    filename = new_name[0] + \
                        self.add_duplication_tag(
                            iteration) + self.file_extension
            else:
                shutil.move(self.src_, os.path.join(self.dst, filename))
                isCopied = True

    def check_hash(self,TimeFilename_obj) :
        if self.hash == TimeFilename_obj.hash:
            self.dst = os.path.join(self.dst_, "duplication")
            print("DuplicationFound:")

###############################################################################
# %%
## find list
list_3 = glob.glob("../unsorted/**", recursive=True)
pictures = []
for x in list_3:
    if x.endswith((".jpg",".png","jpeg",".JPG",".PNG","JPEG")):
        pictures.append(TimestampFilename(x,"./sorted"))
# %%
for i, x in enumerate(pictures):
    for y in pictures[i+1:]:
        x.check_hash(y)
    x.move_file()
# %%
# Media stuff
import pytz
import datetime
from win32com.propsys import propsys, pscon

fn=".\get_info.mp4"
properties = propsys.SHGetPropertyStoreFromParsingName(fn)
dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
# %%

if not isinstance(dt, datetime.datetime):
    dt = datetime.datetime.fromtimestamp(int(dt))
    dt = dt.replace(tzinfo=pytz.timezone('UTC'))

dt_tokyo = dt.astimezone(pytz.timezone('Asia/Tokyo'))

# %%

from PIL import Image

fn="20150816-124854.JPG"
exif = Image.open(fn)._getexif()
# int value is key for lookup
# orig time = 36868
dat = exif.get(t[0])
sub = exif.get(t[1], 0)
# %%
