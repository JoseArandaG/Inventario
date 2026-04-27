from django.shortcuts import render

# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .db_utils import llamar_sp_login

@api_view(['POST'])
@permission_classes([AllowAny]) # Cualquiera puede intentar loguearse
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    resultado = llamar_sp_login(username, password)

    if resultado and resultado[0] == "Login exitoso":
        # Extraemos los datos del usuario que devolvió el SP
        user_data = {
            "id": resultado[1],
            "username": resultado[2],
            "nombre": resultado[3],
            "rol": resultado[4]
        }

        # --- GENERACIÓN DEL TOKEN ---
        # Usamos el username para identificar al token (puedes usar el ID)
        refresh = RefreshToken.for_user(type('User', (), {'id': user_data['id'], 'username': user_data['username']}))
        
        return Response({
            "status": "success",
            "access": str(refresh.access_token), # Este es el que usará para todo
            "refresh": str(refresh),             # Este es para renovar el acceso
            "user": user_data
        })
    
    return Response({"status": "error", "message": resultado[0] if resultado else "Error"}, status=401)