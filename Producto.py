from abc import ABC, abstractmethod


class Producto(ABC):
    def __init__(self, nombre, precio=None):
        self.nombre = nombre
        self._precio = None
        # el Combo no recibe precio porque lo calcula con sus productos
        if precio is not None:
            self.precio = precio

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor.strip() == "":
            raise ValueError("El nombre no puede estar vacio")
        self._nombre = valor.strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        self._precio = valor

    @abstractmethod
    def calcular_precio(self):
        pass

    @abstractmethod
    def esta_disponible(self, dia):
        pass

    # agregado por el documento: sirve para contar los envases
    @abstractmethod
    def contar_platos(self):
        pass

    # agregado para mostrar los descuentos; solo el Combo tiene descuento
    def calcular_descuento(self):
        return 0
