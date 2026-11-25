from PagoEfectivo import PagoEfectivo
from PagoQR import PagoQR
from PagoTarjeta import PagoTarjeta

try:
    total_cuenta = float(input("Ingresa el total a pagar (Bs): "))

    print("\nElige el metodo de pago:")
    print("1. Efectivo")
    print("2. QR")
    print("3. Tarjeta")
    opcion = input("Opcion (1-3): ")

    if opcion == "1":
        detalle = input("Detalle (ej. Pago en caja): ")
        monto = float(input("Monto entregado por el cliente (Bs): "))
        pago = PagoEfectivo(detalle, monto)
    elif opcion == "2":
        detalle = input("Detalle (ej. Banco/Yape): ")
        codigo = input("Codigo QR (10 digitos): ")
        pago = PagoQR(detalle, codigo)
    elif opcion == "3":
        detalle = input("Banco o tipo de tarjeta (ej. Visa): ")
        numero = input("Numero de tarjeta (16 digitos): ")
        pago = PagoTarjeta(detalle, numero)
    else:
        print("Opcion no valida.")
        pago = None

    if pago:
        pago.procesar_pago(total_cuenta)
        pago.generar_comprobante()

except ValueError as e:
    print(f"\nError en los datos ingresados: {e}")