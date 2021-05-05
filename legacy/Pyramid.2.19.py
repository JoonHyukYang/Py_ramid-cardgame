import random
import datetime
import time
import sys
from tkinter import *
from PIL import Image, ImageTk

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
                cards.append(Card(ImageTk.PhotoImage(Image.open(v+s+".gif")), v))
        random.shuffle(cards)
        return cards

class Deck:
    def __init__(self):
        self.__deck = Card.fresh_deck()

    @property
    def deck(self):
        return self.__deck

class Drawpile:
    def __init__(self, pile, root):
        self.k = ImageTk.PhotoImage(Image.open("back192.gif"))
        self.doh_pic = ImageTk.PhotoImage(Image.open("doh_pic.gif"))
        self.pile = pile

    def doh(self,root) :
        if self.py[7] != [] :
            self.py[7][0]["state"] = DISABLED
        self.py[7].insert(0,Checkbutton(self.root, text = -100, \
            image = self.doh_pic, command = lambda: self._sum(7,0) ,selectimage=self.b))
        self.py[7][0].deselect()
        self.py[7][0].place(x =250 , y =500)

    @property
    def get(self):
        if self.pile != []:
            return self.pile.pop() 
        else :
            self.d.destroy()

class Pyramid(Drawpile):
    def __init__(self, deck, root, difficulty):
        self.count = difficulty
        self.root = root
        super().__init__(deck.deck, root)
        self.b = ImageTk.PhotoImage(Image.open("back192.gif"))
        self.total = 0
        self.cod = []
        self.__py = []
        
        self.j = Button(root, command=self.count_joker, image=self.b)
        self.j.image = self.b
        self.joker()
        
        self.d = Button(self.root, command = lambda: self.open_drawing(), image=self.b)
        self.d.image = self.b
        self.d.place(x =140, y=500)
        self.newpy()

    def count_joker(self):
        self.count-=1
        self.joker()
        return self.doh(self.root)

    def newpy(self):
        self.__py = []
        for i in range(7):
            self.__py.append([])
            for j in range(i+1):
                p = self.get
                if i != 6:
                    self.__py[i].append(Checkbutton(self.root, text = p.value, image=p.cardImage, 
                        selectimage=self.b))
                    self.nn(self.__py,i,j)
                    self.__py[i][j]["state"] = DISABLED
                    self.__py[i][j].select()
                else:
                    self.__py[i].append(Checkbutton(self.root, text = p.value, image=p.cardImage, 
                        selectimage=self.b))
                    self.nn(self.__py,i,j)
                    self.__py[i][j].deselect()
                self.__py[i][j].image = p.cardImage
                self.__py[i][j].selectimage = self.b
        self.__py.append([])
        self.open_drawing()
    
    def _sum(self, i, j):
        self.cod.append((i,j))
        if self.total != 0:
            self.total += int(self.py[i][j]["text"])
            if self.total == 13 or self.total < 0:
                self.total = 0
                for x in self.cod:
                    self.remove(x[0],x[1])
                self.cod = []
            else:
                self.total = 0
                for x in self.cod:
                    self.__py[x[0]][x[1]].deselect()  
                self.cod = []
        else:
            self.total += int(self.py[i][j]["text"])
            if self.total == 13:
                self.total = 0
                for x in self.cod:
                    self.remove(x[0],x[1])
                self.cod = []         

    def nn(self, ll, i,j):
        ll[i][j]["command"] = lambda: self._sum(i,j)

    def open_drawing(self):
        tmp = self.get
        if tmp != None:
            self.py[7].insert(0,Checkbutton(self.root, text = tmp.value, \
                image=tmp.cardImage, command = lambda: self._sum(7,0) ,selectimage=self.b))
            self.py[7][0].image = tmp.cardImage
            self.py[7][0].deselect()
            self.py[7][0].place(x =250 , y =500)
        self.draw()
    
    @property
    def py(self):
        return self.__py

    def open(self):
        for i in range(0,7):
            for j in range(i+1):
                if i != 6  and self.isselect(i, j):
                    self.__py[i][j]["state"] = NORMAL
                    self.__py[i][j].deselect()
        if self.py[7] != []:
            self.__py[7][0]["state"] = NORMAL
                    
    def print_py(self):
        for i in range(7):
            x = (6-i) * 80 / 2
            y = i * 98 / 2
            for j in range(i+1):
                if self.__py[i][j] != None:
                    self.__py[i][j].place(x = x + 80*j + 40, y = 49 + y)
        

    def isselect(self, x, y):
        if 0 <= x <= 7 and 0 <= y <= x and self.py[x][y] != None:
            if x in [6,7]:
                return True
            return self.py[x+1][y] == None and self.py[x+1][y+1] == None
        else:
            return False

    def iscorrect(self, x1, y1, x2, y2):
        if self.__py[x1][y1]["text"] == "0" or self.__py[x2][y2]["text"] == "0":
            return True
        else:
            return int(self.__py[x1][y1]["text"]) + int(self.__py[x2][y2]["text"]) == 13

    # 리팩토링 필요
    def remove(self, x, y):
        self.py[x][y].destroy()
        if x == 7:
            if len(self.py[7]) == 1:
                self.open_drawing()
                self.__py[7] = self.__py[7][:1]
            else:
                self.py[7] = self.__py[7][1:]
        else:
            self.__py[x][y] = None
        self.open()
        self.print_py()

    def draw(self):
        if self.pile != []:
            self.d.place(x =140, y=500)
        Label(text =str(len(self.pile)).center(4),font = ("",15), \
            bg = "Darkgreen", fg = "White").place(x = 100, y = 580)


    def joker(self):
        if self.count <= 0:
            self.j.destroy()
        else:
            self.j.place(x =420, y=500)
        Label(text =str(self.count),font = ("",15), \
            bg = "Darkgreen", fg = "White").place(x = 510, y = 580)

class PyramidController():
    def __init__(self, difficulty, root):
        """
        컨트롤러가 하는일이 없음...... 이것도 리팩토링 대상
        """
        self.root = root
        self.difficulty = difficulty
        self.canvas = Canvas(root, width=100, height=100, bg='DarkGreen', \
            bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid()
        self.nowhour = int(time.strftime('%H'))
        self.nowminate = int(time.strftime('%M'))
        self.nowsecond = int(time.strftime('%S'))
        self.Pyramid = Pyramid(Deck(), root, self.difficulty)
        self.animate()
        self.Pyramid.print_py()

    def animate(self):
        self.canvas.delete(ALL)
        timer = 120 - ((int(time.strftime('%H')) * 3600 + int(time.strftime('%M')) * \
            60 + int(time.strftime('%S'))) - (self.nowhour * 3600 + self.nowminate * 60 + self.nowsecond))
        
        if timer == 0:
            Reader.ox_widgets(self.root)
        else:
            self.canvas.after(10, self.animate)
            if timer > 50:
                self.canvas.create_text(50, 40,text=timer,font = ("",20),fill="White")
            elif timer > 10:
                self.canvas.create_text(50, 40,text=timer,font = ("",20),fill="Yellow")
            else:
                self.canvas.create_text(50, 40,text=timer,font = ("",20),fill="Red")

class Reader:
    @staticmethod
    def difficulty_widgets(root):
        frame = Frame(root)
        Label(frame, text ='난이도',font = ("",15)).grid(row=0,column=1,pady=6, sticky=S)
        difficulty = IntVar()
        b1=Radiobutton(frame, text=' 쉬움',
            variable = difficulty, value = 2).grid(row = 1, column = 0, padx = 10, pady = 3)
        b3=Radiobutton(frame, text='어려움',
            variable = difficulty, value = 0).grid(row = 1, column = 2, padx = 10)
        b2=Radiobutton(frame, text=' 보통',
            variable = difficulty, value = 1).grid(row = 1, column = 1, padx = 10)
        Button(frame, text="게임 시작",command = lambda : Reader.closed(root, frame, difficulty.get())
            ).grid(row=2, column=1, pady=3)
        frame.pack(pady=270)

    @staticmethod
    def ox_widgets(root):
        frame = Frame(root)
        Label(frame, text="GAME OVER").grid(row=0,column=1,padx=50,pady=3)
        Button(frame, command = quit, text="OK!").grid(row=1, column=1,padx=10,pady=3)
        frame.pack(pady=280)

    @staticmethod
    def closed(root, frame, num):
        frame.pack_forget()
        PyramidController(num, root)

def main():
    root = Tk()
    root.title("Pyramid Solitaire")
    root.geometry("650x650")
    root.configure(bg='darkgreen')
    Reader.difficulty_widgets(root)
    root.mainloop()

main()
