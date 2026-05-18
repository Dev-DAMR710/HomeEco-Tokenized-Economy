"""
-------------------------------------------------------------------------------
UNIVERSIDAD DE MANIZALES
Estudiante: Diego Alejandro Morales
Proyecto: HomeEco - Sistema de Economia Domestica Tokenizada
-------------------------------------------------------------------------------
Este modulo establece los "contratos" o interfaces base del sistema. 
Utilizamos Clases Base Abstractas (ABC) para garantizar que cualquier tipo de 
tarea o estado implementado en el futuro siga las reglas de nuestra arquitectura.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Protocol

class IEstadoTarea(ABC):
    """
    Interfaz que define el comportamiento de los estados de una tarea.
    Aplicamos el Patron State para delegar la logica de transicion a objetos especificos.
    """
    @abstractmethod
    def registrar_ejecucion(self, tarea: 'ITarea', usuario: 'IUsuario') -> None:
        """Define que sucede cuando alguien intenta realizar la tarea en este estado."""
        pass

    @abstractmethod
    def validar(self, tarea: 'ITarea', validador: 'IUsuario') -> None:
        """Define las reglas para que una tarea pase de pendiente a verificada."""
        pass

    @property
    @abstractmethod
    def nombre(self) -> str:
        """Retorna el nombre descriptivo del estado."""
        pass


class ITarea(ABC):
    """
    Contrato base para todas las tareas del hogar.
    Define la estructura que permite el calculo dinamico de puntos y la gestion de estados.
    """
    def __init__(self, descripcion: str, puntos_base: int):
        self.descripcion = descripcion
        self.puntos_base = puntos_base
        self.fecha_creacion = datetime.now()
        self._estado: IEstadoTarea = None  # Se inicializara en las clases concretas
        self.ejecutor: 'IUsuario' = None

    @abstractmethod
    def calcular_puntos(self) -> int:
        """
        Calcula el valor actual de la tarea. 
        Este metodo es el corazon de la economia dinamica del sistema.
        """
        pass

    @property
    def estado(self) -> IEstadoTarea:
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado: IEstadoTarea):
        self._estado = nuevo_estado


class IUsuario(Protocol):
    """
    Definicion del protocolo de Usuario. 
    Usamos Protocol para permitir una estructura flexible de usuarios sin 
    obligar a una jerarquia de herencia rigida si no es necesario.
    """
    nombre: str
    balance_puntos: float

    def acumular_puntos(self, cantidad: float) -> None:
        ...

    def deducir_puntos(self, cantidad: float) -> None:
        ...
