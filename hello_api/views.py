import json
from xmlrpc.client import Transport
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from hello_api.entities.DTO import ResultDTO
from hello_api.entities.user import User
from hello_api.entities.animal import Animal

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