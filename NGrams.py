'''
Created on Feb 8th, 2016

@author: Mingzhi Yu

'''

import sys, math,copy,string,random,operator
import numpy as np

'''
N-Grams Model

This Program is an implementation of N-gram model, including
unigram, bigrams and trigrams.


Input:
    integer: the n of N-gram, which n is 1,2,3;
    file_train: training file, which is in .text
    file_test: test file, which is in .text
    file_dev: developement set for configuring threshold and lambdas

Output    
    metrics : Probility model 
    `: Perplexity of model

'''

'''
Constants
'''

totalLen = 0

unigramDict = dict()
bigramDict = dict()
trigramDict = dict()

uniDict = dict()
biDict = dict()
triDict = dict()

Threshold = 2
weightList = []
punctuation = '!"#$%&\'()*+,-.:;=?@[]^_`{|}~'



'''----------------------------------Probility Dict Generator---------------------------------'''


def Unigram():
    print "Constructing unidict..."
    global uniDict
    uniDict.clear()
    uniDict = { k : float(unigramDict[k])/totalLen for k in unigramDict}
    print "---------------UniDict-----------------"
    print uniDict
    print "Done!\n"
    return uniDict

def Bigram():
    print "Constructing Bidict..."
    global biDict
    biDict.clear()
    biDict = {pair : float(bigramDict[pair])/unigramDict[pair[0]] for pair in bigramDict}
    print "---------------BiDict-----------------"
    print biDict
    print "Done!\n"
    return biDict

def Trigram():
    print "Constructing Tridict..."
    global triDict
    triDict.clear()
    triDict = {pair : float(trigramDict[pair])/bigramDict[(pair[0],pair[1])] for pair in trigramDict}
    print "---------------TriDict-----------------"
    print triDict
    print "Done!\n"
    return triDict

        
'''----------------------------------------Main--------------------------------------------'''


def main(n,trainfile,devfile,testfile):

    retrain = True

    if n == '1':

        while (retrain == True):
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~Round~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            print "the threshold for UNK is at this time: ", Threshold
            unigramDict.clear()
            trainUnigram(trainfile)
            Unigram()  # Get unidict
            #Test on devfile in order to get proper UNK threshold
            retrain = threshold(devfile)  
            #print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            
        print "======================================Test=============================\n"
        print "UNK Threshold for test is : ", Threshold
        Pr_List = testUnigram(testfile)
        #print "---------------Pr_List------------"
        #print Pr_List
        #print " Total length of Pr_List: ", len(Pr_List)
        PP = perplexity(Pr_List)
        print "Please notice that if the perplexity is Infinity, that means the probability is extremely low."
        print "Please notice the program does not negative logrithm of the perplexity."
        print "The perplexity of the test file is: " + str(PP) 
        print "======================================Test=============================\n"
        

    elif n == '2':
        while (retrain):
            unigramDict.clear()
            bigramDict.clear()
            trainBigram(trainfile)
            Unigram()
            Bigram() # Get unidict
            retrain = threshold(devfile)
        # Test on devfile in order to get proper UNK threshold


        print "======================================Test=============================\n"
        print "UNK Threshold for test is : ", Threshold
        Pr_List = testBigram(testfile)
        temp = []
        for pr in Pr_List:
            temp.append(pr[1])
        PP = perplexity(temp)
        print "Please notice that if the perplexity is Infinity, that means the probability is extremely low."
        print "Please notice the program does not negative logrithm of the perplexity."
        print "The perplexity of the test file is: " + str(PP) 
        print "===================================================================\n"
        
    elif n == '2s':
        while (retrain) :
            unigramDict.clear()
            bigramDict.clear()
            trainBigram(trainfile)
            Unigram()  # Get unidict
            Bigram()    # Get bidict
            retrain = threshold(devfile)
        # Test on devfile in order to get the weights and proper UNK threshold
        Pr_List = testBigram(devfile)
        weightList = weight_climbing(Pr_List,2)

        # DO TEST
        print "======================================Test=============================\n"
        print "UNK Threshold for test is : ", Threshold
        print "The lambdas are : "
        print weightList[:2]
        Pr_List = testBigram(testfile)
        Pr_inter_List = interpolation(Pr_List,2)
        PP = perplexity(Pr_inter_List)
        print "Please notice that if the perplexity is Infinity, that means the probability is extremely low."
        print "Please notice the program does not negative logrithm of the perplexity."
        print "The perplexity of the test file is: " + str(PP) 
        print "===================================================================\n"
        

        
    elif n == '3':
        while (retrain) :
            unigramDict.clear()
            bigramDict.clear()
            trigramDict.clear()
            trainTrigram(trainfile)
            Unigram()  # Get unidict
            Bigram()    # Get bidict
            Trigram()  # Get tridict
            retrain = threshold(devfile)
        # Test on devfile in order to get the weights and proper UNK threshold
        Pr_List = testTrigram(testfile)
        temp = []
        for pr in Pr_List:
            temp.append(pr[2])
        PP = perplexity(temp)
        print "Please notice that if the perplexity is Infinity, that means the probability is extremely low."
        print "Please notice the program does not negative logrithm of the perplexity."
        print "The perplexity of the test file is: " + str(PP) 
        

    elif n == '3s':
        while (retrain) :
            unigramDict.clear()
            bigramDict.clear()
            trigramDict.clear()
            trainTrigram(trainfile)
            Unigram()   # Get unidict 
            Bigram()    # Get bidict
            Trigram()   # Get tridict
            retrain = threshold(devfile)
        # Test on devfile in order to get the weights and proper UNK threshold
        Pr_List = testTrigram(devfile)
        weightList = weight_climbing(Pr_List,3)

        # DO TEST
        print "======================================Test=============================\n"
        print "UNK Threshold for test is : ", Threshold
        print "The lambdas are : "
        print weightList[:3]
        Pr_List = testTrigram(testfile)
        Pr_inter_List = interpolation(Pr_List,3)
        PP = perplexity(Pr_inter_List)
        print "Please notice that if the perplexity is Infinity, that means the probability is extremely low."
        print "Please notice the program does not negative logrithm of the perplexity."
        print "The perplexity of the test file is: " + str(PP) 
        print "===================================================================\n"


    else:
        print "Error. Please re-enter your command"



'''------------------------------------Auxilary Functions------------------------------'''
def threshold(devfile):
    global Threshold
    temp = Threshold 
    curPr_List = testUnigram(devfile)
    #print "curPr_List: ",curPr_List
    curPP = perplexity(curPr_List)

    Threshold = Threshold - 1
    if Threshold <= 1: 
        Threshold = temp
        #print " Find the good threshold: ", Threshold
        return False  # true for true threshold. Which means not retrain
    
    Pr_List = testUnigram(devfile)
    PP = perplexity(Pr_List)
    #print "PP: ", PP
    #print "curPP", PP
    if curPP > PP:
        Threshold = temp
        #print " Find the good threshold: ", Threshold
        return False  # true for true threshold. Which means not retrain
    else:
        return True




def interpolation(Pr_List,n):
    Pr_inter_List = []
    
    for pr in Pr_List:

        if n == 2:
            Pr_inter = weightList[0] * pr[0] + weightList[1] * pr[1]
            Pr_inter_List.append(Pr_inter)
        else:
            Pr_inter = weightList[0] * pr[0] + weightList[1] * pr[1] + weightList[2] * pr[2]
            Pr_inter_List.append(Pr_inter)
            

    return Pr_inter_List



def weight_climbing(pr_list,ngram):
    '''
    This is a fake hill climbing algorithm to calculate the weights that maximize the
    perplexity.
    It will climb 10 times


    Input: A List of tuples. It is the (pr_uni,pr_bi,pr_tri) for a list of bigram or trigram
           Integer 2 or 3: when 2, bigram analysis. When 3, Trigram analysis
    Output: A List of lambda that will maximum the perplexity
    '''
    maxWeights = [1,1,1]
    
    maxPerplexity = 0
    Pr_inter_List = [] # a list of interpolation probability
    i = 0

    if ngram == 2:
        # Initial 
        lambda_uni = random.uniform(0,1)
        lambda_bi = 1 - lambda_uni

        for pr in pr_list:
                pr_inter = lambda_uni * pr[0] + lambda_bi * pr[1]
                Pr_inter_List.append(pr_inter)

        curPerplexity = perplexity(Pr_inter_List)


        while (curPerplexity > maxPerplexity):

            if (lambda_uni + lambda_bi > 1 or lambda_uni < 0 or lambda_bi < 0): break

            maxPerplexity = curPerplexity
            maxWeights[0] = lambda_uni
            maxWeights[1] = lambda_bi


            
            node1 = (lambda_uni + 0.1,lambda_bi-0.1)
            node2 = (lambda_uni-0.1,lambda_bi+0.1)
            nodelist= [node1,node2]


            #lambda_uni_up = lambda_uni + 0.1
            #lambda_bi_up = 1 - lambda_uni
            
            hillpoint = []
            for node in nodelist:
                uni = node[0]
                bi = node[1]
                templist = []
                
                
                for pr in pr_list:
                    pr_inter = uni * pr[0] + bi * pr[1]
                    templist.append(pr_inter)

                hillpoint.append(perplexity(templist))

            index, value = max(enumerate(hillpoint), key=operator.itemgetter(1))
            winNode = nodelist[index]


            curPerplexity = value
            lambda_uni = winNode[0]
            lambda_bi = winNode[1]

            i += 1
            #print "lambda_uni,lambda_bi have once been: ", lambda_uni, lambda_bi
                
        #print "Hill Climbing has been climbed by %i times, and then reach the local max"  % i
        

    else:
        # Initial 
        lambda_uni = random.uniform(0,1)
        lambda_bi = random.uniform(0,1 - lambda_uni)
        lambda_tri = 1 - lambda_uni - lambda_bi


        for pr in pr_list:
                pr_inter = lambda_uni * pr[0] + lambda_bi * pr[1] + lambda_tri * pr[2]
                Pr_inter_List.append(pr_inter)

        curPerplexity = perplexity(Pr_inter_List)

        while (curPerplexity > maxPerplexity):

            if (lambda_uni + lambda_bi > 1 or lambda_uni < 0 or lambda_bi < 0): break

            maxPerplexity = curPerplexity
            maxWeights[0] = lambda_uni
            maxWeights[1] = lambda_bi
            maxWeights[2] = lambda_tri
            
            node1 = (lambda_uni+0.1,lambda_bi-0.1,lambda_tri)
            node2 = (lambda_uni+0.1,lambda_bi,lambda_tri-0.1)
            node3 = (lambda_uni-0.1,lambda_bi+0.1,lambda_tri)
            node4 = (lambda_uni,lambda_bi+0.1,lambda_tri-0.1)
            node5 = (lambda_uni,lambda_bi-0.1,lambda_tri+0.1)
            node6 = (lambda_uni-0.1,lambda_bi,lambda_tri+0.1)
            nodelist= [node1,node2,node3,node4,node5,node6]

            
            hillpoint = []
            for node in nodelist:
                uni = node[0]
                bi = node[1]
                tri = node[2]
                templist = []
                
                
                for pr in pr_list:
                    pr_inter = uni * pr[0] + bi * pr[1] + tri * pr[2]
                    templist.append(pr_inter)

                hillpoint.append(perplexity(templist))

            index, value = max(enumerate(hillpoint), key=operator.itemgetter(1))
            winNode = nodelist[index]


            curPerplexity = value
            lambda_uni = winNode[0]
            lambda_bi = winNode[1]
            lambda_tri = winNode[2]

            i += 1
            #print "lambda_uni,lambda_bi,lambda_tri have once been: ", lambda_uni, lambda_bi,lambda_tri
                
        #print "Hill Climbing has been climbed by %i times, and then reach the local max"  % i

    global weightList                   
    weightList = maxWeights
    return weightList
    


def perplexity(prlist):

    denominator = 1 
    if len(prlist) == 0 :
        print "ERROR!"   
    for pr in prlist:
        if pr == 0:
            print "The probability of the whole text is 0 because there is some word's probability is 0"
            return '------Infinity------'
        else:
            denominator = denominator * (1/pr)
    print "The probability of the whole text is: ", 1/denominator
    
    if denominator == 0:
        print "The probability of the whole text is 0 because there probability is extremely low"
        return '------Infinity-------'


    else:
        perlexity = (math.pow(float(denominator),(1/len(prlist))))
        return perlexity



def pr_uni(word):
    
    #Get the Unigram probability
    p = 0
    if word != '<s>' and word !='</s>':
        p = uniDict[word]

    return p

def pr_bi(bigram):
    #Get the Bigram probability
    p = 0
    if (bigram[0],bigram[1]) in biDict:
        p = biDict[(bigram[0],bigram[1])]
    else:
        p = 0
    return p

def pr_tri(trigram):
    #Get the Trigram probability
    p = 0
    if (trigram[0],trigram[1],trigram[2]) in triDict:
        p = triDict[(trigram[0],trigram[1],trigram[2])]
    else:
        p = 0
    return p

'''------------------------------------Test Part------------------------------------'''


def testUnigram(testfile):
    '''
    Input: file - testfile
    Output: List - Probability List
    '''
    print "Opening Testing File..."
    sys.stdout.flush()

    testList = []

    testfd = open(testfile,"r+")
    print "The testfile %s is opened: " % testfd.name 
    for line in testfd:
        line = line.strip()
        if(line != ""):
            tempList = line.lower().split(" ")           
            temp = ''
            for word in tempList:                
                for punc in punctuation:
                    temp = word.replace(punc,'')
                if temp != '<s>' and temp != '</s>' and temp.isalnum():
                    if temp not in unigramDict: 
                        temp = 'UNK'                   
                    testList.append(temp)
    testfd.close()
    #print "------------TestList -----------"
    #print testList
    #print "\n"
    #print "------------Totel Length of Test List -----------"
    #print len(testList)


    
    #Get the Unigram probability
    Pr_List = []
    
    for x in range(0,len(testList)):
        Pr_uni = 0
        first = testList[x]       
        
        if first != '<s>' and first != '</s>':
            Pr_uni = pr_uni(first)
            #print "for the word: ", first, " the prob is: ", Pr_uni 
        Pr_List.append(Pr_uni)

    return Pr_List


def testBigram(testfile):
    '''
    Input: file - testfile
    Output: List - Probability List
    '''
    print "Opening Testing File..."
    
    testList = []

    testfd = open(testfile,"r+")
    print "The testfile %s is opened: " % testfd.name 
    for line in testfd:
        line = line.strip()
        if(line != ""):
            firstList = line.lower().split(" ")
            #print firstList
            tempList = []
            for word in firstList:
                if word == '<s>' or word == '</s>' or word.isalnum():
                    tempList.append(word)
            #print tempList
            temp = ''
            for word in tempList:
                for punc in punctuation:
                    temp = word.replace(punc,'')
                #print temp
                if temp not in unigramDict:
                    temp = 'UNK'
                #print temp
                testList.append(temp)
    testfd.close()
    #print "--------------TestList------------- "
    #print testList
    
    #Get the Bigram probability
    Pr_List = []
    for x in range(0,len(testList)-1):

        first = testList[x] 
        second = testList[x+1]

        Pr_uni = pr_uni(first)

        if first =='</s>' and second =='<s>':
            Pr_bi = 1
        else:        
            Pr_bi = pr_bi((first,second))
        
        #print "for the word: (", first,second,") the prob is: ", Pr_bi
        Pr_List.append((Pr_uni,Pr_bi))

    return Pr_List

def testTrigram(testfile):
    '''
    Input: file - testfile
    Output: List - Probility List 
    '''

    print "Opening Testing File..."
    sys.stdout.flush()

    testList = []

    testfd = open(testfile,"r+")
    print "The testfile %s is opened: " % testfd.name 
    for line in testfd:
        line = line.strip()
        if(line != ""):
            firstList = line.lower().split(" ")
            tempList = []
            for word in firstList:
                if word == '<s>' or word == '</s>' or word.isalnum():
                    tempList.append(word)
            temp = ''
            for word in tempList:
                for punc in punctuation:
                    temp = word.replace(punc,'')
                if temp not in unigramDict:
                    temp = 'UNK'
                testList.append(temp)
    testfd.close()
    #print "The testList is: ", testList
    
    #Get the probability List
    Pr_List = []
    for x in range(0,len(testList)-2):

        first = testList[x] 
        second = testList[x+1]
        third = testList[x+2]

        Pr_uni = pr_uni(first)

        if first =='</s>' and second =='<s>':
            Pr_bi = 1
            Pr_tri = 1
        
            

        elif second =='</s>' and third =='<s>':
            Pr_tri = 1
        
        else:
            Pr_tri = pr_tri((first,second,third))
            Pr_bi = pr_bi((first,second))

 
        Pr_List.append((Pr_uni,Pr_bi,Pr_tri))
        #print "for trigram: (",first,second,third, ") the prob is: ", Pr_tri

    return Pr_List
        
'''--------------------------------------------Train Part--------------------------------------'''    

def trainTrigram(trainfile):
    '''
    Read the file and preprocess the string input.
    '''
    trainList = []
    filebuffer = ''



    '''
    Train Trigram on training File
    '''
    print "Opening Training File..."
    sys.stdout.flush()
    
    trainfd = open(trainfile,"r+")
    print "The trainfile %s is opened: " % trainfd.name
    for line in trainfd:
        if (len(line.strip())!=0):
            filebuffer += line.strip()

    #print filebuffer

    sentences = filebuffer.split('</s>')
    #print sentences

    for s in sentences:
        if (s!=''):
            s = s + '</s>'
            List = s.split(' ')
            for word in List:
                for punc in punctuation:
                    word = word.replace(punc,'')
                trainList.append(word)

    tempList = copy.deepcopy(trainList)
    trainfd.close()
    print "Done!"

    #print tempList
    #Read word into unigram
    for x in tempList:
        if x not in unigramDict:
            unigramDict[x] = 0
        unigramDict[x] += 1
    unigramDict['UNK'] = 0 #Add UNK to dict
    print "Done!"           

      
    # Threshold Delete
    print "Replacing all infrequent words with UNK token...\n"
    toDelete = []
    for key in unigramDict:
        if unigramDict[key] < Threshold and key != 'UNK':
            unigramDict['UNK'] += unigramDict[key]
            toDelete.append(key)
    for key in toDelete:
        del unigramDict[key]
        for i,v in enumerate(tempList):
            if v == key:
                tempList[i] = 'UNK'

            

    #Read tuples into bigram dic
    for x in range(0,len(tempList)-1):
        first = tempList[x]
        second = tempList[x+1]
        if (first,second) not in bigramDict:
            bigramDict[(first,second)] = 0
        bigramDict[(first,second)] += 1

    # Remove the tuple of ('<s>','</s>') from bigram
    if bigramDict[('</s>','<s>')] > 0:
        del bigramDict[('</s>','<s>')]



    #Read tuples into trigram dic
    wrap = 0 
    for x in range(0,len(tempList)-2):
        first = tempList[x]
        second = tempList[x+1]
        third = tempList[x+2]
        # Remove the tuple of ('<\s>','<s>', 'Some word')
        #                     ('some word', <s>','</s>',)
        if first == '</s>' and second == '<s>':
            wrap += 1
        elif second == '</s>' and third == '<s>':
            wrap += 1
        else:
            if (first,second,third) not in trigramDict:
                trigramDict[(first,second,third)] = 0
            trigramDict[(first,second,third)] += 1


      

    print "----------------------------------------"
    print "             unigram                    "
    print unigramDict
    print "/n"
    print "----------------------------------------"
    print "             bigram                   "
    print bigramDict
    print "/n"
    print "----------------------------------------"
    print "             trigram                    "
    print trigramDict

  
    global totalLen
    vocabLen = len(bigramDict)
    totalLen = len(trainList) 
 
        
    print "----------------------------------------"
    print ("    Bigram size: %d" % vocabLen)
    print ("    Total words: %d" % totalLen)
    print "----------------------------------------"

            
    print "Done!"


    

def trainBigram(trainfile):
    '''
    Read the file and preprocess the string input.
    '''
    trainList = []
  
    
    '''
    Train bigram on training File
    '''
    print "Opening Training File..."
    sys.stdout.flush()
    filebuffer = ''
    trainList = []
    
    trainfd = open(trainfile,"r+")
    print "The trainfile %s is opened: " % trainfd.name
    for line in trainfd:
        if len(line.strip())!=0:
            filebuffer += line.strip()
            #tempList = []
            #line = '<s> ' + line.strip() + ' </s>'
    sentences = filebuffer.split(" </s>")
    for s in sentences:
        #print s
        s = s + ' ' + '</s>'
        #print s
        List = s.split(" ")
        #print List
        for word in List:
            for punc in punctuation:
                word = word.replace(punc,'')
            if word == '<s>' or word == '</s>' or word.isalnum():
                trainList.append(word)
    #print trainList
    tempList = copy.deepcopy(trainList)
    trainfd.close()
    print "Done!"

    # Read item into unigram dic
    for item in tempList:
        if item not in unigramDict:
            unigramDict[item] = 0
        unigramDict[item] += 1
    unigramDict['UNK'] = 0 #Add UNK to dict


    # To avoid conflict with destructive deletion of keys, we create a buffer
    # of keys to be deleted later (namely after we exit the loop).
    print "Replacing all infrequent words with UNK token..."
    sys.stdout.flush()
    toDelete = []
    for key in unigramDict:
        if unigramDict[key] < Threshold and key != 'UNK':
            unigramDict['UNK'] += unigramDict[key]
            toDelete.append(key)
    for key in toDelete:
        del unigramDict[key]
        for i,v in enumerate(tempList):
            if v == key:
                tempList[i] = 'UNK'
    #delete <s> and </s> from unigram



    # Read tuples into bigram dic
    for x in range(0,len(tempList)-1):
        first = tempList[x]
        second = tempList[x+1]
        if (first,second) not in bigramDict:
            bigramDict[(first,second)] = 0
        bigramDict[(first,second)] += 1

    print "---------bigramDict-------------"
    print bigramDict
    # Remove the tuple of ('<s>','</s>')
    if bigramDict[('</s>','<s>')] >= 0:
        del bigramDict[('</s>','<s>')]


    
    print "----------------------------------------"
    print "             unigram                    "
    print unigramDict
    print "/n"
    print "----------------bigramDict-----------------------"
    print bigramDict
   
    global totalLen
    vocabLen = len(bigramDict)
    # We don't count <s> and </s>
    totalLen = len(trainList)
    # Del <s> and </s>

 
        
    print "----------------------------------------"
    print ("    Vocabulary size: %d" % vocabLen)
    print ("    Total words: %d" % totalLen)
    print "----------------------------------------"

            
    print "Done!"



def trainUnigram(trainfile):
    
    '''
    Read the file and preprocess the string input.
    '''

    '''
    Train unigram on training File...
    '''
    print "Opening Training File..."
    
    trainList = []
    devList = []
    filebuffer = ''
        
    trainfd = open(trainfile,"r+")
    print "The file %s is opened: " % trainfd.name
    for line in trainfd:
        #print line
        filebuffer += line
            #tempList = []
            #line = '<s> ' + line.strip() + ' </s>'
    sentences = filebuffer.split(" </s>")

    for s in sentences:
        #print s
        s = s + ' ' + '</s>'
        #print s
        templist = s.split(" ")
        for word in templist:
            for punc in punctuation:
                word = word.strip().replace(punc,'')
            if word != '':
                trainList.append(word)
    if len(trainList) == 0: return
    #print "------------TrainList -----------"
    #print trainList
    #print "Done!"

    
    '''
    Reading unigram on training file
    '''

    print "Train trainig corpus"
    for item in trainList:
        if item not in unigramDict:
            unigramDict[item] = 0
        unigramDict[item] += 1
    unigramDict['UNK'] = 0 #Add UNK to dict
    #print "Done!"
  
    print "Replacing all infrequent words with UNK token...\n"
    sys.stdout.flush()
    toDelete = []
    for key in unigramDict:
        if unigramDict[key] < Threshold and key != 'UNK':
            unigramDict['UNK'] += unigramDict[key]
            toDelete.append(key)
    for key in toDelete:
        del unigramDict[key]


    print "----------------------------------------"
    print "             unigram                    "
    print unigramDict

    
    
    vocabLen = len(unigramDict)
    global totalLen
    totalLen = len(trainList)

    print "----------------------------------------"
    print ("    Vocabulary size: %d" % vocabLen)
    print ("    Total words: %d" % totalLen)
    print "----------------------------------------"

        
    
    


if __name__ == "__main__":
    if len(sys.argv) == 5:
        print "Usage:",        
        main(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4])
    else:
        print "Error"
        exit(0)
