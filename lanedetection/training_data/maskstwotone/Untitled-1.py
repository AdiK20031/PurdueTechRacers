
from PIL import Image
from numpy import asarray
image = Image.open('lane06.png')
numpydata = asarray(image)
 
# data
print(numpydata[300])