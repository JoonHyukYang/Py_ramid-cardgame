class Pyramid():
    """docstring for Pyramid"""
    def __init__(self):
        self.py_card = Deck()
        self.__py = newpy()
        # for i in range(0, 7):
        #     self.__py.append([])
        #     for j in range(i+1):
        #         self.__py[i].append(self.py_card.next())
        # self.__py.append([self.py_card.next(False)])
        # print(len(self.py_card.deck))

    def newpy(self):
        tmp_py = []
        for i in range(0, 7):
            tmp_py.append([])
            for j in range(i+1):
                tmp_py[i].append(self.py_card.next())
        tmp_py.append([self.py_card.next(False)])
        print(len(self.py_card.deck))
        return tmp_py

    @property
    def py(self):
        return self.__py

    def open(self):
        for i in range(0,7):
            for j in range(i+1):
                if i == 6 and self.__py[i][j] != "" and not self.__py[i][j].face_up:
                    self.__py[i][j].flip()
                elif self.__py[i][j] != "" and i != 6 and j != 6 and \
                     self.__py[i+1][j] == "" and \
                     self.__py[i+1][j+1] == "" and \
                     not self.__py[i][j].face_up and \
                     self.__py[i][j] != "":
                    self.__py[i][j].flip()

    def print_py(self):
        k = 1
        for i in range(0, 7):
            print(end = "     "*(7-k))
            for j in range(i+1):
                print(str(self.__py[i][j]).center(10), end = " ")
            print()
            k += 1
        print(self.__py[7][0])

    def isselect(self, x, y):
        if x != 6:
            return self.__py[x+1][y].face_up and self.__py[x+1][y+1].face_up
        else:
            return True
    
    def iscorrect(self, x1, y1, x2, y2):
        if self.__py[x1][y1].value == 0 or self.__py[x2][y2].value == 0:
            return True
        else:
            return self.__py[x1][y1].value + self.__py[x2][y2].value == 13

    def remove(self, x, y):
        if x == 7:
            self.__py[x] = self.__py[x][1:]
        else:
            self.__py[x][y] = ""

    def draw(self):
        self.__py[7].insert(0, self.py_card.next(False))

    def isfail(self):
        py_card = self.py
        open_card_list = [self.py[7][0]]
        print("")
        for i in py_card :
            if i == True :
                open_card_list.append(i)
        for i in open_card_list :
            if i.value == 13 :
                return False
        for i in range(len(open_card_list)):
            for j in range(i+1,len(open_card_list)):
                if open_card_list[i].value + open_card_list[j].value == 13:
                    return False
