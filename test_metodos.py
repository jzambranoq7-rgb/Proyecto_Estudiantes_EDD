import os
import views

def test_completo():
    
    if os.path.exists("data/estudiantes.json"):
        os.remove("data/estudiantes.json")
    print("\n--- INICIO DE PRUEBAS DE MÉTODOS ---\n")

    
    print("1. Probando crear_estudiante()...")
    ok, msg = views.crear_estudiante({
        "nombre": "Carlos",
        "apellido": "Vera",
        "email": "carlos@escuela.edu",
        "carnet": "EST001"
    })
    print(f"   Resultado: {ok} -> {msg}")
    assert ok is True

    
    print("\n2. Probando validación de carnet duplicado...")
    ok, msg = views.crear_estudiante({
        "nombre": "Ana",
        "apellido": "Rios",
        "email": "ana@escuela.edu",
        "carnet": "EST001" 
    })
    print(f"   Resultado esperado (False): {ok} -> {msg}")
    assert ok is False

    
    views.crear_estudiante({
        "nombre": "Ana",
        "apellido": "Rios",
        "email": "ana@escuela.edu",
        "carnet": "EST002"
    })

    
    print("\n3. Probando obtener_todos()...")
    todos = views.obtener_todos()
    print(f"   Estudiantes registrados: {len(todos)}")
    assert len(todos) == 2

    
    print("\n4. Probando buscar_estudiantes()...")
    hallados = views.buscar_estudiantes("carlos")
    print(f"   Encontrados con 'carlos': {len(hallados)}")
    assert len(hallados) == 1

    
    print("\n5. Probando agregar_nota_estudiante()...")
    
    ok_inv, msg_inv = views.agregar_nota_estudiante(1, "Estructuras de Datos", 25)
    print(f"   Nota 25 rechazada: {not ok_inv} -> {msg_inv}")
    assert ok_inv is False

    
    views.agregar_nota_estudiante(1, "Estructuras de Datos", 18)
    views.agregar_nota_estudiante(1, "Programación", 20)
    views.agregar_nota_estudiante(2, "Estructuras de Datos", 15)
    views.agregar_nota_estudiante(2, "Base de Datos", 17)
    
    est1 = views.obtener_por_id(1)
    print(f"   Promedio estudiante 1: {est1.obtener_promedio()} (Esperado: 19.0)")
    assert est1.obtener_promedio() == 19.0

    
    print("\n6. Probando materias_ofertadas()...")
    materias = views.materias_ofertadas()
    print(f"   Materias registradas sin duplicar: {materias}")
    assert len(materias) == 3

    
    print("\n7. Probando materias en común...")
    ok, msg, comunes = views.estudiantes_en_comun(1, 2)
    print(f"   Comunes entre 1 y 2: {comunes}")
    assert "Estructuras De Datos" in comunes or "Estructuras de Datos" in comunes

    
    print("\n8. Probando actualizar_estudiante()...")
    ok, msg = views.actualizar_estudiante(1, {"nombre": "Carlos Alberto"})
    print(f"   Actualización: {ok} -> {msg}")
    assert ok is True

    
    print("\n9. Probando eliminar_estudiante()...")
    ok, msg = views.eliminar_estudiante(2)
    print(f"   Eliminación: {ok} -> {msg}")
    assert ok is True
    assert len(views.obtener_todos()) == 1

    print("\n TODAS LAS PRUEBAS UNITARIAS PASARON EXITOSAMENTE.")

if __name__ == "__main__":
    test_completo()