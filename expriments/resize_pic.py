Fname='4970.jpg'
from PIL import Image

im=Image.open(Fname)
w,h=im.size

W=1024
im=im.resize([W,h])
im=im.crop((0,350,W,355))
im.save("4970.bmp")
