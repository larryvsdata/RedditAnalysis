# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 19:54:40 2017

@author: Erman
"""


    
import csv
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


subjectBodyDict={}
wordDict={}
bodies=[]
personDict={}
subjectPersonDict={}
personTopicDict={}


def getPersonTopicDict(author,subject,personTopicDict):
    if author in personTopicDict:
        incrementToDict(subject,personTopicDict[author])
    else:
        dummy={}
        personTopicDict[author]=dummy
        incrementToDict(subject,personTopicDict[author])
        
    return personTopicDict
    


def formSubjectPersonDict(author,body,subject,subjectPersonDict):
    
    if subject in subjectPersonDict:
        personDict=subjectPersonDict[subject]
        personDict=getPersonDict(author,body,personDict)
        subjectPersonDict[subject]=personDict
    else:
        personDict={}
        personDict=getPersonDict(author,body,personDict)
        subjectPersonDict[subject]=personDict
        
    return subjectPersonDict

def getMaxPerSubjectnPerson(word,subject,subjectPersonDict):
        personDict=subjectPersonDict[subject]
        return getMaxWPerP(word,personDict)

def formWDict(body,wDict):
    
    body=body.split()
    for word in body :
        word=word.lower()
        word=cleanUpPunct(word)
        if not isStop(word):
            incrementToDict(word,wDict)
    return wDict

def addToDict(key,value,Dictionary):
    if key in Dictionary:
        Dictionary[key].append(value)
    else:
        Dictionary[key]=[value]

    return Dictionary
 
      

def incrementToDict(key,Dictionary):
    if key in Dictionary:
        Dictionary[key]+=1
    else:
        Dictionary[key]=1

    return Dictionary     
    
    
def checkPunctuation(letter):
    if letter=='.' or letter==',' or letter=='?' or letter=='!' or letter=='"' or letter==':'or letter==' 'or letter==';'or letter=='\n'or letter=='\t':
        return True
    else:
        return False
    
        
def cleanUpPunct(word):
    letterList=""
    for ii in range(len(word)):
        if not checkPunctuation(word[ii]):
            letterList=letterList+word[ii]
            
    return letterList
    
    
def brushBody(body_split):
    newBody=[]
    for word in body_split:
        word=word.lower()
        word=cleanUpPunct(word)
        newBody.append(word)
    return newBody

def differenceQuery(word,dict1,dict2):
    
    try:
        value=dict2[word]-dict1[word]
    except:
        return 0
    
    return value

    

def plotBars(xlabel,ylabel,wordValues,CommonWordList,worddDict,rDict):
    sent_series = pd.Series.from_array(wordValues) 


    plt.figure(figsize=(102, 15))
    ax = sent_series.plot(kind='bar')
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    rects = ax.patches
    labels = []
    i=0
#    label=""

    for rect in rects:
            height=wordValues[i]
            try:
                words=rDict[height]
                for word in words:
                    if word not in labels:
                        labels.append(word)
                        label=word
                        break
            except:
                print ""
            ax.text(rect.get_x() + rect.get_width()/2, height , label, ha='center', va='bottom')
            i=i+1
            
            
            
            
def getReverseDict( wDict):
    reverseDict={}
    for word in wDict:
        wValue=wDict[word]
        if wValue not in reverseDict:
            reverseDict[wValue]=[word]
        else:
            reverseDict[wValue].append(word)
    return reverseDict
    
def getCommonWords(maxNum,worddDict):    
    wordValues=worddDict.values()
    
    
    wordValues.sort(reverse=True)
    wordValues=wordValues[0:maxNum]
    
    RevDict=getReverseDict( worddDict)
    CommonWordList=[]
    
    for ii in range(maxNum):
        word=RevDict[wordValues[ii]]
        if word not in CommonWordList:
            CommonWordList.append( RevDict[wordValues[ii]])    
            
    return [CommonWordList,wordValues]


def isStop(word):

    stop1 = stopwords.words('english')
    stop2=["i","he's","she's","it's","i'm","don't","that's","can't","it","  ","I", "i "," i","a","the","to","is","she","but","we","and","has","of","in","that","this","of","not"," ",""]
    stop3=["-","would","us","something","going","also","go","didn't","said","i've","yes","yeah","doesn't","[deleted]","[deleted]}"]
    if word in stop1 or word in stop2 or word in stop3:
        return True
    else:
        return False

def getOccurrances(bodies,maxNum,commonWordList):
    
    occurrances=np.zeros([maxNum,maxNum])
    
    for ii in range(maxNum):
        for jj in range (ii+1,maxNum):
            for body in bodies:
                body_split=body.split()
                body_split=brushBody(body_split)
                word1=commonWordList[ii][0]
                word2=commonWordList[jj][0]
#                print word1,word2,body_split,word1 in body_split,word2 in body_split,"\n"
                if word1 in body_split and word2 in body_split:
                    occurrances[ii][jj]=occurrances[ii][jj]+1.0
#                    print "xx"
    
    
    return occurrances
    
    
def getOccurrances2(bodies,pList,nList,keyList):
    keyLength=len(keyList)
    pLength=len(pList)  
    nLength=len(nList)
    pOccurrances=np.zeros([keyLength,pLength])
    nOccurrances=np.zeros([keyLength,nLength])
    
    for ii in range(keyLength):
        for jj in range (pLength):
            for body in bodies:
                body_split=body.split()
                body_split=brushBody(body_split)
                word1=keyList[ii]
                word2=pList[jj]
#                print word1,word2,body_split,word1 in body_split,word2 in body_split,"\n"
                if word1 in body_split and word2 in body_split:
                    pOccurrances[ii][jj]=pOccurrances[ii][jj]+1.0

    for ii in range(keyLength):
        for jj in range (nLength):
            for body in bodies:
                body_split=body.split()
                body_split=brushBody(body_split)
                word1=keyList[ii]
                word2=nList[jj]
#                print word1,word2,body_split,word1 in body_split,word2 in body_split,"\n"
                if word1 in body_split and word2 in body_split:
                    nOccurrances[ii][jj]=nOccurrances[ii][jj]+1.0

    return [pOccurrances,nOccurrances]


    
def getTotalCount(commonWordList,wDict):
    total=0
    for word in commonWordList:
        total=total+wDict[word[0]]
    return total
    
def getTotalCount2(llist,wDict):
    total=0
    for word in llist:
        if word in wDict:
            total=total+wDict[word]
    return total

def getPmiMatrix(commonWordList,wDict,maxNum,occurrances):    
    pmiMatrix=np.zeros([maxNum,maxNum])
    total=getTotalCount(commonWordList,wDict)
    
    for ii in range(maxNum):
        for jj in range (ii+1,maxNum):
            pmiMatrix[ii][jj]=math.log(total*occurrances[ii][jj]/(wordDict[commonWordList[ii][0]]*wordDict[commonWordList[jj][0]]))
    
    return pmiMatrix
    
def getWordLists(cutoff):
    with open('word_scores.txt','r') as infile:
        text_in=infile.readlines()
       
    positives=[]
    negatives=[]
    
    
    for str in text_in:
        oneSent=str.split("\n")
        oneSentString=oneSent[0]
        sss=oneSentString.split("\t")
         
        if int(sss[1])>cutoff:
            positives.append(sss[0])
        elif int(sss[1])<-cutoff:
            negatives.append(sss[0])
            
    return [positives,negatives]
            
def getKeywordPmi(wDict,cutoff,bodies):
    [positives,negatives]=getWordLists(cutoff)
    keyWords=["reddit","ron","paul","government","bush"]
    total1=getTotalCount2(positives,wDict)
    total2=getTotalCount2(negatives,wDict)
    total3=getTotalCount2(keyWords,wDict)
    total=total1+total2+total3
    
    keyLength=len(keyWords)
    pLength=len(positives)  
    nLength=len(negatives)
#    print total1,total2,total3
    
    [pOccurrances,nOccurrances]= getOccurrances2(bodies,positives,negatives,keyWords)
#    print pOccurrances,nOccurrances
    
    positivesPmi=np.zeros([keyLength,pLength])
    negativesPmi=np.zeros([keyLength,nLength])
    
    for ii in range(keyLength):
        for jj in range (ii+1,pLength):
            try:
                if (pOccurrances[ii][jj]>0 and wordDict[keyWords[ii]]>0 and wordDict[positives[jj]]>0) :
                    positivesPmi[ii][jj]=math.log(1.0*total*pOccurrances[ii][jj]/(wordDict[keyWords[ii]]*wordDict[positives[jj]]))
#                    print positivesPmi[ii][jj]
            except:
                positivesPmi[ii][jj]=0.0
       
    for ii in range(keyLength):
        for jj in range (ii+1,nLength):
            try:
                if (nOccurrances[ii][jj]>0 and wordDict[keyWords[ii]]>0 and wordDict[negatives[jj]]>0): 

                    negativesPmi[ii][jj]=math.log(1.0*total*nOccurrances[ii][jj]/(wordDict[keyWords[ii]]*wordDict[negatives[jj]]))
            except:
                negativesPmi[ii][jj]=0.0
    return [positivesPmi,negativesPmi]



    
def getDifference(wList1,wList2):
    length1=len(wList1)
    length2=len(wList2)
    length=min(length1,length2)
    
    difference=0.0
    for ii in range(length):
        if not getCoincidence(wList1[ii],wList2[ii]):
            difference+=1.0
#            print wList1[ii]
    return (difference/float(length))

    
def getCoincidence(List1,List2):
    result=False
    
    for element in List1:
        if element in List2:
            result=True
            break
    return result
    



def getPersonDict(author,body,personDict):
         
    dummy={}
    if author not in personDict:
            personDict[author]=dummy
            
    
    body_split=body.split()
    for word in body_split:
            word=word.lower()
            word=cleanUpPunct(word)
            if not isStop(word)  :
                                
                wDict=personDict[author]
                if not(word=="" or word=="-"):
                    if wDict.has_key(word):
                        wDict[word]+=1
                    else:
                        wDict[word]=1 
                    
                    personDict[author]=wDict
                    

                
    return personDict   
    
def getDictofSubject(subject,subjectBodyDict):
    bodies=subjectBodyDict[subject]
    wordDict={}    

    for body in bodies:
        body_split=body.split()
        for word in body_split:
            word=word.lower()
            word=cleanUpPunct(word)
            if not isStop(word)  :
                wordDict=incrementToDict(word,wordDict)

    
    return wordDict
    
    
def getMaxWPerP(word,pDict):
    occurrance=0
    
    for dictionary in pDict:
        personListDict=pDict.values()
        for dictionary2 in personListDict:
            try:
                
                number=dictionary2[word]
            except:
                number=0
#            print number  
            if number>occurrance:
                occurrance=number
    
    return occurrance
    
def totalNoise2(wordDict,commonWordList,epsilon,pDict):
    import numpy as np
    newDict=wordDict.copy()
    epsilon=1.0*epsilon/len(commonWordList)
    for wList in commonWordList:
        
        for word in wList:
            
            delta=getMaxWPerP(word,pDict)
            noise=math.fabs(np.random.laplace(delta,1/epsilon))
#            factor=math.fabs(np.random.laplace(0,epsilon))
            #factor=math.fabs(delta*epsilon)

            print newDict[word]
            newDict[word]+=int(noise)
#            print newDict[word]
            print noise
    return newDict
    

#############################################
files=['RC_2007-10','RC_2007-11','RC_2007-12']
#files=['RC_2007-10']
wordDict={} 

for fil in files:

    with open(fil) as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
#            print row   
#            print "\n"
            subjectFound=False
            bodyFound=False
            authorFound=False
            
            for item in row:
                item_splt=item.split(":")
                if item_splt[0]=="subreddit":
                    subject=item_splt[1]
                    subjectFound=True

                elif item_splt[0]=="id":
                    try:
                        idd=item_splt[1]
                    except:
                        print "list error"
                elif item_splt[0]=="parent_id":
                    try:
                        parent_id=item_splt[1]
                    except:
                        print "parent id error"
                elif item_splt[0]=="subreddit_id":
                    subreddit_id=item_splt[1]
                elif item_splt[0]=="author":
                    author=item_splt[1]
                    authorFound=True
#                    print author
                elif item_splt[0]=="score":
                    score=item_splt[1]
                elif item_splt[0]=="name":
                    name=item_splt[1]
                    
                elif item_splt[0]=="score_hidden":
                    score_hidden=item_splt[1]  
                elif item_splt[0]=="body" :
                    bodyFound=True
                    try:
                        body=item_splt[1] 
                    except:
                        bodyFound=False
                    if body !="[deleted]" and body !='"[deleted]"' and body !='[deleted]}'and bodyFound:
                        if subjectFound:
                                addToDict(subject,body,subjectBodyDict)
                            
                                wordDict=formWDict(body,wordDict)                
                                bodies.append(body)
                                if authorFound:
                                    personDict=getPersonDict(author,body,personDict)
                                    subjectPersonDict=formSubjectPersonDict(author,body,subject,subjectPersonDict)
                                    personTopicDict=getPersonTopicDict(author,subject,personTopicDict)





import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

maxNum=20
#[CommonWordList,wordValues]=getCommonWords(maxNum,wordDict)
#occurrances=getOccurrances(bodies,maxNum,CommonWordList)   
#pmiMatrix=getPmiMatrix(CommonWordList,wordDict,maxNum,occurrances)
#    

#Original
[CommonWordListOr,wordValuesOr]=getCommonWords(maxNum,wordDict)
epsilon=1.0
#
newDictOrNoised=totalNoise2(wordDict,CommonWordListOr,epsilon,personDict)
#
[CommonWordListOrNoised,wordValuesOrNoised]=getCommonWords(maxNum,newDictOrNoised)
#print getDifference(CommonWordListOrNoised,CommonWordListOr) 
#

print "STOP"
reverseDictionaryOr=getReverseDict(wordDict)
plotBars("Words","Number of Occurances",wordValuesOr,CommonWordListOr,wordDict,reverseDictionaryOr)

reverseDictionaryNoised=getReverseDict(newDictOrNoised)
plotBars("Words","Number of Occurances",wordValuesOrNoised,CommonWordListOrNoised,newDictOrNoised,reverseDictionaryNoised)

#

##


##Word Cloud
#reverseDictionary1=getReverseDict(wordDict)
#plotBars("Words","Number of Occurances",wordValues,CommonWordList,wordDict,reverseDictionary1)
#[positivesPmi,negativesPmi]=getKeywordPmi(wordDict,3,bodies)



#Subject Dictionaries
subjectDict=getDictofSubject('"politics"',subjectBodyDict)
reverseDictionaryS=getReverseDict(subjectDict)
[CommonWordListS,wordValuesS]=getCommonWords(maxNum,subjectDict)
plotBars("Words","Number of Occurances",wordValuesS,CommonWordListS,subjectDict,reverseDictionaryS)

#
subjectDictNoised=totalNoise2(subjectDict,CommonWordListS,epsilon,subjectPersonDict['"politics"'])
reverseDictionarySNoised=getReverseDict(subjectDictNoised)

[CommonWordListSNoised,wordValuesSNoised]=getCommonWords(maxNum,subjectDictNoised)
plotBars("Words","Number of Occurances",wordValuesSNoised,CommonWordListSNoised,subjectDictNoised,reverseDictionarySNoised)

#print getDifference(CommonWordListS,CommonWordListSNoised) 
#
#



