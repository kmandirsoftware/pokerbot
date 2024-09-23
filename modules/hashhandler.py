class HashHandler:
    def __init__(self, screen_position, mapped_dictionary={}):
        self.screen_position = screen_position
        self.mapped_dictionary = mapped_dictionary
    def take_screenshot(self):
        im = ImageGrab.grab(bbox=self.screen_position)
        im.save('hash.png')
        return imagehash.phash(Image.open('hash.png'))
    def identify_hash(self, image_hash):
      if str(image_hash) in self.mapped_dictionary:
          print(self.mapped_dictionary[str(image_hash)])
      else:
          print('no hash present')
    def take_screenshot_and_identify(self): 
        h = self.take_screenshot()
        self.identify_hash(h)