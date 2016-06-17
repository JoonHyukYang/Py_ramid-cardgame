import random
import datetime
import time
from tkinter import *

class App():
    def __init__(self,master):
        self.master = master
        self.frame1 = Frame(master)
        # self.difficulty = 0
        Label(self.frame1,text='Difficulty',font='bold').grid(row=0,column=1,pady=5)
        self.difficulty=IntVar()
        self.difficulty.set(None)
        b1=Radiobutton(self.frame1,text='Easy',
            variable=self.difficulty, value=2).grid(row=1, column=0, padx=10, pady=3)
        b2=Radiobutton(self.frame1,text='Normal',
            variable=self.difficulty, value=1).grid(row=1, column=1, padx=10)
        b3=Radiobutton(self.frame1,text='Hard',
            variable=self.difficulty, value=0).grid(row=1, column=2, padx=10)
        Label(self.frame1,text=self.Difficultyty).grid(row=3,column=1,pady=5)
        Button(self.frame1, text="Game Start",command=self.closed).grid(row=2, column=1, sticky=S, pady=3)
        self.frame1.pack(pady=200)
    
    def closed(self):
        self.frame1.pack_forget()
        print(self.difficulty)
        PyramidController(self.difficulty,self.master)

class PyramidController():
    def __init__(self, difficulty,master):
        self.frame1 = Frame(master)
        self.deck = Deck()
        self.Pyramid = Pyramid(self.deck)
        self.difficulty = difficulty
        print(self.difficulty)
        Label(self.frame1,text=self.difficulty).grid(row=0,column=1)
        self.frame1.pack(pady=250)
    
    def tick(time1=''):
        # get the current local time from the PC
        time2 = time.strftime('%H:%M:%S')
        # if time string has changed, update it
        if time2 != time1:
            time1 = time2
            clock.config(text=time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        clock.after(200, tick)

    def play(self):
        Pyramid = self.Pyramid
        difficulty = self.difficulty
        score = 0
        now = datetime.datetime.now()
        nowhour = int(now.strftime('%H'))
        nowminate = int(now.strftime('%M'))
        nowsecond = int(now.strftime('%S'))
        while True: 
            now = datetime.datetime.now()
            time = 300 - ((int(now.strftime('%H')) * 3600 + int(now.strftime('%M')) * 60 + int(now.strftime('%S'))) - (nowhour * 3600 + nowminate * 60 + nowsecond))
            Pyramid.open()
            Pyramid.print_py()
            if time < 0:
                print("Game Over")
                print("Your score is",score)
                break
            while True:
                mod = input("Joker Draw Cod : ")
                if mod == "Joker":
                    if difficulty > 0:
                        difficulty -= 1
                        Pyramid.joker()
                        break
                    else:
                        print("No Joker")
                elif mod == "Draw":
                    Pyramid.draw()
                    break
                elif mod == "Cod":
                    x1, y1 = Reader.get_cod("첫번째 좌표 입력 : ")
                    while not Pyramid.isselect(x1, y1):
                        x1, y1 = Reader.get_cod("첫번째 좌표 입력 : ")
                    if Pyramid.py[x1][y1].value == 13:
                        Pyramid.remove(x1,y1)
                        score += 150
                        break
                    else:
                        x2, y2 = Reader.get_cod("두번째 좌표 입력 : ")
                        while not Pyramid.isselect(x2, y2):
                            x2, y2 = Reader.get_cod("두번째 좌표 입력 : ")
                        if Pyramid.iscorrect(x1,y1,x2,y2):
                            Pyramid.remove(x1,y1)
                            Pyramid.remove(x2,y2)
                            score += 300
                            break
                        else:
                            print("Not 13")
            if Pyramid.isfail(difficulty) == True:
                Pyramid.print_py()
                print("Game Over")
                print("Your score is",score)
                break
            if Pyramid.py[0][0].rank == "":
                print("Clear")
                score += len(Pyramid.pile) * 100 + difficulty * 500 + time * 10
                print("Your score is",score)
                break

def main():
    root = Tk()
    root.title("Pyramid Solitaire")
    root.geometry("987x610")
    root.configure(bg='darkgreen')
    App(root)
    root.mainloop()
    

class Card:
    """defines Card class"""
    __suits = ("", "Joker", "Diamond", "Heart", "Spade", "Clover")
    __ranks = ("", "Joker", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

    def __init__(self, suit, rank, face_up=True):
        """creates a playing card object 
        arguments:
        suit -- must be in Card.__suits
        rank -- must be in Card.__ranks
        face_up -- True or False (defaut True)
        """
        if suit in Card.__suits and rank in Card.__ranks:
            self.__suit = suit
            self.__rank = rank
            self.__face_up = face_up
        else:
            print("Error: Not a valid card")
        self.__value = Card.__ranks.index(self.__rank) - 1

    def __str__(self):
        """returns its string representation"""
        if self.__face_up:
            return self.__suit + "." + self.__rank
        else:
            return "xxxxx" + "." + "xx"

    @property
    def suit(self):
        """its suit value in Card.__suits"""
        return self.__suit

    @property
    def rank(self):
        """its rank value in Card.__ranks"""
        return self.__rank

    @property
    def face_up(self):
        """its face_up value : True or False"""
        return self.__face_up

    @property
    def value(self):
        """its face value according to blackjack rule"""
        return self.__value

    def flip(self):
        """flips itself"""
        self.__face_up = not self.__face_up

    @staticmethod
    def fresh_deck():
        """returns a brand-new deck of shuffled cards with all face down"""
        cards = []
        for s in Card.__suits[2:]:
            for r in Card.__ranks[2:]:
                cards.append(Card(s,r))
        random.shuffle(cards)
        return cards

class Deck:
    """defines Deck class"""
    def __init__(self):
        """creates a deck object consisting of 52 shuffled cards 
        with all face down"""
        self.__deck = Card.fresh_deck()

    def next(self, open=True):
        """removes a card from deck and returns the card
        with its face up if open == True, or 
        with its face down if open == False
        """
        card = self.__deck.pop()
        if open :
            card.flip()
        return card

    @property
    def deck(self):
        return self.__deck

class Reader:
    @staticmethod
    def ox(message):
        """returns True if player inputs 'o' or 'O',
                   False if player inputs 'x' or 'X'"""
        response = input(message).lower()
        while not (response == 'o' or response == 'x'):
            response = input(message).lower()
        return response == 'o'

    @staticmethod
    def difficulty(message):
        response = input(message)
        while not (response.isdigit() or (response in ["1", "2", "3"])):
            response = input(message)
        if response == "4":
            return 100000
        return 3 - int(response)

    @staticmethod
    def get_cod(message):
        x, comma, y = input(message).partition(",")
        while comma == "" or not x.isdigit() or not y.isdigit():
            response = input(message)
            x, comma, y = response.partition(",")
        return (int(x), int(y))

class Drawpile:
    """docstring for Drawpile"""
    def __init__(self, pile):
        self.pile = pile

    def get(self):
        a = self.pile.pop()
        a.flip()
        return a

    # @staticmethod
    # def joker():
    #     return Card("Joker", "Joker")

class Pyramid(Drawpile):
    """docstring for Pyramid"""
    def __init__(self, deck):
        super().__init__(deck.deck)
        self.__py = self.newpy()

    def newpy(self):
        tmp_py = []
        for i in range(0, 7):
            tmp_py.append([])
            for j in range(i+1):
                tmp_py[i].append(self.get())
        tmp_py.append([self.get()])
        tmp_py[7][0].flip()
        return tmp_py

    @property
    def py(self):
        return self.__py

    def open(self):
        for i in range(0,7):
            for j in range(i+1):
                if i != 6 and not self.py[i][j].face_up and self.isselect(i, j):
                    self.py[i][j].flip()
                elif i == 6 and not self.py[i][j].face_up:
                    self.py[i][j].flip()
        if not self.py[7][0].face_up:
            self.py[7][0].flip()
                    
    def print_py(self):
        k = 1
        for i in range(0, 7):
            print(end = "     "*(7-k))
            for j in range(i+1):
                print(str(self.__py[i][j]).center(10), end = " ")
            print()
            k += 1
        print(self.__py[7][0], len(self.pile))

    def isselect(self, x, y):
        if 0 <= x <= 7 and 0 <= y <= x and self.py[x][y].rank != "":
            if x in [6, 7]:
                return True
            return self.__py[x+1][y].rank == "" and self.__py[x+1][y+1].rank == ""
        else:
            return False

    
    def iscorrect(self, x1, y1, x2, y2):
        if self.__py[x1][y1].value == 0 or self.__py[x2][y2].value == 0:
            return True
        else:
            return self.__py[x1][y1].value + self.__py[x2][y2].value == 13

    def remove(self, x, y):
        if x == 7:
            if len(self.py[7]) == 1:
                self.draw()
                self.__py[7] = self.__py[7][:1]
            else:
                self.py[7] = self.__py[7][1:]
        else:
            self.__py[x][y] = Card("", "", True)

    def draw(self):
        if self.pile != []:
            self.__py[7].insert(0, self.get())
        else:
            print("카드가 없습니다.")

    def joker(self):
        self.__py[7].insert(0, Card("Joker", "Joker", True))


    def isfail(self,difficulty):
        py_card = self.py
        open_card_list = [self.py[7][0]]
        check_list = []
        if difficulty == 0 :
            if len(self.pile) == 0:
                for i in py_card[:7] :
                    for j in i :
                        if j.face_up == True :
                            open_card_list.append(j)
                for i in open_card_list :
                    if i.value in [13, 0] :
                        return False
                    for j in open_card_list :
                        check_list.append(i.value + j.value)
                if 13 in check_list :
                    return False
                else :
                    return True
            else:
                return False


main()
