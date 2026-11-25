from Producto import Producto
from ComboProducto import ComboProducto
from variante import DESCUENTO_COMBO, MAX_PRODUCTOS_COMBO


class Combo(Producto):
    def __init__(self, nombre, descuento=DESCUENTO_COMBO):
        super().__init__(nombre)
        if descuento < 0 or descuento >= 1:
            raise ValueError("El descuento debe estar entre 0 y 1")
        self._descuento = descuento
        self._max_productos = []      # lista de ComboProducto (asi esta en el diagrama)

    @property
    def descuento(self):
        return self._descuento

    @property
    def max_productos(self):
        return list(self._max_productos)      # copia, para que nadie cambie la lista

    def agregar_producto(self, producto, cantidad=1):
        # un combo no puede contenerse a si mismo
        if producto is self:
            raise ValueError("Un combo no puede contenerse a si mismo")
        self._max_productos.append(ComboProducto(self, producto, cantidad))

    # un combo debe tener 2 o mas productos (y el maximo de la variante)
    def validar_combo(self):
        total = 0
        for item in self._max_productos:
            total += item.cantidad
        if total < 2:
            raise ValueError("Un combo debe tener 2 o mas productos")
        if MAX_PRODUCTOS_COMBO is not None and total > MAX_PRODUCTOS_COMBO:
            raise ValueError("El combo tiene demasiados productos")

    # suma de los productos, sin descuento
    def calcular_total(self):
        total = 0
        for item in self._max_productos:
            total += item.calcular_precio()     # si el producto es otro combo, usa su propio calcular_precio
        return round(total, 2)

    # suma de los productos menos el descuento
    def calcular_precio(self):
        return round(self.calcular_total() * (1 - self._descuento), 2)

    def calcular_descuento(self):
        return round(self.calcular_total() - self.calcular_precio(), 2)

    # el combo esta disponible solo si todos sus productos lo estan
    def esta_disponible(self, dia):
        for item in self._max_productos:
            if not item.producto.esta_disponible(dia):
                return False
        return True

    def contar_platos(self):
        total = 0
        for item in self._max_productos:
            total += item.producto.contar_platos() * item.cantidad
        return total
