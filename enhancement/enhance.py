from PIL import ImageEnhance
import Image
image = Image.open("accept.jpg")

color= ImageEnhance.Sharpness(image)#0.0-1.0
sharp=ImageEnhance.Color(image)#0.0-1.0-2.0
contrast=ImageEnhance.Contrast(image)#0.0-1.0 gray to orginal
bright=ImageEnhance.Brightness(image)#0.0-1.0 black to orginal

fc = 2.0
im=sharp.enhance(fc)
#im=bright.enhance(fc)
im.save("im" + '.jpg')
