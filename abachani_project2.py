import os
import re
import sys
import nltk
import json
import copy
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
        self.length = 0

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
        self.length += 1
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
    inv = {}

    with open (inFile, 'r') as inputfile:
        index = 0
        for i in inputfile:
            parts = re.split(r'\t+', i.rstrip('\t'))
            fileId = parts[0]
            token = parts[1].rstrip('\n')

            dict_entry = preprocess(token)
            fileIds.append(fileId)
            tokens.append(token)
            
            d[fileId] = dict_entry
            all_words.extend(dict_entry)
            index+=1
    
    print(len(d))

    all_words = set(all_words)

    return d,fileIds,tokens,all_words
    

def preprocess(sent):
     
    ps = PorterStemmer() 
    stop_words = set(stopwords.words('english'))   

    x = re.sub('[^A-Za-z0-9]+', " ", sent)
    inter = x.strip().lower().split(" ")
    finalrow = [ps.stem(w) for w in inter if not w in stop_words]

    return (finalrow)

def process_queryFile(inFile):
    sent = []
    with open (inFile, 'r') as inputfile:
        for i in inputfile:
            toAdd = preprocess(i)
            sent.append(i.rstrip())
    # print(words)
    return sent

def get_postings(word,d):
    ret = []
    for key,value in d.items():
        if word in value:
            ret.append(int(key))
    return ret

def get_LinkedList(li):
    retList = LinkedList()
    for x in li:
        retList.insert_at_end(x)
    
    return retList

def merge_lists(l1,l2):
    comp = 0

    merged = []
    i = 0
    j = 0
    while i < len(l1) and j < len(l2):
        if l1[i] == l2[j]:
            merged.append(l1[i])
            i+=1
            j+=1
        
        elif(l1[i] < l2[j]):
            i+=1
        
        else:
            j+=1

        comp+=1

    return merged,comp

def merge_lists_LL(postings_list1, postings_list2):
    merged_list = LinkedList()
    pl1 = copy.copy(postings_list1)
    pl2 = copy.copy(postings_list2)
    comparisons = 0

    if pl1 is not None and pl2 is not None:
        p1 = pl1.start_node
        p2 = pl2.start_node

    while p1 and p2:
        if p1.value == p2.value:
            merged_list.insert_at_end(p1.value)
            p1 = p1.next
            p2 = p2.next

        elif p1.value < p2.value:
            # merged_list.add_node(p1.data)
            p1 = p1.next

        else:
            # merged_list.add_node(p2.data)
            p2 = p2.next

        comparisons += 1

    return merged_list, comparisons

def TAATAND_LL(sent,d):
    # print("For sent : " + sent)
    merged = None
    total_comp = 0
    total_same = 0

    postings = {}
    pt = []
    words = []
    words = preprocess(sent)
    print(words)

    for word in words:
        pst = get_LinkedList(get_postings(word,d))
        postings[word] = pst
        pt.append(pst)
    
    if len(pt) == 1:
        merged = get_LinkedList(get_postings(words[0],d))
    else:
        for i in range(1,len(postings)):
            if merged is not None:
                merged, comp = merge_lists_LL(merged,postings[words[i]])
                total_comp += comp
            else:
                merged, comp = merge_lists_LL(postings[words[i-1]],postings[words[i]])
                total_comp += comp
    # print(sent,total_comp)

    return merged, merged.length, total_comp

def TAAT_List(sent,d):
    merged = None
    total_comp = 0

    postings = {}
    pt = []
    words = []
    words.extend(preprocess(sent))
    for word in words:
        pst = get_postings(word,d)
        postings[word] = pst
        pt.append(pst)
    
    print(words)

    if len(pt) == 1:
        merged = get_postings(words[0],d)
    else:
        for i in range(1,len(pt)):
            if merged:
                merged, comp = merge_lists(merged,postings[words[i]])
                total_comp += comp
            else:
                merged, comp = merge_lists(postings[words[i-1]],postings[words[i]])
                total_comp += comp
    # print(sent,total_comp)

    return merged, len(merged), total_comp


def DAAT_AND(sent,d,fileIds,all_words):

    words = preprocess(sent)
    count = 0
    maxL = 0
    dcount = 0
    pls = []
    for word in words:
        pl = get_postings(word,d)
        pls.append(pl)

    print(words)
    # pls.sort(key=len)
    # pls = sorted(pls,key=lambda x: (-len(x), x))

    temp_index = 0
    for i in range(len(pls[0])):
        count = 1
        for j in range(1,len(pls)):
            flag = 0
            for k in range(temp_index,len(pls[j])):
                dcount+=1
                if pls[0][i] == pls[j][k]:
                    count+=1
                    break
                elif pls[0][i] < pls[j][k]:
                    temp_index = k
                    flag = 1
                    break
            if flag == 1:
                break

    return dcount


def create_output_file(query_sent,outFile,d):
    with open(outFile, 'w') as outpufile:
        d2 = {}
        data = {}
        data["postingsList"] = {}
        data["daatAnd"] = {}
        for sent in query_sent:
            words = preprocess(sent)
            for word in words:
                d2[word] = get_postings(word,d)
                data["postingsList"][word] = d2[word]

        for sent in query_sent:
            post, same, comp = TAATAND_LL(sent,d)
            data["daatAnd"][sent] = {}
            data["daatAnd"][sent]["results"] = post.traverse_list()
            data["daatAnd"][sent]["num_docs"] = same
            data["daatAnd"][sent]["num_comparisons"] = comp

        # print(data)
        json.dump(data, outpufile, indent=4)


def main():

    inF = sys.argv[1]
    ouF = sys.argv[2]
    quF = sys.argv[3]

    # print(inF,ouF,quF)

    d,fileIds,tokens,all_words = process_file(inF)

    # inverted = inverted_index(inF,d)

    # print(inverted)

    query_sent = process_queryFile(quF)
    # x = DAAT_AND()

    # create_output_file(query_sent,ouF,d)

    for sent in query_sent:
    #     res,same,comp = TAATAND_LL(sent,d)
        print(sent)
        x = DAAT_AND(sent,d,fileIds,all_words)
        print("comp DAAT - " + str(x))
        print()
        res1,same1,comp1 = TAAT_List(sent,d)
        print("comp TAAT_List - " + str(comp1))
        print()
        res,same,comp = TAATAND_LL(sent,d)
        print("comp TAAT_LL - " + str(comp))
        print()




main()