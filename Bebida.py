from Producto import Producto


class Bebida(Producto):
    TIPOS = ["refresco natural", "gaseosa"]

    def __init__(self, nombre, precio_vaso, tipo, jarra=False):
        super().__init__(nombre, precio_vaso)
        self.tipo = tipo
        self._jarra = jarra       # True si la bebida se vende en jarra

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        if valor not in self.TIPOS:
            raise ValueError("Tipo de bebida no valido")
        self._tipo = valor

    # precio de la jarra: 3 veces el precio del vaso
    def jarra(self):
        return round(self._precio * 3, 2)

    def calcular_precio(self):
        if self._jarra:
            return self.jarra()
        return self._precio

    def esta_disponible(self, dia):
        return True

    def contar_platos(self):
        return 0       # las bebidas no cuentan como plato
