from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .db_utils import llamar_sp_login

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Ejecutamos el SP
            resultado = llamar_sp_login(username, password)

            if resultado:
                # El orden de 'resultado' depende de cómo definimos el RETURNS TABLE en SQL
                # [0] mensaje, [1] id, [2] username, [3] nombre, [4] rol, [5] fecha
                mensaje = resultado[0]
                
                if mensaje == "Login exitoso":
                    return JsonResponse({
                        "status": "success",
                        "message": mensaje,
                        "user_data": {
                            "id": resultado[1],
                            "username": resultado[2],
                            "nombre": resultado[3],
                            "rol": resultado[4]
                        }
                    }, status=200)
                else:
                    return JsonResponse({"status": "error", "message": mensaje}, status=401)
            
            return JsonResponse({"status": "error", "message": "Error interno"}, status=500)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
            
    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)