from modelos.servicio import Servicio
from excepciones.excepciones_personalizadas import ParametroFaltanteError

class ReservaSala(Servicio):
    """Servicio de reserva de salas. Cobra por hora."""
    
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, capacidad_personas: int):
        super().__init__(identificador, nombre, tarifa_base)
        self.capacidad_personas = capacidad_personas

    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if duracion <= 0:
            raise ParametroFaltanteError("La duración de la reserva debe ser mayor a cero.")
        
        # Si la sala es para más de 20 personas, cobra un recargo del 10%
        recargo = 1.10 if self.capacidad_personas > 20 else 1.0
        subtotal = (self.tarifa_base * duracion) * recargo
        
        return self._aplicar_tasas(subtotal, impuesto, descuento)

    def describir(self) -> str:
        return f"Reserva de Sala [{self.identificador}]: {self.nombre} (Capacidad: {self.capacidad_personas} pers.)"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos. Cobra por día."""
    
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(identificador, nombre, tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if duracion <= 0:
            raise ParametroFaltanteError("La duración del alquiler debe ser mayor a cero.")
        
        # Si se alquila por más de 5 días, se aplica un descuento automático del 5%
        descuento_auto = 0.05 if duracion >= 5 else 0.0
        subtotal = self.tarifa_base * duracion
        
        # Sumamos el descuento automático al descuento manual
        descuento_total = descuento + descuento_auto
        
        return self._aplicar_tasas(subtotal, impuesto, descuento_total)

    def describir(self) -> str:
        return f"Alquiler de Equipo [{self.identificador}]: {self.nombre} (Tipo: {self.tipo_equipo})"


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría. Cobra por hora, pero con un mínimo de 2 horas."""
    
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, especialidad: str):
        super().__init__(identificador, nombre, tarifa_base)
        self.especialidad = especialidad

    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if duracion <= 0:
            raise ParametroFaltanteError("La duración de la asesoría debe ser mayor a cero.")
        
        # Regla de negocio: las asesorías tienen un cobro mínimo de 2 horas
        horas_a_cobrar = max(duracion, 2.0)
        subtotal = self.tarifa_base * horas_a_cobrar
        
        return self._aplicar_tasas(subtotal, impuesto, descuento)

    def describir(self) -> str:
        return f"Asesoría Especializada [{self.identificador}]: {self.nombre} (Especialidad: {self.especialidad})"