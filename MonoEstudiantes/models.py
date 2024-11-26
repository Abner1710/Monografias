from django.db import models

class Monografia(models.Model):
    id_monografia = models.AutoField(primary_key=True)  # Clave primaria
    titulo = models.CharField(max_length=255) 
    fecha_defensa = models.DateField()  
    nota_defensa = models.FloatField()  
    tiempo_otorgado = models.IntegerField()  
    tiempo_defensa = models.IntegerField()
    tpr = models.IntegerField()  

    def __str__(self):
        return self.titulo


class Docente(models.Model):
    id_docente = models.AutoField(primary_key=True)  # Clave primaria
    nombres = models.CharField(max_length=100)  
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, null=True, blank=True)  
    telefono = models.BigIntegerField(null=True, blank=True)  
    anio_nacimiento = models.DateField()  

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Estudiante(models.Model):
    carnet = models.CharField(primary_key=True, max_length=20)  # Clave primaria
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.BigIntegerField(null=True, blank=True)
    anio_nacimiento = models.DateField()
    monografia = models.ForeignKey(Monografia, on_delete=models.CASCADE)  # Relación con Monografía

    def __str__(self):
        return f"{self.carnet} - {self.nombres} {self.apellidos}"


class ProfMon(models.Model):
    monografia = models.ForeignKey(Monografia, on_delete=models.CASCADE)  # Relación con Monografía
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)  # Relación con Docente
    rol = models.CharField(max_length=50)  # Rol del profesor en la monografía

    class Meta:
        unique_together = ('monografia', 'docente')  # Garantiza que no se repitan combinaciones
