from flask import Flask , render_template, request, redirect, url_for, flash
import pyodbc
import re

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=tcp:servidorbdcmb19.database.windows.net,1433;"
    "DATABASE=Tarea1 BD;"
    "UID=AdminCMB19;"
    "PWD=adminbdCMB05;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=60;"
)

print(" Conexión exitosa")
def obtener_empleados():
    
    cursor = connection.cursor()            # Abrir cursor para ejecutar SQL
    cursor.execute("EXEC ObtenerEmpleados1") # ejecuta el SP 
    resultados = cursor.fetchall()          #  Trae todos los resultados
    empleados = []                          # Crea lista vacía para guardar empleados
    for fila in resultados:                 #  Recorre cada fila del resultado
        empleados.append({
            "id": fila[0],
            "nombre": fila[1],
            "salario": fila[2]
        })
    return empleados    



def insertar_empleado(nombre, salario):
    try:
        cursor = connection.cursor()                                #  Abre cursor
        cursor.execute(
            "EXEC InsertEmpleado1 @Nombre=?, @Salario=?",            #  ejecuta  el SP con  los parámetros
            (nombre, salario)                                       
        )
        connection.commit()                                         # Confirmar los cambios en la BD
        return "Empleado insertado"  
    except pyodbc.Error as e:
         raise Exception(e.args[1])                               


#-------------------------------------------------------------------------------------
#para ver todos los empleados
app = Flask(__name__)

@app.route("/")  # ruta principal
def pantalla_principal():
    empleados=obtener_empleados()
    return render_template ("index.html",empleados=empleados)

@app.route("/insertar", methods=["GET"])
def mostrar_insertar():
    return render_template("insertar.html")

@app.route("/insertar", methods=["POST"])
def procesar_insertar():
    nombre = request.form["nombre"]
    salario = request.form["salario"]

    try:
        salario = float(salario)
        mensaje = insertar_empleado(nombre, salario)
    except Exception as e:
        mensaje = f"Error al insertar: {str(e)}"

    empleados = obtener_empleados()
    return render_template("index.html", empleados=empleados, mensaje=mensaje)





























#@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        salario = request.form["salario"]

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DECLARE @ResultCode INT, @ResultMessage NVARCHAR(200);
                EXEC dbo.InsertEmpleado1 @Nombre=?, @Salario=?, 
                     @ResultCode=@ResultCode OUTPUT, @ResultMessage=@ResultMessage OUTPUT;
                SELECT @ResultCode AS Code, @ResultMessage AS Message;
            """, (nombre, salario))
            row = cursor.fetchone()
            conn.commit()
            mensaje = row.Message
        except Exception as e:
            mensaje = f"Error: {e}"

    # cargar lista de empleados
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC dbo.ObtenerEmpleados1")
    empleados = cursor.fetchall()

    return render_template("index.html", empleados=empleados, mensaje=mensaje) 

if __name__ == "__main__":
    app.run(debug=True)
