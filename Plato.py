from Producto import Producto
from variante import DIAS


class Plato(Producto):
    def __init__(self, nombre, precio, dias_disponibles=None):
        super().__init__(nombre, precio)
        if dias_disponibles is None:
            dias_disponibles = DIAS      # si no se indica, se vende todos los dias
        self.dias_disponibles = dias_disponibles

    @property
    def dias_disponibles(self):
        return self._dias_disponibles

    @dias_disponibles.setter
    def dias_disponibles(self, valor):
        for dia in valor:
            if dia not in DIAS:
                raise ValueError("Dia no valido: " + dia)
        self._dias_disponibles = list(valor)

    def calcular_precio(self):
        return self._precio

    def esta_disponible(self, dia):
        return dia in self._dias_disponibles

    def contar_platos(self):
        return 1       # un plato cuenta como 1 plato
