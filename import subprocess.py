import bcrypt
import multiprocessing as mp
import hashlib

# Ruta a los archivos
hash_file_meneate = "./g13_meneate.txt"
passwords_file = "./breaker.txt"
output_file = "./contraseñas_rotas.txt"

# Función para obtener el SHA-256 de una contraseña
def sha256_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Función para verificar si una contraseña coincide con el hash bcrypt
def check_password(hash_bcrypt, password):
    prehash = sha256_hash(password)
    print("Prehash:", prehash, "\nHash:", hash_bcrypt)
    if prehash[:16] == hash_bcrypt[:16]:
        return bcrypt.checkpw(password.encode('utf-8'), hash_bcrypt.encode('utf-8'))
    return False

# Cargar los hashes de g13_meneate.txt
def load_hashes(file_path):
    hashes = []
    with open(file_path, 'r') as file:
        for line in file:
            user, hash_bcrypt = line.strip().split(':')
            hashes.append((user, hash_bcrypt))
    return hashes

# Cargar las contraseñas de breaker.txt
def load_passwords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Función que intentará romper un solo hash usando varias contraseñas
def crack_single_hash(args):
    user, hash_bcrypt, passwords = args
    for password in passwords:
        if check_password(hash_bcrypt, password):
            print(f"Contraseña correcta para {user}: {password}")
            return (user, password)
    return None

# Usar multiprocessing para romper las contraseñas en paralelo
def crack_passwords_parallel(hashes, passwords):
    cracked_passwords = []
    num_cores = mp.cpu_count()  # Obtener el número de núcleos
    chunk_size = len(passwords) // num_cores  # Dividir contraseñas en chunks
    password_chunks = [passwords[i:i + chunk_size] for i in range(0, len(passwords), chunk_size)]
    
    with mp.Pool(num_cores) as pool:
        # Preparar los argumentos para pasar a cada proceso
        args = [(user, hash_bcrypt, password_chunks[i % num_cores]) for i, (user, hash_bcrypt) in enumerate(hashes)]
        results = pool.map(crack_single_hash, args)

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

