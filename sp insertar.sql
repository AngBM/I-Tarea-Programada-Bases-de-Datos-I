CREATE PROCEDURE insertar_empleado (@Nombre VARCHAR(128),@Salario Money )

AS
BEGIN 

INSERT INTO dbo.Empleado (Nombre,Salario)
VALUES (@Nombre, @Salario);
END;
GO