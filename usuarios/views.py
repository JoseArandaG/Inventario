from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from .db_utils import actualizar_usuario_sp, cambiar_password_sp, crear_usuario_sp, eliminar_usuario_sp, gestionar_bloqueo_sp, listar_usuario_sp, login_sp, modificar_estado_usuario_sp
from .utils import obtener_tokens_para_usuario
from .permission import TieneRol

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Llamamos a tu SP en Supabase
    resultado = login_sp(username, password)

    if resultado and resultado[0] == "Login exitoso":
        
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
            
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

# Listar Usuarios
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Solo usuarios logueados pueden ver la lista
def usuario_listar(request):
    try:
        usuarios = listar_usuario_sp()
        return Response({
            "status": "success", 
            "usuarios": usuarios
        })
    except Exception as e:
        return Response({
            "status": "error", 
            "message": str(e)
        }, status=500)
        

# Crear Usuario
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Recomendado: solo personal autorizado crea usuarios
def usuario_crear(request):
    try:
        # Extraemos los datos del JSON enviado desde el Front o Postman
        data = request.data
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        password = data.get('password') # Recuerda que luego deberías encriptarla
        direccion = data.get('direccion')
        correo = data.get('correo')
        telefono = data.get('telefono')

        # Llamada al SP
        nuevo_username = crear_usuario_sp(nombre, apellido, password, direccion, correo, telefono)

        if nuevo_username:
            # Opcional: Crear también el usuario en la tabla de Django para que pueda loguearse luego
            User.objects.create_user(username=nuevo_username, email=correo)
            
            return Response({
                "status": "success",
                "message": "Usuario creado exitosamente",
                "username": nuevo_username
            }, status=201)
        
        return Response({"status": "error", "message": "No se pudo crear el usuario"}, status=400)

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)

#Actualizar Usuario
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def usuario_actualizar(request):
    try:
        data = request.data
        username = data.get('username')

        if not username:
            return Response({"status": "error", "message": "Username requerido"}, status=400)

        # Intentamos ejecutar el SP
        actualizar_usuario_sp(
            username,
            data.get('nombre'),
            data.get('apellido'),
            data.get('direccion'),
            data.get('correo'),
            data.get('telefono')
        )

        return Response({
            "status": "success",
            "message": "Usuario actualizado correctamente"
        })

    except Exception as e:
        # Aquí capturamos el RAISE EXCEPTION del SP
        # El mensaje vendrá dentro de str(e)
        error_mensaje = str(e)
        
        # Limpiamos un poco el mensaje si viene con prefijos de Postgres
        if "CONTEXT:" in error_mensaje:
            error_mensaje = error_mensaje.split("CONTEXT:")[0].strip()

        return Response({
            "status": "error",
            "message": error_mensaje
        }, status=404) # 404 porque el recurso (usuario) no fue encontrado
        
#Eliminar Usuario
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def usuario_eliminar(request, username): # Pasamos el username por la URL
    try:
        # Llamamos al SP
        eliminar_usuario_sp(username)

        # Si el SP tuvo éxito, también eliminamos la referencia en Django
        # para mantener la sincronización que hicimos en el login.
        User.objects.filter(username=username).delete()

        return Response({
            "status": "success",
            "message": f"Usuario {username} eliminado correctamente del sistema."
        })

    except Exception as e:
        # Capturamos el RAISE EXCEPTION del SP
        return Response({
            "status": "error",
            "message": str(e).split("CONTEXT:")[0].strip()
        }, status=404)
        
#Gestion de Bloqueo
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_gestionar_bloqueo(request):
    try:
        data = request.data
        username = data.get('username')
        bloquear = data.get('bloquear') # Debe ser un booleano (true/false)

        if username is None or bloquear is None:
            return Response({"status": "error", "message": "Username y estado de bloqueo son requeridos"}, status=400)

        # Llamada al SP
        mensaje_exito = gestionar_bloqueo_sp(username, bloquear)

        return Response({
            "status": "success",
            "message": mensaje_exito
        })

    except Exception as e:
        # Capturamos el RAISE EXCEPTION si el usuario no existe
        return Response({
            "status": "error",
            "message": str(e).split("CONTEXT:")[0].strip()
        }, status=404)
        
#Modificar estado Usuario
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_modificar_estado(request):
    try:
        data = request.data
        username = data.get('username')
        nuevo_estado = data.get('nuevo_estado') # Ej: 'activo' o 'inactivo'

        if not username or not nuevo_estado:
            return Response({
                "status": "error", 
                "message": "Username y nuevo_estado son requeridos"
            }, status=400)

        # Llamada al SP
        mensaje_resultado = modificar_estado_usuario_sp(username, nuevo_estado)
    
        return Response({
            "status": "success",
            "message": mensaje_resultado
        })

    except Exception as e:
        # Captura el RAISE EXCEPTION del SP
        return Response({
            "status": "error",
            "message": str(e).split("CONTEXT:")[0].strip()
        }, status=404)
        
#Cambiar Contraseña Usuario
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def usuario_cambiar_password(request):
    try:
        data = request.data
        # Puedes sacar el username del token para mayor seguridad
        username = request.user.username 
        password_actual = data.get('password_actual')
        nueva_password = data.get('nueva_password')

        if not password_actual or not nueva_password:
            return Response({
                "status": "error", 
                "message": "Ambas contraseñas son requeridas"
            }, status=400)

        # Ejecución del SP
        resultado, mensaje = cambiar_password_sp(username, password_actual, nueva_password)

        return Response({
            "status": "success",
            "message": mensaje
        })

    except Exception as e:
        # Captura los RAISE EXCEPTION del SP
        error_mensaje = str(e).split("CONTEXT:")[0].strip()
        return Response({
            "status": "error",
            "message": error_mensaje
        }, status=400)