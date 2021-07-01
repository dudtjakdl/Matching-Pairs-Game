import sqlite3
from tkinter import *
from tkinter import messagebox
from game import *

class Login:
    def __init__(self, parent):
        self.Parent = parent
        
        self.login = Frame(parent)
        self.login.pack()
        
        Label(self.login, text="아이디", width=15).grid(row=0, column=0)
        self.user_id = Entry(self.login, width=25)
        Label(self.login, text="비밀번호", width=15).grid(row=1, column=0)
        self.user_pw = Entry(self.login, width=25, show="●")
        Button(self.login, text="회원가입", width=20, command=self.signIn).grid(row = 2, column=0)
        Button(self.login, text="로그인", width=20, command=self.loginCheck).grid(row = 2, column=1)

        self.user_id.grid(row=0, column=1)
        self.user_pw.grid(row=1, column=1)
        
    def signIn(self):
        self.signin = Toplevel(self.Parent)
        self.signin.title("회원가입")
    
        Label(self.signin, text="아이디(10자 이내)").grid(row= 0, column= 0)
        Label(self.signin, text="비밀번호(10자 이내)").grid(row= 1, column= 0)
        Label(self.signin, text="비밀번호확인").grid(row= 2, column= 0)
        Label(self.signin, text="닉네임(10자 이내)").grid(row= 3, column= 0)
    
        self.signin_id = Entry(self.signin, width=20)
        self.signin_password = Entry(self.signin, width=20, show="●")
        self.signin_password_check = Entry(self.signin, width=20, show="●")
        self.signin_nickname = Entry(self.signin, width=20)
    
        self.signin_id.grid(row= 0, column= 1)
        self.signin_password.grid(row= 1, column= 1)
        self.signin_password_check.grid(row= 2, column= 1)
        self.signin_nickname.grid(row= 3, column= 1)
    
        Button(self.signin, width = 20, text = "확인", command = self.signIn_button).grid(row = 4, column=1)

        self.signin.mainloop()
        
    def loginCheck(self):
        con, cur = None, None
        con = sqlite3.connect("gameDB")
        cur = con.cursor()
    
        cur.execute("SELECT * FROM userTable")
    
        ID = self.user_id.get()
        password = self.user_pw.get()
    
        while(True):
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("error","존재하지 않는 아이디입니다.")
                return
            elif row[0] == ID:
                if row[1] == password:
                    messagebox.showinfo("로그인 성공",row[2]+"님 환영합니다.")
                    self.user = row[2]
                    break
                else:
                    messagebox.showerror("error","비밀번호가 틀렸습니다.")
                    return
            else:
                continue
        
        self.login.destroy()
        game = Game(self.user,self.Parent)
        
    def signIn_button(self):
    
        con, cur = None, None
        con = sqlite3.connect("gameDB")
        cur = con.cursor()
    
        cur.execute("SELECT * FROM userTable")
    
        id_list = []
        nickname_list = []
    
        while(True):
            row = cur.fetchone()
            if row == None:
                break
            id_list.append(row[0])
            nickname_list.append(row[2])

        message = ""
    
        ID = self.signin_id.get()
        password = self.signin_password.get()
        nickname = self.signin_nickname.get()
    
        if ID in id_list:
            message += "이미 사용하고 있는 아이디입니다.\n"
    
        if password != self.signin_password_check.get():
            message += "비밀번호가 맞지 않습니다.\n"
        
        if nickname in nickname_list:
            message += "이미 사용하고 있는 닉네임입니다.\n"
    
        if message == "":
            params = (ID, password, nickname)
            #sql = "INSERT INTO userTable VALUES('"+ID+"','"+password+"',"+nickname+")"
            cur.execute("INSERT INTO userTable VALUES (?, ?, ?)", params)
            #cur.execute(sql)
            con.commit()
            con.close()
            messagebox.showinfo("가입 완료","회원가입이 완료되었습니다.")
            self.signin.destroy()
        else:
            messagebox.showerror("error",message)