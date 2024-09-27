from PIL import ImageGrab
from PIL import Image
import imagehash

class HashHandler:
    def __init__(self, screen_position, mapped_dictionary={}):
        self.screen_position = screen_position
        self.mapped_dictionary = mapped_dictionary
    def take_screenshot(self,fname):
        im = ImageGrab.grab(bbox=self.screen_position)
        im.save(fname)
        image_file = Image.open(fname)
        image_file= image_file.convert('L')
        image_file.save(fname)
        return imagehash.phash(Image.open(fname))
    def identify_hash(self, image_hash):
      if str(image_hash) in self.mapped_dictionary:
          mysuit = self.mapped_dictionary[str(image_hash)]
          return mysuit
      else:
          print('no hash present')
          return "?"
    def take_screenshot_and_identify(self): 
        h = self.take_screenshot()
        self.identify_hash(h)