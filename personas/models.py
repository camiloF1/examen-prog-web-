from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class UsuarioManager(BaseUserManager):   #aca definimos 2 metodos, uno para crear usuario normal y usuario administrador
    def create_user(self,email,username,nombre,apellido,password = None):
        if not email:
            raise ValueError('EL usuario debe contener email')

        user = self.model(username = username, email = email, nombre = nombre, apellido = apellido)

        user.set_password(password) #esto encripta la contraseña
        user.save()
        return user

    def create_superuser(self,username,email,nombre,apellido,password):
        user = self.create_user(email, username = username, nombre = nombre, apellido = apellido, password=password)
        user.usuario_administrador = True
        user.save()
        return user




class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de Usuario' ,unique = True, max_length=100, primary_key = True)
    email = models.CharField('Correo', max_length=100, blank = True, null = True)
    nombre = models.CharField('Nombre', max_length=50, blank = True, null = True)
    apellido = models.CharField('Apellido', max_length=50, blank = True, null = True)
    usuario_activo = models.BooleanField(default = True)
    usuario_administrador = models.BooleanField(default = False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido']

    def __str__(self):
        return f'{self.username},{self.apellido}'
    
    def has_perm(self,perm,obj = None):  #este metodo nos permite usar el usuario como adm
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador




def cargarFotoProducto(instance, filename):
    return "fotosProductos/foto_{0}_{1}".format(instance.idProducto,filename)


class Producto(models.Model):
    idProducto = models.CharField(max_length=5, primary_key=True)
    nombreProducto = models.CharField(max_length=30, blank=True, null=True)
    stock   = models.IntegerField(blank=True, null=True)
    precio   = models.IntegerField(blank=True, null=True)
    foto = models.ImageField(upload_to=cargarFotoProducto, null=True)

    def __str__(self):
        return self.idProducto+", "+self.nombreProducto+", "+str(self.stock)\
               +", "+str(self.precio)+", "+self.foto.__str__()


