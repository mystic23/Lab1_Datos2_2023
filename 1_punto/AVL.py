from node import Node

class ArbolBinarioBalanceado:
    def __init__(self,nodos=None) -> None:
        '''
        Iniciamos el arbol binario balanceado con una raíz
        '''
        self.root = None
        if nodos is not None:
            self.agregar_nodos(nodos)
    
    def agregar_nodo(self, value: int):
        '''
        Permite agregar un nodo al arbol

        Args: 
            value (int) : [Value of a node]
        '''
        # Le agrega a la raíz el siguiente nodo el cual lo agregaremos de manera recursiva en la funcion "agregar_nodo_recursivamente"
        self.root = self.agregar_nodo_recursivamente(self.root, value)
        # print(f'Se acaba de agregar {value}')
    
    def agregar_nodos(self,nodos):
        """
        Permite agregar varios nodos al tiempo

        Args:
            nodos(list) : [lista de valores a insertar]
        """
        for x in nodos:
            self.root = self.agregar_nodo_recursivamente(self.root,x)

    def agregar_nodo_recursivamente(self, current: int, value: int) -> Node:
        '''
        Permite agregar de manera recursiva un nodo al arbol

        Args:
            current (int) : [Current node]
            value   (int) : [Vale of the node we want to add]
        
        Returns:
            Node : Node we're going to add
        '''

        # Preguntamos que si el nodo actual es distinto de None, que me retorne el nodo con el valor que
        # queremos agregar (recordar que retorna un nodo porque lo queremos usar en el método de arriba llamado
        # agregar_nodo)
        if not current:
            return Node(value)

        # Si el valor es menor al valor del nodo actual, ira a la izquierda    
        elif value < current.value:
            current.left = self.agregar_nodo_recursivamente(current.left, value)
        # Misma lógica para el lado derecho
        else:
            current.right = self.agregar_nodo_recursivamente(current.right, value)
        
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

        if factor_equilibrio > 1 and value < current.left.value:
            return self.rotacion_derecha(current)
        
        # Aquí lo mismo pero cuando se va a desbalancear hacia la derecha
        if factor_equilibrio < -1 and value > current.right.value:
            return self.rotacion_izquierda(current)
        
        # Se realiza una rotación doble derecha (condiciones que me dijo chatgpt)
        if factor_equilibrio > 1 and value > current.left.value:
            current.left = self.rotacion_izquierda(current.left)
            return self.rotacion_derecha(current)
        
        # Se realiza una rotación doble izquierda (condiciones que me dijo chatgpt)
        if factor_equilibrio < -1 and value < current.right.value:
            current.right = self.rotacion_derecha(current.right)
            return self.rotacion_izquierda(current)
        
        return current
    
    def eliminar_nodo(self,root,value):
        '''
        Permite agregar de manera recursiva un nodo al arbol

        Args:
            root (int) : [Current node]
            value   (int) : [Vale of the node we want to delete]
        
        '''
        # Borrado de un BST tradicional
        if root is None: 
            return root
        if value < root.value: #Avanzamos por el arbol
            root.left = self.eliminar_nodo(root.left,value)
        elif value>root.value:
            root.right = self.eliminar_nodo(root.right,value)
        else: # cuando llegamos al que tenga el value
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
            # replace root with smallest in right subtree
            root.value = temp.value
            root.right = self.eliminar_nodo(root.right,temp.value)

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
            print(f'{root.value}', end=' ')
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
    
    def existe_nodo(self,value)->bool:
        """
        Busca un nodo, avisando si no es hallado
        
        Args:
            value:[value of node to find]

        Returns:
            True [If there is a node with value]
            False [if there is not ]
        """
        node = self.buscar_nodo_recursivo(self.root,value)
        # Usa llamado recursivo para guardar el resultado
        if node is None:
            return False
        else:
            return True
        
    def buscar_nodo(self,value):
        """
        Busca un nodo, avisando si no es hallado
        
        Args:
            value:[value of node to find]
        """
        node = self.buscar_nodo_recursivo(self.root,value)
        # Usa llamado recursivo para guardar el resultado
        if node is None:
            print(f"{value} no fue hallado")

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
            if value<root.value:
                return self.buscar_nodo_recursivo(root.left,value)
            elif value>root.value:
                return self.buscar_nodo_recursivo(root.right,value)
            elif value == root.value:
                print(f"{root} height {root.height} left:{root.left} right {root.right}")
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
    
    def buscar_padre(self,value)->Node:
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
        if self.root.value == value:
            return None
        else:
            traversed = []
            traversed.append(self.root)
            if self.root.value == value:
                self.root = None
            else:
                while len(traversed) !=0:
                    x = traversed.pop(0)
                    if x.left is not None:
                        if x.left.value == value:
                            return x
                        else:
                            traversed.append(x.left)
                    if x.right is not None:
                        if x.right.value == value:
                            return x
                        else:
                            traversed.append(x.right)

    def uncle(self,value):
        """
        Muestra (si lo tiene) el tío 
        de un nodo

        Args:
            value:[value of node whose uncle we search]
        """
        father = self.buscar_padre(value) #  buscar papá
        if father is None:
            print(f"{value} has no father, therefore no uncle")
        elif father is self.root:
            print("father is root so there is no uncle")
        else:
            traversed = []
            traversed.append(self.root)
            if self.root.value == value: # find grandad select non father-child
                self.root = None
            else:
                while len(traversed) !=0:
                    x = traversed.pop(0)
                    if x.left is not None:
                        if x.left.value == father.value:
                            if x.right is not None:
                                print(f"uncle of {value} is {x.right}")
                                return
                        else:
                            traversed.append(x.left)
                    if x.right is not None:
                        if x.right.value == father.value:
                            if x.left is not None:
                                print(f"uncle of {value} is {x.left}")
                                return
                        else:
                            traversed.append(x.right)

    def grandad(self,value):
        """
        Muestra (si lo tiene) el abuelo de un nodo

        Args:
            value:[value of node whose uncle we search]
        """
        father = self.buscar_padre(value) # determino padre
        if father is None:
            print(f"{value} has no father, therefore no grandad")
        elif father is self.root:
            print("father is root, so there is no grandad")
        else:
            grandad = self.buscar_padre(father.value) # abuelo = padre de padre
            print(f"grandad of {value} is {grandad}")


# Instanciamos el arbol binario balanceado
#arbol = ArbolBinarioBalanceado([10,5,15,3,7,13,18,4,2,1])
arbol = ArbolBinarioBalanceado([10,7,14,5,12,15,8,4,11,13,6,9,16])

#arbol = ArbolBinarioBalanceado([3,5,2,4])
#arbol.root = arbol.eliminar_nodo(arbol.root,2)

# Probando el recorrido por niveles
arbol.levelOrderPrint(arbol.root)
arbol.root = arbol.eliminar_nodo(arbol.root,10)
arbol.levelOrderPrint(arbol.root)
'''
Referencias: 
   
    - https://openai.com/blog/chatgpt/
    - https://www.utm.mx/~jahdezp/archivos%20estructuras/Arboles%20AVL.pdf
    - https://es.wikipedia.org/wiki/Rotaci%C3%B3n_de_%C3%A1rboles
    - https://www.geeksforgeeks.org/level-order-tree-traversal/
    
'''