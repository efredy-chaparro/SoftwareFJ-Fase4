from modelos.entidad import Entidad
from excepciones.excepciones_personalizadas import ClienteInvalidoError
from utils.logger import registrar_info, registrar_error
import re

class Cliente(Entidad):
    """Representa un cliente. Usa encapsulación con atributos privados (__)."""
    
    def __init__(self, identificador: str, nombre: str, documento: str, email: str, telefono: str):
        super().__init__(identificador)
        # Atributos privados (doble guion bajo)
        self.__nombre = None
        self.__documento = None
        self.__email = None
        self.__telefono = None
        
        # Usamos los setters para validar desde la creación
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    # --- PROPIEDADES (GETTERS Y SETTERS) ---

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        if not valor.replace(" ", "").isalpha():
            raise ClienteInvalidoError("El nombre solo debe contener letras.")
        self.__nombre = valor.strip().title()

    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str):
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El documento no puede estar vacío.")
        if not valor.isdigit():
            raise ClienteInvalidoError("El documento debe ser numérico.")
        self.__documento = valor.strip()

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        # Validación simple con expresión regular
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not valor or not re.match(patron, valor):
            raise ClienteInvalidoError(f"El email '{valor}' no es válido.")
        self.__email = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El teléfono no puede estar vacío.")
        # Permite números y el signo +
        if not re.match(r'^\+?\d{7,15}$', valor):
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 15 dígitos.")
        self.__telefono = valor.strip()

    # --- MÉTODOS ABSTRACTOS IMPLEMENTADOS ---

    def describir(self) -> str:
        return f"Cliente [{self.identificador}]: {self.nombre} (Doc: {self.documento}) - Email: {self.email}"

    def validar(self) -> bool:
        # Al usar properties en el __init__, si es inválido ya lanzó error.
        # Este método sirve para re-validar si se requiere.
        if not self.__nombre or not self.__documento or not self.__email or not self.__telefono:
            raise ClienteInvalidoError("El cliente tiene datos incompletos.")
        return True