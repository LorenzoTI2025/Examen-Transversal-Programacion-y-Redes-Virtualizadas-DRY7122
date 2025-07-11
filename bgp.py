
def es_as_privado(asn):
    return (64512 <= asn <= 65534) or (4200000000 <= asn <= 4294967294)

try:
    print("*****************************")
    numero_as = int(input("Ingrese el número de AS: "))
    if es_as_privado(numero_as):
        print(f"El AS {numero_as} es PRIVADO.")
    else:
        print(f"El AS {numero_as} es PÚBLICO.")
except ValueError:
    print("Por favor, ingrese un número válido.")
