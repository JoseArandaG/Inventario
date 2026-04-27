from django.db import connection

# Verifica que el nombre sea llamar_sp_login
def llamar_sp_login(p_username, p_password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sp_login(%s, %s)", [p_username, p_password])
        row = cursor.fetchone()
    return row