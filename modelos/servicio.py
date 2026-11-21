from abc import ABC, abstractmethod
from modelos.entidad import Entidad
from excepciones.excepciones_personalizadas import ServicioNoDisponibleError, ParametroFaltanteError

class Servicio(Entidad, ABC):
    """Clase abstracta que representa un servicio ofrecido por Software FJ."""
    
    def __init__(self, identificador: str, nombre: str, tarifa_base: float):
        super().__init__(identificador)
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = True

    @abstractmethod
    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo del servicio. 
        Al tener parámetros opcionales (impuesto, descuento), simulamos
        la sobrecarga de métodos exigida en la guía."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Describe el servicio."""
        pass

    def validar(self) -> bool:
        """Validación genérica para todos los servicios."""
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")
        if self.tarifa_base <= 0:
            raise ServicioNoDisponibleError("La tarifa base debe ser mayor a cero.")
        return True

    def _aplicar_tasas(self, subtotal: float, impuesto: float, descuento: float) -> float:
        """Método auxiliar para aplicar impuestos y descuentos (evita repetir código)."""
        if impuesto < 0 or descuento < 0:
            raise ParametroFaltanteError("El impuesto y el descuento no pueden ser negativos.")
        
        total = subtotal * (1 + impuesto)  # Aplica impuesto
        total = total * (1 - descuento)    # Aplica descuento
        return round(total, 2)