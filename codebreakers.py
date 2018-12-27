# -*- coding: utf-8 -*-
"""
PIC16 - Spring 2018
Final Project: Game

Grant Huang
"""

import tkinter as Tk
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from decode import masterDecode
from encode import Code


class Game(object):
    '''the Codebreakers program!'''
   
    def __init__(self, master):
        '''creates title screen'''
        self.master = master
        self.w = 626
        self.h = 500
        self.canvas = Tk.Canvas(master,width=self.w,height=self.h,bg='black')
        self.canvas.pack()
        
        self.img = Tk.PhotoImage(file='brickwall.gif')
        self.background = Tk.Label(image=self.img)
        self.background.image = self.img
        self.background.pack()
        self.background.place(x=0,y=0,width=self.w,height=self.h)
        
        self.text = Tk.Label(master,text='Codebreakers',font=('courier',40),bg='black',fg='white')
        self.text.pack()
        self.text.place(x=self.w/8,y=self.h/6)
        
        self.button = Tk.Button(master,text="decode",font=('courier',25),height=1,width=10)
        self.button.bind("<Button-1>", self.decodeMode) #bind(signal(left-click), slot(call checkClick))
        self.button.pack()
        self.button.place(x=self.w/8,y=self.h/2)
        
        self.button2 = Tk.Button(master, text="encode",font=('courier',25),height=1,width=10)
        self.button2.bind("<Button-1>", self.encodeMode)
        self.button2.pack()
        self.button2.place(x=self.w/8,y=self.h*2/3)
        
        self.credits = Tk.Button(master, text="Credits",font=('courier',22),height=1,width=10,
                                 bg='black',fg='white')
        self.credits.bind("<Button-1>", self.creditScreen)
        self.credits.pack()
        self.credits.place(x=self.w*5.2/8,y=self.h*5/6)
       
    def decodeMode(self, ev):
        '''enters screen for decoding messages'''
        self.clearTitleScreen()

        self.decodeInstructions = Tk.Label(self.master, text ='Enter message:',
                                  font=('courier',25), bg='black',fg='white')
        self.decodeInstructions.pack()
        self.decodeInstructions.place(x=self.w/8, y=self.h/10)
        
        self.messageEntry = Tk.Text(self.master,height=10,width=60)
        self.messageEntry.pack()
        self.messageEntry.place(x=self.w/8,y=self.h/5)
   
        self.decryptbutton = Tk.Button(self.master,text="decrypt",font=('courier',15),height=1,width=10)
        self.decryptbutton.bind("<Button-1>", self.decrypt) #bind(signal(left-click), slot(call checkClick))
        self.decryptbutton.pack()
        self.decryptbutton.place(x=self.w*14.5/26,y=self.h*9/10)
        
        self.backbutton = Tk.Button(self.master,text="back",font=('courier',15),
                                    ba='black',fg='white',height=1,width=10)
        self.backbutton.bind("<Button-1>", self.totitle)
        self.backbutton.pack()
        self.backbutton.place(x=self.w*7/9,y=self.h*9/10)
        
        self.note = Tk.Label(self.master, text ='(this thing works best for long messages)',
                                  font=('courier',12), bg='black',fg='white')
        self.note.pack()
        self.note.place(x=self.w/7,y=self.h*14/17)
        
        self.translation = Tk.Text(self.master,height=10,width=60)
        
        self.alphabet = Tk.Entry(self.master, width=26,font=('courier',10))
        self.alphabet.insert(0, "abcdefghijklmnopqrstuvwxyz")
        self.alphabet.configure(state='disabled')
        self.alphabet.pack()
        self.alphabet.place(x=self.w/5,y=self.h*15.4/17)
        
        var = Tk.StringVar()
        var.trace_variable("w", self.on_write)
        
        self.code = Tk.Entry(self.master,width=26,textvariable=var,font=('courier',10))
        self.code.pack()
        self.code.place(x=self.w/5,y=self.h*15.9/17)
        self.code.configure(state='disabled')
        
        self.alphabetnote = Tk.Label(self.master, text ='ciphertext->\n plaintext',
                                  font=('courier',10), bg='black',fg='white')
        self.alphabetnote.pack()
        self.alphabetnote.place(x=22,y=self.h*15.3/17)
    
        
    def decrypt(self,ev):
        '''decodes user inputed message and displays to screen'''
        messageinput = self.messageEntry.get("1.0",'end-1c')
        decodeOutput = masterDecode(messageinput)
        decryption = decodeOutput[0]
        mapping = decodeOutput[1]
        
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
        #print mapping
        
        for i in range(len(letters)):
            if len(mapping[letters[i]]) == 1:
                letters = letters[:i] + mapping[letters[i]][0] + letters[i+1:]
            else:
                letters = letters[:i] + '_' + letters[i+1:]

        letters = ''.join(letters)
        self.code.config(state='normal')
        self.code.insert(0, letters)
        self.code.configure(state='disabled')
                
        self.translation.delete('1.0', 'end')
        self.translation.pack()
        self.translation.place(x=self.w/8,y=self.h/2)
        self.translation.insert(1.0, decryption)
        
    def encodeMode(self,ev):
        '''enters screen for encrypting message'''
        self.clearTitleScreen()
        
        self.encodeInstructions = Tk.Label(self.master, text ='Enter message:',
                                  font=('courier',25), bg='black',fg='white')
        self.encodeInstructions.pack()
        self.encodeInstructions.place(x=self.w/8, y=self.h/10)
        
        self.messageEntry = Tk.Text(self.master,height=10,width=60)
        
        self.encryptbutton = Tk.Button(self.master,text="encrypt",font=('courier',15),height=1,width=10)
        self.encryptbutton.bind("<Button-1>", self.encrypt) #bind(signal(left-click), slot(call checkClick))
        self.encryptbutton.pack()
        self.encryptbutton.place(x=self.w*14.5/26,y=self.h*9/10)
        
        
        self.messageEntry.pack()
        self.messageEntry.place(x=self.w/8,y=self.h/5)
        
        self.backbutton = Tk.Button(self.master,text="back",font=('courier',15),
                                    ba='black',fg='white',height=1,width=10)
        self.backbutton.bind("<Button-1>", self.totitle2)
        self.backbutton.pack()
        self.backbutton.place(x=self.w*7/9,y=self.h*9/10)
        
        self.note = Tk.Label(self.master, text ='Provide alphabet: ',
                                  font=('courier',12), bg='black',fg='white')
        self.note.pack()
        self.note.place(x=self.w/8,y=self.h*14/17)
        
        self.alphabet = Tk.Entry(self.master, width=26,font=('courier',10))
        self.alphabet.insert(0, "abcdefghijklmnopqrstuvwxyz")
        self.alphabet.configure(state='disabled')
        self.alphabet.pack()
        self.alphabet.place(x=self.w/5,y=self.h*15/17)
        
        self.var = Tk.StringVar()
        self.var.trace_variable("w", self.on_write)
        
        self.code = Tk.Entry(self.master,width=26,textvariable=self.var,font=('courier',10))
        self.code.pack()
        self.code.place(x=self.w/5,y=self.h*15.5/17)
        
        self.translation = Tk.Text(self.master,height=10,width=60)
        
    def on_write(self,*args):
        '''prevents user from inputting more than 26 letters in alphabet'''
        s = self.var.get()
        max_len = 26
        if len(s) > max_len:
            self.var.set(s[:max_len])
            
    def encrypt(self,ev):
        '''encodes user message and displays to screen'''
        messageinput = self.messageEntry.get("1.0",'end-1c')
        cipherinput = self.code.get()
        cipher = Code(cipherinput)
        encryption = cipher.encode(messageinput)
         
        self.translation.delete('1.0', 'end')
        self.translation.pack()
        self.translation.place(x=self.w/8,y=self.h/2)
        self.translation.insert(1.0, encryption)          
    
    def creditScreen(self,ev):
        '''enters credit screen'''
        self.clearTitleScreen()
        
        self.credittext = Tk.Label(self.master, text ='Credits',
                                  font=('courier',35), bg='black',fg='white')
        self.credittext.pack()
        self.credittext.place(x=self.w/3, y=self.h/7)
        
        self.grant = Tk.Label(self.master, text ='Designed and programmed by\n Grant Huang',
                                  font=('courier',20), bg='black',fg='white')
        self.grant.pack()
        self.grant.place(x=self.w/7, y=self.h/3)
        
        self.wall = Tk.Label(self.master, text ='''Background created by Harryarts\n  and obtained from Freepik.com''',
                                  font=('courier',20), bg='black',fg='white')
        self.wall.pack()
        self.wall.place(x=self.w/10, y=self.h/2)
        
        self.special = Tk.Label(self.master, text ='Special thanks to inventwithpython.com\n for decoding algorithm and dicionary',
                                  font=('courier',18), bg='black',fg='white')
        self.special.pack()
        self.special.place(x=self.w/15, y=self.h*2/3)
        
        self.backbutton = Tk.Button(self.master,text="Back",font=('courier',15),
                                    ba='black',fg='white',height=1,width=10)
        self.backbutton.bind("<Button-1>", self.totitle3)
        self.backbutton.pack()
        self.backbutton.place(x=self.w*7/9,y=self.h*9/10)
    
    def totitle(self,ev):
        '''returns to title screen from decode mode'''
        self.decodeInstructions.destroy()
        self.messageEntry.destroy()
        self.decryptbutton.destroy()
        self.backbutton.destroy()
        self.translation.destroy()
        self.note.destroy()
        self.alphabet.destroy()
        self.code.destroy()
        self.alphabetnote.destroy()
        
        self.retrieveTitleScreen()
    
    def totitle2(self,ev):
        '''returns to title screen from encode mode'''
        self.encodeInstructions.destroy()
        self.messageEntry.destroy()
        self.encryptbutton.destroy()
        self.backbutton.destroy()
        self.note.destroy()
        self.alphabet.destroy()
        self.code.destroy()
        self.translation.destroy()
        
        self.retrieveTitleScreen()
        
    def totitle3(self,ev):
        '''returns to title screen from credit screen'''
        self.credittext.destroy()
        self.grant.destroy()
        self.wall.destroy()
        self.backbutton.destroy()
        self.special.destroy()
        
        self.retrieveTitleScreen()
    
    def clearTitleScreen(self):
        '''hides the title screen widgets'''
        self.text.place_forget()
        self.button.place_forget()
        self.button2.place_forget()
        self.credits.place_forget()
        
    def retrieveTitleScreen(self):
        '''reshows the title screen widgets'''
        self.text.pack()
        self.text.place(x=self.w/8,y=self.h/6)
        self.button.pack()
        self.button.place(x=self.w/8,y=self.h/2)
        self.button2.pack()
        self.button2.place(x=self.w/8,y=self.h*2/3)
        self.credits.pack()
        self.credits.place(x=self.w*5.2/8,y=self.h*5/6)
        
def main():
    root = Tk.Tk()
    game = Game(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
    

   