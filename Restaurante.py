from Combo import Combo
from Cliente import Cliente
from Pedido import ENTREGADO, CANCELADO
from PedidoLocal import PedidoLocal
from PedidoParaLlevar import PedidoParaLlevar
from PedidoDelivery import PedidoDelivery


# gestor del menu, los clientes y los pedidos
class Restaurante:
    def __init__(self):
        self._productos = []
        self._clientes = []
        self._pedidos = []

    @property
    def productos(self):
        return list(self._productos)      # copia: no se modifica desde fuera

    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def pedidos(self):
        return list(self._pedidos)

    def registrar_producto(self, producto):
        self._productos.append(producto)

    def registrar_cliente(self, nombre, telefono, direccion):
        cliente = Cliente(nombre, telefono, direccion)   # Cliente valida sus datos
        self._clientes.append(cliente)
        return cliente

    # items: lista de tuplas (producto, cantidad)
    def armar_combo(self, nombre, items):
        combo = Combo(nombre)
        for producto, cantidad in items:
            combo.agregar_producto(producto, cantidad)
        combo.validar_combo()
        self._productos.append(combo)
        return combo

    def menu_disponible(self, dia):
        menu = []
        for p in self._productos:
            if p.esta_disponible(dia):
                menu.append(p)
        return menu

    def crear_pedido_local(self, cliente, mesa):
        # una mesa no puede tener dos pedidos abiertos
        for p in self._pedidos:
            if p.tipo == "Local" and p.mesa == mesa and p.estado not in (ENTREGADO, CANCELADO):
                raise ValueError("La mesa " + str(mesa) + " ya tiene un pedido abierto")
        pedido = PedidoLocal(cliente, mesa)
        self._pedidos.append(pedido)
        return pedido

    def crear_pedido_para_llevar(self, cliente):
        pedido = PedidoParaLlevar(cliente)
        self._pedidos.append(pedido)
        return pedido

    def crear_pedido_delivery(self, cliente, zona):
        pedido = PedidoDelivery(cliente, zona)
        self._pedidos.append(pedido)
        return pedido

    # reporte de ventas de un dia: por tipo de pedido y los 3 productos mas vendidos
    def mostrar_reporte(self, fecha):
        por_tipo = {}
        vendidos = {}
        for p in self._pedidos:
            if p.estado == CANCELADO or p.metodo_pago is None:
                continue
            if p.fecha.date() != fecha.date():
                continue
            por_tipo[p.tipo] = por_tipo.get(p.tipo, 0) + p.calcular_total()
            for d in p.detalles:
                nombre = d.producto.nombre
                vendidos[nombre] = vendidos.get(nombre, 0) + d.cantidad
        print("REPORTE DE VENTAS", fecha.strftime("%d/%m/%Y"))
        total = 0
        if len(por_tipo) == 0:
            print("  No hay ventas cobradas hoy")
        for tipo in por_tipo:
            print(f"  {tipo}: Bs {por_tipo[tipo]:.2f}")
            total += por_tipo[tipo]
        print(f"  TOTAL: Bs {total:.2f}")
        print("Top 3 productos mas vendidos:")
        ranking = sorted(vendidos.items(), key=lambda par: par[1], reverse=True)
        for nombre, cantidad in ranking[:3]:
            print(f"  {nombre}: {cantidad}")