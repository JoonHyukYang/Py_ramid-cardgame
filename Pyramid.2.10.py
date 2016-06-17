import random
import datetime
import time
from tkinter import *
from PIL import Image, ImageTk

class PyramidController():
    def __init__(self, difficulty, root):
        self.difficulty = difficulty
        self.canvas = Canvas(root, width=50, height=50, bg='DarkGreen', bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid()
        self.nowhour = int(time.strftime('%H'))
        self.nowminate = int(time.strftime('%M'))
        self.nowsecond = int(time.strftime('%S'))
        self.Pyramid = Pyramid(Deck(), root)
        self.Pyramid.joker(root)
        self.Pyramid.draw(root)
        self.Pyramid.print_py()

    def animate(self):
        self.canvas.delete(ALL)
        timer = 300 - ((int(time.strftime('%H')) * 3600 + int(time.strftime('%M')) * 60 + int(time.strftime('%S'))) - (self.nowhour * 3600 + self.nowminate * 60 + self.nowsecond))
        self.canvas.create_text(28, 25,text=timer,fill="White")
        self.canvas.after(10, self.animate)

    def play(self):
        Pyramid = self.Pyramid
        difficulty = self.difficulty
        score = 0
        now = datetime.datetime.now()
        nowhour = int(now.strftime('%H'))
        nowminate = int(now.strftime('%M'))
        nowsecond = int(now.strftime('%S'))
        while True: 
            # now = datetime.datetime.now()
            # time = 300 - ((int(now.strftime('%H')) * 3600 + int(now.strftime('%M')) * 60 + int(now.strftime('%S'))) - (nowhour * 3600 + nowminate * 60 + nowsecond))
            Pyramid.open()
            Pyramid.print_py()
            # if time < 0:
            #     print("Game Over")
            #     print("Your score is",score)
            #     break
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
    Reader.difficulty_widgets(root)
    root.mainloop()
    

class Card:

    __values = ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13")
    __suits = ("c", "s", "d", "h")

    def __init__(self, cardImage, value):
        self.__value = value
        self.__cardImage = cardImage

    @property
    def value(self):
        return self.__value

    @property
    def cardImage(self):
        return self.__cardImage

    @staticmethod
    def fresh_deck():
        cards = []
        for v in Card.__values:
            for s in Card.__suits:
                cards.append(Card(v+s+".gif", v))
        random.shuffle(cards)
        return cards

class Deck:
    """defines Deck class"""
    def __init__(self):
        """creates a deck object consisting of 52 shuffled cards 
        with all face down"""
        self.__deck = Card.fresh_deck()

    # def next(self):
    #     card = self.__deck.pop()
    #     return card

    @property
    def deck(self):
        return self.__deck

class Reader:

    @staticmethod
    def difficulty_widgets(root):
        frame = Frame(root)
        Label(frame, text ='Difficulty',font = 'Bold').grid(row=0,column=1,pady=5)
        difficulty = IntVar()
        b1=Radiobutton(frame, text='Easy',
            variable = difficulty, value = 2).grid(row = 1, column = 0, padx = 10, pady = 3)
        b2=Radiobutton(frame, text='Normal',
            variable = difficulty, value = 1).grid(row = 1, column = 1, padx = 10)
        b3=Radiobutton(frame, text='Hard',
            variable = difficulty, value = 0).grid(row = 1, column = 2, padx = 10)
        Button(frame, text="Game Start",command = lambda : Reader.closed(root, frame, difficulty.get())
            ).grid(row=2, column=1, sticky=S, pady=3)
        frame.pack(pady=10)

    @staticmethod
    def ox_widgets(root):
        frame = Frame(root)
        Label(frame, text="Play more?").grid(row=0,column=0)
        if Button(frame, text="Yes").grid(row=2, column=0, sticky=W):
            return True
        Button(frame, command = quit, text="No").grid(row=2, column=1, sticky=E)
        frame.pack(pady=10)

    @staticmethod
    def closed(root, frame, num):
        frame.pack_forget()
        PyramidController(num, root).animate()

class Drawpile:
    """docstring for Drawpile"""
    def __init__(self, pile, root):
        self.k = ImageTk.PhotoImage(Image.open("back192.gif"))
        self.root = root
        self.drawpile = []
        self.pile = pile

    def open_drawing(self,root):
        tmp = self.get.cardImage
        if self.drawpile != []:
            self.drawpile[-1].state = DISABLED
        self.drawpile.append(Checkbutton(root, image=tmp))
        self.drawpile[-1].image = tmp
        self.drawpile[-1].place(x = 220 , y = 400 )

    def doh(self,root) :
        d = Button(root, image = self.doh_pic).place(x = 220, y = 400)


    @property
    def get(self):
        return self.pile.pop()



    # @staticmethod
    # def joker():
    #     return Card("Joker", "Joker")

class Pyramid(Drawpile):
    """docstring for Pyramid"""
    def __init__(self, deck, root):
        self.b = ImageTk.PhotoImage(Image.open("back192.gif"))
        self.doh_pic = ImageTk.PhotoImage(Image.open("doh_pic.gif"))
        self.root = root
        super().__init__(deck.deck, root)
        self.__py = []
        self.newpy()

    def newpy(self):
        self.__py = []
        for i in range(7):
            self.__py.append([])
            for j in range(i+1):
                tmp = self.get
                og = Image.open(tmp.cardImage)
                p = ImageTk.PhotoImage(og)
                if i != 6:
                    self.__py[i].append(Checkbutton(self.root,image=p, width="73",
                        height="98", state=DISABLED, selectimage=self.b, command = lambda: print(tmp.value)))
                else:
                    self.__py[i].append(Checkbutton(self.root,image=p, width="73", 
                        height="98", selectimage=self.b, command = lambda: print(tmp.value)))
                self.__py[i][-1].image = p
                self.__py[i][-1].selectimage = self.b

    @property
    def py(self):
        return self.__py

    def open(self):
        for i in range(0,7):
            for j in range(i+1):
                if i != 6  and self.isselect(i, j):
                    self.py[i][j].state = ACTIVE
                    
    def print_py(self):
        for i in range(7):
            x = (6-i) * 80 / 2
            y = i * 98 / 2
            for j in range(i+1):
                if self.__py[i][j] != None:
                    self.__py[i][j].place(x = x + 80*j + 40, y = 49 + y)

    def isselect(self, x, y):
        if 0 <= x <= 7 and 0 <= y <= x and self.py[x][y] != None:
            if x in [6, 7]:
                return True
            return self.py[x+1][y] != None and self.py[x+1][y+1] != None
        else:
            return False

    
    def iscorrect(self, x1, y1, x2, y2):
        if self.__py[x1][y1].value == 0 or self.__py[x2][y2].value == 0:
            return True
        else:
            return self.__py[x1][y1].value + self.__py[x2][y2].value == 13

    #수정필요
    def remove(self, x, y):
        self.__py[x][y] = None

    def draw(self, root):
        if self.pile != []:
            d = Button(root, command=self.open_drawing, image=self.b)
            d.image = self.b
            d.place(x =140 ,y=400)

    def joker(self, root):

        j = Button(root, command=self.doh, image=self.b)
        j.image = self.b
        j.place(x=420, y=400)


    def isfail(self,difficulty):
        py_card = self.py
        open_card_list = [self.drawpile[-1]]
        check_list = []
        if difficulty == 0 :
            if len(self.pile) == 0:
                for i in py_card :
                    for j in i :
                        if j.face_up == True :
                            open_card_list.append(j)
                for i in open_card_list :
                    if i.value == 13 :
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
