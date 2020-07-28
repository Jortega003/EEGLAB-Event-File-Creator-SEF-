import os
import pandas as pd
import numpy as np
#import win32api
import tkinter
from tkinter import Button
from tkinter import filedialog
from tkinter import *

def computeEVT(file):
    currentdirc = os.getcwd()
    file = (file)
    
    
    ############## READING THE FILE ##################
    #Read the file
    df = pd.read_csv(file)
    
    #Read the columns
    for i in df:
        columns = i.split("\t")
     
    #Make a list with each line in the csv seperetated
    NewDF = [] 
    for i in df['number\tlatency\tduration\tchannel\tbvtime\tbvmknum\ttype\tcode\turevent']:
        i = i.split("\t")
        NewDF.append(i)
        
    #Creat a new dataframe where the seperated data will go
    f = pd.DataFrame()
    
    #Set the columns
    for i in columns:
        f[i] = []
    
    #Create the new database
    n = 0 
    c = len(NewDF) #Set the end
    
    for i in NewDF:
        
        if n == c:
            break
        
        else:
            f.loc[n] = NewDF[n]
            n = n + 1
    
    #Replace blanks in code with NaN
    f["code"] = f["code"].replace(r'\s+',np.nan,regex=True).replace('',np.nan)
    
    ###############################################################################
    
    #Read the keys
    h = open("REC_Key.txt", "r")
    file = (h.read())
    
    #Split the file by line
    file = file.split("\n")
    
    #Split each line by TAB and add it to a list
    REC_Key = []
    for i in file:
        REC_Key.append(i.split("\t"))
        
    #Input it in the df
    #Seperate the code and label
    code = []
    for i in REC_Key:
        code.append(i[0])
        
    label = []
    for i in REC_Key:
        label.append(i[1])
    
    len(label)
    ##################################################################################
    #Switch new code and label
    
    #Remove S6
    f = f[f.type != "S  6"]
    
    #Remove S5
    f = f[f.type != "S  5"]
    
    G = f['code']
    
    #Make a new list with the variables
    empty = []
    for i in G:
        empty.append(i)
    
    #Switch each stimulus with each label one by one
    n = 0
    for i in empty:  
        if i == "Stimulus":
            empty[empty.index(i)] = label[n]
            n = n + 1
    
    f["code"] = empty
    
    # do the same for the code
    G = f['type']
    
    empty = []
    for i in G:
        empty.append(i)
    
    #Switch each stimulus with each code one by one
    n = 0
    
    for i in empty:
        if i == "S  1":
            empty[empty.index(i)] = code[n]
            n = n + 1
    
    f["type"] = empty
    
    ########################################################################################
    #sSwitch Delay for its corresponding delay type
    G = f['code']
    
    empty = []
    for i in G:
        empty.append(i)
    
    n = -1
    
    #Read the type and switch the code for the proper Delay
    for i in f["type"]:
        n = n + 1
        if i == "52":
            print(i)
            empty[n] = "Delay2"
        if i == "55":
            empty[n] = "Delay5"
        if i == "59":
            empty[n] = "Delay9"
    
    f["code"] = empty
            
    for i in f["code"]:
        print(i)
    
    f.to_csv(e.get()+ ".csv", index=False)
    #win32api.MessageBox(None, 'DONE: EVT has been created.', "EVT Creator", 0x00001000)
    print("DONE: EVT CREATED")
        
    ###########################################################################################

def startnow(file):
    computeEVT(file)

def callback():
    name= filedialog.askopenfilename()
    print (name)
    startnow(name)

root = Tk()
e = Entry(root)
e.pack()

def nani():
    print (e.get()) # This is the text you may want to use later
    
def setdirect():
    dir_name = filedialog.askdirectory()
    os.chdir(dir_name)
    currentdirc = os.getcwd()
    
errmsg = 'Error!'
Button(text='Set Directory', command=setdirect).pack(fill=tkinter.X)
Button(text='File Open', command=callback).pack(fill=tkinter.X) 

root.mainloop()