from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from . import views 

urlpatterns = [
    path('', login_required(views.home), name='home'),  # Requiere autenticación para la página de inicio
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('estudiante/', login_required(views.EstudianteListView.as_view()), name='listar_estudiantes'),
    path('estudiante/crear/', login_required(views.EstudianteCreateView.as_view()), name='crear_estudiante'),
    path('docente/', login_required(views.DocenteListView.as_view()), name='listar_docentes'),
    path('docente/crear/', login_required(views.DocenteCreateView.as_view()), name='crear_docente'),
    path('monografia/crear/', login_required(views.MonografiaCreateView.as_view()), name='crear_monografia'),
    path('monografia/asignar_roles/', login_required(views.AsignarRolCreateView.as_view()), name='asignar_roles'),
    path('obtener-datos-monografia/<int:id>/', login_required(views.obtener_datos_monografia), name='obtener_datos_monografia'),
    path('estudiante/modificar/<str:pk>/', login_required(views.EstudianteUpdateView.as_view()), name='modificar_estudiante'),
    path('docente/modificar/<int:pk>/', login_required(views.DocenteUpdateView.as_view()), name='modificar_docente'),
    path('monografia/modificar/<int:pk>/', login_required(views.MonografiaUpdateView.as_view()), name='modificar_monografia'),
    path('monografia/', login_required(views.MonografiaListView.as_view()), name='listar_monografias'),
]

urlpatterns += [
    path('logout/', LogoutView.as_view(), name='logout'),
]
