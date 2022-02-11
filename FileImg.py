# %%
from PIL import Image as pil_img
import imagehash
from exif import Image as exif_img
from FileSeed import FileSeed

class FileImg(FileSeed):
    def __init__(self, src_, dst_):
        super().__init__(src_, dst_)
        self.imghash = imagehash.average_hash(pil_img.open(src_))
        with open(src_, 'rb') as fp:
            exif_obj = exif_img(fp)
        self.exif = exif_obj
        # Comment on the absence of exif
        # An empty mind(exif) is like unto a freshly turned sod; 
        # if not sown with the seeds of love, duty and honour, (exif)
        # the insidious weeds of heresy will take root.
        # Therefore reliance on create/mod/accessed date
# %%