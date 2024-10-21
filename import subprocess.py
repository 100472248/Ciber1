import subprocess
import os

# Define la ruta a John the Ripper y a los archivos de hashes
john_path = "/opt/homebrew/bin/john"  # Asegúrate de que esta ruta sea correcta
hash_file_meneate = "g13_meneate.txt"
hashes_file = "hashes.txt"  # Archivo con las contraseñas rotas de ForoMotos

# Opción para ejecutar John the Ripper usando las contraseñas rotas
def run_john_the_ripper_with_dict():
    try:
        print("Verificando si el archivo de hashes de Meneate está vacío...")
        if is_file_empty(hash_file_meneate):
            print(f"El archivo {hash_file_meneate} está vacío.")
            return

        print("Ejecutando John the Ripper con el diccionario de contraseñas rotas...")
        result = subprocess.run([john_path, '--wordlist=' + hashes_file, hash_file_meneate], capture_output=True, text=True)

        print("Salida de John the Ripper:")
        print(result.stdout)

        print("Extrayendo contraseñas rotas...")
        show_result = subprocess.run([john_path, '--show', hash_file_meneate], capture_output=True, text=True)
        print("Contraseñas rotas:")
        print(show_result.stdout)

    except Exception as e:
        print(f"Error: {e}")

def is_file_empty(file_path):
    return os.stat(file_path).st_size == 0

if __name__ == "__main__":
    run_john_the_ripper_with_dict()
