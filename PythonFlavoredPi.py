# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import Tkinter
import tkMessageBox
import string
import random

global clickedQ
clickedQ = False

prompts = [ "Type your question here...",
            "Type your first answer here...",
            "Type your second answer here...",
            "Type your third (optional) answer here...",
            "Type your fourth (optional) answer here..." ]

texts = []

infos = [ "You have not entered a question!",
          "You have not entered your first answer!",
          "You have not entered your second answer!" ]
confirm = "Are you sure your question is ready?"
good = "Your question has been sent!"
goodTitle = "Success!"
noGoodTitle = "Problem!"
confirmTitle = "Send your Question"

results = []

def clearBoxQ(event):
   global clickedQ
   if (clickedQ == False):
      entries[0].delete(0, 26)
      entries[0].config(fg = "black")
      clickedQ = True

def sendResults():
   for i, info in enumerate(infos):
      if texts[i].get() == (prompts[i]):
         tkMessageBox.showwarning( noGoodTitle, info)
         return
   if tkMessageBox.askyesno( confirmTitle, confirm):
      tkMessageBox.showinfo( goodTitle, good)
      getAnswer()

def getAnswer():
   results = Tkinter.Tk()
   labelQ = Tkinter.Label( results, bg = "white", width = 45, height = 2, bd = 5, text = texts[0].get())
   labelA1 = Tkinter.Label( results, bg = "red", width = 45, height = 2, bd = 5, text = texts[1].get())
   labelA2 = Tkinter.Label( results, bg = "red", width = 45, height = 2, bd = 5, text = texts[2].get())
   randomA = [0, 1]
   answer = random.choice(randomA)
   if (answer == 0):
      labelA1.config(bg = "green")
   else:
      labelA2.config(bg = "green")
   labelQ.pack()
   labelA1.pack()
   labelA2.pack()
   results.mainloop()

top = Tkinter.Tk()
texts = [ Tkinter.StringVar(value = p) for p in prompts ]
entries = [ Tkinter.Entry(top, bd = 5, width = 50, fg = "gray", textvariable = t) for t in texts ]
sendButton = Tkinter.Button(top, bd = 5, text = "Send", command = sendResults)

entries[0].bind("<Button-1>", clearBoxQ)

Tkinter.Label(top, text = "Question:").pack()
entries[0].pack()
Tkinter.Label(top, text = "Answers:").pack()
for entry in entries[1:]:
   entry.pack()
sendButton.pack()
top.mainloop()

