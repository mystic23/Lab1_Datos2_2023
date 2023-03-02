from BPtree import BPTree
import time

start_time = time.time()

order4 = BPTree(4,{1:"David",2:"Pedro",3:"Luke",
                   4:"Mary"})
order4.printTree()

order4.searchData(1,"Pedro")

print(time.time()-start_time)






