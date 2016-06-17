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
        self.Pyramid = Pyramid(Deck(), root, self.difficulty)
        self.animate()
        # self.Pyramid.draw(root)
        self.Pyramid.print_py()
        # self.Pyramid.py[6][6]
        # self.Pyramid.joker(root,self.difficulty)
        # self.play()

    def animate(self):
        self.canvas.delete(ALL)
        timer = 300 - ((int(time.strftime('%H')) * 3600 + int(time.strftime('%M')) * 60 + int(time.strftime('%S'))) - (self.nowhour * 3600 + self.nowminate * 60 + self.nowsecond))
        self.canvas.create_text(28, 25,text=timer,fill="White")
        self.canvas.after(10, self.animate)

    def play(self):
        pass

def main():
    root = Tk()
    root.title("Pyramid Solitaire")
    root.geometry("650x650")
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
                cards.append(Card(ImageTk.PhotoImage(Image.open(v+s+".gif")), v))
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
        frame.pack(pady=250)

    @staticmethod
    def ox_widgets(root):
        frame = Frame(root)
        Label(frame, text="Play more?").grid(row=0,column=0)
        if Button(frame, text="Yes").grid(row=2, column=0, sticky=W):
            return True
        Button(frame, command = quit, text="No").grid(row=2, column=1, sticky=E)
        frame.pack(pady=250)

    @staticmethod
    def closed(root, frame, num):
        frame.pack_forget()
        PyramidController(num, root)

class Drawpile:
    """docstring for Drawpile"""
    def __init__(self, pile, root):
        self.k = ImageTk.PhotoImage(Image.open("back192.gif"))
        self.doh_pic = ImageTk.PhotoImage(Image.open("doh_pic.gif"))
        self.pile = pile



    def doh(self,root) :
        if self.py[7] != [] :
            self.py[7][0]["state"] = DISABLED
        self.py[7].insert(0,Checkbutton(self.root, text = -100, image = self.doh_pic, command = lambda: self._sum(7,0) ,selectimage=self.b))
        self.py[7][0].deselect()
        self.py[7][0].place(x =250 , y =500)

    @property
    def get(self):
        if self.pile != []:
            return self.pile.pop() 
        else :
            self.d.destroy()

class Pyramid(Drawpile):
    """docstring for Pyramid"""
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
        self.joker(self.root)
        # self.j.place(x =420, y=500)
        
        
        self.d = Button(self.root, command = lambda: self.open_drawing(), image=self.b)
        self.d.image = self.b
        self.d.place(x =140, y=500)

        self.newpy()

    def count_joker(self):
        self.count-=1
        self.joker(self.root)
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

    
    def _sum(self, i, j):
        self.cod.append((i,j))
        if self.total != 0:
            self.total += int(self.py[i][j]["text"])
            # print(self.total)
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
        ll[i][j]["command"] = lambda: self._sum(i,j) #ll[i][j]["text"] #self.isselect(i,j)


    def open_drawing(self):
        tmp = self.get
        if tmp != None:
            if self.py[7] != [] :
                self.py[7][0]["state"] = DISABLED
            self.py[7].insert(0,Checkbutton(self.root, text = tmp.value, image=tmp.cardImage, command = lambda: self._sum(7,0) ,selectimage=self.b))
            self.py[7][0].image = tmp.cardImage
            self.py[7][0].deselect()
            self.py[7][0].place(x =250 , y =500)
    


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
        self.draw()


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

    #수정필요
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
        # self.d.destroy()
        if self.pile != []:
            self.d.place(x =140, y=500)

    def joker(self,root):
        if self.count <= 0:
            self.j.destroy()
        else:
            self.j.place(x =420, y=500)

    def isfail(self,difficulty):
        py_card = self.py
        open_card_list = [self.drawpile[-1]]
        check_list = []
        if difficulty == 0 :
            if len(self.pile) == 1:
                for i in py_card :
                    for j in i :
                        if j["state"] == normal :
                            open_card_list.append(j)
                for i in open_card_list :
                    if i["text"] == 13 :
                        return False
                    for j in open_card_list :
                        check_list.append(i["text"] + j["text"])
                if 13 in check_list :
                    return False
                else :
                    return True
            else:
                return False


main()
