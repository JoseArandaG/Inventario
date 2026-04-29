from django.db import connection

# Verifica que el nombre sea llamar_sp_login
def login_sp(p_username, p_password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sp_login(%s, %s)", [p_username, p_password])
        row = cursor.fetchone()
    return row


# Listar Usuario
def listar_usuario_sp():
    with connection.cursor() as cursor:
        # Llamamos al nuevo SP que adaptamos para Supabase
        cursor.execute("SELECT * FROM sp_usuario_listar()")
        
        # Obtenemos los nombres de las columnas
        columns = [col[0] for col in cursor.description]
        
        # Convertimos cada fila en un diccionario {'columna': valor}
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

# Crear Usuario
def crear_usuario_sp(nombre, apellido, password, direccion, correo, telefono):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM sp_usuario_crear(%s, %s, %s, %s, %s, %s)",
            [nombre, apellido, password, direccion, correo, telefono]
        )
        row = cursor.fetchone()
        return row[0] if row else None

# Actualizar Usuario
def actualizar_usuario_sp(username, nombre, apellido, direccion, correo, telefono):
    with connection.cursor() as cursor:
        # Al ejecutar esto, si el SP lanza RAISE EXCEPTION, 
        # Python saltará directamente al 'except' de la vista.
        cursor.execute(
            "SELECT sp_usuario_actualizar(%s, %s, %s, %s, %s, %s)",
            [username, nombre, apellido, direccion, correo, telefono]
        )
    return True

#Eliminar Usuario
def eliminar_usuario_sp(username):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT sp_usuario_eliminar(%s)",
            [username]
        )
    return True

#Gestion de Bloqueo
def gestionar_bloqueo_sp(username, bloquear):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT sp_usuario_gestionarbloqueo(%s, %s)",
            [username, bloquear]
        )
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    
#Modificar Estado Usuario
def modificar_estado_usuario_sp(username, nuevo_estado):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT sp_usuario_modificarestado(%s, %s)",
            [username, nuevo_estado]
        )
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    
    
#Cambiar Contraseña Usuario
def cambiar_password_sp(username, password_actual, nueva_password):
    with connection.cursor() as cursor:
        # Llamamos a la función que retorna una fila con dos columnas
        cursor.execute(
            "SELECT * FROM sp_usuario_cambiarpassword(%s, %s, %s)",
            [username, password_actual, nueva_password]
        )
        row = cursor.fetchone()
        # Retorna una tupla: ('Éxito', 'Contraseña actualizada correctamente.')
        return row