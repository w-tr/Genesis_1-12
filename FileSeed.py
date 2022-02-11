# %%
import os
import time
import pathlib
import hashlib
import shutil

class FileSeed():
    """Each file has generic information in order to be processed on a computer.

    The metadata associated to a picture and a text file may be 
    different. Fortunately they will share this master class metadata.
    """
    def __init__(self, src_, dst_):
        """Extract meaningful information."""
        # -----------------------------------------------------------
        # Check the file exists. We are not Philistines
        # -----------------------------------------------------------
        try:
            f = open(src_)
            f.close()
            self.isValid = True
        except FileNotFoundError:
            print("File not file!!! Investigate - ", src_)
            self.isValid = False
            return
        # Archive init information
        self.src_ = str(src_)
        self.dst_ = str(dst_)
        # -----------------------------------------------------------
        # OS Filesystem information on disk location & filetype.
        # -----------------------------------------------------------
        temp = pathlib.Path(src_)
        self.file_parent = temp.parent
        self.file_name = temp.name
        self.file_extension = temp.suffix
        # -----------------------------------------------------------
        # OS Filesystem information on build time.
        # -----------------------------------------------------------
        # People in forensics will tell you this information is subject
        # to manipulation. Regardless 
        #   - find min of (creation, access and modified) time 
        self.build_time = min(os.path.getctime(
            src_), os.path.getatime(src_), os.path.getmtime(src_))
        self.build_year = time.gmtime(self.build_time).tm_year
        self.build_month = time.gmtime(self.build_time).tm_mon
        # Create time related destination path. N.B Overwrite if file
        # specific metadata exists and is different.
        self.dst = os.path.join(
            dst_, str(self.build_year), f"{self.build_month:02}")
        # -----------------------------------------------------------
        # Create hash
        # -----------------------------------------------------------
        # Every file can be hashed. 
        # In the past I had a Xilinx project generate .bitfiles with
        # different hash checksums. 
        # It turned out that the xilinx project included information 
        # about build date etc. This corrupted the hash. However when
        # the file was parsed and only the content was analyses it
        # showed that the data was verifible.
        # TODO: Find out about files and meta. For example if I take
        # TODO --- a photo with my phone. Is the file generated
        # TODO --- going to be different compared to the same file
        # TODO --- downloaded from facebook/google drive?
        # TODO --- It's a known fact that facebook remove geotag info.
        # ----------------------------------------
        # Create processed information
        # ----------------------------------------
        # md5 is a broken crypto hash, but okay for data integrity.
        # Furthermore a file like an image could be identical but have
        # metadata changed. This change = different hash
        md5hash = hashlib.md5()
        with open(src_, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5hash.update(byte_block)
        self.hash = md5hash.hexdigest()

    #def move_file(

# %%
