# TP: CRUD de Persona (GET y POST)

API REST en Python con Flask para dar de alta y consultar personas (DNI y nombre).

## Reglas
- El DNI no se puede repetir (devuelve 409).
- El nombre empieza con mayúscula, sigue con minúsculas y tiene como máximo 30 caracteres (si no, devuelve 400).

## Cómo correrlo
```bash
pip install -r requirements.txt
python app.py
```
La API queda en `http://127.0.0.1:5000`.

## Endpoints
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/personas` | Lista todas las personas |
| GET | `/personas/<dni>` | Trae una persona por DNI (404 si no existe) |
| POST | `/personas` | Crea una persona |

Body del POST (en Thunder Client: pestaña Body → JSON):
```json
{ "dni": 30123456, "nombre": "Juan" }
```

## Pruebas con Thunder Client
1. POST `/personas` con `{"dni": 30123456, "nombre": "Juan"}` → 201
2. Repetir el mismo POST → 409 "El DNI ya existe"
3. POST con `{"dni": 1, "nombre": "juan"}` → 400 (nombre inválido)
4. GET `/personas` → lista con Juan
5. GET `/personas/30123456` → Juan
6. GET `/personas/999` → 404
