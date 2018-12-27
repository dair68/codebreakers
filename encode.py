# -*- coding: utf-8 -*-
"""
PIC16 - Spring 2018
Final Project: Game

Grant Huang
"""

import random as rand

class Code(object):
    '''creates a simple substitution cipher'''
    
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O'
                    ,'P','Q','R','S','T','U','V','W','X','Y','Z']
    
    def __init__(self, letters='abcdefghijklmnopqrstuvwxyz'):
        '''
        turns a string of up to 26 lowercase letters/underscores L1L2L3...L24L25L26 into cipher
        where a=L1, b=L2, c=L3,...,x=L24,y=L25,z=L26.
        '''
    
        cipherbet = letters.upper()
        if len(cipherbet) < 26:
            cipherbet = cipherbet + '_'*(26 - len(cipherbet))
            
        self.code = {Code.alphabet[i]:cipherbet[i] for i in range(len(cipherbet))}
        self.translation = {self.code[k]:k for k in self.code}
       
    def encode(self,message):
        '''encodes a message'''
        encrypted = []
        
        for char in message:
            if char.upper() in self.code:
                encrypted.append(self.code[char.upper()])
            else:
                encrypted.append(char)
                
        return ''.join(encrypted)
    
    def decode(self,message):
        '''decodes a message'''
        decrypted = []
        
        for char in message:
            if char.upper() in self.translation:
                decrypted.append(self.translation[char.upper()])
            else:
                decrypted.append(char)
                
        return ''.join(decrypted)
        
#reverse = 'zyxwvutsrqponmlkjihgfedcba'
#atbash = Code(reverse)
#print atbash.code
#print atbash.translation
#
#message = 'hello world'
#hidden = atbash.encode(message)
#print hidden
#
#print atbash.decode(hidden)

    
class Shift(Code):
    '''Creates a shift cipher aka Caesar cipher'''
    
    def __init__(self, n, direction='left'):
        '''
        Creates a shift code, where each letter is substituted with with the nth
        letter to the left or the right. e.g. for Caesar Cipher:
            
            ABCDEFGHIJKLMNOPQRSTUVWXYZ
            xyzabcdefghijklmnopqrstuvw 
            
            each letter is substituted with the 3rd letter to the left. 
            Note that A,B, and C have their ciphertext wrap around to x,y,z.
        '''
    
        shifted = ''
        if direction == 'left':
            #shifted = [alphabet[(i-n)%26].lower() for i in range(len(alphabet))]
            for i in range(len(self.alphabet)):
                shifted = shifted + self.alphabet[(i-n)%26].lower()
        else:
            for i in range(len(self.alphabet)):
                shifted = shifted + self.alphabet[(i+n)%26].lower()
        
        #print shifted
        super(Shift,self).__init__(shifted)
    
#caesar = Shift(3)
#print caesar.code
#print caesar.translation
#text = 'The quick brown fox jumps over the lazy dog.'
#hidden = caesar.encode(text)
#print hidden
#print caesar.decode(hidden)

class Atbash(Code):
    '''creates the atbash i.e. reversed alphabet cipher'''
    
    def __init__(self):
        '''creates cipher where A=z, B=y, C=x, ..., Y=b, Z=a'''
        
        reverse = 'zyxwvutsrqponmlkjihgfedcba'
        super(Atbash,self).__init__(reverse)
    
#reverse = Atbash()
#word = 'wizard'
#print reverse.encode(word)
#print reverse.decode('irk')

class Keyword(Code):
    '''Generates cipher from a keyword'''
    
    def __init__(self, word):
        '''
        places keyword with repeat letters removed at beginning of alphabet
        to create cipher. subsequent letters are just the remaining alphabet
        letters in order. 
           
        e.g. if the word is OCTOBER, the ciphertext is octberadfghjiklmnpqsuvwxyz
        '''
        
        edit = []
        for i in word:
            if i.upper() in self.alphabet and i not in edit:
                edit.append(i)
        edit = ''.join(edit)
        edit = edit.upper()
        
        letters_left = [i for i in Code.alphabet]
        cipher = []
        for i in edit:
            cipher.append(i)
            if i in letters_left:
                letters_left.remove(i)
        
        if letters_left:
            for i in range(len(cipher)):
                if cipher[i] == '-':
                    cipher[i] = letters_left[0]
                    letters_left.pop(0)
            while letters_left:
                cipher.append(letters_left[0])
                letters_left.pop(0)
                
       # print cipher
        cipher = ''.join(cipher)
        super(Keyword,self).__init__(cipher)

#kryptos = Keyword('Kryptos')
#print kryptos.code
#text = 'knowledge is power!'
#print kryptos.encode(text)
        
class RandCode(Code):
    '''creates a random simple substitution cipher'''
    
    def __init__(self):
        '''Randomly assigns one-to-one cipher text to plaintext alphabet'''
        
        randomized = rand.sample(self.alphabet, len(self.alphabet))
        super(RandCode,self).__init__(randomized)

#wildcard = RandCode()
#print wildcard.code.values()
#print Code.alphabet
        
def main():     
    shift = Code('xyzabcdefghijklmnopqrstuvw')
    message = '''To be, or not to be: that is the question:
    Whether ‘tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune,
    Or to take arms against a sea of troubles,
    And by opposing end them? To die: to sleep;
    No more; and by a sleep to say we end
    The heart-ache and the thousand natural shocks
    That flesh is heir to, ‘tis a consummation
    Devoutly to be wish’d. To die, to sleep;
    To sleep: perchance to dream: ay, there’s the rub;
    For in that sleep of death what dreams may come'''
    print (message)
    print (shift.encode(message))
    
if __name__ == '__main__':
    main()
