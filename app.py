import re

from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False  # para que "José" se vea bien en las respuestas

# Nombre: primera letra mayúscula, resto minúsculas, máximo 30 caracteres en total
PATRON_NOMBRE = re.compile(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñü]{0,29}$")

# "Base de datos" en memoria: la clave es el DNI, así no se puede repetir
personas = {}


def validar_persona(datos):
    """Devuelve un mensaje de error, o None si los datos son válidos."""
    if not isinstance(datos, dict):
        return "Se esperaba un JSON con dni y nombre"

    dni = datos.get("dni")
    nombre = datos.get("nombre")

    if not isinstance(dni, int) or isinstance(dni, bool) or dni <= 0:
        return "El DNI debe ser un número entero positivo"
    if not isinstance(nombre, str) or not PATRON_NOMBRE.match(nombre):
        return ("El nombre debe empezar con mayúscula, seguir con minúsculas "
                "y tener como máximo 30 caracteres")
    return None


@app.get("/personas")
def listar_personas():
    return jsonify(list(personas.values())), 200


@app.get("/personas/<int:dni>")
def obtener_persona(dni):
    persona = personas.get(dni)
    if persona is None:
        return jsonify({"error": "Persona no encontrada"}), 404
    return jsonify(persona), 200


@app.post("/personas")
def crear_persona():
    datos = request.get_json(silent=True)

    error = validar_persona(datos)
    if error:
        return jsonify({"error": error}), 400

    if datos["dni"] in personas:
        return jsonify({"error": "El DNI ya existe"}), 409

    persona = {"dni": datos["dni"], "nombre": datos["nombre"]}
    personas[persona["dni"]] = persona
    return jsonify(persona), 201


if __name__ == "__main__":
    app.run(debug=True)
