print("Verificador de VLAN")
print("Escriba 'salir' para terminar.\n")

while True:
    entrada = input("Ingrese el número de VLAN: ")

    if entrada.lower() == "salir":
        print("Programa finalizado.")
        break

    try:
        vlan = int(entrada)

        if 1 <= vlan <= 1005:
            print("La VLAN ingresada pertenece al rango NORMAL.\n")
        elif 1006 <= vlan <= 4094:
            print("La VLAN ingresada pertenece al rango EXTENDIDO.\n")
        else:
            print("Número de VLAN inválido. Debe estar entre 1 y 4094.\n")
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número entero válido o 'salir'.\n")
