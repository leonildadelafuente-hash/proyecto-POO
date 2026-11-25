from MetodoPago import MetodoPago


class PagoTarjeta(MetodoPago):
    def __init__(self, detalle, numero_tarjeta):
        super().__init__("Tarjeta", detalle)
        self.numero_tarjeta = numero_tarjeta
        self._comision = 0.03       # 3 % a cargo del cliente

    @property
    def numero_tarjeta(self):
        return self._numero_tarjeta

    @numero_tarjeta.setter
    def numero_tarjeta(self, valor):
        if not valor.isdigit():
            raise ValueError("El numero de tarjeta solo lleva digitos")
        self._numero_tarjeta = valor

    @property
    def comision(self):
        return self._comision

    # monto de la comision: 3 % del total
    def calcular_comision(self):
        return round(self._total * self._comision, 2)

    def procesar_pago(self, total):
        self._total = total

    def calcular_cambio(self):
        return 0        # con tarjeta no hay cambio

    def generar_comprobante(self):
        print("===== COMPROBANTE =====")
        print("Metodo:", self._tipo)
        print("Detalle:", self._detalle)
        print("Tarjeta: **** " + self._numero_tarjeta[-4:])
        print(f"Total del pedido: Bs {self._total:.2f}")
        print(f"Comision 3%: Bs {self.calcular_comision():.2f}")
        print(f"Total cobrado: Bs {self._total + self.calcular_comision():.2f}")