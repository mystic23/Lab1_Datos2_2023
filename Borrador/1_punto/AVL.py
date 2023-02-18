from node import Node

class ArbolBinarioBalanceado:
    def __init__(self) -> None:
        '''
        Iniciamos el arbol binario balanceado con una raíz
        '''
        self.root = None
    
    def agregar_nodo(self, value: int):
        '''
        Permite agregar un nodo al arbol

        Args: 
            value (int) : [Value of a node]
        '''
        # Le agrega a la raíz el siguiente nodo el cual lo agregaremos de manera recursiva en la funcion "agregar_nodo_recursivamente"
        self.root = self.agregar_nodo_recursivamente(self.root, value)
        # print(f'Se acaba de agregar {value}')
    
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
        if factor_equilibrio < -1 and value < current.right.valor:
            current.right = self.rotacion_derecha(current.right)
            return self.rotacion_izquierda(current)
        
        return current
    
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
        Rotación simple derecha de un arbol balanceado

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

# Instanciamos el arbol binario balanceado
arbol = ArbolBinarioBalanceado()

# Agregamos algunos nodos al árbol
arbol.agregar_nodo(10)
arbol.agregar_nodo(5)
arbol.agregar_nodo(15)
arbol.agregar_nodo(3)
arbol.agregar_nodo(7)
arbol.agregar_nodo(13)
arbol.agregar_nodo(18)
arbol.agregar_nodo(4)
arbol.agregar_nodo(2)
arbol.agregar_nodo(1)

# Probando si funciona el autobalanceo
print(arbol.root.left.left.left)

print(arbol.get_hight(arbol.root.left.left.left))

'''
Referencias: 

    - https://openai.com/blog/chatgpt/
    - https://www.utm.mx/~jahdezp/archivos%20estructuras/Arboles%20AVL.pdf
    - https://es.wikipedia.org/wiki/Rotaci%C3%B3n_de_%C3%A1rboles
    
'''