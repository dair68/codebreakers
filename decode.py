# -*- coding: utf-8 -*-
"""
PIC16 - Spring 2018
Final Project: Game

Grant Huang
"""

import re
from makeWordPatterns import wordPattern
from wordPatterns import allPatterns
from wordPatterns import dictionary

#1. Find the word pattern for each cipherword in the ciphertext.
#2. Find the list of English word candidates that each cipherword could decrypt to.
#3. Create one cipherletter mapping for each cipherword using the cipherword’s list of candidates. (A cipherletter mapping is just a dictionary value.)
#4. Intersect each of the cipherletter mappings into a single intersected cipherletter mapping.
#5. Remove any solved letters from the intersected cipherletter mapping.

def blankLetterMap():
    '''creates ciphertext alphabet mapped to nothing'''

    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O'
                    ,'P','Q','R','S','T','U','V','W','X','Y','Z']
    
    return {i:[] for i in alphabet}

#map1 = blankLetterMap()
#print (map1)

def addLetters(mapping, codeword, plainword):
    '''adds potential plaintext letters to a mapping based on a codeword
       and a potential translation'''

    for i in range(len(codeword)):
        if plainword[i] not in mapping[codeword[i]]:
            mapping[codeword[i]].append(plainword[i])
            
def intersectMaps(map1, map2, *maps):
    '''finds the intersection in plaintext letters for multiple maps'''

    intersectMap = {}
    for k in map1:
        mappings = [set(map1[k]), set(map2[k])] + [set(m[k]) for m in maps]
        letterintersect = set()
        for m in mappings:
            if m:
                if letterintersect:
                    letterintersect = letterintersect.intersection(m)
                else:
                    letterintersect = m
        intersectMap[k] = list(letterintersect)
    return intersectMap
    
def removeSolvedLetters(intersectmap):
    '''finds letters in intersected map with only one possible translation and 
        removes instances of that translation from elsewhere in map'''
        
    mapping = dict(intersectmap)    
    loopAgain = True

    solved = []
    while loopAgain:
        #print solved
        loopAgain = False
        solved = []
        for k in mapping:
            if len(mapping[k]) == 1:
                solved.append(mapping[k][0])
        for k in mapping:
            for i in solved:
                if len(mapping[k]) != 1 and i in mapping[k]:
                    mapping[k].remove(i)
                    if len(mapping[k]) == 1: #new letter revealed, must cycle through again
                        loopAgain = True
    return mapping
            

def attemptDecryption(message, mapping):
    '''attempts to decrypt a message with a letter mapping. Ambiguous letters/
       missing letters replaced with _'''

    translation =[]

    for i in message:
        if i in mapping:
            if len(mapping[i]) == 1:
                translation.append(mapping[i][0])
            else:
                translation.append('_')
        else:
            translation.append(i)
            
    return ''.join(translation)

def cleanUp(message, decryption, mapping):
    '''attempts to fill in for _ in a decrypted message and the most current
        mapping'''
    message = message.upper()
    decryption = decryption.upper()
    
    hiddenwords = re.findall('([A-Z]+)',message) 
    translated = re.findall('([A-Z\_]+)',decryption)
    
    incomplete = {hiddenwords[i]:translated[i] for i in range(len(hiddenwords)) 
                if '_' in translated[i]}
    #print(incomplete)
    
    remainingletters = {k:mapping[k] for k in mapping if len(mapping[k]) != 1}
    #print (remainingletters)
    loopAgain = True
    
    #searches through dictionary for possible words for words containing _
    while loopAgain:
        loopAgain = False
        for w in incomplete:
            possiblewords = []
            if incomplete[w].count('_') == 1:
                #print w
                i = incomplete[w].index('_')
                possiblewords = [incomplete[w].replace('_',l)  for l in remainingletters[w[i]]]

                actualwords = [words for words in possiblewords if words in dictionary]
                #print (actualwords)
                if len(actualwords) == 1:
                    mapping[w[i]] = [actualwords[0][i]]
                    # print w
                    #print incomplete
                    incomplete.pop(w)
                    loopAgain = True
                    break
    
    #print(mapping)
    return attemptDecryption(message, mapping)
                

def masterDecode(message):
    '''attempts to decode a simple substitution cipher. Returns decoded string
        and mapping for fairly certain letters.'''

    message = message.upper()
    message = message.replace('_',' ')
    words = re.findall('([A-Za-z]+)',message)
    #print (words)

    patterns = [wordPattern(w) for w in words]
    codepatterns = {words[i]:patterns[i] for i in range(len(words))}
    #print (codepatterns)
    
    patternmap = {}
        
    for i in patterns:
        if i in allPatterns:
            patternmap[i] = allPatterns[i]
        else:
            patternmap[i] = []
            
    #print (patternmap)
    
    wordchoices = {i:patternmap[codepatterns[i]] for i in codepatterns}
    #print (wordchoices)
    
    maps = []
    
    for k in wordchoices:
        lettermap = blankLetterMap()
        for i in wordchoices[k]:
            addLetters(lettermap,k,i)
        maps.append(lettermap)
        
    #print (maps)
    intersection = intersectMaps(*maps)
    #print (intersection)
    finalmap = removeSolvedLetters(intersection)
    #print (finalmap)
    
    decryption = attemptDecryption(message, finalmap)
    finaldecryption = cleanUp(message, decryption, finalmap)
    #print (finalmap)
    while decryption != finaldecryption:
        decryption = finaldecryption
        finaldecryption = cleanUp(message, finaldecryption, finalmap)
    return finaldecryption, finalmap


def main():
    message2 = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    print(message2)
    decoded2 = masterDecode(message2)[0]
    print (decoded2)    
    
if __name__ == '__main__':
    main()



    