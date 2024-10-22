import subprocess
import os

# Define la ruta a John the Ripper y a los archivos de hashes
john_path = "/snap/john-the-ripper/639/run/john"  # Asegúrate de que esta ruta sea correcta
hash_file_meneate = "g13_meneate.txt"
hashes_file = "breaker.txt"  # Archivo con las contraseñas rotas de ForoMotos
comando_break = f"john --wordlist={hashes_file} --format=Raw-MD5 {hash_file_meneate}"
comando_read = f"john --show --format=Raw-MD5 {hash_file_meneate}"

# Opción para ejecutar John the Ripper usando las contraseñas rotas
def run_john_the_ripper_with_dict():
    try:
        print("Verificando si el archivo de hashes de Meneate está vacío...")
        if is_file_empty(hash_file_meneate):
            print(f"El archivo {hash_file_meneate} está vacío.")
            return

        print("Ejecutando John the Ripper con el diccionario de contraseñas rotas...")
        result = subprocess.run(comando_break, shell=True, capture_output=True, text=True)

        print("Salida de John the Ripper:")
        print(result.stdout)

        print("Extrayendo contraseñas rotas...")
        show_result = subprocess.run(comando_read, shell=True, capture_output=True, text=True)
        print("Contraseñas rotas:")
        print(show_result.stdout)

    except Exception as e:
        print(f"Error: {e}")

def is_file_empty(file_path):
    return os.stat(file_path).st_size == 0

if __name__ == "__main__":
    run_john_the_ripper_with_dict()
