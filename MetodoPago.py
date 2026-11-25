from abc import ABC, abstractmethod


class MetodoPago(ABC):
    def __init__(self, tipo, detalle):
        self._tipo = tipo
        self.detalle = detalle      # usa el setter para validar
        self._total = 0

    @property
    def tipo(self):
        return self._tipo

    @property
    def detalle(self):
        return self._detalle

    @detalle.setter
    def detalle(self, valor):
        if valor.strip() == "":
            raise ValueError("El detalle no puede estar vacio")
        self._detalle = valor

    @abstractmethod
    def procesar_pago(self, total):
        pass

    @abstractmethod
    def generar_comprobante(self):
        pass

    @abstractmethod
    def calcular_cambio(self):
        pass