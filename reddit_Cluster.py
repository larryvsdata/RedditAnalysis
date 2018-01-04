# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 12:05:11 2017

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
subjectList=[]
personList=[]



def addToList(val,myList):
    if val not in myList:
        myList.append(val)

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
    
    
    
    
def getReverseDict( wDict):
    reverseDict={}
    for word in wDict:
        wValue=wDict[word]
        if wValue not in reverseDict:
            reverseDict[wValue]=[word]
        else:
            reverseDict[wValue].append(word)
    return reverseDict
    
    
    
    
def isStop(word):

    stop1 = stopwords.words('english')
    stop2=["i","he's","she's","it's","i'm","don't","that's","can't","it","  ","I", "i "," i","a","the","to","is","she","but","we","and","has","of","in","that","this","of","not"," ",""]
    stop3=["-","would","us","something","going","also","go","didn't","said","i've","yes","yeah","doesn't","[deleted]","[deleted]}"]
    if word in stop1 or word in stop2 or word in stop3:
        return True
    else:
        return False
        
        
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
                                    addToList(subject,subjectList)
                                    addToList(author,personList)

##################################
#CLUSTERING

subjectList=['"programming"','"politics"','"science"','"business"','"gaming"','"entertainment"','"sports"']


def getFeaturesMatrix(subjectList,personList,personTopicDict):
    
    subjectLength=len(subjectList)
    personLength=len(personList)
    
    
    
    X=np.zeros([personLength,subjectLength])
    
    for ii in range(personLength):
        for jj in range(subjectLength):
            subject=subjectList[jj]
            author=personList[ii]
            
            try:
                X[ii][jj]=X[ii][jj]+1.0*personTopicDict[author][subject]
            except:
                continue
    return X

def checkLength(Row,cutOff):
    sum=0.0
    for item in Row:
        sum+=item*item
    if math.sqrt(sum)>=cutOff:
        return True
    else:
        return False
        
def normalizeRow(Row):
    sum=0.0
    for item in Row:
        sum+=item*item
    normalized=math.sqrt(sum)
#    print Row,normalized
    for ii in range(len(Row)):
        Row[ii]=Row[ii]/normalized
#    print Row,normalized
    return Row

def redefineMatrix(X,cutOff):
    
    
    Xp=np.zeros([1,len(X[1,:])])
    
    for ii in range(len(X[:,1])):
        if checkLength(X[ii,:],cutOff):
            Xp=np.vstack((Xp, X[ii,:]))
    Xp=np.delete(Xp, 0, 0)  
    for ii in range(len(Xp[:,1])):    
        Xp[ii,:]=normalizeRow(Xp[ii,:])

    return Xp

def getSquareDifference(row1,row2):
    error=0.0
    for ii in range(len(row1)):
        error+= (row1[ii]-row2[ii])**2
    return error

def calculateError(labels,centers,fMatrix):
    error=0.0
    for ii in range(len(labels)):
        label=labels[ii]
        center=centers[label]
        location=fMatrix[ii,:]
        error+=getSquareDifference(center,location)
    return error
    
def optimizeClusterN(clusterNStart,ClusterNEnd,fMatrix):  
    from sklearn.cluster import KMeans
    delta=0.05
    error=100000.0
    clNumber=0
    labelsFinal=[]
    centersFinal=[]
    for clusterNumber in range(clusterNStart,ClusterNEnd):
        kmeans = KMeans(n_clusters=clusterNumber, random_state=0).fit(fMatrix)
        labels=kmeans.labels_
        centers=kmeans.cluster_centers_
        errorFound=calculateError(labels,centers,fMatrix)
#        print errorFound
        if errorFound<error:
            if math.fabs(error-errorFound)/error<delta:
                error=errorFound
                labelsFinal=labels
                centersFinal=centers
                clNumber=clusterNumber
                break
            else:
                error=errorFound
                labelsFinal=labels
                centersFinal=centers
                clNumber=clusterNumber
         
        
            
    return labelsFinal,centersFinal,clNumber
    
    
def getTagsOfCenters(centers):
       midTags=["Programmer","Political","Curious","Businessman","Gamer","Leisure Person","Sportive"]
       highTags=["Serious Coder","Activist","Scientist","Boss","Nerd","Super Outgoing","Sports Freak"]
       
       cutOff1=0.25
       cutOff2=0.75
       tagsList=[]
       for ii in range(len(centers[:,1])):
           str=""
           for jj in range(len(centers[1,:])):
               if centers[ii,jj]>cutOff1:
                   if centers[ii,jj]>cutOff2:
                       str+=" "+highTags[jj]
                   else:
                       str+=" "+midTags[jj]
    
           if str=="":
                str="Featureless"
           tagsList.append(str)
       return tagsList

       
def tagUsers(labels,tagsList):
    userTags=[]
    for ii in range(len(labels)):
        userTags.append(tagsList[labels[ii]])
    
    return userTags

###########################################
#sklearn
from sklearn.cluster import KMeans
cutOff=10.0
featsMatrix1=getFeaturesMatrix(subjectList,personList,personTopicDict)
featsMatrix2=redefineMatrix(featsMatrix1,cutOff)


clusterBottom=2
clusterTop=50
[labelsFinal,centersFinal,clusterNumber]=optimizeClusterN(clusterBottom,clusterTop,featsMatrix2)


tagsList=getTagsOfCenters(centersFinal)
userTags=tagUsers(labelsFinal,tagsList)
