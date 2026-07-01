from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ══════════════════════════════════════════════════════════════
# NIVEL 0 — Extiende el User de Django
# ══════════════════════════════════════════════════════════════
class Profile(models.Model):
    ROL_CHOICES = [
        ('admin',    'Administrador'),
        ('operador', 'Operador'),
        ('vendedor', 'Vendedor'),
        ('viewer',   'Solo lectura'),
    ]
    user             = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    foto             = models.ImageField(upload_to='profiles/', blank=True, null=True)
    cedula           = models.CharField(max_length=10, blank=True, null=True)
    telefono         = models.CharField(max_length=15, blank=True, null=True)
    rol              = models.CharField(max_length=20, choices=ROL_CHOICES, default='operador')
    estado           = models.BooleanField(default=True)
    bio              = models.TextField(blank=True, null=True)
    cargo            = models.CharField(max_length=100, blank=True, null=True)
    departamento     = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.get_full_name() or self.user.username}'


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


# ══════════════════════════════════════════════════════════════
# NIVEL 1 — Tablas base sin dependencias
# ══════════════════════════════════════════════════════════════
class Galpon(models.Model):
    nombre     = models.CharField(max_length=50)
    capacidad  = models.IntegerField(default=0)
    ubicacion  = models.CharField(max_length=100, blank=True, null=True)
    descripcion= models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name        = 'Galpón'
        verbose_name_plural = 'Galpones'
        ordering            = ['nombre']


class Alimento(models.Model):
    TIPO_CHOICES = [
        ('concentrado', 'Concentrado'),
        ('maiz',        'Maíz'),
        ('soya',        'Soya'),
        ('vitaminas',   'Vitaminas'),
        ('mineral',     'Mineral'),
        ('otro',        'Otro'),
    ]
    nombre         = models.CharField(max_length=100)
    tipo           = models.CharField(max_length=50, choices=TIPO_CHOICES, default='otro')
    unidad_medida  = models.CharField(max_length=20, default='kg')
    stock          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descripcion    = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} ({self.stock} {self.unidad_medida})'

    class Meta:
        ordering = ['nombre']


class Cliente(models.Model):
    nombres   = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    telefono  = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    correo    = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.nombres} {self.apellidos or ""}'.strip()

    def get_full_name(self):
        return f'{self.nombres} {self.apellidos or ""}'.strip()

    class Meta:
        ordering = ['nombres']


# ══════════════════════════════════════════════════════════════
# NIVEL 2 — Dependen del nivel 1
# ══════════════════════════════════════════════════════════════
class Ave(models.Model):
    ESTADO_CHOICES = [
        ('activo',    'Activo'),
        ('baja',      'Baja'),
        ('vendido',   'Vendido'),
        ('muerto',    'Muerto'),
    ]
    raza         = models.CharField(max_length=80)
    cantidad     = models.IntegerField(default=0)
    fecha_ingreso= models.DateField()
    estado       = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    galpon       = models.ForeignKey(Galpon, on_delete=models.SET_NULL, null=True, related_name='aves')

    def __str__(self):
        return f'{self.raza} — {self.cantidad} aves ({self.galpon})'

    class Meta:
        ordering = ['-fecha_ingreso']


class Alimentacion(models.Model):
    fecha      = models.DateField()
    porcion    = models.DecimalField(max_digits=8, decimal_places=2)
    observacion= models.TextField(blank=True, null=True)
    alimento   = models.ForeignKey(Alimento, on_delete=models.SET_NULL, null=True, related_name='alimentaciones')
    galpon     = models.ForeignKey(Galpon, on_delete=models.SET_NULL, null=True, related_name='alimentaciones')
    usuario    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='alimentaciones')

    def __str__(self):
        return f'Alimentación {self.fecha} — {self.galpon}'

    class Meta:
        ordering            = ['-fecha']
        verbose_name        = 'Alimentación'
        verbose_name_plural = 'Alimentaciones'


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente',  'Pendiente'),
        ('proceso',    'En proceso'),
        ('completado', 'Completado'),
        ('cancelado',  'Cancelado'),
    ]
    fecha     = models.DateField()
    estado    = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente   = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, related_name='pedidos')
    usuario   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pedidos')

    def __str__(self):
        return f'Pedido #{self.pk} — {self.cliente}'

    class Meta:
        ordering = ['-fecha']


class Produccion(models.Model):
    fecha          = models.DateField()
    cantidad_huevos= models.IntegerField(default=0)
    huevos_rotos   = models.IntegerField(default=0)
    observaciones  = models.TextField(blank=True, null=True)
    usuario        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='producciones')

    def __str__(self):
        return f'Producción {self.fecha} — {self.cantidad_huevos} huevos'

    class Meta:
        ordering            = ['-fecha']
        verbose_name        = 'Producción'
        verbose_name_plural = 'Producciones'


class Alerta(models.Model):
    ESTADO_CHOICES = [
        ('activa',   'Activa'),
        ('resuelta', 'Resuelta'),
        ('ignorada', 'Ignorada'),
    ]
    descripcion = models.CharField(max_length=250)
    fecha       = models.DateField()
    estado      = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    alimento    = models.ForeignKey(Alimento, on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name='alertas')

    def __str__(self):
        return f'Alerta {self.fecha} — {self.descripcion[:40]}'

    class Meta:
        ordering = ['-fecha']


# ══════════════════════════════════════════════════════════════
# NIVEL 3 — Dependen del nivel 2
# ══════════════════════════════════════════════════════════════
class DetallePedido(models.Model):
    pedido          = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    cantidad_huevos = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal        = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad_huevos * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Detalle #{self.pk} — Pedido #{self.pedido_id}'

    class Meta:
        verbose_name        = 'Detalle de pedido'
        verbose_name_plural = 'Detalles de pedido'


class Distribucion(models.Model):
    fecha        = models.DateField()
    destino      = models.CharField(max_length=100)
    observaciones= models.TextField(blank=True, null=True)
    pedido       = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True,
                                     blank=True, related_name='distribuciones')

    def __str__(self):
        return f'Distribución {self.fecha} → {self.destino}'

    class Meta:
        ordering            = ['-fecha']
        verbose_name        = 'Distribución'
        verbose_name_plural = 'Distribuciones'


# ══════════════════════════════════════════════════════════════
# NIVEL 4 — Ventas y Facturas
# ══════════════════════════════════════════════════════════════
class Venta(models.Model):
    METODO_CHOICES = [
        ('efectivo',     'Efectivo'),
        ('transferencia','Transferencia'),
        ('tarjeta',      'Tarjeta'),
        ('cheque',       'Cheque'),
    ]
    fecha       = models.DateField()
    total       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=20, choices=METODO_CHOICES, default='efectivo')
    factura     = models.ForeignKey('Factura', on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name='ventas')

    def __str__(self):
        return f'Venta #{self.pk} — ${self.total}'

    class Meta:
        ordering = ['-fecha']


class Factura(models.Model):
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha          = models.DateField()
    subtotal       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva            = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pedido         = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True,
                                       blank=True, related_name='facturas')

    def __str__(self):
        return f'Factura {self.numero_factura} — ${self.total}'

    class Meta:
        ordering = ['-fecha']


# ══════════════════════════════════════════════════════════════
# CALENDARIO (ya existía)
# ══════════════════════════════════════════════════════════════
class Evento(models.Model):
    TIPOS = [
        ('vacuna',      '💉 Vacuna'),
        ('veterinario', '🩺 Veterinario'),
        ('entrada',     '📦 Entrada de alimentos'),
        ('salida',      '🚚 Salida de alimentos'),
        ('observacion', '📝 Observación'),
        ('otro',        '📌 Otro'),
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