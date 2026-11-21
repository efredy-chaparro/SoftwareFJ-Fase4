from modelos.cliente import Cliente
from modelos.servicios_especializados import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from modelos.reserva import Reserva
from excepciones.excepciones_personalizadas import (
    ClienteInvalidoError, 
    ServicioNoDisponibleError, 
    ReservaInvalidaError, 
    ParametroFaltanteError,
    SoftwareFJError
)
from utils.logger import registrar_info, registrar_error

def ejecutar_simulacion():
    print("==================================================")
    print("   SISTEMA INTEGRAL SOFTWARE FJ - SIMULACIÓN")
    print("==================================================\n")
    registrar_info("--- INICIO DE LA SIMULACIÓN GLOBAL ---")

    # ---------------------------------------------------------
    # OPERACIÓN 1: Registro VÁLIDO de Cliente
    # ---------------------------------------------------------
    print("Op 1: Registro válido de cliente...")
    try:
        cliente1 = Cliente("C001", "Didier Martinez", "1098765432", "didier@email.com", "+573001234567")
        print("    Cliente creado:", cliente1.nombre)
    except Exception as e:
        print("    Error:", e)

    # ---------------------------------------------------------
    # OPERACIÓN 2: Registro INVÁLIDO de Cliente (Email malo)
    # ---------------------------------------------------------
    print("\nOp 2: Registro inválido de cliente (email malo)...")
    try:
        cliente2 = Cliente("C002", "Ana Gomez", "123", "ana-correo-malo", "3001234567")
    except ClienteInvalidoError as e:
        print(f"    Error esperado capturado: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 3: Creación CORRECTA de Servicio
    # ---------------------------------------------------------
    print("\nOp 3: Creación correcta de servicio (Sala)...")
    try:
        sala1 = ReservaSala("S001", "Sala de Juntas A", 45000, 15)
        print("    Servicio creado:", sala1.describir())
    except Exception as e:
        print("    Error:", e)

    # ---------------------------------------------------------
    # OPERACIÓN 4: Creación INCORRECTA de Servicio (Tarifa negativa)
    # ---------------------------------------------------------
    print("\nOp 4: Creación incorrecta de servicio (Tarifa negativa)...")
    try:
        equipo_malo = AlquilerEquipo("E002", "Laptop Dañada", -50000, "Computo")
        equipo_malo.validar() # Esto lanzará el error
    except ServicioNoDisponibleError as e:
        print(f"    Error esperado capturado: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 5: Reserva EXITOSA
    # ---------------------------------------------------------
    print("\nOp 5: Reserva exitosa...")
    try:
        reserva1 = Reserva(cliente1, sala1, duracion=4)
        costo1 = reserva1.procesar(impuesto=0.19)
        print(f"    Reserva realizada. Costo total: ${costo1}")
    except Exception as e:
        print("    Error inesperado:", e)

    # ---------------------------------------------------------
    # OPERACIÓN 6: Reserva FALLIDA (Servicio No Disponible)
    # ---------------------------------------------------------
    print("\nOp 6: Reserva fallida (Servicio ocupado)...")
    try:
        asesoria = AsesoriaEspecializada("A001", "Asesoría en Redes", 80000, "Redes")
        asesoria.disponible = False # Lo bloqueamos
        reserva2 = Reserva(cliente1, asesoria, duracion=2)
        reserva2.procesar()
    except SoftwareFJError as e:
        print(f"    Error esperado capturado: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 7: Reserva FALLIDA (Parámetro faltante/error en cálculo)
    # ---------------------------------------------------------
    print("\nOp 7: Reserva fallida (Duración negativa)...")
    try:
        equipo1 = AlquilerEquipo("E001", "Proyector 4K", 25000, "Video")
        # Al procesar, calculará el costo y la duración negativa lanzará excepción
        reserva3 = Reserva(cliente1, equipo1, duracion=-2)
        reserva3.procesar()
    except (ReservaInvalidaError, ParametroFaltanteError) as e:
        print(f"    Error esperado capturado: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 8: Cancelación de Reserva
    # ---------------------------------------------------------
    print("\nOp 8: Cancelación de reserva...")
    try:
        cliente3 = Cliente("C003", "Carlos Ruiz", "55566677", "carlos@email.com", "3115556666")
        sala2 = ReservaSala("S002", "Sala Creativa", 30000, 10)
        reserva4 = Reserva(cliente3, sala2, duracion=2)
        reserva4.cancelar()
        print("    Reserva cancelada correctamente.")
    except Exception as e:
        print("    Error inesperado:", e)

    # ---------------------------------------------------------
    # OPERACIÓN 9: Intento de procesar reserva cancelada (Falla lógica)
    # ---------------------------------------------------------
    print("\nOp 9: Procesar reserva cancelada (debe fallar)...")
    try:
        reserva4.procesar()
    except ReservaInvalidaError as e:
        print(f"    Error esperado capturado: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 10: Reserva con Descuento y Sobrecarga
    # ---------------------------------------------------------
    print("\nOp 10: Reserva con descuento (Demostración de sobrecarga)...")
    try:
        cliente4 = Cliente("C004", "Sofia Lopez", "99887766", "sofia@email.com", "3223334444")
        asesoria2 = AsesoriaEspecializada("A002", "Asesoría en IA", 120000, "IA")
        reserva5 = Reserva(cliente4, asesoria2, duracion=3)
        # Aplicamos un descuento del 15% y un IVA del 19%
        costo5 = reserva5.procesar(impuesto=0.19, descuento=0.15)
        print(f"    Reserva con descuento realizada. Costo total: ${costo5}")
    except Exception as e:
        print("    Error:", e)

    print("\n==================================================")
    print("   SIMULACIÓN FINALIZADA - REVISA LOS LOGS")
    print("==================================================")
    registrar_info("--- FIN DE LA SIMULACIÓN GLOBAL ---")

if __name__ == "__main__":
    ejecutar_simulacion()