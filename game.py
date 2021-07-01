from tkinter import *
from tkinter import messagebox
import random
import time
import threading
import tkinter.font
import ranking

class Card:
    def __init__(self, back, front, parent): #parent는 카드 놓는 frame
            self.Parent = parent
            
            self.back_image = PhotoImage(file = back)
            self.front_image = PhotoImage(file = front)
            self.label = Label(parent, image = self.back_image)
            self.label.image = self.back_image
            
            self.pair = ''
            self.front = False
            
    def turn_front(self):
        self.label.configure(image = self.front_image)
        self.front = True

    def turn_back(self):
        self.label.configure(image = self.back_image)
        self.front = False

class Game:
    def __init__(self, user, parent):
        self.Parent = parent
        self.user = user
        
        self.level_select()
        
    def level_select(self):
        self.level_frame = Frame(self.Parent)
        self.level_frame.pack()
        
        font=tkinter.font.Font(family="맑은 고딕", size=15)
        
        Label(self.level_frame,text = "<게임 난이도를 선택하세요>", font = font).pack()
        self.var = IntVar()
        
        font=tkinter.font.Font(family="맑은 고딕", size=10)
        
        level_rb1 = Radiobutton(self.level_frame, text = "level 1 : 카드그림 쉬움", font = font, variable = self.var, value = 1)
        level_rb2 = Radiobutton(self.level_frame, text = "level 2 : 카드그림 중간", font = font, variable = self.var, value = 2)
        level_rb3 = Radiobutton(self.level_frame, text = "level 3 : 카드그림 어려움", font = font, variable = self.var, value = 3)
        level_rb1.pack(); level_rb2.pack(); level_rb3.pack(); 
        
        Button(self.level_frame, text = "확인", width = 15, command = self.place).pack()
        
    def place(self):
        self.level = self.var.get()
        
        if self.level == 0: #난이도를 선택하지 않았을때 에러창 띄움
            messagebox.showerror("error","난이도를 선택해주세요.")
            return
        elif self.level == 1:
            self.score = 30
            self.time = 60
        elif self.level == 2:
            self.score = 40
            self.time = 80
        else:
            self.score = 50
            self.time = 100
        
        self.level_frame.destroy()
        self.card_frame = Frame(self.Parent)
        self.card_frame.pack(side=LEFT)
        
        self.create_card(self.level)
        
        self.sub_frame = Frame(self.Parent)
        self.sub_frame.pack(side=RIGHT)
        
        font=tkinter.font.Font(family="맑은 고딕", size=15)
        
        self.label_score = Label(self.sub_frame, text = "점수: " + str(self.score), font = font)
        self.label_time = Label(self.sub_frame, text = "시간: " + str(self.time), font = font)
        
        self.label_score.pack(); self.label_time.pack()
        
        self.start_button = Button(self.sub_frame, text = "게임시작", width = 15, command = self.game_start)
        self.start_button.pack(padx = 10, pady = 10)

    def timer(self):
        
        self.time_record = 0 # 걸린시간 0초로 초기화
        
        while(True):
            time.sleep(1)
            self.time -= 1
            self.time_record += 1
            self.label_time.configure(text = "시간: " + str(self.time))

            if self.time == 0 or self.score <= 0: # 시간이 0이 됐거나 점수가 0이하일때 게임 오버
                self.text_label.configure(text = "Game Over!!")
                Button(self.sub_frame, text = "다시하기", command = self.regame).pack(padx = 10, pady = 10)
                Button(self.sub_frame, text = "레벨선택", command = self.reselect).pack(padx = 10, pady = 10)
                Button(self.sub_frame, text = "끝내기", command = self.quit).pack(padx = 10, pady = 10)
                self.Parent.focus_set()
                return
            elif self.correct_pair == 10: # 10개의 모든 카드 쌍을 뒤집으면 시간 멈추기
                return
            elif self.time <= 10:
                self.label_time.configure(fg = 'red')
            elif self.score <= 10:
                self.label_score.configure(fg = 'red')
            elif self.score > 10:
                self.label_score.configure(fg = 'black')
    
                
    def game_start(self):
        t = threading.Thread(target = self.initial_open) # 카드 처음에 3초 뒤집기
        t.start()
        
    def game_playing(self):
        self.card_index = 0
        self.turn_over = [] # 카드를 뒤집었을때 뒤집은 카드 리스트에 추가 (2개가 채워지면 서로 맞는지 비교)
        self.correct_pair = 0 #지금까지 맞춘 카드 쌍 총 갯수 (10이면 모든 쌍 다 맞추고 게임 종료)
        self.combo = 0
        
        #self.combo_label = Label(self.sub_frame, text = "Combo " + str(self.combo)) 
        self.card_list[self.card_index].label.configure(bg = 'black')
        
        self.card_frame.focus_set() # 카드 프레임으로 포커스 고정
        self.card_frame.bind("<a>", self.push_A)
        self.card_frame.bind("<d>", self.push_D)
        self.card_frame.bind("<w>", self.push_W)
        self.card_frame.bind("<s>", self.push_S)
        self.card_frame.bind("<space>", self.push_space)
        
    def game_end(self):
        self.Parent.focus_set()
        self.record = self.score + self.time
        
        Button(self.sub_frame, text = "다시하기", command = self.regame).pack(padx = 10, pady = 10)
        Button(self.sub_frame, text = "레벨선택", command = self.reselect).pack(padx = 10, pady = 10)
        Button(self.sub_frame, text = "끝내기", command = self.quit).pack(padx = 10, pady = 10)
        
        rank = ranking.Ranking(self.user, self.record, self.level, self.time_record, self.Parent)
    
    def push_A(self,event):

        if self.card_index in [0, 5, 10, 15]:
            return
        else:
            self.card_list[self.card_index].label.configure(bg = 'SystemButtonFace')
            self.card_index -= 1
            self.card_list[self.card_index].label.configure(bg = 'black')
    
    def push_D(self,event):
        
        if self.card_index in [4, 9, 14, 19]:
            return
        else:
            self.card_list[self.card_index].label.configure(bg = 'SystemButtonFace')
            self.card_index += 1
            self.card_list[self.card_index].label.configure(bg = 'black')
    
    def push_W(self,event):
        
        if self.card_index in [0, 1, 2, 3, 4]:
            return
        else:
            self.card_list[self.card_index].label.configure(bg = 'SystemButtonFace')
            self.card_index -= 5
            self.card_list[self.card_index].label.configure(bg = 'black')
    
    def push_S(self,event):
    
        if self.card_index in [15 ,16, 17, 18, 19]:
            return
        else:
            self.card_list[self.card_index].label.configure(bg = 'SystemButtonFace')
            self.card_index += 5
            self.card_list[self.card_index].label.configure(bg = 'black')
    
    def push_space(self, event):
        
        if self.card_list[self.card_index].front: # 이미 선택한 카드를 또 선택했을 때 아무 액션 없이 바로 함수 종료
            return
        
        self.card_list[self.card_index].turn_front()
        self.turn_over.append(self.card_list[self.card_index])
        
        if len(self.turn_over) == 2:
            self.a = self.turn_over[0]
            self.b = self.turn_over[1]
            
            if self.a.pair == self.b.pair: # 짝을 맞췄을때
                self.turn_over = []
                self.correct_pair += 1
                self.score_up()
            else: # 짝을 틀렸을때
                t1 = threading.Thread(target = self.incorrect_action)
                t1.start()
                self.turn_over = []
                self.score_down()
        if self.correct_pair == 10: # 10개의 모든 카드 쌍을 뒤집으면 게임 종료
            self.text_label.configure(text = "Game End!!")
            self.game_end()
            
                
    def incorrect_action(self): # 선택한 카드가 서로 다를때 뒤집는 함수 (틀렸을때 액션)
        time.sleep(0.7)
        self.a.turn_back()
        self.b.turn_back()
        
    def score_up(self): # 점수를 올리는 함수
        
        if self.level == 1:
            up_score = 5
        elif self.level == 2:
            up_score = 7
        else:
            up_score = 10
        
        self.combo += 1
        self.text_label.configure(text = str(self.combo) + " Combo!!")
            
        self.score += up_score * self.combo
        self.label_score.configure(text = "점수: " + str(self.score))
        
    def score_down(self):

        if self.level == 1:
            down_score = 3
        elif self.level == 2:
            down_score = 5
        else:
            down_score = 8
            
        self.combo = 0
        self.text_label.configure(text = str(self.combo) + " Combo!!")
        
        self.score -= down_score
        self.label_score.configure(text = "점수: " + str(self.score))
        
    def initial_open(self):
        
            self.start_button.destroy()
            
            for i in range(len(self.card_list)):
                self.card_list[i].turn_front()
                
            font=tkinter.font.Font(family="맑은 고딕", size= 15)
                
            self.text_label = Label(self.sub_frame, text = "3", font = font, fg = 'blue')
            self.text_label.pack()
            time.sleep(1)
            self.text_label.configure(text = "2")
            time.sleep(1)
            self.text_label.configure(text = "1")
            time.sleep(1)
            self.text_label.configure(text = "0")
            time.sleep(0.3)
            self.text_label.configure(text = "Game Start!!")
            
            for i in range(len(self.card_list)):
                self.card_list[i].turn_back()
                
            self.t2 = threading.Thread(target = self.timer) # 타이머 함수 실행
            self.t2.start()
            
            self.game_playing()
            
    def create_card(self,level):
        self.card_list = []
        back_name = "images/back.png"
            
        for i in range(1,11):
            front_name = "images/level"+str(level)+ "/" + str(i) + ".png"
            card1 = Card(back_name, front_name, self.card_frame)
            card2 = Card(back_name, front_name, self.card_frame)
            card1.pair = i
            card2.pair = i
            self.card_list.append(card1)
            self.card_list.append(card2)
            
        random.shuffle(self.card_list)
        
        for i in range(4):
            for j in range(5):
                self.card_list[i*5 + j].label.grid(row = i, column = j)

    def regame(self):
        self.card_frame.destroy()
        self.sub_frame.destroy()
        self.place()

    def reselect(self):
        self.card_frame.destroy()
        self.sub_frame.destroy()
        self.level_select()
        
    def quit(self):
        self.Parent.destroy()