from Tkinter import *
import sqlite3
import tkFont
from PIL import ImageFont, Image, ImageDraw

class JeopardyGame(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Jeopardy!")
        screenX= self.winfo_screenwidth()
        screenY= self.winfo_screenheight()
        TKwidth=590
        TKheight = 560
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
        for f in (MainMenu, TopicsPage, PlayGame):
            frame=f(self.container,self)
            frame.grid(row=0, column=0, sticky=NW+SE)
            self.frames[f]=frame
        self.show_frame(MainMenu)

    def show_frame(self, cls):
        self.frames[cls].tkraise()
        

    def twoSequences(self, *functions):
        def func(*args, **kwargs):
            for function in functions:
                function(*args, **kwargs)
        return func


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
        self.add_topic.place(x=230, y=100)

        self.quit = Button(self)
        self.quit["text"] = "Quit"
        self.quit["command"] =  self.controller.quitgame
        self.quit.place(x=535, y=430)

    def TopicChoosen(self, Menu_topic):
        self.updateDropdown()

##        GameScreen_SQL = """SELECT * FROM {TableName}"""
##        sql_command= GameScreen_SQL.format(TableName=Menu_topic)
##        results = cursor.execute(sql_command)

##        global questionanswer
##        questionanswer=[]
##        for row in results:
##            questionanswer.append(row)
##
##        for item in questionanswer:
##            print item
        topicChosen = Menu_topic
        
        if Menu_topic != "none":
            self.controller.show_frame(PlayGame)

    def updateDropdown(self):
        results= cursor.execute("SELECT table_name FROM all_tables")
        for row in results:
            for item in row:
                if item not in AvailableTopics:
                    AvailableTopics.append(item)
                    
        self.menu= OptionMenu(self, self.var, *AvailableTopics, command = self.TopicChoosen)
        self.menu.config(width=15, height=1)
        self.menu.place(x=222.5, y=60)
        self.menu.after(2000, self.updateDropdown)
            
################################################################################
class TopicsPage(BaseFrame):
    def addTABLEToDatabase(self):
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

        if NewTopicName in AvailableTopics:
            self.topicAddedLabel=Label(self.addtopicpage)
            self.topicAddedLabel["text"]="Topic Already Exists. Go back to Edit Topic."
            self.topicAddedLabel.pack(side="bottom", anchor="s", fill="x")
        elif NewTopicName not in AvailableTopics:
            NewTopic_SQL = """CREATE TABLE "{TableName}" (tableID INTEGER PRIMARY KEY,
                            Subject CHAR(20), Question CHAR(50), Answer CHAR(30), Difficulty CHAR(6));"""
            
            TopicNames_SQL = """INSERT INTO all_tables VALUES(NULL, '{TopicName}');"""

            sql_command = TopicNames_SQL.format(TopicName=NewTopicName)
            cursor.execute(sql_command)
            sql_command = NewTopic_SQL.format(TableName=NewTopicName)
            cursor.execute(sql_command)
            self.topicAddedLabel=Label(self.addtopicpage)
            self.topicAddedLabel["text"]="Topic Added."
            self.topicAddedLabel.pack(side="bottom", anchor="s", fill="x")
        self.topicAddedLabel.after(2000, self.clear_label)
        self.updateList(AvailableTopics, "Select a topic...")

##        entry=self.entries[0]
##        entry.pack_forget()
##        label=self.labels[0]
##        label["text"]=newtopicinput
##        label.config(font=("Helvetica", 18, "bold"), fg="black")
        


    def clear_label(self):
        self.topicAddedLabel.pack_forget()

    def delete_topic(self):
        try:
            index=self.listbox.curselection()
            value=self.listbox.get(index[0])
            self.listbox.delete(index)

            DeleteTopic_SQL="""DROP TABLE "{TableName}";"""
            DeleteTopicName_SQL= """DELETE FROM all_tables WHERE table_name = '{TableName}';"""
            sql_command = DeleteTopic_SQL.format(TableName=value)
            cursor.execute(sql_command)
            sql_command2 = DeleteTopicName_SQL.format(TableName=value)
            cursor.execute(sql_command2)
            conn.commit()

            if value in AvailableTopics:
                AvailableTopics.remove(value)
            

        except IndexError:
            pass

    def popup(self, action):
        popupframe=Toplevel(self)
        title="""{Action} Topic"""
        title=title.format(Action=action)
        popupframe.title(title)
        screenX= popupframe.winfo_screenwidth()
        screenY= popupframe.winfo_screenheight()
        TKwidth=400
        TKheight = 300
        TkPosX=(screenX - TKwidth)/2
        TkPosY=(screenY - TKheight)/2
        popupframe.geometry("%sx%s+%s+%s"%(TKwidth,TKheight,TkPosX,(TkPosY-100)))

        if action == 'Add':
            self.addtopicpage= Frame(popupframe)
            self.addtopicpage.pack()

            self.inputItemLabel=Label(self.addtopicpage, text="Enter topic name:")
            self.inputItemLabel.pack(anchor=CENTER)

            self.inputItemEntry=Entry(self.addtopicpage)
            self.inputItemEntry.pack(anchor=CENTER)

            self.enterbutton = Button(self.addtopicpage)
            self.enterbutton["text"] = "Enter"
            self.enterbutton["command"] = self.addTABLEToDatabase
            self.enterbutton.pack(anchor=CENTER)
                                    

            self.quit = Button(self.addtopicpage)
            self.quit["text"] = "Quit"
            self.quit["command"] =  popupframe.destroy
            self.quit.pack(side="right",anchor="se")


        elif action == 'Edit':
            self.edittopicpage= Frame(popupframe)
            self.edittopicpage.pack()
            try:
                index=self.listbox.curselection()
                value=self.listbox.get(index[0])

                self.listbox= Listbox(self.edittopicpage)
                self.listbox.pack(side='left')
                
                self.listbox.insert(END, "Select a Question or Answer...")

                QuestionsAnswers = []
                EditTopicTable_SQL="""SELECT Question, Answer FROM {TableName};"""
                sql_command=EditTopicTable_SQL.format(TableName=value)
                results = cursor.execute(sql_command)
                
                for row in results:
                    for item in row:
                        QuestionsAnswers.append(item)

                for item in QuestionsAnswers:
                    self.listbox.insert(END, item)

            except IndexError:
                pass


##            self.inputItemLabel=Label(self.addtopicpage, text=value, font=("Helvetica", 18, "bold"), fg="black")
##            self.inputItemLabel.pack(anchor="s")
            
##            self.entries=[]
##            self.labels=[]
##            for item in ["Enter Category:","Enter Question:", "Enter Answer:"]:
##
##                self.inputItemLabel=Label(self.addtopicpage, text=item)
##                self.inputItemLabel.pack(anchor="s")
##                
##                self.labels.append(self.inputItemLabel)
##
##                self.inputItemEntry=Entry(self.addtopicpage)
##                self.inputItemEntry.pack(anchor="s")
##                
##                self.entries.append(self.inputItemEntry)
##
##            self.var=StringVar(self)
##            self.var.set("Choose a Difficulty")
##
##            self.inputDifficulty= OptionMenu(self.addtopicpage, self.var, *difficulty)
##            self.inputDifficulty.pack(anchor="s")            
##
##            self.enterbutton = Button(self.addtopicpage)
##            self.enterbutton["text"] = "Enter"
##            self.enterbutton["command"] = self.addTABLEToDatabase
##            self.enterbutton.pack(anchor="s")

            self.quit = Button(self.edittopicpage)
            self.quit["text"] = "Quit"
            self.quit["command"] =  popupframe.destroy
            self.quit.pack(side="right",anchor="se")
        
        popupframe.mainloop()

    def create_widgets(self):
        self.listbox= Listbox(self)
        self.listbox.place(x=215, y=130)
        
        self.listbox.insert(END, "Select a topic...")

        for item in AvailableTopics:
            self.listbox.insert(END, item)

        self.edittopic =Button(self, text="Edit Topic", command= lambda: self.popup('Edit'))
        self.edittopic.place(x=260, y=310)

        self.addtopic=Button(self, text="Add Topic", command= lambda: self.popup('Add'))
        self.addtopic.place(x=260, y=335)

        self.deletetopic =Button(self, text="Delete Topic", command=self.delete_topic)
        self.deletetopic.place(x=254, y=360)
        
        self.mainmenu=Button(self)
        self.mainmenu['text']= "Back to Main Menu"
        self.mainmenu["command"] = lambda: self.controller.show_frame(MainMenu)
        self.mainmenu.pack(side="bottom", anchor=SE)

    def updateList(self, listname, first_selection):
        results= cursor.execute("SELECT table_name FROM all_tables")
        for row in results:
            for item in row:
                if item not in AvailableTopics:
                    AvailableTopics.append(item)
        self.listbox.delete(0,END)
        self.listbox.insert(END, first_selection)
        for item2 in listname:
            self.listbox.insert(END, item2)



        
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
class PlayGame(BaseFrame):
    def create_widgets(self):
        self.mainmenu=Button(self, width=10, font=("Helvetica", 8))
        self.mainmenu['text']= "Main Menu"
        self.mainmenu["command"] = lambda: self.controller.show_frame(MainMenu)
        self.mainmenu.grid(row=0, column=5)

        self.quit = Button(self)
        self.quit["text"] = "Quit"
        self.quit["command"] =  self.controller.quitgame
        self.quit.place(x=535, y=430)

        for col in range(0,5):
            photo1 = PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/200dollars.gif")
            photo1 = photo1.subsample(3,3)
            self.button=Button(self, image=photo1)
            self.button.image=photo1
            self.button.grid(row=1, column=col)

            photo2= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/400dollars.gif")
            photo2 = photo2.subsample(3,3)
            self.button=Button(self, image=photo2)
            self.button.image=photo2
            self.button.grid(row=2, column=col)

            photo3= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/600dollars.gif")
            photo3 = photo3.subsample(3,3)
            self.button=Button(self, image=photo3)
            self.button.image=photo3
            self.button.grid(row=3, column=col)

            photo4= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/800dollars.gif")
            photo4 = photo4.subsample(3,3)
            self.button=Button(self, image=photo4)
            self.button.image=photo4
            self.button.grid(row=4, column=col)

            photo5= PhotoImage(file="/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Images/1000dollars.gif")
            photo5 = photo5.subsample(3,3)
            self.button=Button(self, image=photo5)
            self.button.image=photo5
            self.button.grid(row=5, column=col)

        for col in range(0,5):
            self.category_label=Label(self, bg="#002290",relief=RAISED,borderwidth=3, text="CATEGORY",fg="white", font=("Baskerville Old Face", 12),height=5, width=15, wraplength=90, justify=CENTER)
            self.category_label.grid(row=0, column=col)       
################################################################################
        
conn=sqlite3.connect("/Users/ashleyrojas/Desktop/Program_Project_Seminar_for_Minors/Myth_and_Arch_Jeopardy_Database.db")
cursor = conn.cursor()

global AvailableTopics
AvailableTopics = []
results= cursor.execute("SELECT table_name FROM all_tables")
for row in results:
    for item in row:
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
