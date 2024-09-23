import pygetwindow as gw
from modules import hashhandler as hh 
import suits

#Ignition_windows = gw.getWindowsWithTitle("No Limit Hold")
Ignition_windows = gw.getWindowsWithTitle("Poker Lobby")
left, top, right, bottom = Ignition_windows[0].left, Ignition_windows[0].top, Ignition_windows[0].right, Ignition_windows[0].bottom
#first suit
l = left+344
t = top +382
r = left + 367
b = top +402

first_card_suit_position = (l,t,r,b)
first_card_suit = hh.HashHandler(first_card_suit_position,suits.suit_hash)
somehash1  = first_card_suit.take_screenshot()
print(somehash1)
first_card_suit.identify_hash(somehash1)
#second suit
l2 = left+382
t2 = top +382
r2 = left + 405
b2 = top +402
second_card_suit_position = (l2,t2,r2,b2)
second_card_suit = hh.HashHandler(second_card_suit_position,suits.suit_hash)
somehash  = second_card_suit.take_screenshot()
print(somehash)
second_card_suit.identify_hash(somehash)

