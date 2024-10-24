import bcrypt
import multiprocessing as mp

# Ruta a los archivos
hash_file_meneate = "./g13_meneate.txt"
passwords_file = "./hashes.txt"
output_file = "./contraseñas_rotas.txt"

# Función para verificar si una contraseña coincide con el hash bcrypt
def check_password(hashes, actual_password):
    password = actual_password[1]
    for hash_bcrypt in hashes:
        print(hash_bcrypt[0], actual_password[0])
        if hash_bcrypt[0] == passwords[0]:
            return bcrypt.checkpw(password.encode('utf-8'), hash_bcrypt[1].encode('utf-8'))
    return False

# Cargar los hashes de g13_meneate.txt
def load_hashes(file_path):
    hashes = []
    with open(file_path, 'r') as file:
        for line in file:
            user1, hash_bcrypt = line.strip().split(':')
            hashes.append([user1, hash_bcrypt])
    return hashes

# Cargar las contraseñas de breaker.txt
def load_passwords(file_path):
    passwords = []
    with open(file_path, 'r') as file:
        for line in file:
            user2, password = line.strip().split(':')
            passwords.append([user2, password])
    return passwords

# Función que intentará romper un solo hash usando varias contraseñas
def crack_single_hash(hashes, passwords):
    for i in range(len(passwords)):
        actual_check= passwords[i]
        if check_password(hashes, actual_check):
            print(f"Contraseña correcta para {actual_check[0]}: {actual_check[1]}")
            return actual_check
    return None

def crack_passwords_parallel(hashes, passwords):
    cracked_passwords = []
    num_cores = mp.cpu_count()  # Obtener el número de núcleos
    with mp.Pool(num_cores) as pool:
        # Preparar los argumentos como una lista de tuplas (hashes y passwords)
        results = pool.starmap(crack_single_hash, [(hashes, password) for password in passwords])

        # Filtrar los resultados no nulos
        cracked_passwords = [result for result in results if result]
    
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
    
    # Romper las contraseñas en paralelo
    cracked_passwords = crack_passwords_parallel(hashes, passwords)
    
    # Guardar las contraseñas rotas
    save_cracked_passwords(cracked_passwords, output_file)
    
    print(f"Proceso completado. Las contraseñas rotas se han guardado en {output_file}.")

