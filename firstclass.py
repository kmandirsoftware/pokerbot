from PIL import Image
from PIL import ImageGrab
import pygetwindow as gw
import imagehash

#found these manually running each spot one by one. Each position I need to clean up 
#which is why there are multiples of the same one. Not every square is the same size
suit_hash = {
        'fa9e81e89a8599c6':'heart',
        'fa9a81e89a85d9c6':'heart',
        'eae187c69e865896':'spade',
        'e6e887a51e56d8a8':'diamond',
        'e6e187c69e865896':'diamond1',
        'e6e887a51e56e8a8':'diamond2',
        'e6e887a51e56b8a8':'diamond3',
        'e6a5a57a1a829aa7':'club'
        }

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

Ignition_windows = gw.getWindowsWithTitle("No Limit Hold")
left, top, right, bottom = Ignition_windows[0].left, Ignition_windows[0].top, Ignition_windows[0].right, Ignition_windows[0].bottom
#first suit
l = left+344
t = top +382
r = left + 367
b = top +402

first_card_suit_position = (l,t,r,b)
first_card_suit = HashHandler(first_card_suit_position,suit_hash)
somehash1  = first_card_suit.take_screenshot()
print(somehash1)
first_card_suit.identify_hash(somehash1)
#second suit
l2 = left+382
t2 = top +382
r2 = left + 405
b2 = top +402
second_card_suit_position = (l2,t2,r2,b2)
second_card_suit = HashHandler(second_card_suit_position,suit_hash)
somehash  = second_card_suit.take_screenshot()
print(somehash)
second_card_suit.identify_hash(somehash)

