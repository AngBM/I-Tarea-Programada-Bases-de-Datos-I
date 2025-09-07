CREATE PROCEDURE InsertEmpleado1 @Nombre VARCHAR(128),@Salario MONEY
AS
BEGIN
    -- Si ya existe un empleado con el mismo nombre
    IF EXISTS (SELECT 1 FROM dbo.Empleado WHERE Nombre = @Nombre)
    BEGIN
        -- Devuelve un error controlado
        RAISERROR('Nombre de empleado ya existe.', 16, 1)
        RETURN
    END

    -- Si no existe, inserta
    INSERT INTO dbo.Empleado (Nombre, Salario)
    VALUES (@Nombre, @Salario)
END
