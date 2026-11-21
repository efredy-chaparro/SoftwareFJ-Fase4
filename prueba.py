from modelos.cliente import Cliente
from modelos.servicios_especializados import ReservaSala, AlquilerEquipo
from modelos.reserva import Reserva
from excepciones.excepciones_personalizadas import ReservaInvalidaError, ParametroFaltanteError
from utils.logger import registrar_info, registrar_error

print("--- PRUEBA DEL BLOQUE 4 (RESERVAS) ---")

# 1. Reserva Exitosa
try:
    c1 = Cliente("C001", "Juan Perez", "12345678", "juan@email.com", "3001234567")
    s1 = ReservaSala("S001", "Sala Magna", 50000, 30)
    
    reserva1 = Reserva(c1, s1, duracion=3)
    costo = reserva1.procesar(impuesto=0.19)
    print(f" Reserva Exitosa: {reserva1.describir()}")
    print(f"   Costo final: ${costo}")
    
except Exception as e:
    print(" Error:", e)

# 2. Intento de procesar una reserva ya confirmada (Debe fallar)
try:
    reserva1.procesar() # Ya está confirmada arriba
except ReservaInvalidaError as e:
    print(" Error capturado (ya confirmada):", e)

# 3. Reserva con datos inválidos (Encadenamiento de excepciones)
try:
    # Intentamos crear una reserva con duración negativa
    reserva_mala = Reserva(c1, s1, duracion=-5)
except ReservaInvalidaError as e:
    print(" Error capturado (creación inválida):", e)
    # Aquí puedes ver el encadenamiento si revisas el log o usas e.__cause__

# 4. Cancelar y luego procesar (Debe fallar)
try:
    c2 = Cliente("C002", "Maria", "87654321", "maria@email.com", "3009876543")
    s2 = AlquilerEquipo("E001", "Proyector", 20000, "Video")
    reserva2 = Reserva(c2, s2, duracion=2)
    reserva2.cancelar()
    reserva2.procesar() # Error porque está cancelada
except ReservaInvalidaError as e:
    print(" Error capturado (cancelada):", e)