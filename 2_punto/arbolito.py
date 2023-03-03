import hashlib

# Función para calcular el hash SHA-256 de un bloque de datos
def sha256(block):
    """_summary_

    Args:
        block (_type_): _description_

    Returns:
        _type_: _description_
    """
    return hashlib.sha256(block).digest()

# Función para construir un árbol de Merkle a partir de una lista de bloques de datos
def build_merkle_tree(blocks):
    # Calcula el hash SHA-256 de cada bloque de datos
    hashes = [sha256(block) for block in blocks]
    
    # Construye el árbol de Merkle recursivamente
    if len(hashes) == 1:
        return hashes[0]
    else:
        left_child = build_merkle_tree(hashes[:len(hashes)//2])
        right_child = build_merkle_tree(hashes[len(hashes)//2:])
        return sha256(left_child + right_child)

# Función para verificar la autenticidad de un archivo descargado
def verify_file(root, blocks):
    # Calcula el hash SHA-256 de cada bloque de datos
    hashes = [sha256(block) for block in blocks]
    
    # Construye el árbol de Merkle a partir de los hashes de los bloques de datos
    merkle_root = build_merkle_tree(hashes)
    
    # Verifica si la raíz del árbol de Merkle calculada coincide con la raíz proporcionada
    return merkle_root == root

# Ejemplo de uso
file_blocks = [b"block1", b"block2", b"block3", b"block4"]
merkle_root = build_merkle_tree(file_blocks)
print("Merkle root:", merkle_root.hex())

# Simula la descarga del archivo
downloaded_blocks = file_blocks[:3] + [b"modified_block"]

# Verifica la autenticidad del archivo descargado
is_valid = verify_file(merkle_root, downloaded_blocks)
print("Archivo válido:", is_valid)
