
with open("hashes.txt", "r") as file1:
    matriz_lineas = file1.readlines()

with open("breaker.txt", "w") as file2:
    for linea in matriz_lineas:
        partes = linea.split(":")
        if len(partes) == 2:
            texto = str(partes[1])
            file2.write(texto)
