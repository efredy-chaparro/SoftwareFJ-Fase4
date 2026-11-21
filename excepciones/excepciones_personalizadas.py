class SoftwareFJError(Exception):
    pass

class ClienteInvalidoError(SoftwareFJError):
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    pass

class ReservaInvalidaError(SoftwareFJError):
    pass

class ParametroFaltanteError(SoftwareFJError):
    pass