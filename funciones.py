import pyodbc


connection = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=tcp:servidorbdcmb19.database.windows.net,1433;"
    "DATABASE=Tarea1 BD;"
    "UID=AdminCMB19;"
    "PWD=adminbdCMB05;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

print(" Conexión exitosa")
def obtener_empleados():
    cursor = connection.cursor()            # Abrir cursor para ejecutar SQL
    cursor.execute("EXEC ObtenerEmpleados") # ejecuta el SP 
    resultados = cursor.fetchall()          #  Trae todos los resultados
    empleados = []                          # Crea lista vacía para guardar empleados
    for fila in resultados:                 #  Recorre cada fila del resultado
        empleados.append({ "id": fila.id,"nombre": fila.Nombre,"salario": fila.Salario   })
    return empleados    



def insertar_empleado(nombre, salario):
    cursor = connection.cursor()                                #  Abre cursor
    cursor.execute(
        "EXEC InsertEmpleado @Nombre=?, @Salario=?",            #  ejecuta  el SP con  los parámetros
        (nombre, salario)                                       
    )
    connection.commit()                                         # Confirmar los cambios en la BD
    return "Empleado insertado"                                 
