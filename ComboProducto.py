from variante import CANTIDAD_MIN, CANTIDAD_MAX


# une un Combo con un producto y dice cuantas unidades lleva
class ComboProducto:
    def __init__(self, combo, producto, cantidad):
        if cantidad < CANTIDAD_MIN or cantidad > CANTIDAD_MAX:
            raise ValueError("La cantidad debe estar entre 1 y 20")
        self._combo = combo
        self._producto = producto
        self._cantidad = cantidad

    @property
    def combo(self):
        return self._combo

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    def calcular_precio(self):
        return self._producto.calcular_precio() * self._cantidad
