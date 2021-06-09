import BotAlgs as bA

class NewContainer:
    def __init__(self, maxSize = None):
        self.maxSize = maxSize
        self.Container = {}
        self.ID = 0
        
    def Remove(self, tag):
        self.Container[tag] = None 

    def AddCategory(self, tag, datastructure = []): #tag ~= name 
        self.Container[str(tag)] = datastructure 
        
    def AddItem(self, tag, item):
        if type(self.Container[str(tag)]) is list:
            self.Container[str(tag)].Add(item)
        else:
            self.Container[str(tag)].append(item)

    def searchCategory(self, item, tag):
        if tag or tag in self.Container:
            #Linear search
            for i in self.Container[tag]:
                if i == item:
                    return i
            return False
        else:
            print("Requires a category tag or tag does not exist!")

class BST:
    def __init__(self, data):
        self.data = data
        self.L     = None
        self.R     = None
    
    def insert(self, value):
        if self.data:
            if value > self.data:
                if self.R:
                    self.R.insert(value)
                else:
                    self.R = BST(value)
    
            elif value < self.data:
                if self.L:
                    self.L.insert(value)
                else:
                    self.L = BST(value)          
            else:
                print("No duplicate numbers")

    def inOrder(self):
        if self.L:
            self.L.inOrder()
        print(self.data)
        if self.R:
            self.R.inOrder()  
    
    def preOrder(self):
        print(self.data)
        if self.L:
            self.L.preOrder
    
    def search(self, value):
        if self.data == value or self.data == None:
            return self.data

        if value > self.data:
            self.data.R.search(value)

        if value < self.data:
            self.data.L.search(value)

    def delete(self):
        pass

class LinkedList:
    class Node:
        def _init_(self, x):
            self.val = x
            self.next = None
    def __init__(self):
        self.Root = None

class Queue:
    def __init__(self, Input = []):
        self.queue = Input

    def Pop(self):
        x = self.queue[0]
        self.queue.pop(0)
        return x
    
    def Push(self, Input):
        self.queue.append(Input)
          
class Stack:
    def __init__(self, Input = []):
        self.stack = Input

    def Pop(self):
        x = self.stack[len(self.stack)-1]
        self.stack.pop(len(self.stack)-1)
        return x
    
    def Push(self, Input):
        self.stack.append(Input)

class NewCommand:
    def __init__(self, function, Custom = False):
        if not Custom:
            self.function = getattr(self, function)
        else:
            self.function = function

class NewNote:
    def __init__(self, note, reminderDate = [0,0,0]): 
        pass
    
class NewSchedule:
    def __init__(self):
        pass