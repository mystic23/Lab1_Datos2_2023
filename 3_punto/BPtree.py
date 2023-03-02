import bisect 
#credit to ChatGPT for finding this method, only usefulness it had for this part

# ON AUTHORSHIP:
# findLeaf based on https://www.geeksforgeeks.org/insertion-in-a-b-tree/
# yet stil heavily modified
# However the rest of the code did seem to me a true B+ Tree
# The rest of the code was done of own account, that is why is crazy

class Node:
    """
    Base class For a Node in a B+ Tree
    """
    def __init__(self,order:int,isLeaf=False) -> None:
        """
        Initializes a Node

        Args:
            order(int):[order of the tree it belongs]
            isLeaf(bool):[Whether is a leaf or not]
        """
        self.order = order # max no. of children it can have
        self.parent = None #parent which contains self
        self.keys = [] #list of indexes 
        self.values = [] #in non-leaf stores Nodes, in leaves stores values
        self.isLeaf = isLeaf
        self.next = None #pointer to next Node in Leaf LinkedList

    def insertion(self,key,value):
        """
        inserts key-value pair in node

        Args:
            key(int):
            value(str/Node): 
        """
        x = bisect.bisect_left(self.keys,key)
        # uses binary search to identify index to place key in sorted list
        self.keys.insert(x,key)
        if self.isLeaf: #In a leaf, key-value pair share index
            self.values.insert(x,value) # add value in same index
        else:
            # a non-leaf has different lengths
            for i in range(len(self.values)):
                if key == self.values[i].keys[0]: # if the key is the same we go to next node
                    self.values.insert(i+1,value)
                    break
                elif key < self.values[i].keys[0]: #if the key we search is smaller go to node
                    self.values.insert(i,value)
                    break
                elif (i+1 ==len(self.values)): # if we are in last key, go to next node
                    self.values.insert(i+1,value)
                    break

    def split(self):
        """
        Splits node in two halves
        
        Returns:
            new_node(Node):[upper half of original self]
        """
        
        mid = len(self.values) // 2 
        #get middle 

        new_node = Node(self.order,self.isLeaf)
        new_node.keys = self.keys[mid:] 
        new_node.values = self.values[mid:]
        # New node has values and keys from middle

        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        #Old node has keys and values before middle
            
        new_node.parent = self.parent
        #keep in the family
        return new_node 
    
    @property
    def is_full(self)->bool:
        """
        Whether the Node has reached limit
        of keys (order)
        """
        return len(self.keys) == self.order
    
    def __repr__(self) -> str:
        return f"{self.keys}"
 
class BPTree:
    def __init__(self,order:int,data=None) -> None:
        self.order = order
        self.root = Node(self.order,True)
        if data is not None:
            self.addNodes(data)

    def addNodes(self,data):
        for k,v in data.items():
            self.addNode(k,v)
    def addNode(self,key,value):
        """
        Adds a key-value pair to tree
        """
        target = self.findLeaf(key) #search Leaf Node
        target.insertion(key,value) #insert key-value pair

        if target.is_full:
            second = target.split() #split node
            target.next = second #connect
            self.insertParent(target,second) #go to parent
            
    def insertParent(self,target:Node,second:Node):
        """
        Adds appropiate key and nodes to parents 
        after splitting due to overflow

        Args:
            target(Node):[first half of split]
            second(Noed)[second half of split]
        
        """
        if self.root == target and target.isLeaf: # if the leaf was root
            #only happens once
            self.root = Node(self.order) # new root, always non leaf
            target.parent = self.root
            second.parent = self.root
            # two halves will be children
            self.root.keys = [second.keys[0]]
            self.root.values = [target,second]
            #initialize lesser of second half as key
            # add each half
        else:
            if target.parent:
                # if there is a parent add
                if target.isLeaf: 
                    #when adding from a leaf, add smallest of second half
                    target.parent.insertion(key=second.keys[0],value=second)
                else:
                    #When adding from a non-leaf add greatest of first half
                    # This one will later be ascended
                    ascended = target.keys[-1]
                    target.parent.insertion(key=target.keys[-1],value=second)
                    target.keys.remove(ascended)

                    #print("second es ",second)
                    #print(second.values)
                    for v in second.values:
                        v.parent = second
                    
                    #assigns to second half its rightful parent
                    
                # add second half to parent
                if target.parent.is_full: # if the parent is now full
                    # a parent will always be non-leaf 

                    #print("Padre lleno")
                    dos = target.parent.split()
                    #split to target parent

                    """ print(target.parent.keys)
                    print(dos.keys) """

                    self.insertParent(target=target.parent,second=dos)
                    #Recursive call to check whole tree
            else:
                newf = (len(target.keys)//2)
                d = target.keys[newf]

                #print(f"d es {d}")
                #print(f"newf será {target.keys[newf]}")

                #we ascend a key
                self.root = Node(self.order)
                target.keys.remove(d)
                self.root.keys = [d]
                self.root.values = [target,second]
                target.parent = self.root
                second.parent = self.root

                for v in second.values:
                    v.parent = second

                """ 
                print(target.values)
                print(second.values)
                """

    def findLeaf(self,key):
        """
        Finds the leaf where a value with key 
        should be inserted

        Args:
            key(int):[key to insert in best place]

        Returns:
            current(node):[leaf node whre key should be]
        """
        current = self.root
        while not current.isLeaf: #until we reach a leaf
            nodes = current.keys
            for i in range(len(nodes)): #through the keys on the node
                if key == nodes[i]: # if the key is the same we go to next node
                    current = current.values[i+1]
                    break
                elif key < nodes[i]: #if the key we search is smaller go to node
                    current = current.values[i]
                    break
                elif (i+1 ==len(current.keys)): # if we are in last key, go to next node
                    current = current.values[i+1]
                    break
                #if the key was bigger, we keep iterating on keys
        return current
    
    def printTree(self):
        """
        Shows the tree first indexes
        and then the linkedlist of leaf nodes

        1.first prints the root keys
        2. Then each child in the same line
        3. Then for each child the keys are shown 

        """
        print("Indexes")
        ls = [self.root]
        while ls:
            x = ls.pop(0)
            if x.isLeaf:
                break
            print("Children of ",x)
            for node in x.values:
                if not x.isLeaf:
                    print(node.keys,end="  ")
                    ls.append(node)
            print()

        print("Leaf Nodes")
        while x is not None:
            for i in range(len(x.keys)):
                print(f"{x.keys[i]} {x.values[i]}",end=" ")
            print()
            x = x.next

    def searchData(self,key,value):
        """
        Determines whether a key-value pair 
        is on the tree

        Args:
            key(int):[key or index of data]
            value(str):[value or name]
        """
        loc = self.findLeaf(key)
        i = 0
        while loc is not None:
            for i in range(len(loc.keys)):
                if loc.keys[i]==key and loc.values[i]==value:
                    print(f"Found after {i} searches")
                    return 
                elif loc.keys[i]!=key and loc.values[i]==value:
                    print(f"found {value} but with key {loc.keys[i]} after {i} searches")
                    return
                i+=1
            loc = loc.next
        print("Not found after {i} searches")

if __name__=="__main__":
    data = {1:"David",2:"Pedro",3:"Luke",4:"John",5:"Paul",6:"Simon",7:"Socorro"
            ,8:"Pas",9:"No",10:"Crazy",11:"creo",12:"Cristina"}
    tree = BPTree(3)
    tree.addNodes(data)
    tree.printTree()
    tree.searchData(12,"Cristina")
    
     