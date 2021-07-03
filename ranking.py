import sqlite3
from tkinter import *
import tkinter.ttk
from datetime import datetime
from operator import itemgetter
import tkinter.font

class Ranking:
        def __init__(self, user, record, level, time, parent):
            """랭킹보드창 위젯 생성 및 배치"""
            self.Parent = parent
            self.user = user
            
            self.ranking = Toplevel(self.Parent)
            self.result_frame = Frame(self.ranking)
            self.result_frame.pack(side = TOP)
            self.rankboard = Frame(self.ranking);
            self.rankboard.pack(side = BOTTOM)
            
            font=tkinter.font.Font(family="맑은 고딕", size=15)
            
            self.result_label = Label(self.result_frame, text = "최종 점수\n(점수 + 남은시간)\n" + str(record), font = font)
            self.result_label.pack()
            self.new_record(user, record, level)
            
            self.insert_data(user, record, level, time)
            self.load_data()
            self.show_rank(self.date)
            
        def insert_data(self, user, record, level, time):
            """게임 결과 데이터 db에 저장"""
            con, cur = None, None
            
            con = sqlite3.connect("gameDB.db")
            cur = con.cursor()
            
            now = datetime.now()
            self.date = str(now.year) + '/' + str(now.month) + '/' + str(now.day) + ' ' + str(now.hour) + ':' + str(now.minute)
            time = str(time) + '초'
            level = 'level'+ str(level)
            
            params = (user, level, record, time, self.date)
            cur.execute("INSERT INTO gameRecord VALUES (?, ?, ?, ?, ?)", params)
            con.commit()
            con.close()
        
        def load_data(self):
            """db에서 저장되어 있는 게임 기록 불러와서 배열에 저장"""
            con, cur = None, None            
            con = sqlite3.connect("gameDB.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM gameRecord")

            self.data = []

            while(True):
                row = cur.fetchone()
                if row == None:
                    break
                self.data.append([row[0],row[1],row[2],row[3],row[4]])

            con.close()

            #gameRecord(user char(10), level char(6), score int, time char(4), date char(20))
        def new_record(self, user, record, level):
            """게임 기록의 최고점수 달성 여부 검사"""
            self.load_data()
            text = ""
            
            record1 = True
            record2 = True
            record3 = True
            
            for row in self.data:
                if row[0] == user:
                    if row[2] > record:
                        record1 = False
                        break
                
            for row in self.data:
                if row[1] == "level" + str(level):
                    if row[2] > record:
                        record2 = False
                        break
                
            for row in self.data:
                if row[2] > record:
                    record3 = False
                    break
                    
            if record1:
                text += "내 기록에서 최고점수를 갱신했습니다!!\n"
            if record2:
                text += "level" + str(level) + " 에서 최고점수를 달성했습니다!!\n"
            if record3:
                text += "전체에서 최고점수를 달성했습니다!!\n"
                
            font=tkinter.font.Font(family="맑은 고딕", size=10)
                
            self.record_label = Label(self.result_frame, text = text, font = font, fg = 'blue')
            self.record_label.pack()
            
        def show_rank(self, date):
            """랭킹보드창의 notebook 위젯 생성 및 배치"""
            notebook=tkinter.ttk.Notebook(self.rankboard)
            notebook.pack()
            
            self.page1 = Frame(self.rankboard)
            notebook.add(self.page1, text = '전체')
            self.page2 = Frame(self.rankboard)
            notebook.add(self.page2, text = '내 기록')
            
            self.view_frame1 = Frame(self.page1)
            self.view_frame2 = Frame(self.page2)
            self.view_frame1.pack()
            self.view_frame2.pack()
            
            self.button_frame1 = Frame(self.page1)       
            self.button_frame2 = Frame(self.page2)
            self.button_frame1.pack()
            self.button_frame2.pack()
            
            self.page1_pack()
            self.page2_pack()
        
        def page1_pack(self):
            """전체 기록 페이지 세부 조정 (스크롤바, 열 추가 등등)"""
            self.treeview1=tkinter.ttk.Treeview(self.view_frame1, columns=["user", "level", 'score', 'time', 'date'], displaycolumns = ["user", "level", 'score', 'time', 'date'])
            self.treeview1.pack(side = LEFT)
            
            scrollbar1=tkinter.ttk.Scrollbar(self.view_frame1, orient="vertical",command=self.treeview1.yview) 
            scrollbar1.pack(side=RIGHT, fill= 'y')
            self.treeview1.configure(yscrollcommand=scrollbar1.set)

            self.var1 = IntVar()
            self.var2 = IntVar()
            self.var3 = IntVar()
            
            ckb1 = Checkbutton(self.button_frame1, text = 'level1', variable = self.var1, command = self.input_data)
            ckb2 = Checkbutton(self.button_frame1, text = 'level2', variable = self.var2, command = self.input_data)
            ckb3 = Checkbutton(self.button_frame1, text = 'level3', variable = self.var3, command = self.input_data)
            
            ckb1.select()
            ckb2.select()
            ckb3.select()
            
            ckb1.grid(row = 0, column = 0)
            ckb2.grid(row = 0, column = 1)
            ckb3.grid(row = 0, column = 2)
            
            
            #columns=["닉네임", "난이도", '점수', '걸린시간', '날짜']
            self.treeview1.column("#0", width=80, anchor="center")
            self.treeview1.column("#1", width=80, anchor="center")
            self.treeview1.column("#2", width=80, anchor="center")
            self.treeview1.column("#3", width=80, anchor="center")
            self.treeview1.column("#4", width=80, anchor="center")
            self.treeview1.column("#5", width=120, anchor="center")
            self.treeview1.heading("#0", text="순위")
            self.treeview1.heading("#1", text="닉네임")
            self.treeview1.heading("#2", text="난이도")
            self.treeview1.heading("#3", text="점수")
            self.treeview1.heading("#4", text="소요시간")
            self.treeview1.heading("#5", text="날짜")
            
            self.data.sort(key = itemgetter(2), reverse = True)
            
            self.input_data()
                    
        def page2_pack(self):
            """내 기록 페이지 세부 조정 (스크롤바, 열 추가 등등)"""
            self.treeview2=tkinter.ttk.Treeview(self.view_frame2, columns=["user", "level", 'score', 'time', 'date'], displaycolumns = ["user", "level", 'score', 'time', 'date'])
            self.treeview2.pack(side = LEFT)

            scrollbar2=tkinter.ttk.Scrollbar(self.view_frame2, orient="vertical",command=self.treeview2.yview) 
            scrollbar2.pack(side=RIGHT, fill= 'y')
            self.treeview2.configure(yscrollcommand=scrollbar2.set)

            self.var4 = IntVar()
            self.var5 = IntVar()
            self.var6 = IntVar()
            
            myckb1 = Checkbutton(self.button_frame2, text = 'level1', variable = self.var4, command = self.input_mydata)
            myckb2 = Checkbutton(self.button_frame2, text = 'level2', variable = self.var5, command = self.input_mydata)
            myckb3 = Checkbutton(self.button_frame2, text = 'level3', variable = self.var6, command = self.input_mydata)
            
            myckb1.select()
            myckb2.select()
            myckb3.select()
            
            myckb1.grid(row = 0, column = 0)
            myckb2.grid(row = 0, column = 1)
            myckb3.grid(row = 0, column = 2)
            
            #columns=["닉네임", "난이도", '점수', '걸린시간', '날짜']
            self.treeview2.column("#0", width=80, anchor="center")
            self.treeview2.column("#1", width=80, anchor="center")
            self.treeview2.column("#2", width=80, anchor="center")
            self.treeview2.column("#3", width=80, anchor="center")
            self.treeview2.column("#4", width=80, anchor="center")
            self.treeview2.column("#5", width=120, anchor="center")
            self.treeview2.heading("#0", text="순위")
            self.treeview2.heading("#1", text="닉네임")
            self.treeview2.heading("#2", text="난이도")
            self.treeview2.heading("#3", text="점수")
            self.treeview2.heading("#4", text="소요시간")
            self.treeview2.heading("#5", text="날짜")
            
            self.data.sort(key = itemgetter(2), reverse = True)
            self.myData = []
            
            for row in self.data:
                if self.user == row[0]:
                    self.myData.append(row)
            
            self.input_mydata()

        def input_data(self):
            """배열에 저장된 전체 기록 데이터 page1 위젯에 삽입"""
            self.treeview1.delete(*(self.treeview1).get_children())
            check_list = []
            
            if self.var1.get():
                check_list.append("level1")
            if self.var2.get():
                check_list.append("level2")
            if self.var3.get():
                check_list.append("level3")
                
            tmp = []
            
            for row in self.data:
                if row[1] in check_list:
                    tmp.append(row)
                    
            for i in range(len(tmp)):
                if tmp[i][-1] == self.date:
                    self.treeview1.insert('', 'end', text=str(i+1) + '위'+'(new)', values=tmp[i], iid=str(i)+"번")
                else:
                    self.treeview1.insert('', 'end', text=str(i+1) + '위', values=tmp[i], iid=str(i)+"번")
        
        def input_mydata(self):
            """배열에 저장된 내 기록 데이터 page2 위젯에 삽입"""
            self.treeview2.delete(*(self.treeview2).get_children())
            check_list = []
            
            if self.var4.get():
                check_list.append("level1")
            if self.var5.get():
                check_list.append("level2")
            if self.var6.get():
                check_list.append("level3")
            
            tmp = []
            
            for row in self.myData:
                if row[1] in check_list:
                    tmp.append(row)
            
            for i in range(len(tmp)):
                if tmp[i][-1] == self.date:
                    self.treeview2.insert('', 'end', text=str(i+1) + '위'+'(new)', values=tmp[i], iid=str(i)+"번")
                else:
                    self.treeview2.insert('', 'end', text=str(i+1) + '위', values=tmp[i], iid=str(i)+"번")