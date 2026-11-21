from abc import ABC, abstractmethod

class Entidad(ABC):
    """Clase abstracta base para todas las entidades del sistema Software FJ."""
    
    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self) -> str:
        return self._identificador

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""
        pass

    @abstractmethod
    def validar(self) -> bool:
        """Valida la entidad. Debe lanzar excepción si es inválida."""
        pass