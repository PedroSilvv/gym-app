from django.contrib import admin
from .models import Esporte, CustomUser, Aluno

class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "username",
        "id"
    )


admin.site.register(Esporte)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Aluno)