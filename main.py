from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import pygetwindow as gw
from modules import hashhandler as hh 
from modules import cards
from modules import strategy
from modules import monteEval
from pprint import pprint
import inspect
import requests
import suits
import locations
import valuelocs

from treys import Card
from treys import Evaluator

evaluator = Evaluator()

Ignition_windows = gw.getWindowsWithTitle("No Limit Hold")
#Ignition_windows = gw.getWindowsWithTitle("Poker Lobby")
left, top, right, bottom = Ignition_windows[0].left, Ignition_windows[0].top, Ignition_windows[0].right, Ignition_windows[0].bottom
global player_cards
global dealer_cards
global myhand
global board

myhand = []
player_cards = []
dealer_cards = []
board = []
mycards = []
dealer_conte_cards = []

def playerscards():
        global dealer_image
        global myhand
        global mycards
        mycards.clear()
        myhand.clear()
        best_hand = []
        player_cards.clear()
        vv=[]
        ss=[]
        actionbutton.deselect()
        wonlostbutton.deselect()

        ai_comment.config(text="Starting to Analyze")
        dealer_image = resize_cards(f'images/cards/default.png')
        dealer_card1.config(image=dealer_image)
        dealer_card2.config(image=dealer_image)
        dealer_card3.config(image=dealer_image)
        dealer_card4.config(image=dealer_image)
        dealer_card5.config(image=dealer_image)
        for card in locations.players_board:
                icard = locations.players_board[card]
                l = left + icard["left"]
                t = top  + icard["top"]
                r = left + icard["right"]
                b = top  + icard["bottom"]
                card_suit_poition = (l,t,r,b)
                card_suit = hh.HashHandler(card_suit_poition,suits.suit_hash)
                filename = card+".png"
                somehash = card_suit.take_screenshot(filename)       
                mycardsuit = card_suit.identify_hash(somehash) 
                if mycardsuit == "?":
                        print(card,somehash)
                else:
                        ss.append(mycardsuit)
        for card in valuelocs.players_board:
                icard = valuelocs.players_board[card]
                l = left + icard["left"]
                t = top  + icard["top"]
                r = left + icard["right"]
                b = top  + icard["bottom"]
                card_value_poition = (l,t,r,b)
                card_value = hh.HashHandler(card_value_poition,suits.value_hash)
                filename = card+"value.png"
                somehash = card_value.take_screenshot(filename)
                mycardvalue = card_value.identify_hash(somehash)        
                if mycardvalue == "?":
                        print(card,somehash)
                else:
                        vv.append(mycardvalue)
        dealt_card = cards.Card(vv[0], ss[0])
        player_cards.append(dealt_card)
        dealt_card = cards.Card(vv[1], ss[1])
        player_cards.append(dealt_card)
        card = vv[1]+ss[1]
        print(card)
        global player_card2_image
        global player_card1_image
        player_card2_image = resize_cards(f'images/cards/{card}.png')
        player_card2.config(image=player_card2_image)
        card = vv[0]+ss[0]
        print(card)
        player_card1_image = resize_cards(f'images/cards/{card}.png')
        player_card1.config(image=player_card1_image)
        suited = "o"
        if ss[0] == ss[1]:
                suited = "s"
        player_hand1 = vv[0]
        player_hand1 += vv[1]
        player_hand1 += suited
        player_hand2 = vv[1]
        player_hand2 += vv[0]
        player_hand2 += suited
        answer=""
        if (player_hand1 in strategy.STier) or (player_hand2 in strategy.STier):
                answer+="Your hand is amazing! [S Tier]\n"
                answer+="Aggressive preflop raise\n"
        elif (player_hand1 in strategy.ATier) or (player_hand2 in strategy.ATier):
                answer+="Your hand is great. [A Tier]\n"
        elif (player_hand1 in strategy.BTier) or (player_hand2 in strategy.BTier):
                answer+="Your hand is decent. [B Tier]\n"
        elif (player_hand1 in strategy.CTier) or (player_hand2 in strategy.CTier):
                answer+="Your hand is poor. [C Tier]\n"                
                answer+="Fold, unless you're going last. \nExamine how the other players are betting pre-flop.\n"
        elif (player_hand1 in strategy.DTier) or (player_hand2 in strategy.DTier):
                answer+="Your hand is awful. [D Tier]\n"
                answer+="Fold preflop. Only play this hand as a small blind.\n"
        else:
                answer+="Your hand is trash!\n"
                answer+="Fold immediately.\n"
        if ss[0] == ss[1]:
                answer+="NOTE: Your cards are suited! Watch for a possible flush draw.\n"
                answer+="##################################\n"
        print (numvillians.get())
        myEquity = monteEval.calcEquity(vv[0]+ss[0],vv[1]+ss[1],int(numvillians.get()),0.5)        
        answer+=f"Equity of hand = {myEquity} \n"
        ai_comment.config(text=answer)
        myURL = f"http://192.168.1.45:8000/dealt/?card1={vv[0]+ss[0]}&card2={vv[1]+ss[1]}&numvillian={int(numvillians.get())}&varience=0.5&folded={int(actionbuttoncheck.get())}&won={int(wonlostbuttoncheck.get())}"
        response = requests.get(myURL)
        biganswer = response.json()
        answer+=f"Big Equity of hand = {biganswer}\n"
        ai_comment.config(text=answer)
        myhand = [
                Card.new(vv[0]+ss[0]),
                Card.new(vv[1]+ss[1])
        ]
        mycards.append(vv[0]+ss[0])
        mycards.append(vv[1]+ss[1])
        return



def dealerFlop():  
        global board
        global dealer_conte_cards
        ss = []
        vv = []    
        dealer_cards.clear()
        dealer_conte_cards.clear()
        for card in locations.dealer_flop_board:
                icard = locations.dealer_flop_board[card]
                l = left + icard["left"]
                t = top  + icard["top"]
                r = left + icard["right"]
                b = top  + icard["bottom"]
                card_suit_poition = (l,t,r,b)
                card_suit = hh.HashHandler(card_suit_poition,suits.suit_hash)
                filename = card+".png"
                somehash = card_suit.take_screenshot(filename)       
                mycardsuit = card_suit.identify_hash(somehash) 
                if mycardsuit == "?":
                        print(card,somehash)
                else:
                        ss.append(mycardsuit)        
        for card in valuelocs.dealers_board:
                icard = valuelocs.dealers_board[card]
                l = left + icard["left"]
                t = top  + icard["top"]
                r = left + icard["right"]
                b = top  + icard["bottom"]
                card_value_poition = (l,t,r,b)
                card_value = hh.HashHandler(card_value_poition,suits.value_hash)
                filename = card+"value.png"
                somehash = card_value.take_screenshot(filename)
                mycardvalue = card_value.identify_hash(somehash)        
                if mycardvalue == "?":
                        print(card,somehash)
                else:
                        vv.append(mycardvalue)
        print (vv)
        print (ss)
        card = vv[0]+ss[0]
        global dealer_image
        global dealer_card2_image
        global dealer_card3_image
        dealer_image = resize_cards(f'images/cards/{card}.png')
        dealer_card1.config(image=dealer_image)
        card = vv[1]+ss[1]
        dealer_card2_image = resize_cards(f'images/cards/{card}.png')
        dealer_card2.config(image=dealer_card2_image)
        card = vv[2]+ss[2]
        dealer_card3_image = resize_cards(f'images/cards/{card}.png')
        dealer_card3.config(image=dealer_card3_image)
        #Find best Hand
        dealt_card = cards.Card(vv[0], ss[0])
        dealer_cards.append(dealt_card)
        dealt_card = cards.Card(vv[1], ss[1])
        dealer_cards.append(dealt_card)
        dealt_card = cards.Card(vv[2], ss[2])
        dealer_cards.append(dealt_card)
        answer=""
        for card in player_cards:
                print(card.value,card.suit)
        for card in dealer_cards:
                print(card.value,card.suit)
        answer = strategy.current_hand(player_cards, dealer_cards)
        print (answer)        
        board = [
                Card.new(vv[0]+ss[0]),
                Card.new(vv[1]+ss[1]),
                Card.new(vv[2]+ss[2])
                ]
        print(myhand)
        evalue = evaluator.evaluate(board, myhand)
        print(evalue)
        dealer_conte_cards.append(vv[0]+ss[0])
        dealer_conte_cards.append(vv[1]+ss[1])
        dealer_conte_cards.append(vv[2]+ss[2])
        answer+=f"Hand has a {evalue} out of 7462 score\n"
        myEquity = monteEval.flopEquity(mycards[0],mycards[1],int(numvillians.get()),0.5,vv[0]+ss[0],vv[1]+ss[1],vv[2]+ss[2])
        answer+=f"Equity of hand = {myEquity} \n"
        ai_comment.config(text=answer)
        myURL = f"http://192.168.1.45:8000/flop/?card1={mycards[0]}&card2={mycards[1]}&numvillian={int(numvillians.get())}&varience=0.5&flop1={vv[0]+ss[0]}&flop2={vv[1]+ss[1]}&flop3={vv[2]+ss[2]}&folded={int(actionbuttoncheck.get())}&won={int(wonlostbuttoncheck.get())}"
        response = requests.get(myURL)
        biganswer = response.json()
        answer+=f"Big Equity of hand = {biganswer}\n"        
        ai_comment.config(text=answer)        
        return

def dealer_turn():  
        ss = []
        vv = []    
        global board
        global myhand
        for card in locations.dealer_turn_board:
                icard = locations.dealer_turn_board[card]
                l = left + icard["left"]
                t = top  + icard["top"]
                r = left + icard["right"]
                b = top  + icard["bottom"]
                card_suit_poition = (l,t,r,b)
                card_suit = hh.HashHandler(card_suit_poition,suits.suit_hash)
                filename = card+".png"
                somehash = card_suit.take_screenshot(filename)       
                mycardsuit = card_suit.identify_hash(somehash) 
                if mycardsuit == "?":
                        print(card,somehash)
                else:
                        ss.append(mycardsuit)        
        for card in valuelocs.dealer_turn_board:
                icard = valuelocs.dealer_turn_board[card]
                l = left + icard["left"]
                t = top  + icard["top"]
                r = left + icard["right"]
                b = top  + icard["bottom"]
                card_value_poition = (l,t,r,b)
                card_value = hh.HashHandler(card_value_poition,suits.value_hash)
                filename = card+"value.png"
                somehash = card_value.take_screenshot(filename)
                mycardvalue = card_value.identify_hash(somehash)        
                if mycardvalue == "?":
                        print(card,somehash)
                else:
                        vv.append(mycardvalue)
        card = vv[0]+ss[0]
        global dealer_card4_image
        dealer_card4_image = resize_cards(f'images/cards/{card}.png')
        dealer_card4.config(image=dealer_card4_image)
        dealt_card = cards.Card(vv[0], ss[0])
        dealer_cards.append(dealt_card)
        answer = strategy.current_hand(player_cards, dealer_cards)
        print (answer)
        board.append(Card.new(vv[0]+ss[0]))
        evalue = evaluator.evaluate(board, myhand)
        print(evalue)
        answer+=f"Hand has a {evalue} out of 7462 score\n"
        dealer_conte_cards.append(vv[0]+ss[0])
        myEquity = monteEval.turnEquity(mycards[0],mycards[1],int(numvillians.get()),0.5,dealer_conte_cards[0],dealer_conte_cards[1],dealer_conte_cards[2],vv[0]+ss[0])
        answer+=f"Equity of hand = {myEquity} \n"
        ai_comment.config(text=answer)
        myURL = f"http://192.168.1.45:8000/turn/?card1={mycards[0]}&card2={mycards[1]}&numvillian={int(numvillians.get())}&varience=0.5&flop1={dealer_conte_cards[0]}&flop2={dealer_conte_cards[1]}&flop3={dealer_conte_cards[2]}&flop4={vv[0]+ss[0]}&folded={int(actionbuttoncheck.get())}&won={int(wonlostbuttoncheck.get())}"
        response = requests.get(myURL)
        biganswer = response.json()
        answer+=f"Big Equity of hand = {biganswer}\n"        
        ai_comment.config(text=answer)

def dealer_river():  
        global board
        global myhand
        ss = []
        vv = []    
        for card in locations.dealer_river_board:
                icard = locations.dealer_river_board[card]
                l = left + icard["left"]
                t = top  + icard["top"]
                r = left + icard["right"]
                b = top  + icard["bottom"]
                card_suit_poition = (l,t,r,b)
                card_suit = hh.HashHandler(card_suit_poition,suits.suit_hash)
                filename = card+".png"
                somehash = card_suit.take_screenshot(filename)       
                mycardsuit = card_suit.identify_hash(somehash) 
                if mycardsuit == "?":
                        print(card,somehash)
                else:
                        ss.append(mycardsuit)        
        for card in valuelocs.dealer_river_board:
                icard = valuelocs.dealer_river_board[card]
                l = left + icard["left"]
                t = top  + icard["top"]
                r = left + icard["right"]
                b = top  + icard["bottom"]
                card_value_poition = (l,t,r,b)
                card_value = hh.HashHandler(card_value_poition,suits.value_hash)
                filename = card+"value.png"
                somehash = card_value.take_screenshot(filename)
                mycardvalue = card_value.identify_hash(somehash)        
                if mycardvalue == "?":
                        print(card,somehash)
                else:
                        vv.append(mycardvalue)
        card = vv[0]+ss[0]
        global dealer_card5_image
        dealer_card5_image = resize_cards(f'images/cards/{card}.png')
        dealer_card5.config(image=dealer_card5_image)
        dealt_card = cards.Card(vv[0], ss[0])
        dealer_cards.append(dealt_card)
        answer = strategy.current_hand(player_cards, dealer_cards)
        print (answer)
        board.append(Card.new(vv[0]+ss[0]))
        dealer_conte_cards.append(vv[0]+ss[0])
        evalue = evaluator.evaluate(board, myhand)
        print(evalue)
        answer+=f"Hand has a {evalue} out of 7462 score\n"
        myEquity = monteEval.riverEquity(mycards[0],mycards[1],int(numvillians.get()),0.5,dealer_conte_cards[0],dealer_conte_cards[1],dealer_conte_cards[2],dealer_conte_cards[3],vv[0]+ss[0])
        answer+=f"Equity of hand = {myEquity} \n"     
        ai_comment.config(text=answer)
        myURL = f"http://192.168.1.45:8000/river/?card1={mycards[0]}&card2={mycards[1]}&numvillian={int(numvillians.get())}&varience=0.5&flop1={dealer_conte_cards[0]}&flop2={dealer_conte_cards[1]}&flop3={dealer_conte_cards[2]}&flop4={dealer_conte_cards[3]}&flop5={vv[0]+ss[0]}&folded={int(actionbuttoncheck.get())}&won={int(wonlostbuttoncheck.get())}"
        response = requests.get(myURL)
        biganswer = response.json()
        answer+=f"Big Equity of hand = {biganswer}\n"                           
        ai_comment.config(text=answer)

def post_win():
        print(mycards)
        myURL = f"http://192.168.1.45:8000/dealt/?card1={mycards[0]}&card2={mycards[1]}&numvillian={int(numvillians.get())}&varience=0.5&&folded={int(0)}&won={int(1)}"
        response = requests.get(myURL)
        biganswer = response.json()
        answer=f"Big Equity of hand = {biganswer}\n"                           
        ai_comment.config(text=answer)
        return

def post_folded():
        print(mycards)
        myURL = f"http://192.168.1.45:8000/dealt/?card1={mycards[0]}&card2={mycards[1]}&numvillian={int(numvillians.get())}&varience=0.5&&folded={int(1)}&won={int(0)}"
        response = requests.get(myURL)
        biganswer = response.json()
        answer=f"Big Equity of hand = {biganswer}\n"                           
        ai_comment.config(text=answer)
        return

def donothing():
        return

def resize_cards(card):
        # Open the image
        our_card_img = Image.open(card)

        # Resize The Image
        our_card_resize_image = our_card_img.resize((150, 218))
        
        # output the card
        global our_card_image
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)

        # Return that card
        return our_card_image

root = Tk()
root.title('Codemy.com - Card Deck')
root.geometry("1280x900")
root.configure(background="green")


# Put cards in frames
# Create Frames For Cards
dealer_cards_frame = LabelFrame(root, text="Dealer")
dealer_cards_frame.grid(row=0, column=0, padx=20, ipadx=20)

dealer_card1 = Label(dealer_cards_frame, text="Card 1")
dealer_card2 = Label(dealer_cards_frame, text="Card 2")
dealer_card3 = Label(dealer_cards_frame, text="Card 3")
dealer_card4 = Label(dealer_cards_frame, text="Card 4")
dealer_card5 = Label(dealer_cards_frame, text="Card 5")

dealer_card1.grid(row=0,column=0,padx=10,pady=10)
dealer_card2.grid(row=0,column=1,padx=10,pady=10)
dealer_card3.grid(row=0,column=2,padx=10,pady=10)
dealer_card4.grid(row=0,column=3,padx=10,pady=10)
dealer_card5.grid(row=0,column=4,padx=10,pady=10)

dealer_image = resize_cards(f'images/cards/default.png')
dealer_card1.config(image=dealer_image)
dealer_card2.config(image=dealer_image)
dealer_card3.config(image=dealer_image)
dealer_card4.config(image=dealer_image)
dealer_card5.config(image=dealer_image)


player_cards_frame = LabelFrame(root, text="Player")
player_cards_frame.grid(row=1, column=0, padx=20, ipadx=20)

player_card1 = Label(player_cards_frame, text="Card 1")
player_card2 = Label(player_cards_frame, text="Card 2")

player_card1.grid(row=0,column=0,padx=10,pady=10)
player_card2.grid(row=0,column=1,padx=10,pady=10)

player_card1.config(image=dealer_image)
player_card2.config(image=dealer_image)

board_info_frame = LabelFrame(root, text="Board Info")
board_info_frame.grid(row=2,column=0, padx=20, ipadx=20)

numvillians = StringVar()
betsize = StringVar()
num_players_label = Label(board_info_frame, text = "# Villians", font = ('calibre',10,'bold'))
num_players_label.grid(row=0,column=0)
num_players_entry = Entry(board_info_frame, width=7, textvariable=numvillians)
num_players_entry.grid(row=0,column=1)
bet_size_label = Label(board_info_frame, text = "Bet Size", font = ('calibre',10,'bold'))
bet_size_label.grid(row=0,column=2)
bet_size_entry = Entry(board_info_frame, width=7, textvariable=betsize)
bet_size_entry.grid(row=0,column=3)
actionbuttoncheck = IntVar()
wonlostbuttoncheck = IntVar()
actionbutton = Checkbutton(board_info_frame, text = "Folded", 
                    variable = actionbuttoncheck, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10) 
actionbutton.grid(row=0,column=4)
wonlostbutton = Checkbutton(board_info_frame, text = "Won", 
                    variable = wonlostbuttoncheck, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2, 
                    width = 10) 
wonlostbutton.grid(row=0,column=5)


button_frame = LabelFrame(root, text="Buttons")
button_frame.grid(row=3,column=0, padx=20, ipadx=20)

shuffle_button = Button(button_frame, text="New hand", font=("Helvetica", 14), command=playerscards)
shuffle_button.grid(row=0, column=0)

card_button = Button(button_frame, text="Flop Came", font=("Helvetica", 14), command=dealerFlop)
card_button.grid(row=0,column=1)

turncard_button = Button(button_frame, text="Turn Came", font=("Helvetica", 14), command=dealer_turn)
turncard_button.grid(row=0,column=2)

rivercard_button = Button(button_frame, text="River Came", font=("Helvetica", 14), command=dealer_river)
rivercard_button.grid(row=0,column=3)

folded_button = Button(button_frame, text="Post Folded", font=("Helvetica", 14), command=post_folded)
folded_button.grid(row=0,column=4)

won_button = Button(button_frame, text="Post Win", font=("Helvetica", 14), command=post_win)
won_button.grid(row=0,column=5)

comments_frame = LabelFrame(root, text="Comments on Hand")
comments_frame.grid(row=4,column=0, padx=20, ipadx=20)

ai_comment = Label(comments_frame, text="Waiting On Hand..." , font=("Helvetica", 18) )
ai_comment.grid(row=0,column=0)

root.bind("<Return>")

root.mainloop()