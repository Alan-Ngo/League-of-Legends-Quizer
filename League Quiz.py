import requests
from tkinter import *
from tkinter import ttk
import tkinter.messagebox

#Enter your API key
APIkey = ""

class Quiz(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.tries = 0
        self.score = 0
        self.wrong = []
        self.initUI()


    def initUI(self):
        self.parent.title("League of Legends Quiz")
        self.pack(fill=BOTH, expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.get_dictionary()

        self.questions = Message(self, text=self.messages(), width=200)
        self.questions.grid(sticky=E + W)

        self.entry = Entry(self)
        self.entry.grid(row=1, sticky=W + E)

        self.results = Message(self, text=str(self.tries)+" \nout of 10")
        self.results.grid(row=2,sticky=E)

        submit = Button(self, text="Submit", command=self.check, relief=RIDGE, background="black", foreground="white")
        submit.grid(row=2)

        #Treeview will become populated when 10 questions are completed
        self.tree = ttk.Treeview(self)
        self.tree.grid(row=3)
        self.tree["columns"] = ("one", "two")
        self.tree.heading("#0", text="Text")
        self.tree.heading("#1", text="Answer")
        self.tree.heading("#2", text="Correct Answer")
        self.tree.column("#1", width=100)
        self.tree.column("#1", width=100)
        self.tree.column("#2", width=100)

        self.parent.bind("<Return>", self.check)

    def get_dictionary(self):
        #Retrieve league API data in json format
        leagueC = requests.get("https://euw1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&tags=all&dataById=false&api_key="+APIkey)
        self.json = leagueC.json()

    def messages(self):
        for data in self.json["data"]:
            #Finds champion names and their titles
            self.champions = self.json["data"][data]["name"]
            self.titles = self.json["data"][data]["title"]
            del self.json["data"][data]
            return("Whose title is this - \n" + self.titles + "\n")

    def check(self,enter=0):
        me=self.entry.get()
        self.tries += 1
        if me.lower() == self.champions.lower():
            self.score+=1
        else:
            self.wrong.append([self.titles,me.lower(),self.champions.lower()])

        self.results.configure(text=str(self.tries) + " \nout of 10")
        self.questions.configure(text=self.messages())
        self.entry.delete(0,END)

        #When 10 questions has passed, show the answers and score
        if self.tries == 10:
            k=tkinter.messagebox.showinfo("Results", "you got:\n" + str(self.score) +"/" + str(self.tries)+" right.")
            print(self.wrong)
            for i in self.wrong:
                self.tree.insert("", 0, text=i[0], values=(i[1], i[2]))
            if k=="ok":
                self.reset()

    def reset(self):
        self.tries = 0
        self.score = 0
        self.results.configure(text=str(self.tries)+" \nout of 10")

def main():
    root = Tk()
    app = Quiz(root)
    root.mainloop()

if __name__ == '__main__':
    main()
