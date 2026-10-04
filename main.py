from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota_estudiante,
    materias_ofertadas, estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'CARNET':<14}{'NOMBRE':<25}{'EMAIL':<26}{'PROMEDIO':<8}")
    print("-" * 78)
    for est in estudiantes:
        print(f"{est.id:<5}{est.carnet:<14}{est.obtener_nombre_completo():<25}"
              f"{est.email:<26}{est.obtener_promedio():<8}")
    print("-" * 78)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("No hay estudiantes registrados.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email o carnet: ")
    encontrados = buscar_estudiantes(termino)
    if not encontrados:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    try:
        id_est = int(input("ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"No existe un estudiante con ID {id_est}")
    else:
        print(f"ID       : {est.id}")
        print(f"Carnet   : {est.carnet}")
        print(f"Nombre   : {est.obtener_nombre_completo()}")
        print(f"Email    : {est.email}")
        print(f"Materias : {', '.join(sorted(est.materias)) if est.materias else 'Ninguna'}")
        print(f"Notas    : {est.notas}")
        print(f"Promedio : {est.obtener_promedio()}")
    pausa()


def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_est = int(input("ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser un entero.")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"No existe un estudiante con ID {id_est}")
        return pausa()

    imprimir_info(f"Editando a {est.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no desee cambiar.\n")

    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(est, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_est, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_est = int(input("ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"No existe un estudiante con ID {id_est}")
        return pausa()

    imprimir_info(f"Se eliminará a: {est}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_est)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA A ESTUDIANTE")
    try:
        id_est = int(input("ID del estudiante: "))
        materia = input("Materia: ").strip()
        nota = float(input("Nota (0 - 20): "))
    except ValueError:
        imprimir_error("Valores numéricos inválidos.")
        return pausa()

    exito, mensaje = agregar_nota_estudiante(id_est, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS (TOTAL)")
    materias = materias_ofertadas()
    if not materias:
        imprimir_info("No hay materias registradas aún.")
    else:
        for m in sorted(materias):
            print(f"  • {m}")
        imprimir_info(f"Total: {len(materias)} materias únicas")
    pausa()


def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN ENTRE DOS ESTUDIANTES")
    try:
        id_a = int(input("ID del primer estudiante: "))
        id_b = int(input("ID del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los IDs deben ser números enteros.")
        return pausa()

    exito, mensaje, comunes = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(mensaje)
    else:
        imprimir_info(mensaje)
        if comunes:
            print(f"Materias compartidas: {', '.join(sorted(comunes))}")
        else:
            print("No comparten ninguna materia.")
    pausa()


def salir():
    imprimir_info("¡Hasta luego!")
    return "salir"


OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos los estudiantes", opcion_ver_todos),
    "3": ("Buscar estudiante", opcion_buscar),
    "4": ("Ver por ID (Detalles)", opcion_ver_por_id),
    "5": ("Actualizar estudiante", opcion_actualizar),
    "6": ("Eliminar estudiante", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver todas las materias ofertadas", opcion_materias_ofertadas),
    "9": ("Materias en común entre 2 estudiantes", opcion_materias_en_comun),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    for tecla, (texto, _) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()
        if tecla not in OPCIONES:
            imprimir_error("Opción inválida.")
            pausa()
            continue

        _, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma finalizado.")