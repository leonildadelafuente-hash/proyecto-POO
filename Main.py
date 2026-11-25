from datetime import datetime
from variante import DIAS, ZONAS_ENVIO
from Plato import Plato
from Bebida import Bebida
from Pedido import EN_PREPARACION, LISTO, ENTREGADO, CANCELADO
from PagoEfectivo import PagoEfectivo
from PagoQR import PagoQR
from PagoTarjeta import PagoTarjeta
from Restaurante import Restaurante


# muestra una lista numerada y devuelve la posicion elegida (empieza en 0)
def elegir(titulo, textos):
    if len(textos) == 0:
        raise ValueError("No hay opciones para elegir")
    print(titulo)
    for i in range(len(textos)):
        print(f"  {i + 1}. {textos[i]}")
    n = int(input("Numero: "))
    if n < 1 or n > len(textos):
        raise ValueError("Opcion fuera de rango")
    return n - 1


def elegir_producto(rest):
    textos = []
    for p in rest.productos:
        textos.append(p.nombre)
    return rest.productos[elegir("Producto:", textos)]


def elegir_cliente(rest):
    textos = []
    for c in rest.clientes:
        textos.append(c.nombre)
    return rest.clientes[elegir("Cliente:", textos)]


def elegir_pedido(rest):
    textos = []
    for p in rest.pedidos:
        textos.append(p.tipo + " de " + p.cliente.nombre + " [" + p.estado + "]")
    return rest.pedidos[elegir("Pedido:", textos)]


def datos_ejemplo(rest):
    silpancho = Plato("Silpancho", 35)
    vaso = Bebida("Mocochinchi vaso", 6, "refresco natural")
    rest.registrar_producto(silpancho)
    rest.registrar_producto(Plato("Pique macho", 55))
    rest.registrar_producto(Plato("Chicharron", 50, ["domingo"]))
    rest.registrar_producto(Plato("Sopa de mani", 25))
    rest.registrar_producto(vaso)
    rest.registrar_producto(Bebida("Mocochinchi jarra", 6, "refresco natural", True))
    rest.registrar_producto(Bebida("Gaseosa vaso", 7, "gaseosa"))
    rest.armar_combo("Combo Valluno", [(silpancho, 1), (vaso, 1)])
    rest.registrar_cliente("Cliente Demo", "71234567", "Cercado")


def registrar_plato(rest):
    nombre = input("Nombre: ")
    precio = float(input("Precio Bs: "))
    texto = input("Dias de venta separados por coma (vacio = todos): ")
    dias = None
    if texto.strip() != "":
        dias = []
        for d in texto.split(","):
            dias.append(d.strip().lower())
    rest.registrar_producto(Plato(nombre, precio, dias))
    print("Plato registrado")


def registrar_bebida(rest):
    nombre = input("Nombre: ")
    precio = float(input("Precio por vaso Bs: "))
    tipo = input("Tipo (refresco natural / gaseosa): ").strip()
    jarra = input("Es jarra? (s/n): ").strip().lower() == "s"
    rest.registrar_producto(Bebida(nombre, precio, tipo, jarra))
    print("Bebida registrada")


def armar_combo(rest):
    nombre = input("Nombre del combo: ")
    items = []
    seguir = True
    while seguir:
        producto = elegir_producto(rest)
        cantidad = int(input("Cantidad: "))
        items.append((producto, cantidad))
        if len(items) >= 2:
            seguir = input("Agregar otro producto? (s/n): ").strip().lower() == "s"
    combo = rest.armar_combo(nombre, items)
    print(f"Combo creado. Precio: Bs {combo.calcular_precio():.2f}")


def ver_menu(rest):
    print("Dias:", ", ".join(DIAS))
    dia = input("Dia de la semana: ").strip().lower()
    if dia not in DIAS:
        raise ValueError("Dia no valido")
    print("MENU DEL", dia.upper())
    for p in rest.menu_disponible(dia):
        print(f"  {p.nombre} - Bs {p.calcular_precio():.2f}")


def registrar_cliente(rest):
    nombre = input("Nombre: ")
    telefono = input("Telefono (8 digitos): ")
    direccion = input("Direccion: ")
    rest.registrar_cliente(nombre, telefono, direccion)
    print("Cliente registrado")


def crear_pedido(rest):
    cliente = elegir_cliente(rest)
    print("1. Local   2. Para llevar   3. Delivery")
    tipo = int(input("Tipo de pedido: "))
    if tipo == 1:
        mesa = int(input("Mesa (1-15): "))
        rest.crear_pedido_local(cliente, mesa)
    elif tipo == 2:
        rest.crear_pedido_para_llevar(cliente)
    elif tipo == 3:
        zonas = []
        textos = []
        for z in ZONAS_ENVIO:
            zonas.append(z)
            textos.append(f"{z} (Bs {ZONAS_ENVIO[z]})")
        zona = zonas[elegir("Zona:", textos)]
        rest.crear_pedido_delivery(cliente, zona)
    else:
        raise ValueError("Tipo de pedido no valido")
    print("Pedido registrado")


def modificar_pedido(rest):
    pedido = elegir_pedido(rest)
    accion = input("1. Agregar producto   2. Quitar producto: ")
    if accion == "1":
        producto = elegir_producto(rest)
        cantidad = int(input("Cantidad: "))
        pedido.agregar_producto(producto, cantidad)
    elif accion == "2":
        productos = []
        textos = []
        for d in pedido.detalles:
            productos.append(d.producto)
            textos.append(d.producto.nombre)
        pedido.quitar_producto(productos[elegir("Quitar:", textos)])
    else:
        raise ValueError("Opcion no valida")
    print("Pedido actualizado")


def cambiar_estado(rest):
    pedido = elegir_pedido(rest)
    estados = [EN_PREPARACION, LISTO, ENTREGADO, CANCELADO]
    nuevo = estados[elegir("Nuevo estado:", estados)]
    pedido.cambiar_estado(nuevo)
    print("Estado actual:", pedido.estado)


def cobrar(rest):
    pedido = elegir_pedido(rest)
    print(f"Total a cobrar: Bs {pedido.calcular_total():.2f}")
    print("1. Efectivo   2. QR   3. Tarjeta")
    opcion = int(input("Metodo de pago: "))
    if opcion == 1:
        monto = float(input("Monto recibido: "))
        metodo = PagoEfectivo("Pago en efectivo", monto)
    elif opcion == 2:
        codigo = input("Codigo de transaccion (10 digitos): ")
        metodo = PagoQR("Pago por QR", codigo)
    elif opcion == 3:
        numero = input("Numero de tarjeta: ")
        metodo = PagoTarjeta("Pago con tarjeta", numero)
    else:
        raise ValueError("Metodo de pago no valido")
    pedido.pagar(metodo)
    metodo.generar_comprobante()


def main():
    rest = Restaurante()
    datos_ejemplo(rest)
    salir = False
    while not salir:
        print("\n===== SABOR VALLUNO =====")
        print("1. Registrar plato")
        print("2. Registrar bebida")
        print("3. Armar combo")
        print("4. Ver menu de un dia")
        print("5. Registrar cliente")
        print("6. Crear pedido")
        print("7. Agregar o quitar productos")
        print("8. Ver detalle del pedido")
        print("9. Cambiar estado del pedido")
        print("10. Cobrar pedido")
        print("11. Reporte de ventas de hoy")
        print("0. Salir")
        try:
            opcion = int(input("Opcion: "))
            if opcion == 0:
                salir = True
            elif opcion == 1:
                registrar_plato(rest)
            elif opcion == 2:
                registrar_bebida(rest)
            elif opcion == 3:
                armar_combo(rest)
            elif opcion == 4:
                ver_menu(rest)
            elif opcion == 5:
                registrar_cliente(rest)
            elif opcion == 6:
                crear_pedido(rest)
            elif opcion == 7:
                modificar_pedido(rest)
            elif opcion == 8:
                elegir_pedido(rest).mostrar_detalle()
            elif opcion == 9:
                cambiar_estado(rest)
            elif opcion == 10:
                cobrar(rest)
            elif opcion == 11:
                rest.mostrar_reporte(datetime.now())
            else:
                print("Opcion no valida")
        except ValueError as error:
            print("Error:", error)


main()

