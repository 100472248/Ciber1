import bcrypt

# Ruta a los archivos
hash_file_meneate = "/Users/pablo/Desktop/Ciber1/g13_meneate.txt"
passwords_file = "/Users/pablo/Desktop/Ciber1/breaker.txt"
output_file = "/Users/pablo/Desktop/Ciber1/contraseñas_rotas.txt"

# Función para verificar si una contraseña coincide con el hash bcrypt
def check_password(hash_bcrypt, password):
    return bcrypt.checkpw(password.encode('utf-8'), hash_bcrypt.encode('utf-8'))

# Cargar los hashes de g13_meneate.txt
def load_hashes(file_path):
    hashes = []
    with open(file_path, 'r') as file:
        for line in file:
            # Separar el usuario del hash
            user, hash_bcrypt = line.strip().split(':')
            hashes.append((user, hash_bcrypt))
    return hashes

# Cargar las contraseñas de breaker.txt
def load_passwords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Intentar romper las contraseñas
def crack_passwords(hashes, passwords):
    cracked_passwords = []
    for user, hash_bcrypt in hashes:
        for password in passwords:
            if check_password(hash_bcrypt, password):
                print(f"¡Contraseña rota! Usuario: {user}, Contraseña: {password}")
                cracked_passwords.append((user, password))
                break  # Salir del bucle si la contraseña ha sido encontrada
    return cracked_passwords

# Guardar las contraseñas rotas en un archivo
def save_cracked_passwords(cracked_passwords, output_file):
    with open(output_file, 'w') as file:
        for user, password in cracked_passwords:
            file.write(f"{user}:{password}\n")

if __name__ == "__main__":
    # Cargar hashes y contraseñas
    hashes = load_hashes(hash_file_meneate)
    passwords = load_passwords(passwords_file)
    
    # Romper las contraseñas
    cracked_passwords = crack_passwords(hashes, passwords)
    
    # Guardar las contraseñas rotas
    save_cracked_passwords(cracked_passwords, output_file)
    
    print(f"Proceso completado. Las contraseñas rotas se han guardado en {output_file}.")
