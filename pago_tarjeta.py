from MetodoPago import MetodoPago
class PagoTarjeta(MetodoPago):
    def __init__(self, detalle, numero_tarjeta):
        super().__init__("Tarjeta", detalle)
        self.numero_tarjeta = numero_tarjeta
    def procesar_pago(self):
        print(f"Procesando pago con tarjeta: {self.detalle}")
    def generar_combrobante(self):
        print("Generando comprobante de pago con tarjeta")
    def calcular_cambio(self):
        print("No aplica para pagos con tarjeta")
        return None
    