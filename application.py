# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 23:16:34 2023

@author: ipnnr
"""
import algorythm as alg
import tkinter
from tkinter import *
from tkinter import ttk 

def calculate():
    w = alg.worker(filename_box.get())
    option = combobox.get()

    res, rows, columns, P = w.calculate(option=="Maximize")
    P=[["{:.3f}".format(xi) for xi in x] for x in P]
    for i in range(len(rows)):
        P[rows[i]][columns[i]]= "["+P[rows[i]][columns[i]]+"]"
        
    result_text =""
    if option=="Maximize":
        result_text+="\n максимальный объем сахара: "
    else:
        result_text+="\n минимальный объем сахара: "
    result_text += str(res)+"\n оптимальный план переработки: "
    
    result_box.delete(index1="1.0",index2="5.0")
    result_box.insert(index = "1.0", chars = result_text)
    t=Table(window, len(rows), len(rows), data = P)
    t.grid(column=1, row = 3)

class Table(Frame):
    """2D matrix of Entry widgets"""
    def __init__(self, parent, rows=0, columns=0, width=16, data=None):
        super().__init__(parent)
  
        if data is not None:
            rows = len(data)
            columns = len(data[0])
        self.rows = rows
        self.columns = columns
        self.cells = []
        self.values = []
        for row in range(rows): 
            for col in range(columns):
                var = StringVar()
                cell = Entry(self, width=width, textvariable=var)
                cell.grid(row=row, column=col)
                self.cells.append(cell)
                self.values.append(var)
                if data:
                    var.set(data[row][col])


window = Tk()
window.geometry('800x500')  

lbl = Label(window, text="filename:")  
lbl.grid(column =0, row =0, pady=20)
filename_box = Entry(window, width=20)
filename_box.grid(column=1, row=0, )  

result_box = Text(window, height=3, width=60)
result_box.grid(column=1, row = 2)

calculate_btn = Button(window, text="calculate", command=calculate)  
calculate_btn.grid(column=3, row=0) 

options = ["Maximize", "Minimize"]
combobox = ttk.Combobox(values=options)
combobox.grid(column=2, row=0)
combobox.current(1)
window.mainloop()