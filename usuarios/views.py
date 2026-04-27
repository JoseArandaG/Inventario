from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .db_utils import llamar_sp_login
from .utils import obtener_tokens_para_usuario
from .permission import TieneRol

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Llamamos a tu SP en Supabase
    resultado = llamar_sp_login(username, password)

    if resultado and resultado[0] == "Login exitoso":
        # Generamos los tokens con el rol incluido
        tokens = obtener_tokens_para_usuario(resultado)
        
        return Response({
            "status": "success",
            "tokens": tokens,
            "user": {
                "nombre": resultado[3],
                "rol": resultado[4]
            }
        })
    
    return Response({"status": "error", "message": "Credenciales incorrectas"}, status=401)