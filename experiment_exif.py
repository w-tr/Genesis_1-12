# %%
# * Files with or without exif
f_without = "C:/opdage/Genesis_1-12/_unsorted_data/whatsapp_jw19bday/WhatsApp Image 2022-02-11 at 20.41.45.jpeg"
f_with = "C:/opdage/Genesis_1-12/_unsorted_data/sorted/2009/05/20090528-123914.JPG"
f_with_c_start_epoch = "C:/opdage/Genesis_1-12/_unsorted_data/sorted/2009/05/20090528-123526.JPG"
f_with_c_start_edited = "C:/opdage/Genesis_1-12/_unsorted_data/sorted/2009/05/20090528-123526 - Copy.JPG"
import hashlib
from exif import Image
with open(f_without, 'rb') as fp:
    obj1 = Image(fp)
with open(f_with, 'rb') as fp:
    obj2 = Image(fp)
with open(f_with_c_start_epoch, 'rb') as fp:
    obj3 = Image(fp)
    md5hash = hashlib.md5()
with open(f_with_c_start_epoch, 'rb') as fp:
    for byte_block in iter(lambda: fp.read(4096), b""):
        md5hash.update(byte_block)
    hash3 = md5hash.hexdigest()
with open(f_with_c_start_edited, 'rb') as fp:
    obj4 = Image(fp)
    md5hash = hashlib.md5()
with open(f_with_c_start_edited, 'rb') as fp:
    for byte_block in iter(lambda: fp.read(4096), b""):
        md5hash.update(byte_block)
    hash4 = md5hash.hexdigest()

print(obj1.has_exif)
# Actually as expected
print(obj2.has_exif)
print(obj2.datetime_original)
# C epoch start
print(obj3.has_exif)
print(obj3.datetime_original)
print(hash3)
# Edited datetime_original
print(obj4.has_exif)
print(obj4.datetime_original)
print(hash4)

# Result is failure
print(hash3 == hash4)
# Undoing datetime_original edit does not restore hash. This is because other
# Metadata is changed. Really need a hash that strips this from hash.

import time
print(type(obj4.datetime_original))
print(type(time.strptime(obj4.datetime_original, "%Y:%m:%d %H:%M:%S")))
y = time.strptime(obj4.datetime_original, "%Y:%m:%d %H:%M:%S")
if (y.tm_year == 1970 and y.tm_mon == 1 and y.tm_mday == 1):
    print("It's the start epoch. We can't used this")
 
# %%
