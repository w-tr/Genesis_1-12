# %%
import os
import pathlib
import time
from PIL import Image
import imagehash
import hashlib
import shutil

class MyPicture():
    """Create a class that can be used to move images, compare hashes etc."""

    def __init__(self, src_, dst_):
        """On creating an object. Extract meaningful information."""
        # Don't test the validity of path, its coming from a glob search
        # Garbage in Garbage out
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
        try:
            self.hash = imagehash.average_hash(Image.open(src_))
        except:
            try:
                md5hash = hashlib.md5()
                with open(src_, "rb") as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        md5hash.update(byte_block)
                self.hash = md5hash.hexdigest()
            except:
                print("File - image is corrupted") 
                self.hash = ""
        

    def _file_timestamp(self):
        """Create a timestamp name for picture."""
        timestamp =  time.strftime("%Y_%m_%d-%H%M%S", time.gmtime(self.build_time))
        return timestamp + self.file_extension

    def move_file(self):
        """Move picture from source to the distination.
        
        If the picture has identical timestamp then iterate instance of name."""
        filename = self._file_timestamp()
        os.makedirs(self.dst, exist_ok=True)
        isCopied = False;
        files_of_dir = os.listdir(self.dst)
        if (self.hash != ""):
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
                        inst = ''.join(filter(lambda i: i.isdigit(), new_name[1]))
                        iteration = int(inst) + 1
                        filename = new_name[0] + \
                            self.add_duplication_tag(
                                iteration) + self.file_extension
                else:
                    shutil.move(self.src, os.path.join(self.dst, filename))
                    isCopied = True
        else:
            print("Could not copy :", self.src)
            

    def add_duplication_tag(self, num):
        """Wrap int into duplication string identifier."""
        return "-(#" + str(num) + ")"
