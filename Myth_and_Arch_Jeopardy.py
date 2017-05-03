from Tkinter import *
from ttk import Treeview
import sqlite3
import tkFont
from PIL import ImageFont, Image, ImageDraw
import random

class JeopardyGame(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Jeopardy!")
        screenX= self.winfo_screenwidth()
        screenY= self.winfo_screenheight()
        TKwidth=590
        TKheight = 460
        TkPosX=(screenX - TKwidth)/2
        TkPosY=(screenY - TKheight)/2
        self.geometry("%sx%s+%s+%s"%(TKwidth,TKheight,TkPosX,TkPosY))
        self.maxsize(width="590", height="460")
        self.minsize(width="590", height="460")
        self.create_widgets()

    def quitgame(self):
        self.destroy()
        sys.exit()

    def create_widgets(self):
        self.container = Frame(self)
        self.container.grid(row=0, column=0, sticky=W+E)

        self.frames={}
        for f in (MainMenu, TopicsPage):
            frame=f(self.container,self)
            frame.grid(row=0, column=0, sticky=NW+SE)
            self.frames[f]=frame
        self.show_frame(MainMenu)

    def show_frame(self, cls):
        self.frames[cls].tkraise()


    def switchFrames(self, currentframe, newframe):
        currentframe.pack_forget()
        self.show_frame(newframe)
        
################################################################################
class BaseFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master, width="590", height="460")
        self.controller=controller
        self.create_widgets()

    def create_widgets(self):
        raise NotImplementedError
################################################################################
class MainMenu(BaseFrame):
    def __init__(self, master, controller):
        Frame.__init__(self, master, width="590", height="460")
        self.controller=controller
        self.create_widgets()
        
    def create_widgets(self):

        self.titleScreen=Label(self, font=("Helvetica", 24, "bold"), fg="blue", width=15, height =1, compound=CENTER)
        self.titleScreen["text"]="This is Jeopardy!"
        self.titleScreen.place(x=200, y=10)

        self.var=StringVar(self)
        self.var.set("Choose a topic")
        
        self.menu= OptionMenu(self, self.var, *AvailableTopics, command = self.TopicChoosen)
        self.menu.config(width=15, height=1)
        self.menu.place(x=222.5, y=60)
        self.menu.after(1500, self.updateDropdown)

        self.add_topic=Button(self, text="Edit/Add topic",command= lambda: self.controller.show_frame(TopicsPage))
        self.add_topic.place(x=240, y=100)

        self.quit = Button(self)
        self.quit["text"] = "Quit"
        self.quit["command"] =  self.controller.quitgame
        self.quit.place(x=535, y=430)

## topic chosen to start the game and go to game frame

    def TopicChoosen(self, Menu_topic):

        Menu_topic = Menu_topic.replace(" ", "_")

        GameScreen_SQL = """SELECT * FROM {TableName}"""
        sql_command= GameScreen_SQL.format(TableName=Menu_topic)
        results = cursor.execute(sql_command)
        
        self.questionanswer=[]
        for row in results:
            self.questionanswer.append(row)

        topicChosen = Menu_topic
        
        if topicChosen != "none":
##            self.controller.show_frame(PlayGame)
            self.PlayGame()

## back to previous frames
            
    def back_to(self):
        self.titleScreen.place(x=200, y=10)
        
        self.var=StringVar(self)
        self.var.set("Choose a topic")
        
        self.menu= OptionMenu(self, self.var, *AvailableTopics, command = self.TopicChoosen)
        self.menu.config(width=15, height=1)
        self.menu.place(x=222.5, y=60)
        self.menu.after(1500, self.updateDropdown)
        
        self.add_topic.place(x=240, y=100)
        self.quit = Button(self)
        self.quit["text"] = "Quit"
        self.quit["command"] =  self.controller.quitgame
        self.quit.place(x=535, y=430)

        self.mainmenu.grid_forget()
        self.quit.place_forget()
        for item in self.buttonList:
            item.grid_forget()
        for item in self.categoryList:
            item.grid_forget()

        try:
            self.selectedquestion.place_forget()
            self.answerSlotLabel.place_forget()
            self.answerSlot.place_forget()
            self.answerSlotButton.place_forget()
            self.mainmenu.place_forget()
        except AttributeError:
            pass

## dropdown menu updated just in case a topic is changed

    def updateDropdown(self):
        results= cursor.execute("SELECT table_name FROM all_tables")
        for row in results:
            for item in row:
                item = item.replace("_", " ")
                if item not in AvailableTopics:
                    AvailableTopics.append(item)
                    
        self.menu= OptionMenu(self, self.var, *AvailableTopics, command = self.TopicChoosen)
        self.menu.config(width=15, height=1)
        self.menu.place(x=222.5, y=60)
##        self.menu.after(2000, self.updateDropdown)

    def PlayGame(self):
        categories=[]
        for item in self.questionanswer:
            if item[1] in categories:
                pass
            else:
                categories.append(item[1])
                
        
        self.titleScreen.place_forget()
        self.menu.destroy()
        self.add_topic.place_forget()
        self.quit.place_forget()

        self.mainmenu=Button(self, width=10, font=("Helvetica", 8))
        self.mainmenu['text']= "Main Menu"
        self.mainmenu["command"] = lambda: self.back_to()
        self.mainmenu.grid(row=0, column=5)

        self.quit = Button(self)
        self.quit["text"] = "Quit"
        self.quit["command"] =  self.controller.quitgame
        self.quit.place(x=535, y=430)

        self.scoreboardDICT={'Team 1':'0','Team 2':'0', 'Team 3':'0', 'Team 4':'0'}

        self.scoreboard=Label(self, width=10,  text= 'Score', font=("Helvetica", 14))
        self.scoreboard.place(x=505, y=100)

        self.scoreteam1=Label(self, width=10,  text= 'Team 1: {Team 1}'.format(**self.scoreboardDICT), font=("Helvetica", 14))
        self.scoreteam1.place(x=503, y=120)
        
        self.scoreteam2=Label(self, width=10,  text= 'Team 2: {Team 2}'.format(**self.scoreboardDICT), font=("Helvetica", 14))
        self.scoreteam2.place(x=503, y=140)
        
        self.scoreteam3=Label(self, width=10,  text= 'Team 3: {Team 3}'.format(**self.scoreboardDICT), font=("Helvetica", 14))
        self.scoreteam3.place(x=503, y=160)
        
        self.scoreteam4=Label(self, width=10,  text= 'Team 4: {Team 4}'.format(**self.scoreboardDICT), font=("Helvetica", 14))
        self.scoreteam4.place(x=503, y=180)


        self.buttonList= []
        for col in range(0,5):
            photo1 = PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/200dollars.gif")
            photo1 = photo1.subsample(3,3)
            self.button=Button(self, image=photo1, command= lambda: self.ButtonClickedinGame('EASY'))
            self.button.image=photo1
            self.button.grid(row=1, column=col)
            self.buttonList.append(self.button)

            photo2= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/400dollars.gif")
            photo2 = photo2.subsample(3,3)
            self.button=Button(self, image=photo2, command= lambda:self.ButtonClickedinGame('EASY'))
            self.button.image=photo2
            self.button.grid(row=2, column=col)
            self.buttonList.append(self.button)

            photo3= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/600dollars.gif")
            photo3 = photo3.subsample(3,3)
            self.button=Button(self, image=photo3, command= lambda:self.ButtonClickedinGame('MEDIUM'))
            self.button.image=photo3
            self.button.grid(row=3, column=col)
            self.buttonList.append(self.button)

            photo4= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/800dollars.gif")
            photo4 = photo4.subsample(3,3)
            self.button=Button(self, image=photo4, command= lambda:self.ButtonClickedinGame('HARD'))
            self.button.image=photo4
            self.button.grid(row=4, column=col)
            self.buttonList.append(self.button)

            photo5= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/1000dollars.gif")
            photo5 = photo5.subsample(3,3)
            self.button=Button(self, image=photo5, command= lambda:self.ButtonClickedinGame('HARD'))
            self.button.image=photo5
            self.button.grid(row=5, column=col)
            self.buttonList.append(self.button)

        self.categoryList=[]
        col=0
        for item in categories:
            self.category_label=Label(self, bg="#000383",relief=RAISED,borderwidth=3, text=item,fg="white", font=("Baskerville Old Face", 18),height=3, width=10, wraplength=90, justify=CENTER)
            self.category_label.grid(row=0, column=col)
            self.categoryList.append(self.category_label)
            col += 1

        self.ALLquestionanswers={}
        self.EASYquestionanswers = {}
        self.MEDIUMquestionanswers= {}
        self.HARDquestionanswers={}

        for item in self.questionanswer:
            question = item[2]
            answer = item[3]
            difficulty = item[4]
            
            if difficulty == 'EASY':
                if question not in self.EASYquestionanswers:
                    self.EASYquestionanswers[question]= answer
                    self.ALLquestionanswers[question]=answer
                    
            if difficulty == 'MEDIUM':
                if question not in self.MEDIUMquestionanswers:
                    self.MEDIUMquestionanswers[question]= answer
                    self.ALLquestionanswers[question]=answer
                    
            if difficulty == 'HARD':
                if question not in self.HARDquestionanswers:
                    self.HARDquestionanswers[question]= answer
                    self.ALLquestionanswers[question]=answer
                    
        
    def ButtonClickedinGame(self, difficulty):
        for item in self.buttonList:
            item.grid_forget()
        for item in self.categoryList:
            item.grid_forget()
        self.mainmenu.grid_forget()

        self.scoreboard.place_forget()
        self.scoreteam1.place_forget()
        self.scoreteam2.place_forget()
        self.scoreteam3.place_forget()
        self.scoreteam4.place_forget()

        question_asked=''
        if difficulty == 'EASY':
            question_asked= random.choice(self.EASYquestionanswers.keys())
        if difficulty == 'MEDIUM':
            question_asked= random.choice(self.MEDIUMquestionanswers.keys())
        if difficulty == 'HARD':
            question_asked= random.choice(self.HARDquestionanswers.keys())
        
        self.selectedquestion=Label(self, text= question_asked, font=("Baskerville Old Face", 24, "bold"), fg="white", bg="#000383", width= 45, height=11, wraplength=500, justify=CENTER, relief=GROOVE, bd=5)
        self.selectedquestion.place(x=20, y=25)

##        self.answerSlotLabel=Label(self, text="Answer:")
##        self.answerSlotLabel.place(x=50, y=350)
##
##        self.answerSlot=Entry(self)
##        self.answerSlot.place(x=110, y=349)
##        self.answerSlot.bind('<Return>', self.checkAnswer)
##
##        self.answerSlotButton = Button(self, text="Enter")
##        self.answerSlotButton.place(x=302, y=349)
##        self.answerSlotButton.bind('<Button>', self.checkAnswer)

        self.showAnswer= Button(self, text='Show Answer', font=('Ariel', 18), width=12, command= lambda: self.checkAnswer(question_asked))
        self.showAnswer.place(x=220, y=360)

        self.mainmenu=Button(self)
        self.mainmenu['text']= "Back to Main Menu"
        self.mainmenu["command"] = lambda:self.back_to()
        self.mainmenu.place(x=390, y=430)


    def checkAnswer(self, questionans):
        self.selectedquestion.config(text="{questionans}".format(questionans=self.ALLquestionanswers[questionans]))
        self.showAnswer.place_forget()

        self.winningTeam=Label(self, text= "Which team got the answer right?")
        self.winningTeam.place(x=200, y=350)

        

################################################################################
class TopicsPage(BaseFrame):
    def __init__(self, master, controller):
        Frame.__init__(self, master, width="590", height="460")
        self.controller=controller
        self.create_widgets()

## adding a new topic to the game

    def addTABLEToDatabase(self, event):
##        info=[]
##        for entry in self.entries:
##            info.append(entry.get())
##
##        newtopicinput = info[0]
##        newcategoryinput=info[1]
##        newquestioninput=info[2]
##        newanswerinput=info[3]

        userInput=self.inputItemEntry.get()
        NewTopicName = userInput.replace(" ", "_")

        if userInput in AvailableTopics:
            self.label=Label(self)
            self.label["text"]="Topic Already Exists."
            self.label.place(x=240, y=410)
        elif userInput not in AvailableTopics:
            NewTopic_SQL = """CREATE TABLE "{TableName}" (tableID INTEGER PRIMARY KEY,
                            Category CHAR(20), Question CHAR(50), Answer CHAR(30), Difficulty CHAR(6));"""
            
            TopicNames_SQL = """INSERT INTO all_tables VALUES(NULL, '{TopicName}');"""

            sql_command = TopicNames_SQL.format(TopicName=NewTopicName)
            cursor.execute(sql_command)
            sql_command = NewTopic_SQL.format(TableName=NewTopicName)
            cursor.execute(sql_command)
            self.label=Label(self)
            self.label["text"]="Topic Added."
            self.label.place(x=260, y=410)
        self.label.after(2000, self.clear_label)
        self.updateList(AvailableTopics, "Select a topic...")

##        entry=self.entries[0]
##        entry.pack_forget()
##        label=self.labels[0]
##        label["text"]=newtopicinput
##        label.config(font=("Helvetica", 18, "bold"), fg="black")
        
    def clear_label(self):
        self.label.place_forget()

## deleteing a topic from the game

    def delete_topic(self):
        try:
            index=self.listboxmain.curselection()
            value=self.listboxmain.get(index[0])
            value=value.replace(" ", "_")

            DeleteTopic_SQL="""DROP TABLE "{TableName}";"""
            DeleteTopicName_SQL= """DELETE FROM all_tables WHERE table_name = '{TableName}';"""
            sql_command = DeleteTopic_SQL.format(TableName=value)
            cursor.execute(sql_command)
            sql_command2 = DeleteTopicName_SQL.format(TableName=value)
            cursor.execute(sql_command2)
            conn.commit()

            if value in AvailableTopics:
                AvailableTopics.remove(value)

            self.updateList(AvailableTopics, "Select a topic...")

            popupframe.destroy()
            
        except IndexError:
            pass

    def popup(self, action):
        global popupframe
        popupframe=Toplevel(self)
        title="""{Action} Topic"""
        title=title.format(Action=action)
        popupframe.title(title)
        screenX= popupframe.winfo_screenwidth()
        screenY= popupframe.winfo_screenheight()
        TKwidth=600
        TKheight = 250
        TkPosX=(screenX - TKwidth)/2
        TkPosY=(screenY - TKheight)/2
        popupframe.geometry("%sx%s+%s+%s"%(TKwidth,TKheight,TkPosX,(TkPosY-100)))

        if action == 'Delete':
            self.deletetopicpage= Frame(popupframe)
            self.deletetopicpage.pack()
            try:
                index=self.listboxmain.curselection()
                value=self.listboxmain.get(index[0])

                warningmessage = "Are you sure you want to delete {TOPIC}?"
                warningmessage= warningmessage.format(TOPIC=value)

                self.warningLabel=Label(self.deletetopicpage, text = warningmessage, font=("Helvetica", 24, "bold"), fg="red", wraplength=350)
                self.warningLabel.pack(side="top")

                self.warningButtonYES=Button(self.deletetopicpage, text="YES", command= self.delete_topic)
                self.warningButtonYES.pack(side="top")

                self.warningButtonNO=Button(self.deletetopicpage, text="NO", command= popupframe.destroy)
                self.warningButtonNO.pack(side="top")


            except IndexError:
                pass

        if action == 'Error':
            pass
  
        popupframe.mainloop()

    def create_widgets(self):
        self.listboxmain= Listbox(self)
        self.listboxmain.place(x=215, y=15)

        self.listboxmain.insert(END, "Select a topic...")

        for item in AvailableTopics:
            self.listboxmain.insert(END, item)

        self.edittopic =Button(self, text="Edit Topic", command= lambda: self.itemselected('Edit'))
        self.edittopic.place(x=260, y=330)

        self.addtopic=Button(self, text="Add Topic", command= lambda: self.itemselected('Add'))
        self.addtopic.place(x=260, y=355)

        self.deletetopic =Button(self, text="Delete Topic", command= lambda: self.itemselected('Delete'))
        self.deletetopic.place(x=254, y=380)
        
        self.mainmenu=Button(self)
        self.mainmenu['text']= "Back to Main Menu"
        self.mainmenu["command"] = self.back_to(MainMenu)
        self.mainmenu.pack(side="bottom", anchor=SE)

## going back to previous frames with their widgets

    def back_to(self, frame):
        try:
            self.scrollbar.pack_forget()
            self.tree.pack_forget()
            self.mainmenu.place_forget()
            self.topicpage.place_forget()
        except AttributeError:
            pass
        self.listboxmain.place(x=215, y=15)
        self.edittopic.place(x=260, y=330)
        self.addtopic.place(x=260, y=355)
        self.deletetopic.place(x=254, y=380)
        self.mainmenu.pack(side="bottom", anchor=SE)

        try:
            self.inputItemLabel.place(x=100, y=298)
            self.inputItemEntry.place(x=220, y=297)
            self.enterbutton.place(x=415, y=297)
        except AttributeError:
            pass
        
        self.controller.show_frame(frame)

## checking to see if there is an item selected. if not, error message shows
        
    def itemselected(self, action):
        if action == 'Delete':
            try:
                index=self.listboxmain.curselection()
                value=self.listboxmain.get(index[0])

                self.popup(action)

            except IndexError:
                self.label=Label(self, text="No topic selected. Please select a topic.")
                self.label.place(x=180, y=410)
                self.label.after(2000, self.clear_label)
                
        if action =='Edit':
            try:
                self.Edit_Topic()

            except IndexError:
                self.label=Label(self, text="No topic selected. Please select a topic.")
                self.label.place(x=180, y=410)
                self.label.after(2000, self.clear_label)

        if action == 'Add':
            self.inputItemLabel=Label(self, text="Enter topic name:")
            self.inputItemLabel.place(x=100, y=298)

            self.inputItemEntry=Entry(self)
            self.inputItemEntry.place(x=220, y=297)
            self.inputItemEntry.bind('<Return>', self.addTABLEToDatabase)

            self.enterbutton = Button(self)
            self.enterbutton["text"] = "Enter"
            self.enterbutton.place(x=415, y=297)
            self.enterbutton.bind('<Button>', self.addTABLEToDatabase)

    def updateList(self, listname, first_selection):
        results= cursor.execute("SELECT table_name FROM all_tables")
        for row in results:
            for item in row:
                item = item.replace("_", " ")
                if item not in AvailableTopics:
                    AvailableTopics.append(item)
        self.listboxmain.delete(0,END)
        self.listboxmain.insert(END, first_selection)
        for item2 in listname:
            self.listboxmain.insert(END, item2)

## edit frame shows with detailed information of what the topic has stored

    def Edit_Topic(self):
        self.listboxmain.place_forget()
        self.edittopic.place_forget()
        self.addtopic.place_forget()
        self.deletetopic.place_forget()
        self.mainmenu.pack_forget()
        
        try:
            self.inputItemLabel.place_forget()
            self.inputItemEntry.place_forget()
            self.enterbutton.place_forget()
        except AttributeError:
            pass

        self.scrollbar= Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=Y, anchor=N)
        
        self.tree= Treeview(self, columns=('Category', 'Question', 'Answer', 'Difficulty'), show='headings', selectmode="browse", yscrollcommand=self.scrollbar.set)

        self.tree.heading("Category", text="Category")
        self.tree.column('Category', width =55,anchor="center")
        
        self.tree.heading("Question", text= "Question")
        self.tree.column('Question', width=290)
        
        self.tree.heading("Answer", text= "Answer")
        self.tree.column('Answer', width=140)
        
        self.tree.heading("Difficulty", text= "Difficulty")
        self.tree.column('Difficulty', width =65, anchor="center")

        self.scrollbar.config(command=self.tree.yview)
        
        try:
            index=self.listboxmain.curselection()
            value1=self.listboxmain.get(index[0])
            value=value1.replace(" ", "_")

            RowsInTable=[]
            EditTopicTable_SQL="""SELECT * FROM {TableName};"""
            sql_command=EditTopicTable_SQL.format(TableName=value)
            results = cursor.execute(sql_command)
            
            for row in results:
                RowsInTable.append(row)
                    
        except IndexError:
            pass

        for item in RowsInTable:
            category=item[1]
            question=item[2]
            answer=item[3]
            difficulty=item[4]

            self.tree.insert('', 'end', values=(category, question, answer, difficulty))

        self.tree.bind("<Double-1>", self.DoubleClick)
        
        self.tree.pack(side=LEFT, anchor=N)

        self.mainmenu=Button(self)
        self.mainmenu['text']= "Back to Main Menu"
        self.mainmenu["command"] = lambda: self.back_to(MainMenu)
        self.mainmenu.place(x=400, y=425)

        self.topicpage=Button(self)
        self.topicpage['text']= "Back to Topic Page"
        self.topicpage["command"] = lambda: self.back_to(TopicsPage)
        self.topicpage.place(x=400, y=400)

##    def editExistingQuestions(self, topic):
##        index=self.listboxmain.curselection()
##        value1=self.listboxmain.get(index[0])
##        
##        info=[]
##        for entry in self.entries:
##            info.append(entry.get())
##
##        topicinput = info[0]
##        categoryinput=info[1]
##        questioninput=info[2]
##        answerinput=info[3]
##        difficultyinput=info[4]


    def DoubleClick(self,event):
        current = self.tree.focus()
        item = self.tree.item(current)
        print item['values']
        

################################################################################
##
##class Difficulty(BaseFrame):
##    def create_widgets(self):
##        self.easybutton = Button(self)
##        self.easybutton["text"]= "EASY"
##        self.easybutton["command"]= lambda: self.controller.show_frame(PlayGame)
##        self.easybutton.grid(row=1, column=0)
##
##        self.mediumbutton = Button(self)
##        self.mediumbutton["text"]= "MEDIUM"
##        self.mediumbutton["command"]= lambda: self.controller.show_frame(PlayGame)
##        self.mediumbutton.grid(row=2, column=0)
##
##        self.hardbutton = Button(self)
##        self.hardbutton["text"]= "HARD"
##        self.hardbutton["command"]= lambda: self.controller.show_frame(PlayGame)
##        self.hardbutton.grid(row=3, column=0)
##
################################################################################
##class PlayGame(BaseFrame):
##    def __init__(self, master, controller):
##        Frame.__init__(self, master, width="590", height="460")
##        self.controller=controller
##        self.create_widgets()
##        
##    def create_widgets(self):
##        self.mainmenu=Button(self, width=10, font=("Helvetica", 8))
##        self.mainmenu['text']= "Main Menu"
##        self.mainmenu["command"] = lambda: self.controller.show_frame(MainMenu)
##        self.mainmenu.grid(row=0, column=5)
##
##        self.quit = Button(self)
##        self.quit["text"] = "Quit"
##        self.quit["command"] =  self.controller.quitgame
##        self.quit.place(x=535, y=430)
##
##        for col in range(0,5):
##            photo1 = PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/200dollars.gif")
##            photo1 = photo1.subsample(3,3)
##            self.button=Button(self, image=photo1, command= lambda:self.controller.show_frame(ButtonClickedinGame))
##            self.button.image=photo1
##            self.button.grid(row=1, column=col)
##
##            photo2= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/400dollars.gif")
##            photo2 = photo2.subsample(3,3)
##            self.button=Button(self, image=photo2, command= lambda:self.controller.show_frame(ButtonClickedinGame))
##            self.button.image=photo2
##            self.button.grid(row=2, column=col)
##
##            photo3= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/600dollars.gif")
##            photo3 = photo3.subsample(3,3)
##            self.button=Button(self, image=photo3, command= lambda:self.controller.show_frame(ButtonClickedinGame))
##            self.button.image=photo3
##            self.button.grid(row=3, column=col)
##
##            photo4= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/800dollars.gif")
##            photo4 = photo4.subsample(3,3)
##            self.button=Button(self, image=photo4, command= lambda:self.controller.show_frame(ButtonClickedinGame))
##            self.button.image=photo4
##            self.button.grid(row=4, column=col)
##
##            photo5= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/1000dollars.gif")
##            photo5 = photo5.subsample(3,3)
##            self.button=Button(self, image=photo5, command= lambda:self.controller.show_frame(ButtonClickedinGame))
##            self.button.image=photo5
##            self.button.grid(row=5, column=col)
##
##        for col in range(0,5):
##            self.category_label=Label(self, bg="#000383",relief=RAISED,borderwidth=3, text="CATEGORY",fg="white", font=("Baskerville Old Face", 12),height=5, width=15, wraplength=90, justify=CENTER)
##            self.category_label.grid(row=0, column=col)
##
################################################################################
##
##class ButtonClickedinGame(BaseFrame):
##    def __init__(self, master, controller):
##        Frame.__init__(self, master, width="590", height="460")
##        self.controller=controller
##        self.create_widgets()
##
##    def create_widgets(self):
##        self.selectedquestion=Label(self, text= "testing a question question", font=("Baskerville Old Face", 24, "bold"), fg="white", bg="#000383", width= 45, height=11, wraplength=500, justify=CENTER, relief=GROOVE, bd=5)
####        self.selectedquestion.config(highlightcolor="white", highlightthickness=3)
##        self.selectedquestion.place(x=20, y=25)
##
##        self.answerSlotLabel=Label(self, text="Answer:")
##        self.answerSlotLabel.place(x=50, y=350)
##
##        self.answerSlot=Entry(self)
##        self.answerSlot.place(x=110, y=349)
##        self.answerSlot.bind('<Return>', self.checkAnswer)
##
##        self.answerSlotButton = Button(self, text="Enter")
##        self.answerSlotButton.place(x=302, y=349)
##        self.answerSlotButton.bind('<Button>', self.checkAnswer)
##
##        self.mainmenu=Button(self)
##        self.mainmenu['text']= "Back to Main Menu"
##        self.mainmenu["command"] = lambda:self.controller.show_frame(MainMenu)
##        self.mainmenu.place(x=400, y=425)
##
##
##    def checkAnswer(self, event):
##
##        userInput=self.answerSlot.get()
##        
##        if userInput == "Yes":
##            print 'yes'
##
##        else:
##            print 'no'
##        

    
################################################################################
        
conn=sqlite3.connect("/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Myth_and_Arch_Jeopardy_Database.db")
cursor = conn.cursor()

global AvailableTopics
AvailableTopics = []
results= cursor.execute("SELECT table_name FROM all_tables")
for row in results:
    for item in row:
        item = item.replace("_", " ")
        AvailableTopics.append(item)

global difficulty
difficulty=['Easy', 'Medium', 'Hard']

global topicChosen
topicChosen="none"




if __name__=="__main__":
    app= JeopardyGame()
    app.mainloop()
    exit()
    
conn.close
