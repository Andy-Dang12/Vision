from Lib.encryption import Ecryption_Image
from PIL import Image

path = "data/New_Zealand_Lake.jpg"
img = Image.open(path)
s2 = Ecryption_Image.encode(img)
s1 = Ecryption_Image.encode(path)

print(s1 == s2)