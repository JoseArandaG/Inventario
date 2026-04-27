from rest_framework import permissions

class TieneRol(permissions.BasePermission):
    """
    Permiso personalizado que permite el acceso basado en una lista de roles.
    """
    def __init__(self, roles_permitidos):
        # Guardamos la lista de roles que pueden pasar (ej: ['Administrador'])
        self.roles_permitidos = roles_permitidos

    def has_permission(self, request, view):
        # 1. Verificamos que el usuario esté autenticado con un token válido
        if not request.user or not request.auth:
            return False
        
        # 2. Extraemos el rol que inyectamos en el token (Payload)
        # request.auth funciona como un diccionario con los datos del JWT
        rol_usuario = request.auth.get('rol')

        # 3. Comparamos: ¿El rol del usuario está en la lista permitida?
        return rol_usuario in self.roles_permitidos