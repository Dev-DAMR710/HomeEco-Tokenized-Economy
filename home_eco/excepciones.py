"""
-------------------------------------------------------------------------------
UNIVERSIDAD DE MANIZALES
Estudiante: Diego Alejandro Morales
Proyecto: HomeEco
-------------------------------------------------------------------------------
Manejo de errores personalizados para el control de la logica de negocio.
"""

class HomeEcoError(Exception):
    """Clase base para errores del sistema HomeEco."""
    pass

class TransicionEstadoInvalida(HomeEcoError):
    """Se lanza cuando se intenta realizar una accion no permitida en el estado actual."""
    pass

class ErrorAuditoria(HomeEcoError):
    """Se lanza cuando un usuario intenta validarse a si mismo o realizar acciones sin permiso."""
    pass
