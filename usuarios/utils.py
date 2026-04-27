from rest_framework_simplejwt.tokens import RefreshToken

# Creamos una clase simple para que SimpleJWT pueda leer el ID
class UserMock:
    def __init__(self, id):
        self.id = id

def obtener_tokens_para_usuario(resultado_db):
    """
    Crea un Access y Refresh token inyectando el ROL de la base de datos.
    Estructura esperada de resultado_db: [mensaje, id, username, nombre, rol]
    """
    user_id = resultado_db[1]
    user_rol = resultado_db[4]

    # Usamos nuestra clase mock en lugar de type()
    user_mock = UserMock(id=user_id)
    
    # Ahora for_user podrá leer user_mock.id sin errores
    refresh = RefreshToken.for_user(user_mock)

    # Inyectamos el rol en el PAYLOAD del token
    refresh['rol'] = user_rol

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }