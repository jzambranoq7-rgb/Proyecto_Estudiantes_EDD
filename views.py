from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


def emails_registrados(excepto_id=None):
    """CONJUNTO para validar duplicados de email en O(1)."""
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def carnets_registrados(excepto_id=None):
    """CONJUNTO para validar duplicados de carnet en O(1)."""
    return {
        registro["carnet"].upper()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


#C

def crear_estudiante(datos):
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        if valores["carnet"].upper() in carnets_registrados():
            return False, f"El carnet '{valores['carnet']}' ya está registrado"

        valores["carnet"] = valores["carnet"].upper()
        estudiante = Estudiante(siguiente_id(), **valores)

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} creado con ID {estudiante.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


#R

def obtener_todos():
    return [Estudiante.desde_diccionario(reg) for reg in gestor.leer()]


def obtener_por_id(id_estudiante):
    for est in obtener_todos():
        if est.id == id_estudiante:
            return est
    return None


#S

def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for reg in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(reg.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(reg))
                break
    return encontrados


#U

def actualizar_estudiante(id_estudiante, cambios):
    try:
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"

        if "carnet" in cambios:
            cambios["carnet"] = cambios["carnet"].upper()
            if cambios["carnet"] in carnets_registrados(excepto_id=id_estudiante):
                return False, "Ese carnet ya lo usa otro estudiante"

        registros = gestor.leer()
        posicion = None
        for indice, reg in enumerate(registros):
            if reg["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un estudiante con ID {id_estudiante}"

        registros[posicion].update(cambios)
        gestor.guardar(registros)
        return True, f"Estudiante {id_estudiante} actualizado"

    except Exception as error:
        return False, f"Error inesperado: {error}"


#D

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    quedan = [reg for reg in registros if reg["id"] != id_estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con ID {id_estudiante}"

    gestor.guardar(quedan)
    return True, f"Estudiante {id_estudiante} eliminado"




def agregar_nota_estudiante(id_estudiante, materia, nota):
    """Agrega una nota (0 a 20) al estudiante indicado."""
    if not (0 <= nota <= 20):
        return False, "La nota debe estar comprendida entre 0 y 20"

    registros = gestor.leer()
    encontrado = False
    for reg in registros:
        if reg["id"] == id_estudiante:
            est = Estudiante.desde_diccionario(reg)
            est.agregar_nota(materia, nota)
            reg.update(est.a_diccionario())
            encontrado = True
            break

    if not encontrado:
        return False, f"No existe un estudiante con ID {id_estudiante}"

    gestor.guardar(registros)
    return True, f"Nota {nota} agregada a la materia '{materia}' para el estudiante {id_estudiante}"


def materias_ofertadas():
    """Devuelve un CONJUNTO con todas las materias registradas sin repetir."""
    todas = set()
    for est in obtener_todos():
        todas |= est.materias  # Unión de conjuntos
    return todas


def estudiantes_en_comun(id_a, id_b):
    """Devuelve las materias que comparten dos estudiantes usando intersección."""
    est_a = obtener_por_id(id_a)
    est_b = obtener_por_id(id_b)

    if not est_a:
        return False, f"No existe el estudiante con ID {id_a}", set()
    if not est_b:
        return False, f"No existe el estudiante con ID {id_b}", set()

    comunes = est_a.materias_en_comun(est_b)
    return True, f"Materias comunes entre {est_a.nombre} y {est_b.nombre}", comunes