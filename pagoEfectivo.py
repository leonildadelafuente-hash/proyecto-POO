from MetodoPago import MetodoPago


class PagoEfectivo(MetodoPago):
    def __init__(self, detalle, monto_recibido):
        super().__init__("Efectivo", detalle)
        self.monto_recibido = monto_recibido

    @property
    def monto_recibido(self):
        return self._monto_recibido

    @monto_recibido.setter
    def monto_recibido(self, valor):
        if valor <= 0:
            raise ValueError("El monto recibido debe ser mayor que cero")
        self._monto_recibido = valor

    def procesar_pago(self, total):
        # el efectivo recibido tiene que alcanzar para pagar
        if self._monto_recibido < total:
            raise ValueError("El monto recibido no cubre el total")
        self._total = total

    def calcular_cambio(self):
        return round(self._monto_recibido - self._total, 2)

    def generar_comprobante(self):
        print("===== COMPROBANTE =====")
        print("Metodo:", self._tipo)
        print("Detalle:", self._detalle)
        print(f"Total: Bs {self._total:.2f}")
        print(f"Recibido: Bs {self._monto_recibido:.2f}")
        print(f"Cambio: Bs {self.calcular_cambio():.2f}")