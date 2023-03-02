from typing import List


class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left = None
        self.right = None
        self._heightCalc = 1
        self.height = 0

    def __str__(self):
        return f"Value: {self.value}"

class User(Node):
    def __init__(self,data:List) -> None:
        """
        Constructor de clase Usuario

        Args:
            data(list):[contains row with info on user]
        """
        self.name = data[0]
        self.ID = int(data[1])
        self.songs = [data[3]]
        self.valences =[data[4]]
        self.left = None
        self.right = None
        self._heightCalc = 1
        self.height = 0

    # Pendiente agregar para media de valencia y canciones tal vez

    def update(self,data):
        """
        Actualiza las listas de canciones y
        promedio para el usuario
        Args:
            data(list):[contains row with info on user]
        """
        self.songs.append(data[3])
        self.valences.append(data[4])
        #añaden nuevos datos a listas
        
    @property
    def valence_mean(self):
        """
        Promedio de valencia de positividad
        de canciones
        """
        #Suma/Longitud = Promedio
        return sum(self.valences)/len(self.valences)

    def __str__(self):
        return f"{self.name}"


    
    