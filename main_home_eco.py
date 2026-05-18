"""
*******************************************************************************
*                                                                             *
*                 HOMEECO: ECONOMIA DOMESTICA TOKENIZADA                      *
*                        UNIVERSIDAD DE MANIZALES                             *
*                 Estudiante: Diego Alejandro Morales                         *
*                                                                             *
*******************************************************************************

NOTA PARA EL PROFESOR:
Estimado profesor, quiero expresar mi mas sincero agradecimiento por el 
conocimiento brindado y por las historias compartidas en clase, las cuales 
no solo nos enseñan código, sino tambien visión empresarial. 

Este programa es la aplicacion practica de los conceptos avanzados de POO 
adquiridos en su asignatura para resolver una problematica latente en mi hogar: 
la reparticion justa de las tareas para un buen vivir. Es increible como algo 
que parece tan cotidiano puede ser un reto de ingenieria, y como a traves de 
la tecnologia y el conocimiento, espero que la convivencia mejore no solo en 
mi casa, sino que este modelo pueda ayudar a mas personas en situaciones similares.

*******************************************************************************
"""

import sys
import os

# Configuracion de rutas para el paquete modular
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from home_eco.motor import Usuario, TareaHogar, TareaUrgente
    from home_eco.economia import MotorEconomia, Auditor
    from home_eco.excepciones import HomeEcoError
except ImportError:
    # Soporte para ejecucion directa si los archivos estan en el mismo nivel
    from motor import Usuario, TareaHogar, TareaUrgente
    from economia import MotorEconomia, Auditor
    from excepciones import HomeEcoError

def imprimir_separador(titulo: str):
    """Organizador visual de consola con estilo academico."""
    print(f"\n{'='*80}")
    print(f"  {titulo.upper()}")
    print(f"{'='*80}")

def ejecutar_sistema():
    # 1. Bienvenida y Nota Personal
    print(__doc__)
    
    # 2. Inicializacion: Cada punto equivale a $100 pesos colombianos (ejemplo)
    motor = MotorEconomia(valor_punto=100.0)
    
    diego = Usuario("Diego")
    ana = Usuario("Ana")
    carlos = Usuario("Carlos")
    
    motor.agregar_usuario(diego)
    motor.agregar_usuario(ana)
    motor.agregar_usuario(carlos)

    # 3. Ciclo Semanal Simulado
    imprimir_separador("Registro de Actividades de la Semana")
    
    # Tarea Hogar con 5 dias de retraso (Sube su valor dinamicamente)
    t1 = TareaHogar("Limpieza profunda de nevera", puntos_base=50, dias_retraso=5)
    # Tarea Urgente (Multiplicador de prioridad)
    t2 = TareaUrgente("Reparacion de fuga en lavadero", puntos_base=80, multiplicador=2.5)
    # Tarea Hogar cotidiana
    t3 = TareaHogar("Organizacion de sala y comedor", puntos_base=30)
    # Tarea Hogar con 2 dias de retraso
    t4 = TareaHogar("Lavar ropa de cama", puntos_base=40, dias_retraso=2)

    # 4. Simulacion de Ejecucion y Auditoria Democratica
    # Diego asume la tarea mas pesada (nevera)
    t1.estado.registrar_ejecucion(t1, diego)
    t1.estado.validar(t1, ana) # Ana valida el trabajo de Diego

    # Ana resuelve la urgencia
    t2.estado.registrar_ejecucion(t2, ana)
    t2.estado.validar(t2, carlos) # Carlos valida el trabajo de Ana

    # Carlos organiza la sala
    t3.estado.registrar_ejecucion(t3, carlos)
    t3.estado.validar(t3, diego) # Diego valida el trabajo de Carlos

    # 5. Cierre de Ciclo y Liquidacion de Suma Cero
    imprimir_separador("Cierre Economico Semanal")
    print(motor.generar_reporte_liquidacion())

    # 6. Verificacion Final de Calidad
    imprimir_separador("Auditoria de Integridad del Sistema")
    if Auditor.auditar_sistema(motor):
        print("[V] VERIFICACION EXITOSA: El sistema cumple con el principio de Suma Cero.")
        print("[V] Todos los balances cuadran matematicamente.")
    else:
        print("[X] ERROR CRITICO: Se ha detectado una inconsistencia en el balance.")

    print(f"\n{'*'*80}")
    print("                HOMEECO - TECNOLOGIA PARA LA CONVIVENCIA")
    print(f"{'*'*80}\n")

if __name__ == "__main__":
    try:
        ejecutar_sistema()
    except HomeEcoError as e:
        print(f"\n[!] ERROR DE LOGICA DE NEGOCIO: {e}")
    except Exception as e:
        print(f"\n[!] ERROR INESPERADO DEL SISTEMA: {e}")
