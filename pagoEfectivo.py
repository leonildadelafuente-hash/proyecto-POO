from MetodoPago import MetodoPago
class PagoEfectivo(MetodoPago):
    def __init__(self, detalle, monto_recibido):
        super().__init__("Efectivo", detalle)
        self.monto_recibido = monto_recibido
    def procesar_pago(self):
        print(f"Procesando pago en efectivo: {self.detalle}")
    def generar_combrobante(self):
        print("Generando comprobante de pago en efectivo")
    def calcular_cambio(self, monto_pagado, monto_recibido):
        cambio = monto_recibido - monto_pagado
        if cambio < 0:
            print("Monto pagado insuficiente")
            return None
        print(f"Cambio a devolver: {cambio}")
        return cambio

    
