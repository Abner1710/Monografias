from django import forms
from .models import Estudiante, Docente, Monografia, ProfMon


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['carnet', 'nombres', 'apellidos', 'direccion', 'telefono', 'anio_nacimiento', 'monografia']
        widgets = {
            'anio_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ['nombres', 'apellidos', 'direccion', 'telefono', 'anio_nacimiento']
        widgets = {
            'anio_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class MonografiaForm(forms.ModelForm):
    class Meta:
        model = Monografia
        fields = ['titulo', 'fecha_defensa', 'nota_defensa', 'tiempo_otorgado', 'tiempo_defensa', 'tpr']
        widgets = {
            'fecha_defensa': forms.DateInput(attrs={'type': 'date'}),
        }


class AsignarRolForm(forms.ModelForm):
    class Meta:
        model = ProfMon
        fields = ['monografia', 'docente', 'rol']
        widgets = {
            'rol': forms.Select(choices=[('Tutor', 'Tutor'), ('Jurado', 'Jurado')]),
        }
