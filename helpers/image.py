"""Image helpers"""
import time
from PIL import Image

def save_image_with_direction(stream, direction):
    """Save image"""
    stream.seek(0)
    image = Image.open(stream)
    image.save('image%s.jpg' % ("-" + direction + "-"+ str(time.time())), format="JPEG")

def save_image_with_filename(stream, filename):
    """Save image with the given filename"""
    stream.seek(0)
    image = Image.open(stream)
    image = image.crop((0, 240, 640, 480))
    image.save(filename, format="JPEG")
