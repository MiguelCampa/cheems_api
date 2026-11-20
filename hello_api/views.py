import json
from xmlrpc.client import Transport
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from hello_api.entities.DTO import ResultDTO
from hello_api.entities.GamesDTO import GamesDTO
from hello_api.entities.user import User
from hello_api.entities.animal import Animal
from hello_api.entities.juegos import Videojuego

def index(request):
    return JsonResponse({"message": "Hello, World!"
        })

@csrf_exempt
@require_POST
def save_user(request):
    data =json.loads(request.body)

    user = User(data['id'], data['name'], data['account'])

    return JsonResponse({
        "id": user.id,
        "name": user.name,
        "account": user.account
    },status=201)

@csrf_exempt
@require_POST
def save_animal(request):
    data = json.loads(request.body)

    animal = Animal(data['name'], data['species'], data['color'])

    return JsonResponse({
        "name": animal.name,
        "species": animal.species,
        "color": animal.color
        },status=201)

@csrf_exempt
@require_POST
def save_DTO(request):
    try:
        data = json.loads(request.body)
        dto = ResultDTO(data['id'], data['success'], data['message'])

        return JsonResponse({
            "id": dto.id,
            "success": dto.success,
            "message": dto.message
        }, status=201)
    except (json.JSONDecodeError, KeyError, TypeError):
        dto = ResultDTO(False, "Failed to save DTO", None)

        return JsonResponse({
            "success": dto.success,
            "message": dto.message,
            "data": dto.data
        }, status=400)


@csrf_exempt
@require_POST
def videojuego(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido o cuerpo vacío"}, status=400)

    nombre = data.get('nombre')
    anio = data.get('anio')

    return JsonResponse({
        "message": "Videojuego recibido",
        "recibido": {"nombre": nombre, "anio": anio}
    }, status=200)


@csrf_exempt
@require_POST
def save_videojuego(request):
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict):
            return JsonResponse({"error": "El cuerpo JSON debe ser un objeto."}, status=400)

        nombre = data.get('nombre')
        anio = data.get('anio')

        if not nombre or not str(nombre).strip() or anio is None:
            return JsonResponse({"error": "Nombre y año son requeridos."}, status=400)

        try:
            anio = int(anio)
        except (TypeError, ValueError):
            return JsonResponse({"error": "El año debe ser un número entero."}, status=400)

        videojuego = Videojuego(nombre=str(nombre).strip(), anio=anio)
        id_videojuego = Videojuego.registrar_videojuego(videojuego)

        return JsonResponse({
            "success": True,
            "message": "Videojuego guardado exitosamente.",
            "videojuego": {"id_videojuego": id_videojuego, "nombre": videojuego.nombre, "anio": videojuego.anio}
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_GET
def get_videojuegos(request):
    try:
        busqueda = request.GET.get('busqueda')
        anio_param = request.GET.get('anio')
        anio = None

        if anio_param is not None and anio_param != "":
            try:
                anio = int(anio_param)
            except ValueError:
                return JsonResponse({"error": "El parámetro 'anio' debe ser un número entero."}, status=400)

        if busqueda or anio is not None:
            videojuegos = Videojuego.obtener_videojuegos(busqueda=busqueda, anio=anio)
        else:
            videojuegos = Videojuego.obtener_todos()

        return JsonResponse({"videojuegos": videojuegos}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_GET
def get_videojuego(request, id_videojuego):
    try:
        videojuego = Videojuego.obtener_videojuego_por_id(id_videojuego)
        resultado = GamesDTO(success=False).Respuesta_Juego(videojuego)

        if not resultado.success:
            return JsonResponse({"success": resultado.success, "message": resultado.message}, status=404)

        return JsonResponse({
            "success": resultado.success,
            "message": resultado.message,
            "videojuego": resultado.data
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT", "PATCH", "POST"])
def update_videojuego(request, id_videojuego):
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict):
            return JsonResponse({"error": "El cuerpo JSON debe ser un objeto."}, status=400)

        nombre = data.get('nombre')
        anio = data.get('anio')

        if nombre is None and anio is None:
            return JsonResponse({"error": "Debes enviar al menos 'nombre' o 'anio' para actualizar."}, status=400)

        if nombre is not None and not str(nombre).strip():
            return JsonResponse({"error": "El nombre no puede estar vacío."}, status=400)

        if anio is not None:
            try:
                anio = int(anio)
            except (TypeError, ValueError):
                return JsonResponse({"error": "El año debe ser un número entero."}, status=400)

        videojuego_actualizado = Videojuego.actualizar_videojuego(
            id_videojuego=id_videojuego,
            nombre=str(nombre).strip() if nombre is not None else None,
            anio=anio
        )

        if not videojuego_actualizado:
            return JsonResponse({"success": False, "message": "Videojuego no encontrado."}, status=404)

        return JsonResponse({
            "success": True,
            "message": "Videojuego actualizado exitosamente.",
            "videojuego": videojuego_actualizado
        }, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def delete_videojuego(request, id_videojuego):
    try:
        eliminado = Videojuego.eliminar_videojuego(id_videojuego)
        if not eliminado:
            return JsonResponse({"success": False, "message": "Videojuego no encontrado."}, status=404)

        return JsonResponse({
            "success": True,
            "message": "Videojuego eliminado exitosamente."
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)