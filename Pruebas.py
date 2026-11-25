from datetime import datetime
from Producto import Producto
from Plato import Plato
from Bebida import Bebida
from Combo import Combo
from Cliente import Cliente
from Pedido import Pedido, EN_PREPARACION, LISTO, ENTREGADO, CANCELADO
from PedidoLocal import PedidoLocal
from PedidoParaLlevar import PedidoParaLlevar
from PedidoDelivery import PedidoDelivery
from MetodoPago import MetodoPago
from PagoEfectivo import PagoEfectivo
from PagoQR import PagoQR
from PagoTarjeta import PagoTarjeta
from Restaurante import Restaurante

# 22/11/2026 es domingo y 23/11/2026 es lunes
DOMINGO = datetime(2026, 11, 22, 13, 0)
LUNES = datetime(2026, 11, 23, 13, 0)

silpancho = Plato("Silpancho", 35)
chicharron = Plato("Chicharron", 50, ["domingo"])
vaso = Bebida("Mocochinchi vaso", 6, "refresco natural")
jarra = Bebida("Mocochinchi jarra", 6, "refresco natural", True)
cliente = Cliente("Ana Perez", "71234567", "Cercado")

combo = Combo("Combo Valluno")
combo.agregar_producto(silpancho)
combo.agregar_producto(vaso)


def prueba_caso_de_referencia():
    # combo = (35 + 6) * 0.90
    assert combo.calcular_precio() == 36.90
    # dos combos por delivery a Quillacollo = 73.80 + 15
    pedido = PedidoDelivery(cliente, "Quillacollo", LUNES)
    pedido.agregar_producto(combo, 2)
    assert pedido.calcular_subtotal() == 73.80
    assert pedido.calcular_total() == 88.80


def prueba_combo_dentro_de_combo():
    combo2 = Combo("Combo Doble")
    combo2.agregar_producto(combo)
    combo2.agregar_producto(silpancho)
    # (36.90 + 35) * 0.90 = 64.71
    assert combo2.calcular_precio() == 64.71
    assert combo2.contar_platos() == 2


def prueba_combo_no_se_contiene():
    try:
        combo.agregar_producto(combo)
        assert False
    except ValueError:
        pass


def prueba_envases_para_llevar():
    pedido = PedidoParaLlevar(cliente, LUNES)
    pedido.agregar_producto(combo, 2)      # 2 platos dentro de combos
    pedido.agregar_producto(silpancho)     # 1 plato
    assert pedido.calcular_cargos() == 6
    assert pedido.envases == 3


def prueba_envio_gratis():
    cercado = PedidoDelivery(cliente, "Cercado", LUNES)
    cercado.agregar_producto(silpancho, 5)     # Bs 175
    assert cercado.calcular_cargos() == 0
    sacaba = PedidoDelivery(cliente, "Sacaba", LUNES)
    sacaba.agregar_producto(silpancho, 5)
    assert sacaba.calcular_cargos() == 15


def prueba_pedido_minimo_delivery():
    pedido = PedidoDelivery(cliente, "Cercado", LUNES)
    pedido.agregar_producto(vaso)              # Bs 6, menos que el minimo
    try:
        pedido.cambiar_estado(EN_PREPARACION)
        assert False
    except ValueError:
        pass


def prueba_disponibilidad():
    assert chicharron.esta_disponible("domingo")
    assert not chicharron.esta_disponible("lunes")
    combo_ch = Combo("Combo Chicharron")
    combo_ch.agregar_producto(chicharron)
    combo_ch.agregar_producto(vaso)
    assert combo_ch.esta_disponible("domingo")
    assert not combo_ch.esta_disponible("martes")
    pedido = PedidoLocal(cliente, 1, LUNES)
    try:
        pedido.agregar_producto(chicharron)
        assert False
    except ValueError:
        pass


def prueba_estados():
    pedido = PedidoLocal(cliente, 3, DOMINGO)
    pedido.agregar_producto(silpancho)
    try:
        pedido.cambiar_estado(LISTO)           # no se puede saltar un estado
        assert False
    except ValueError:
        pass
    pedido.cambiar_estado(EN_PREPARACION)
    try:
        pedido.cambiar_estado(CANCELADO)       # solo se cancela desde REGISTRADO
        assert False
    except ValueError:
        pass
    try:
        pedido.agregar_producto(silpancho)     # solo se agrega en REGISTRADO
        assert False
    except ValueError:
        pass
    pedido.cambiar_estado(LISTO)
    pedido.cambiar_estado(ENTREGADO)
    otro = PedidoLocal(cliente, 4, DOMINGO)
    otro.cambiar_estado(CANCELADO)
    assert otro.estado == CANCELADO


def prueba_validaciones():
    try:
        Cliente("Luis", "51234567")            # no empieza en 6 o 7
        assert False
    except ValueError:
        pass
    try:
        Plato("Gratis", 0)                     # precio debe ser mayor que cero
        assert False
    except ValueError:
        pass
    try:
        PedidoLocal(cliente, 16)               # mesa del 1 al 15
        assert False
    except ValueError:
        pass
    pedido = PedidoLocal(cliente, 5, DOMINGO)
    try:
        pedido.agregar_producto(silpancho, 21) # cantidad de 1 a 20
        assert False
    except ValueError:
        pass


def prueba_jarra():
    assert jarra.calcular_precio() == 18


def prueba_clases_abstractas():
    for clase, args in [(Producto, ("x", 1)), (Pedido, (cliente, "x")), (MetodoPago, ("x", "y"))]:
        try:
            clase(*args)
            assert False
        except TypeError:
            pass


def prueba_mesa_ocupada():
    rest = Restaurante()
    cli = rest.registrar_cliente("Rosa", "61234567")
    rest.crear_pedido_local(cli, 7, DOMINGO)
    try:
        rest.crear_pedido_local(cli, 7, DOMINGO)
        assert False
    except ValueError:
        pass


def prueba_pagos():
    # efectivo: combo de 36.90 pagado con 50
    pedido = PedidoLocal(cliente, 8, DOMINGO)
    pedido.agregar_producto(combo)
    pedido.pagar(PagoEfectivo("Caja", 50))
    assert pedido.metodo_pago.calcular_cambio() == 13.10
    # el delivery no acepta tarjeta
    delivery = PedidoDelivery(cliente, "Quillacollo", LUNES)
    delivery.agregar_producto(combo, 2)
    try:
        delivery.pagar(PagoTarjeta("Tarjeta", "4111222233334444"))
        assert False
    except ValueError:
        pass
    delivery.pagar(PagoQR("QR", "1234567890"))
    # tarjeta: 70 + 3 % = 72.10
    local = PedidoLocal(cliente, 9, DOMINGO)
    local.agregar_producto(silpancho, 2)
    local.pagar(PagoTarjeta("Tarjeta", "4111222233334444"))
    assert local.metodo_pago.calcular_comision() == 2.10


def prueba_reporte():
    rest = Restaurante()
    pedido = PedidoDelivery(cliente, "Quillacollo", LUNES)
    pedido.agregar_producto(combo, 2)
    pedido.pagar(PagoQR("QR", "1234567890"))
    rest._pedidos.append(pedido)
    por_tipo, top = rest.reporte_ventas(LUNES)
    assert por_tipo["Delivery"][0] == 1
    assert top[0] == ("Combo Valluno", 2)


pruebas = [
    prueba_caso_de_referencia, prueba_combo_dentro_de_combo,
    prueba_combo_no_se_contiene, prueba_envases_para_llevar,
    prueba_envio_gratis, prueba_pedido_minimo_delivery,
    prueba_disponibilidad, prueba_estados, prueba_validaciones,
    prueba_jarra, prueba_clases_abstractas, prueba_mesa_ocupada,
    prueba_pagos, prueba_reporte,
]
for prueba in pruebas:
    prueba()
    print("OK:", prueba.__name__)
print("Todas las pruebas pasaron")