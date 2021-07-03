from tkinter import *
from login import *

if __name__ == '__main__':
    root = Tk()
    root.title('짝 맞추기 게임')
    
    login = Login(root)
    root.mainloop()