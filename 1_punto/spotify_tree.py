from node import Node,User
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

class Spotify_Tree:
    def __init__(self,dataframe) -> None:
        '''
        Iniciamos el arbol binario balanceado con una raíz
        '''
        self.root = None
        self.agregar_nodos(dataframe)
    
    def agregar_nodo(self, data):
        '''
        Permite agregar un nodo al arbol

        Args: 
            data (List) : [User_name,User_ID,Artist_name,Track,valence]
        '''
        # Le agrega a la raíz el siguiente nodo el cual lo agregaremos de manera recursiva en la funcion "agregar_nodo_recursivamente"
        self.root = self.agregar_nodo_recursivamente(self.root, data)
    
    def agregar_nodos(self,dataframe):
        """
        Permite agregar varios nodos al tiempo

        Args:
            dataframe(Dataframe) : [dataframe with users info]
        """
        
        for index in range(len(dataframe["User_ID"])):
            id = self.convertir_id(dataframe["User_ID"].iloc[index])
            # representar en caracteres numericos el ID
            if not self.existe_nodo(int(id)):
                #alteramos el dataframe para poder pasar el nuevo id
                dataframe["User_ID"].iloc[index] = id 
                # si no está ya un usuario con el ID agregarlo al arbol
                self.agregar_nodo(dataframe.iloc[index].tolist())
            else:
                self.retornar_nodo(int(id)).update(dataframe.iloc[index].tolist())
        

    def agregar_nodo_recursivamente(self, current: int, data) -> User:
        '''
        Permite agregar de manera recursiva un nodo al arbol

        Args:
            current (int) : [Current node]
            data (List) : [row of dataframe with data]
        
        Returns:
            User : User we're going to add
        '''
        id = int(data[1]) # para comparar correctamente como entero
        # Preguntamos que si el nodo actual es distinto de None, que me retorne el nodo con el valor que
        # queremos agregar (recordar que retorna un nodo porque lo queremos usar en el método de arriba llamado
        # agregar_nodo)
        if not current:
            return User(data)

        # Si el valor es menor al valor del nodo actual, ira a la izquierda   
        elif id < current.ID:
            current.left = self.agregar_nodo_recursivamente(current.left, data)
        # Misma lógica para el lado derecho
        else:
            current.right = self.agregar_nodo_recursivamente(current.right, data)
        
        # Vamos a asignarle la altura al nodo 
        current.height = 1 + max(self.get_hight(current.left), self.get_hight(current.right))
        
        # Falculamos el factor de equilibrio de los nodos a los caules estamos recorriendo para verificar
        # de inmediato si se deben realizar rotaciones o no
        factor_equilibrio = self.balanced_factor(current)
        
        # Aqui entra la lógica para que se autobalancee 

        # Aqui considero si el factor de equilibrio es 2 o más y que el valor del nodo que este agregando
        # sea menor que la hoja (creo que todos saben que es una hoja), si va a la izquierda es que se va a desbalancear
        # hacia la izq así que hacemos una rotación derecha

        # Definición de Hoja: Nodo sin hijos

        if factor_equilibrio > 1 and id < current.left.ID:
            return self.rotacion_derecha(current)
        
        # Aquí lo mismo pero cuando se va a desbalancear hacia la derecha
        if factor_equilibrio < -1 and id > current.right.ID:
            return self.rotacion_izquierda(current)
        
        # Se realiza una rotación doble derecha (condiciones que me dijo chatgpt)
        if factor_equilibrio > 1 and id > current.left.ID:
            current.left = self.rotacion_izquierda(current.left)
            return self.rotacion_derecha(current)
        
        # Se realiza una rotación doble izquierda (condiciones que me dijo chatgpt)
        if factor_equilibrio < -1 and id < current.right.ID:
            current.right = self.rotacion_derecha(current.right)
            return self.rotacion_izquierda(current)
        
        return current
    
    def eliminar_nodo(self,root,ID:int):
        '''
        Permite agregar de manera recursiva un nodo al arbol

        Args:
            root (int) : [Current node]
            ID   (int) : [ID of user we want to delete]
        
        '''
        # Borrado de un BST tradicional
        if root is None: 
            return root
        if ID < root.ID: #Avanzamos por el arbol
            root.left = self.eliminar_nodo(root.left,ID)
        elif ID>root.ID:
            root.right = self.eliminar_nodo(root.right,ID)
        else: # cuando llegamos al que tenga el ID
        #se remplaza con algun hijo o tenga o None si no tiene
            if root.left is None: #hijo único derecho
                temp = root.right
                root = None
                return temp

            elif root.right is None: #hijo único izquierdo
                temp = root.left
                root = None
                return temp
            #si tiene dos hijos
            temp = self.leftmost(root.right) 
            # remplazamos la raiz con el menor usuario del sub arbol derecho
            root.ID,root.name = temp.ID,temp.name
            root.right = self.eliminar_nodo(root.right,temp.ID)

        #Se actualiza la altura
        root.height = 1 + max(self.get_hight(root.left),
                            self.get_hight(root.right)) 
        # Se calcula el factor de equilibrio 
        factor = self.balanced_factor(root)
 
        # desbalanceado a la derecha
        if factor<-1 and self.balanced_factor(root.right)<=0: 
            return self.rotacion_izquierda(root)
        if factor<-1 and  self.balanced_factor(root.right)>0:
            root.right = self.rotacion_derecha(root.right)
            return self.rotacion_izquierda(root)

        #desbalanceado a la izquierda
        if factor>1 and  self.balanced_factor(root.left)>=0: 
            return self.rotacion_derecha(root)
        if factor>1 and self.balanced_factor(root.left)<0: 
            root.left = self.rotacion_izquierda(root.left)
            return self.rotacion_derecha(root)
        
        return root
        
    # Calculamos el factor de equilibrio 
    def balanced_factor(self, current: Node) -> int:
        '''
        Retorna el factor de equilibrio de un nodo

        Args:
            current (Node) : [Node for which we're trying to find the balance factor]

        Returns:
            Node : Returns the balanced factor of the node
        '''
        if not current:
            return 0
        return self.get_hight(current.left) - self.get_hight(current.right)
    
    def get_hight(self, current: Node) -> int:
        '''
        Devuelve la altura del arbol/subarbol de donde estemos tomando la raíz

        Args:
            current (Node) : [Node for which we're trying to find the height]
        '''
        if not current:
            return 0
        return current.height
    
    def levelOrderPrint(self, root: Node) -> None:
        '''
        Imprime el recorrido por niveles

        Args:
            root (Node) : [Our tree's root]
        '''
        height = self.get_hight(root)

        for level in range(1, height+1):
            print(f'Level {level}', end=': ')
            self.levelOrderTravel(root, level)
            print('\n')

    def levelOrderTravel(self, root: Node, level: int) -> None:
        '''
        Recorre el arbol por niveles

        Args:
            root  (Node) : [Node from where we're going to start the moving]
            level (int)  : [Respective level of the node where we started to move]
        '''
        if root is None:
            return
        if level == 1:
            print(f'{root.name}', end=' ')
        elif level > 1:
            self.levelOrderTravel(root.left, level-1)
            self.levelOrderTravel(root.right, level-1)
    
    def rotacion_derecha(self, current: Node) -> Node:
        '''
        Rotación simple derecha de un arbol balanceado

        Args: 
            current (Node) : [Node where there're unbalanced factor]
        '''
        nueva_raiz = current.left
        current.left = nueva_raiz.right
        nueva_raiz.right = current
        
        # Arreglamos las respectivas alturas de los nodos que estamos moviendo
        current.height = 1 + max(self.get_hight(current.left), self.get_hight(current.right))
        nueva_raiz.height = 1 + max(self.get_hight(nueva_raiz.left), self.get_hight(nueva_raiz.right))
        
        return nueva_raiz
    
    def rotacion_izquierda(self, current: Node) -> Node:
        '''
        Rotación simple izquierda de un arbol balanceado

        Args:
            current (Node) : [Node where there're unbalanced factor]
        '''
        nueva_raiz = current.right
        current.right = nueva_raiz.left
        nueva_raiz.left = current
        
        # Arreglamos las respectivas alturas de los nodos que estamos moviendo
        current.height = 1 + max(self.get_hight(current.left), self.get_hight(current.right))
        nueva_raiz.height = 1 + max(self.get_hight(nueva_raiz.left), self.get_hight(nueva_raiz.right))
        
        return nueva_raiz
    
    def existe_nodo(self,ID)->bool:
        """
        Busca un nodo, avisando si no es hallado
        
        Args:
            value:[value of node to find]

        Returns:
            True [If there is a node with value]
            False [if there is not ]
        """
        node = self.buscar_nodo_recursivo(self.root,ID)
        # Usa llamado recursivo para guardar el resultado
        if node is None:
            return False
        else:
            return True

    def buscar_nodo(self,ID):
        """
        Busca un nodo, avisando si no es hallado
        
        Args:
            ID(int):[ID of node to find]
        """
        node = self.buscar_nodo_recursivo(self.root,ID)
        # Usa llamado recursivo para guardar el resultado
        if node is None:
            print("No hallado")
        else:
            print(f"{node.name} valence {node.valence_mean} height {node.height} left:{node.left} right {node.right}")

    def retornar_nodo(self,ID)->User:
        """
        retorna un nodo
        
        Args:
            ID(int):[ID of node to find]
        Returns:
            node:[node being searched if found]
            None:[otherwise]
        """
        node = self.buscar_nodo_recursivo(self.root,ID)
        # Usa llamado recursivo para guardar el resultado
        if node is None:
            return None
        else:
            return node

    def buscar_nodo_recursivo(self,root,value):
        """
        Busca recursivamente un nodo
        y muestra la altura e hijos

        Args:
            root(Node): [current node]
            value(int/str): [value of node we search]
        """
        if root is None:
            return None
        else:
            if value<root.ID:
                return self.buscar_nodo_recursivo(root.left,value)
            elif value>root.ID:
                return self.buscar_nodo_recursivo(root.right,value)
            elif value == root.ID:
                return root
    
    def leftmost(self,root)->Node:
        """
        Regresa el nodo mas pequeño
        en un (sub)árbol

        Args:
            root(Node): [root of tree]
        """
        P = root
        lvl = 0
        while P.left is not None:
            lvl += 1
            P = P.left
        return P
    
    def rightmost(self,root)->Node:
        """
        Regresa el nodo con ID mas grande
        en un (sub)árbol

        Args:
            root(Node): [root of tree]
        """
        P = root
        lvl = 0
        while P.right is not None:
            lvl += 1
            P = P.right
        return P
    
    def buscar_padre(self,ID:int)->Node:
        """
        Busca el padre de nodo con value

        Args:
            value:[value whose father we look for]

        Returns:
            Node:[if there is a father]
            None:[if there cannot be a father]
        """
        if self.root is None:
            print("None")
            return
        if self.root.ID == ID:
            return None
        else:
            traversed = []
            traversed.append(self.root)
            if self.root.ID == ID:
                self.root = None
            else:
                while len(traversed) !=0:
                    x = traversed.pop(0)
                    if x.left is not None:
                        if x.left.ID == ID:
                            return x
                        else:
                            traversed.append(x.left)
                    if x.right is not None:
                        if x.right.ID == ID:
                            return x
                        else:
                            traversed.append(x.right)

    def uncle(self,ID):
        """
        Muestra (si lo tiene) el tío 
        de un nodo

        Args:
            ID:[ID of node whose uncle we search]
        """
        father = self.buscar_padre(ID) #  buscar papá
        if father is None:
            print(f"it has no father, therefore no uncle")
        elif father is self.root:
            print("father is root so there is no uncle")
        else:
            traversed = []
            traversed.append(self.root)
            if self.root.ID == ID: # find grandad select non father-child
                self.root = None
            else:
                while len(traversed) !=0:
                    x = traversed.pop(0)
                    if x.left is not None:
                        if x.left.ID == father.ID:
                            if x.right is not None:
                                print(f"uncle is {x.right}")
                                return
                        else:
                            traversed.append(x.left)
                    if x.right is not None:
                        if x.right.ID == father.ID:
                            if x.left is not None:
                                print(f"uncle  is {x.left}")
                                return
                        else:
                            traversed.append(x.right)

    def grandad(self,ID):
        """
        Muestra (si lo tiene) el abuelo de un nodo

        Args:
            ID:[ID of node whose uncle we search]
        """
        father = self.buscar_padre(ID) # determino padre
        if father is None:
            print(f"it has no father, therefore no grandad")
        elif father is self.root:
            print("father is root, so there is no grandad")
        else:
            grandad = self.buscar_padre(father.ID) # abuelo = padre de padre
            print(f"grandad  is {grandad}")

    def dar_ID(self,root,name):
        """
        Busca un usuario con nombre dado,
        devuelve el ID del primero q halle

        Args:
            root(User):[root of tree]
            name(str):[name we look in User]
        """
        if root is None:
            return None
        else:
            #print(f"{name.lower()} {root.name.lower()}")
            if name.lower() in root.name.lower():
                return root.ID #valida que tenga el nombre
            #recursion izquierda
            res1 = self.dar_ID(root.left,name)
            if res1:
                return res1
            #recursion derecha
            res2 = self.dar_ID(root.right,name)
            return res2
    
    def convertir_id(self,text: str) -> str:
        '''
        Devuelve un ID en su formato ASCII

        Args:
            text (str) : [Text that we'll transform into ASCII representation]
        '''
        carSplit = [letra for letra in text]
        ascii_rep = [ord(k) for k in carSplit]
        nuevoID = ''.join([str(i) for i  in ascii_rep])

        return nuevoID

#Se juntan los 3 csv en un solo dataframe            
df = pd.read_csv("1_punto\\data\\User_track_data.csv")
df1 = pd.read_csv("1_punto\\data\\User_track_data_2.csv")
m1 = pd.merge(df,df1,how="outer") # m1 = df+df1
df2 = pd.read_csv("1_punto\\data\\User_track_data_3.csv")
mega_df = pd.merge(m1,df2,how="outer") # mega_df = df2+m1


tree = Spotify_Tree(mega_df)
tree.levelOrderPrint(tree.root)
tree.buscar_nodo(tree.dar_ID(tree.root,"J"))

print("Number of songs",len(tree.retornar_nodo(tree.dar_ID(tree.root,"J")).songs))

print("First song",tree.retornar_nodo(tree.dar_ID(tree.root,"J")).songs[0])