import pygetwindow as gw
from modules import hashhandler as hh 
import suits
import locations

Ignition_windows = gw.getWindowsWithTitle("No Limit Hold")
#Ignition_windows = gw.getWindowsWithTitle("Poker Lobby")
left, top, right, bottom = Ignition_windows[0].left, Ignition_windows[0].top, Ignition_windows[0].right, Ignition_windows[0].bottom


for card in locations.board:
        icard = locations.board[card]
        l = left + icard["left"]
        t = top  + icard["top"]
        r = left + icard["right"]
        b = top  + icard["bottom"]
        card_suit_poition = (l,t,r,b)
        card_suit = hh.HashHandler(card_suit_poition,suits.suit_hash)
        somehash = card_suit.take_screenshot()
        print(card,somehash)
        card_suit.identify_hash(somehash)


