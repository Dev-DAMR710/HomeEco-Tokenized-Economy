"""
-------------------------------------------------------------------------------
UNIVERSIDAD DE MANIZALES
Estudiante: Diego Alejandro Morales
Proyecto: HomeEco - Motor de Tareas y Estados
-------------------------------------------------------------------------------
En este modulo implementamos la logica concreta de los estados y las tareas.
Aplicamos el Patron State para manejar las transiciones y el calculo dinamico
de puntos segun el tipo de tarea.
"""

from datetime import datetime, timedelta
from typing import Optional
from home_eco.contratos import IEstadoTarea, ITarea, IUsuario
from home_eco.excepciones import TransicionEstadoInvalida, ErrorAuditoria

class EstadoDisponible(IEstadoTarea):
    @property
    def nombre(self) -> str:
        return "Disponible"

    def registrar_ejecucion(self, tarea: ITarea, usuario: IUsuario) -> None:
        tarea.ejecutor = usuario
        tarea.estado = EstadoPendiente()
        print(f"[!] Tarea '{tarea.descripcion}' registrada por {usuario.nombre}. Pendiente de validacion.")

    def validar(self, tarea: ITarea, validador: IUsuario) -> None:
        raise TransicionEstadoInvalida("No se puede validar una tarea que no ha sido ejecutada.")


class EstadoPendiente(IEstadoTarea):
    @property
    def nombre(self) -> str:
        return "Pendiente de Validacion"

    def registrar_ejecucion(self, tarea: ITarea, usuario: IUsuario) -> None:
        raise TransicionEstadoInvalida("Esta tarea ya ha sido realizada y espera validacion.")

    def validar(self, tarea: ITarea, validador: IUsuario) -> None:
        if tarea.ejecutor == validador:
            raise ErrorAuditoria("No puedes validar tu propia tarea. Se requiere auditoria cruzada.")
        
        puntos = tarea.calcular_puntos()
        tarea.ejecutor.acumular_puntos(puntos)
        tarea.estado = EstadoVerificado()
        print(f"[V] Tarea '{tarea.descripcion}' verificada por {validador.nombre}. {tarea.ejecutor.nombre} recibe {puntos} puntos.")


class EstadoVerificado(IEstadoTarea):
    @property
    def nombre(self) -> str:
        return "Verificada"

    def registrar_ejecucion(self, tarea: ITarea, usuario: IUsuario) -> None:
        raise TransicionEstadoInvalida("Esta tarea ya fue completada y verificada.")

    def validar(self, tarea: ITarea, validador: IUsuario) -> None:
        raise TransicionEstadoInvalida("Esta tarea ya ha sido verificada previamente.")


class TareaHogar(ITarea):
    """
    Tarea estandar que incrementa su valor con el paso del tiempo (Degradacion).
    """
    def __init__(self, descripcion: str, puntos_base: int, dias_retraso: int = 0):
        super().__init__(descripcion, puntos_base)
        self.estado = EstadoDisponible()
        # Simulamos dias de retraso para el calculo dinamico
        self.fecha_creacion = datetime.now() - timedelta(days=dias_retraso)

    def calcular_puntos(self) -> int:
        dias_transcurridos = (datetime.now() - self.fecha_creacion).days
        # Algoritmo de incremento: 5 puntos extra por cada dia de retraso
        incremento = dias_transcurridos * 5
        return self.puntos_base + incremento


class TareaUrgente(ITarea):
    """
    Tarea de alta prioridad con multiplicador fijo pero que expira pronto.
    """
    def __init__(self, descripcion: str, puntos_base: int, multiplicador: float = 2.0):
        super().__init__(descripcion, puntos_base)
        self.estado = EstadoDisponible()
        self.multiplicador = multiplicador

    def calcular_puntos(self) -> int:
        # Las tareas urgentes valen mucho mas desde el inicio
        return int(self.puntos_base * self.multiplicador)


class Usuario:
    """
    Implementacion concreta del usuario con balance de puntos.
    """
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.balance_puntos: float = 0.0

    def acumular_puntos(self, cantidad: float) -> None:
        self.balance_puntos += cantidad

    def deducir_puntos(self, cantidad: float) -> None:
        self.balance_puntos -= cantidad

    def __str__(self) -> str:
        return f"Usuario: {self.nombre} | Balance: {self.balance_puntos} pts"
