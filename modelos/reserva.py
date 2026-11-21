from modelos.cliente import Cliente
from modelos.servicio import Servicio
from excepciones.excepciones_personalizadas import ReservaInvalidaError, ParametroFaltanteError
from utils.logger import registrar_info, registrar_error

class Reserva:
    """Representa la reserva de un servicio por parte de un cliente."""
    
    # Estados posibles (simulan un Enum, pero más simple)
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: float):
        # ENCADENAMIENTO DE EXCEPCIONES: Si algo falla en la validación inicial, 
        # lo atrapamos y lanzamos nuestra excepción personalizada con 'from e'.
        try:
            if not isinstance(cliente, Cliente):
                raise TypeError("El objeto no es un Cliente válido.")
            if not isinstance(servicio, Servicio):
                raise TypeError("El objeto no es un Servicio válido.")
            if duracion <= 0:
                raise ValueError("La duración debe ser mayor a cero.")
            
            self.cliente = cliente
            self.servicio = servicio
            self.duracion = duracion
            self.estado = self.PENDIENTE
            self.costo_total = 0.0
            
            registrar_info(f"Reserva creada en estado PENDIENTE: {self.cliente.nombre} - {self.servicio.nombre}")
            
        except Exception as e:
            # Encadenamiento: 'from e' guarda el error original para trazabilidad
            raise ReservaInvalidaError("No se pudo crear la reserva debido a datos inválidos.") from e

    def procesar(self, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Procesa la reserva: valida el servicio, calcula el costo y confirma."""
        try:
            if self.estado == self.CANCELADA:
                raise ReservaInvalidaError("No se puede procesar una reserva cancelada.")
            if self.estado == self.CONFIRMADA:
                raise ReservaInvalidaError("La reserva ya fue confirmada previamente.")
                
            # Validamos que el servicio esté disponible (puede lanzar ServicioNoDisponibleError)
            self.servicio.validar()
            
            # Calculamos el costo (puede lanzar ParametroFaltanteError)
            self.costo_total = self.servicio.calcular_costo(self.duracion, impuesto, descuento)
            
            # Si todo sale bien, confirmamos
            self.estado = self.CONFIRMADA
            registrar_info(f"Reserva CONFIRMADA para {self.cliente.nombre}. Costo: ${self.costo_total}")
            return self.costo_total
            
        except (ReservaInvalidaError, ParametroFaltanteError) as e:
            # Registramos el error y lo relanzamos para que quien llamó se entere
            registrar_error(f"Error al procesar reserva: {e}")
            raise
        except Exception as e:
            # Atrapamos cualquier otro error inesperado, lo registramos y lanzamos uno nuevo encadenado
            registrar_error(f"Error inesperado procesando reserva: {e}")
            raise ReservaInvalidaError("Error grave al procesar la reserva.") from e

    def cancelar(self) -> None:
        """Cancela la reserva si es posible."""
        try:
            if self.estado == self.CANCELADA:
                raise ReservaInvalidaError("La reserva ya está cancelada.")
            
            self.estado = self.CANCELADA
            registrar_info(f"Reserva CANCELADA para {self.cliente.nombre}.")
            
        except Exception as e:
            registrar_error(f"Error al cancelar reserva: {e}")
            raise

    def describir(self) -> str:
        return (f"Reserva [{self.estado}] - Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Duración: {self.duracion}h | "
                f"Costo: ${self.costo_total}")