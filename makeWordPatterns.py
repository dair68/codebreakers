# -*- coding: utf-8 -*-
"""
PIC16 - Spring 2018
Final Project: Game

Grant Huang 
"""

import pprint

def wordPattern(word):
    '''converts string of letters into numbers, with each distinct letter 
       assigned a number. e.g. puppy -> 0.1.0.0.2'''

    pattern = []
    letters = {}
    w = word.upper()
    for i in w:
        if i not in letters:
            letters[i] = str(len(letters))
        pattern.append(letters[i])
            
    return '.'.join(pattern)

#word = 'Puppy'
#print (wordPattern(word))

def main():
    dictionary = open('tweakeddictionary.txt')
    words = dictionary.read()
    words = str.split(words.upper(),'\n')
    dictionary.close()
    
    allPatterns = {}

    for w in words:
        p = wordPattern(w)
        if p not in allPatterns:
            allPatterns[p] = []
        allPatterns[p].append(w)
        
    #print(allPatterns)

    p_dict = open('wordPatterns.py', 'w')
    p_dict.write('allPatterns = ')
    p_dict.write(pprint.pformat(allPatterns))
    p_dict.write('\ndictionary = ')
    p_dict.write(pprint.pformat(words))
    p_dict.close()

if __name__ == '__main__':
    main()