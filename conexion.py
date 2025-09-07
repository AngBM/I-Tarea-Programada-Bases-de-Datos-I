from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Conexión
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=tcp:servidorbdcmb19.database.windows.net,1433;"
    "DATABASE=Tarea1 BD;"     
    "UID=AdminCMB19;"
    "PWD=adminbdCMB05;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def get_connection():
    return pyodbc.connect(conn_str)

@app.route("/", methods=["GET", "POST"])
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
