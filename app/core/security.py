import bcrypt

# 1. Convierte una contraseña en texto plano a un Hash seguro e irreversible
def generar_hash_contrasena(contrasena_plana: str) -> str:
    # Genera una sal (salt) aleatoria y calcula el hash
    sal = bcrypt.gensalt()
    contrasena_bytes = contrasena_plana.encode('utf-8')
    hash_bytes = bcrypt.hashpw(contrasena_bytes, sal)
    return hash_bytes.decode('utf-8')

# 2. Compara la contraseña que ingresa el usuario con el hash guardado en la BD
def verificar_contrasena(contrasena_plana: str, hash_almacenado: str) -> bool:
    contrasena_bytes = contrasena_plana.encode('utf-8')
    hash_bytes = hash_almacenado.encode('utf-8')
    return bcrypt.checkpw(contrasena_bytes, hash_bytes)







