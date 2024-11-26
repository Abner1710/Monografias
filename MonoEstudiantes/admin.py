from django.contrib import admin
from .models import Monografia, Docente, Estudiante, ProfMon
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Registra tus modelos personalizados
admin.site.register(Monografia)
admin.site.register(Docente)
admin.site.register(Estudiante)
admin.site.register(ProfMon)

# Opcional: Extender la administración del usuario si necesitas personalizarla
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
