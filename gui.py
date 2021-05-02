import tkinter as tk
from tkinter import ttk
from tkinter import *
from Vector_Space_Model import start
#from BooleanRetrievalModel import pre

def show():

    idf_val, tempList= start(raw_query.get())
    result_list = []

    if len(tempList) >= 1:
        for i in range(1,len(tempList)+1):
            result_list.append([i, str(tempList[i-1]) + ".txt"])
    for i, (num, name) in enumerate(result_list, start=1):
        listBox.insert("", "end", values=( i, idf_val[i], name))
def rs():
    for i in listBox.get_children():
        listBox.delete(i)

root = tk.Tk()
root.title('Vector Space Model')
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()

positionRight = int(root.winfo_screenwidth()/2 - windowWidth)
positionDown = int(root.winfo_screenheight()/2 - windowHeight)
root.geometry("+{}+{}".format(positionRight, positionDown)) 


raw_query = StringVar()

L1 = Label(root,padx=0, text="Enter your query")
L1.grid( row = 0,column=0 ,columnspan=3,padx=0,ipadx = 0)
E1 = Entry(root, bd =5, textvariable = raw_query)
E1.grid(row=1, column=0,columnspan=5,padx=0,ipadx=0)


button = Button(root, fg = "Red", text='Search', width=25, command=show)
button.grid(row=2,column=0,columnspan=3,padx=0)

cols = ('Sr.No','Similarity', 'Document Number')
listBox = ttk.Treeview(root, columns=cols, show='headings', height = 15)

for col in cols:
    listBox.heading(col, text=col)    
listBox.grid(row=3, column=0, columnspan=2)

closeButton = tk.Button(root, text="Close",fg = "Red",
width=15, command=exit).grid(row=4, columnspan=1 ,column =0)
reset = tk.Button(root, text="Try Again?",fg = "Red", width=15, command=rs).grid(row=4, columnspan=1,column =1)
root.mainloop()