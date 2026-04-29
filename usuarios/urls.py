# usuarios/urls.py
from django.urls import path
from .views import api_login, usuario_cambiar_password, usuario_crear, usuario_eliminar, usuario_gestionar_bloqueo, usuario_listar, usuario_actualizar, usuario_modificar_estado

urlpatterns = [
    path('login/', api_login, name='api_login'),
    path('usuario/listar/', usuario_listar, name='usuario_listar'), # Cambiamos 'usuarios/' por 'listar/'
    path('usuario/crear/', usuario_crear, name='usuario_crear'), # Agregamos la ruta para crear usuario
    path('usuario/actualizar/', usuario_actualizar, name='usuario_actualizar'), # Agregamos la ruta para actualizar usuario
    path('usuario/eliminar/<str:username>/', usuario_eliminar, name='usuario_eliminar'), # Agregamos la ruta para eliminar usuario
    path('usuario/gestionar-bloqueo/', usuario_gestionar_bloqueo, name='usuario_gestionar_bloqueo'), # Agregamos la ruta para gestionar bloqueo
    path('usuario/modificar-estado/', usuario_modificar_estado, name='usuario_modificar_estado'), # Agregamos la ruta para modificar estado
    path('usuario/actualizar-password/', usuario_cambiar_password, name='usuario_cambiar_password'), # Agregamos la ruta para actualizar contraseña   
]