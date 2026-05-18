"""
-------------------------------------------------------------------------------
UNIVERSIDAD DE MANIZALES
Estudiante: Diego Alejandro Morales
Proyecto: HomeEco - Sistema de Liquidacion y Auditoria
-------------------------------------------------------------------------------
Este modulo contiene el "cerebro" del sistema: el Motor de Economia.
Aqui se implementa el algoritmo de Suma Cero para equilibrar las cargas de 
trabajo domestico mediante compensaciones economicas.
"""

from typing import List, Dict
from home_eco.motor import Usuario, ITarea, EstadoVerificado

class MotorEconomia:
    """
    Gestiona el balance general de la casa y realiza el cierre semanal.
    Aplica conceptos de agregacion y logica algoritmica para la suma cero.
    """
    def __init__(self, valor_punto: float = 0.5):
        self.usuarios: List[Usuario] = []
        self.historial_tareas: List[ITarea] = []
        self.valor_punto = valor_punto  # Cuanto vale cada punto en dinero real

    def agregar_usuario(self, usuario: Usuario) -> None:
        self.usuarios.append(usuario)

    def registrar_tarea(self, tarea: ITarea) -> None:
        self.historial_tareas.append(tarea)

    def calcular_promedio_esfuerzo(self) -> float:
        """Calcula la media de puntos acumulados por todos los usuarios."""
        if not self.usuarios:
            return 0.0
        total_puntos = sum(u.balance_puntos for u in self.usuarios)
        return total_puntos / len(self.usuarios)

    def generar_reporte_liquidacion(self) -> str:
        """
        Genera el reporte de cierre semanal con el balance de suma cero.
        """
        promedio = self.calcular_promedio_esfuerzo()
        reporte = []
        reporte.append("="*60)
        reporte.append("       REPORTE DE LIQUIDACION SEMANAL - HOMEECO")
        reporte.append("="*60)
        reporte.append(f"Esfuerzo Promedio de la Casa: {promedio:.2f} pts\n")

        deudores = []
        acreedores = []

        for u in self.usuarios:
            diferencia = u.balance_puntos - promedio
            monto_dinero = diferencia * self.valor_punto
            
            estado = "SOBRE LA MEDIA" if diferencia >= 0 else "BAJO LA MEDIA"
            reporte.append(f"- {u.nombre:10} | Puntos: {u.balance_puntos:6.2f} | Dif: {diferencia:+7.2f} | {estado}")
            
            if diferencia < 0:
                deudores.append({'nombre': u.nombre, 'deuda': abs(monto_dinero)})
            elif diferencia > 0:
                acreedores.append({'nombre': u.nombre, 'credito': monto_dinero})

        reporte.append("\n" + "-"*60)
        reporte.append("           INSTRUCCIONES DE COMPENSACION")
        reporte.append("-"*60)

        if not deudores:
            reporte.append("La casa esta en perfecto equilibrio. No hay pagos pendientes.")
        else:
            # Algoritmo de distribucion de pagos
            for deudor in deudores:
                for acreedor in acreedores:
                    if deudor['deuda'] <= 0: break
                    if acreedor['credito'] <= 0: continue

                    pago = min(deudor['deuda'], acreedor['credito'])
                    reporte.append(f"[!] {deudor['nombre']} debe transferir ${pago:.2f} a {acreedor['nombre']}")
                    
                    deudor['deuda'] -= pago
                    acreedor['credito'] -= pago

        reporte.append("\n" + "="*60)
        return "\n".join(reporte)

class Auditor:
    """
    Clase de utilidad para centralizar validaciones de calidad.
    """
    @staticmethod
    def auditar_sistema(motor: MotorEconomia) -> bool:
        """Verifica que el sistema cumpla con la regla de suma cero."""
        total_diferencias = sum(u.balance_puntos - motor.calcular_promedio_esfuerzo() for u in motor.usuarios)
        # La suma de las diferencias respecto al promedio siempre debe ser (casi) cero
        return abs(total_diferencias) < 0.001
