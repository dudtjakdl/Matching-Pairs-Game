from tkinter import *
import login

if __name__ == '__main__':
    root = Tk()
    root.title('짝 맞추기 게임')
    
    login = login.Login(root)
    root.mainloop()