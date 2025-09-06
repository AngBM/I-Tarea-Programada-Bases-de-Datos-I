USE BD1_PrimeraTarea;
GO
CREATE OR ALTER PROCEDURE dbo.sp_Empleado_Listar
AS
BEGIN
  SET NOCOUNT ON;
  SELECT id, Nombre, Salario
  FROM dbo.Empleado
  ORDER BY Nombre ASC;
END;
GO
