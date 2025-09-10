from flask import Flask , render_template, request, redirect, url_for, flash
import pyodbc
import re
import urllib.parse

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
    cursor = connection.cursor()
    try:
        cursor.execute("EXEC InsertEmpleado1 @Nombre=?, @Salario=?", (nombre, salario))
        connection.commit()
        return f"Empleado '{nombre}' insertado con éxito."
    except pyodbc.ProgrammingError as pe:
        if "Nombre de empleado ya existe" in str(pe):
            return f"Error: El nombre '{nombre}' ya existe."
        else:
            return f"Error de programación: {str(pe)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"
    finally:
        cursor.close()

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


@app.route("/insertar", methods=["GET", "POST"])
def procesar_insertar():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        salario = request.form["salario"].strip()
        try:
            salario = float(salario)
        except ValueError:
            mensaje = "El salario debe ser un número válido."
            return render_template("insertar.html", mensaje=mensaje)
        
        mensaje = insertar_empleado(nombre, salario)
        # Redirigir a la página principal con el mensaje como parámetro
        return render_template("insertar.html", mensaje=mensaje)

    
    return render_template("insertar.html")



if __name__ == "__main__":
    app.run(debug=True)

