# dashboard/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user             = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    foto             = models.ImageField(upload_to='profiles/', blank=True, null=True)
    telefono         = models.CharField(max_length=20, blank=True, null=True)
    bio              = models.TextField(blank=True, null=True)
    cargo            = models.CharField(max_length=100, blank=True, null=True)
    departamento     = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'


# Crear el perfil automáticamente cuando se crea un usuario
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Crear perfil de calendario
class Profile(models.Model):
    user             = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    foto             = models.ImageField(upload_to='profiles/', blank=True, null=True)
    telefono         = models.CharField(max_length=20, blank=True, null=True)
    bio              = models.TextField(blank=True, null=True)
    cargo            = models.CharField(max_length=100, blank=True, null=True)
    departamento     = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'


class Evento(models.Model):
    TIPOS = [
        ('vacuna',       '💉 Vacuna'),
        ('veterinario',  '🩺 Veterinario'),
        ('entrada',      '📦 Entrada de alimentos'),
        ('salida',       '🚚 Salida de alimentos'),
        ('observacion',  '📝 Observación'),
        ('otro',         '📌 Otro'),
    ]

    titulo      = models.CharField(max_length=200)
    tipo        = models.CharField(max_length=20, choices=TIPOS, default='otro')
    descripcion = models.TextField(blank=True, null=True)
    fecha       = models.DateField()
    hora        = models.TimeField(blank=True, null=True)
    cantidad    = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unidad      = models.CharField(max_length=50, blank=True, null=True)
    creado_por  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='eventos')
    creado_en   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha', '-creado_en']

    def __str__(self):
        return f'{self.titulo} — {self.fecha}'