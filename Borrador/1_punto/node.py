from typing import List


class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):
        return f"Value: {self.value}"

class User(Node):
    def __init__(self,data) -> None:
        self.name = data[0]
        self.ID = data[1]
        self.left = None
        self.right = None
        self.height = 1
    # Pendiente agregar para media de valencia y canciones tal vez
    def __str__(self):
        return f"{self.name}"
    