from utils.logger import registrar_info, registrar_error
from excepciones.excepciones_personalizadas import ClienteInvalidoError

registrar_info("Sistema iniciado correctamente.")
registrar_error("Prueba de error controlado.")

try:
    raise ClienteInvalidoError("Documento del cliente vacío.")
except ClienteInvalidoError as e:
    print(f"Capturada correctamente: {e}")
    registrar_error(f"ClienteInvalidoError: {e}")