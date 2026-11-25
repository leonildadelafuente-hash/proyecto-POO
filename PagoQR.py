from MetodoPago import MetodoPago


class PagoQR(MetodoPago):
    def __init__(self, detalle, codigo):
        super().__init__("QR", detalle)
        self.codigo = codigo

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not self.validar_codigo(valor):
            raise ValueError("El codigo debe tener 10 digitos")
        self._codigo = valor

    # el codigo es valido si tiene 10 caracteres y todos son numeros
    def validar_codigo(self, codigo):
        return len(codigo) == 10 and codigo.isdigit()

    def procesar_pago(self, total):
        self._total = total

    def calcular_cambio(self):
        return 0        # con QR se paga el monto exacto

    def generar_comprobante(self):
        print("===== COMPROBANTE =====")
        print("Metodo:", self._tipo)
        print("Detalle:", self._detalle)
        print("Codigo de transaccion:", self._codigo)
        print(f"Total: Bs {self._total:.2f}")