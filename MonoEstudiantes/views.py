from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Estudiante, Docente, Monografia, ProfMon
from .forms import EstudianteForm, DocenteForm, MonografiaForm, AsignarRolForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente tras el registro
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:  # Si el usuario ya está autenticado, redirigirlo al home
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido de nuevo, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    monografias = Monografia.objects.all()

    data = []
    for monografia in monografias:
        estudiantes = Estudiante.objects.filter(monografia=monografia)
        docentes = ProfMon.objects.filter(monografia=monografia)

        data.append({
            'monografia': monografia,
            'estudiantes': estudiantes,
            'docentes': docentes
        })

    return render(request, 'home.html', {'data': data})


def obtener_datos_monografia(request, id):
    monografia = get_object_or_404(Monografia, id_monografia=id)
    estudiantes = Estudiante.objects.filter(monografia=monografia)
    docentes = ProfMon.objects.filter(monografia=monografia)

    datos_monografia = {
        'titulo': monografia.titulo,
        'fecha_defensa': monografia.fecha_defensa.strftime('%Y-%m-%d'),
        'nota_defensa': monografia.nota_defensa,
        'tiempo_otorgado': monografia.tiempo_otorgado,
        'tiempo_defensa': monografia.tiempo_defensa,
        'tpr': monografia.tpr,
        'estudiantes': [
            {
                'nombres': estudiante.nombres,
                'apellidos': estudiante.apellidos,
                'carnet': estudiante.carnet,
            } for estudiante in estudiantes
        ],
        'docentes': [
            {
                'nombres': docente.docente.nombres,
                'apellidos': docente.docente.apellidos,
                'rol': docente.rol,
            } for docente in docentes
        ]
    }
    return JsonResponse(datos_monografia)


class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'estudiante/listar.html'
    context_object_name = 'estudiantes'


class EstudianteCreateView(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'estudiante/crear.html'
    success_url = reverse_lazy('listar_estudiantes')

    def form_valid(self, form):
        monografia = form.cleaned_data['monografia']

        # Validar si la monografía ya tiene 3 estudiantes asignados
        if Estudiante.objects.filter(monografia=monografia).count() >= 3:
            form.add_error('monografia', 'Esta monografía ya tiene el número máximo de estudiantes asignados (3).')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        # Mensaje de error en caso de que el formulario sea inválido
        messages.error(self.request, 'Error al asignar estudiante. Por favor, revise los datos ingresados.')
        return super().form_invalid(form)
    
class EstudianteUpdateView(UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'estudiante/modificar.html'
    success_url = reverse_lazy('listar_estudiantes')

    def form_invalid(self, form):
        messages.error(self.request, 'Error al modificar el estudiante. Revise los datos ingresados.')
        return super().form_invalid(form)


class DocenteListView(ListView):
    model = Docente
    template_name = 'docente/listar.html'
    context_object_name = 'docentes'


class DocenteCreateView(CreateView):
    model = Docente
    form_class = DocenteForm
    template_name = 'docente/crear.html'
    success_url = reverse_lazy('listar_docentes')

class DocenteUpdateView(UpdateView):
    model = Docente
    form_class = DocenteForm
    template_name = 'docente/modificar.html'
    success_url = reverse_lazy('listar_docentes')

    def form_invalid(self, form):
        messages.error(self.request, 'Error al modificar el docente. Revise los datos ingresados.')
        return super().form_invalid(form)


class MonografiaCreateView(CreateView):
    model = Monografia
    form_class = MonografiaForm
    template_name = 'monografia/crear.html'
    success_url = reverse_lazy('home')

class MonografiaListView(ListView):
    model = Monografia
    template_name = 'monografia/listar.html'
    context_object_name = 'monografias'

class MonografiaUpdateView(UpdateView):
    model = Monografia
    form_class = MonografiaForm
    template_name = 'monografia/modificar.html'
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Error al modificar la monografía. Revise los datos ingresados.')
        return super().form_invalid(form)

class AsignarRolCreateView(CreateView):
    model = ProfMon
    form_class = AsignarRolForm
    template_name = 'monografia/asignar_roles.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        monografia = form.cleaned_data['monografia']
        docente = form.cleaned_data['docente']
        rol = form.cleaned_data['rol']

        # Validar si ya existe un tutor asignado
        if rol == 'Tutor' and ProfMon.objects.filter(monografia=monografia, rol='Tutor').exists():
            form.add_error('rol', 'Esta monografía ya tiene un tutor asignado.')
            return self.form_invalid(form)

        # Validar si ya hay 3 jurados asignados
        if rol == 'Jurado' and ProfMon.objects.filter(monografia=monografia, rol='Jurado').count() >= 3:
            form.add_error('rol', 'Esta monografía ya tiene el número máximo de jurados asignados (3).')
            return self.form_invalid(form)

        # Validar que el docente no esté asignado a la misma monografía en otro rol
        if ProfMon.objects.filter(monografia=monografia, docente=docente).exists():
            form.add_error('docente', 'Este docente ya está asignado a esta monografía en otro rol.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        # Mensaje de error en caso de que el formulario sea inválido
        messages.error(self.request, 'Error al asignar el rol. Por favor, revise los datos ingresados.')
        return super().form_invalid(form)
    
