from django.contrib import admin
from django.contrib.auth.models import User

# Caso queira personalizar o comportamento do admin para o User, você pode fazer isso aqui.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Não é necessário registrar o User novamente, porque ele já está registrado por padrão.
# Apenas personalizamos o admin do User
admin.site.unregister(User)  # Primeiro, desregistramos o modelo User
admin.site.register(User, UserAdmin)  # Agora, registramos com a personalização
