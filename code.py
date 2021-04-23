import os
import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


# The data structure for every element in the linked list. 
class Node:
    def __init__(self, value = None, next = None):
        self.value = value
        self.next = next

#The linked list
class LinkedList:

    def __init__(self, index=0, mode="simple"):
        self.start_node = None # Head pointer
        self.end_node = None # Tail pointer
        # Additional attributes
        self.index = index 
        self.mode = "simple"

    # Method to traverse a created linked list
    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            print("List has no element")
            return
        else:
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                traversal.append(n.value)
                n = n.next
            return traversal

    # Method to insert elements in the linked list
    def insert_at_end(self, value):
        # determine data type of the value
        if 'list' in str(type(value)):
            self.mode = "list"

        # Initialze a linked list element of type "Node" 
        new_node = Node(value)
        n = self.start_node # Head pointer

        # If linked list is empty, insert element at head
        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            return "Inserted"
        
        elif self.mode == "list":
            if self.start_node.value[self.index] >= value[self.index]:
                self.start_node = new_node
                self.start_node.next = n
                return "Inserted"

            elif self.end_node.value[self.index] <= value[self.index]:
                self.end_node.next = new_node
                self.end_node = new_node
                return "Inserted"

            else:
                while value[self.index] > n.value[self.index] and value[self.index] < self.end_node.value[self.index] and n.next is not None:
                    n = n.next

                m = self.start_node
                while m.next != n and m.next is not None:
                    m = m.next
                m.next = new_node
                new_node.next = n
                return "Inserted"
        else:
            # If element to be inserted has lower value than head, insert new element at head
            if self.start_node.value >= value:
                self.start_node = new_node
                self.start_node.next = n
                return "Inserted"

            # If element to be inserted has higher value than tail, insert new element at tail
            elif self.end_node.value <= value:
                self.end_node.next = new_node
                self.end_node = new_node
                return "Inserted"

            # If element to be inserted lies between head & tail, find the appropriate position to insert it
            else:
                while value > n.value and value < self.end_node.value and n.next is not None:
                    n = n.next

                m = self.start_node
                while m.next != n and m.next is not None:
                    m = m.next
                m.next = new_node
                new_node.next = n
                return "Inserted"

def process_file(inFile):

    fileIds = []
    tokens = []
    all_words = []
    d = {}

    with open (inFile, 'r') as inputfile:
        index = 0
        for i in inputfile:
            parts = re.split(r'\t+', i.rstrip('\t'))
            fileId = parts[0]
            token = parts[1].rstrip('\n')
            dict_entry = preprocess(token)
            fileIds.append(fileId)
            tokens.append(token)
            d[fileIds[index]] = dict_entry
            all_words.extend(dict_entry)
            index+=1
    all_words = set(all_words)

    return d,fileIds,tokens,all_words
    

def preprocess(sent):
     
    ps = PorterStemmer() 
    stop_words = set(stopwords.words('english'))   

    x2 = re.sub('[^A-Za-z0-9- ]+', '', sent)
    x = re.sub('-'," ",x2)
    inter = x.strip().lower().split(" ")
    finalrow = [ps.stem(w) for w in inter if not w in stop_words]
    
    return set(finalrow)

def process_queryFile(inFile):
    words = []
    sent = []
    with open (inFile, 'r') as inputfile:
        for i in inputfile:
            toAdd = preprocess(i)
            sent.append(i.rstrip())
            words.extend(toAdd)
    return sent,words

def get_postings(word,d):
    ret = []
    for key,value in d.items():
        if word in value:
            ret.append(int(key))
    return sorted(ret)

def get_LinkedList(li):
    retList = LinkedList()
    for x in li:
        retList.insert_at_end(x)
    
    return retList

def DaatAnd(sent,d):
    processed_words = preprocess(sent)
    retD = []
    dictD = {}
    i = 0
    for word in processed_words:
        app = get_postings(word,d)
        retD.append(app)
        dictD[word] = app

    print("dict -")
    minLen = len(retD[0])
    minKey = ""
    for k,v in dictD.items():
        if len(v) <= minLen:
            minLen = len(v)
            minKey = k
        print(k,v)
    print()
    print()
    num_comp = 0
    prev = 0
    total = 0
    for n in dictD[minKey]:
        interm_comp = 0
        for i in processed_words:
            if i != minKey:
                toComp = dictD[i]
                for b in toComp:
                    if b <= n:
                        interm_comp+=1
                    else:
                        break
        num_comp = interm_comp - prev
        prev = interm_comp
        total += num_comp + 1
        print(num_comp)
    print("num_comp - " + str(total))

    finalset = set(retD[0])

    for i in range(len(retD)):
        finalset = finalset & set(retD[i])
    
    return finalset,total

def get_sentences(inFile):
    sent = []
    with open (inFile, 'r') as inputfile:
        for i in inputfile:
            sent.append(i)
    
    return sent

def create_output(query_words,query_sent,outFile,d):
    with open (outFile, 'w') as outpufile:
        outpufile.write("{\n")
        outpufile.write("postingsList: {\n")
        d2 = {}
        for word in query_words:
            d2[word] = get_postings(word,d)
            outpufile.write(word)
            outpufile.write(":")
            outpufile.write(d2[word])
            outpufile.write("\n")
        outpufile.write("},")
        outpufile.write("daatAnd")
        for sent in query_sent:
            outpufile.write(sent)
            outpufile.write(":")
            outpufile.write("{\n")
            outpufile.write("results : ")
            x,y = DaatAnd(sent,d)
            outpufile.write(x)
            outpufile.write(",\n")
            outpufile.write("num_docs : ")
            outpufile.write(len(x))
            outpufile.write("num_comparisons : ")
            outpufile.write(y)
            outpufile.write("},")



def main():

    input_text = []
    inFile = 'input_corpus.txt'
    queryFile = 'queries.txt'

    d,fileIds,tokens,all_words = process_file(inFile)

    new_dict = {}
    new_dictLL = {}

    for word in all_words:
        postings = get_postings(word,d)
        new_dict[word] = postings
        new_dictLL[word] = LinkedList()
        for x in postings:
            new_dictLL[word].insert_at_end(int(x))
        # print(word,new_dict[word])

    query_words = process_queryFile(queryFile)
    query_sent,query_words = process_queryFile(queryFile)
    # print(query_sent, query_words)

    create_output(query_words,query_sent,d)

    for sent in query_sent:
        ans = DaatAnd(sent,d)
        print('"' + sent + '"')
        print("results : " + str(sorted(ans)))
        print("num docs : " + str(len(ans)))
        print()
main()