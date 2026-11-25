# variante.py
# Aqui van los valores que cambian segun la variante del docente.
# CAMBIA los valores marcados con (*) por los de su enunciado.

# dias de la semana: en minuscula y empezando en lunes
# (Pedido usa DIAS[fecha.weekday()], por eso el orden importa)
DIAS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

# cantidad permitida por producto (DetallePedido y ComboProducto)
CANTIDAD_MIN = 1
CANTIDAD_MAX = 20

# combo
DESCUENTO_COMBO = 0.10        # (*) 0.10 = 10 % de descuento
MAX_PRODUCTOS_COMBO = None    # (*) None = sin limite, o pon un numero (ej: 5)

# pedido local
MESA_MIN = 1
MESA_MAX = 15

# pedido para llevar
ENVASE_POR_PLATO = 1          # (*) Bs que cuesta el envase de cada plato

# pedido delivery
ZONAS_ENVIO = {               # (*) zona: costo del envio en Bs
    "Cercado": 10,
    "Sacaba": 15,
    "Quillacollo": 15,
}
PEDIDO_MINIMO_DELIVERY = 30   # (*) subtotal minimo en Bs para delivery
ENVIO_GRATIS_DESDE = None     # (*) None = nunca gratis, o un monto (ej: 150)
ENVIO_GRATIS_SOLO_CERCADO = False   # (*) True = el envio gratis solo vale en Cercado
MINUTOS_RETRASO = None        # (*) None = no se controla, o minutos (ej: 45)
