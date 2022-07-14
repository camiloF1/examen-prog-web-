from django.shortcuts import render, redirect

from .models import Producto, UsuarioManager, Usuario
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from personas.models import Usuario, Producto
from .forms import FormularioLogin, FormularioUsuario
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from personas.Carrito import Carrito
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .serializers import ProductoSerializer

# Create your views here.

def productos_crud(request):
    print("estoy en Productos Crud...")
    context={} 
    return render(request,"personas/productos_add.html",context)

def productosAdd(request):
    print("estoy en controlador ProductosAdd...")
    context={}
    if request.method == "POST":
        print("contralador productos es un post...") 
        opcion=request.POST.get("opcion","")
        print("opcion="+opcion)
        #Listar
        if opcion=="Editar" or opcion == "Volver":
            productos = Producto.objects.all()
            context ={'productos':productos}
            print("enviando datos a productos_list")
            return render(request,"personas/productos_list.html",context) 
        #Agregar
        if opcion=="Agregar":
            idProducto=request.POST["idProducto"]
            nombreProducto=request.POST["nombreProducto"]
            stock=int(request.POST["stock"])
            precio=int(request.POST["precio"])
            fotoProducto=request.FILES["fotoProducto"]

       
            if idProducto != "" and nombreProducto != "" and stock >=0 and precio >=0:

                producto = Producto(idProducto, nombreProducto, stock, precio,
                                    fotoProducto) 
                producto.save()
                context={'mensaje':"Ok, datos grabados..."}
            else:
                context={'mensaje':"Error, los campos no deben estar vacios"}

           #Agregar
        if opcion=="Actualizar":
            idProducto=request.POST["idProducto"]
            nombreProducto=request.POST["nombreProducto"]
            stock=int(request.POST["stock"])
            precio=int(request.POST["precio"])
            try:
                fotoProducto=request.FILES["fotoProducto"]
            except:
                fotoProducto=""
       
            if idProducto != "" and nombreProducto != "" and stock >=0 \
                and precio >=0:

                producto = Producto(idProducto, nombreProducto, stock, precio,
                                    fotoProducto) 
                producto.save()
                context={'mensaje':"Ok, datos grabados..."}
            else:
                context={'mensaje':"Error, los campos no deben estar vacios"}
            return render(request,"personas/productos_edit.html",context) 


    return render(request,"personas/productos_add.html",context)   

def productos_del(request, pk):
    mensajes=[]
    errores=[]
    productos = Producto.objects.all()
    try:
        producto=Producto.objects.get(idProducto=pk)
        context={}
        if producto:
           producto.delete()
           mensajes.append("Bien, datos eliminados...")

           context = {'productos': productos,  'mensajes': mensajes, 'errores':errores}

           return render(request, 'personas/productos_list.html', context)

    except:
        print("Error, rut no existe")
        errores.append("Error rut no encontrado.")
        context = {'productos': productos,  'mensajes': mensajes, 'errores':errores}
        return render(request, 'personal/productos_list.html', context)

def productos_edit(request, pk):
    mensajes=[]
    errores=[]   
    
    context={}
    #productos = Producto.objects.all()
    #try:
    producto=Producto.objects.get(idProducto=pk)

    context={}
    if producto:
        print("Edit encontró a producto...")
        mensajes.append("Bien, datos eliminados...")

        context = {'producto': producto,  'mensajes': mensajes, 'errores':errores}

        return render(request, 'personas/productos_edit.html', context)
    
    return render(request, 'personas/productos_list.html', context)



def productos_list(request, pk):
    mensajes=[]
    errores=[]

    context={}
    producto=Producto.objects.gets(idProducto=pk)
    context={}
    if producto:
        print("list encontro a producto")
        mensajes.append("bien, productos listados")
        context = {'producto': producto, 'mensajes':mensajes, 'errores':errores}
        return render(request, 'personas/productos_list.html', context)
    return render(request,"personas/productos_list.html", context)


def indexNormal(request):
    print("estoy en index...")
    context={}
    return render(request,"personas/indexNormal.html",context)

def indexUsuario(request):
    print("estoy en index de usuario...")
    context={}
    return render(request,"personas/indexUsuario.html", context)

def indexAdmin(request):
    print("estoy en index admin")
    context={}
    return render(request,"personas/indexAdmin.html", context)


def carrito(request):
    print("estoy en carrito")
    context={}
    return render(request, 'personas/carrito.html', context)


def tienda(request):
    productos = Producto.objects.all()
    return render(request, "personas/listado.html", {'productos':productos})


class ListarUsuarios(ListView):
    model = Usuario
    template_name= 'personas/listarUsuarios.html'
    
    def get_queryset(self):
        return self.model.objects.filter(usuario_activo=True)



class RegistrarUsuario(CreateView):
    model = Usuario 
    form_class = FormularioUsuario
    template_name = 'personas/registrarUsuarios.html'
    success_url = reverse_lazy('indexUsuario')


class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('indexUsuario')

class LoginAdministrador(FormView):
    template_name = 'loginAdmistrador.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('indexAdmin')


def usuarios_del(request,pk):
    mensajes=[]
    errores=[]
    usuarios = Usuario.objects.all()
    try:
        usuario=Usuario.objects.get(username=pk)
        context={}
        if usuario:
           usuario.delete()
           mensajes.append("usuario eliminado")

           context = {'usuarios':usuarios, 'mensajes':mensajes,'errores':errores}

           return render(request, 'personas/listarUsuarios.html', context)
    
    except:
        print("error, usuario no existe")
        errores.append("error, username no encontrado")
        context={'personas':usuarios,'mensajes':mensajes,'errores':errores}
        return render(request, 'personal/listarUsuarios.html', context)


def usuarios_edit(request,pk):
    mensajes=[]
    errores=[]

    context={}

    usuario = Usuario.objects.get(username=pk)

    context={}
    if usuario:
        print("se encontró a usuario")
        mensajes.append("bien, datos eliminados")

        context = {'usuario':usuario,'mensajes':mensajes,'errores':errores}

        return render(request,'personas/editarUsuarios.html', context)


def editarUsuarios(request):
    print("estoy en controlador editusuarios")
    context={}
    if request.method == "POST":
        print("controlador es un post")
        opcion=request.POST.get("opcion","")
        print("opcion="+opcion)
        if opcion=="Editar" or opcion =="Volver":
            usuario = Usuario.objects.all()
            context ={'personas':usuario}
            print("enviando datos usuarios_edit")
            return render(request,"personas/listarUsuarios.html", context)

        if opcion=="Agregar":
            username=request.POST["username"]
            email=request.POST["email"]
            nombre=request.POST["nombre"]
            apellido=request.POST["apellido"]

            if username !="" and email !="" and nombre !="" and apellido !="":
                usuario = Usuario(username, email, nombre, apellido)
                usuario.save()
                context={'mensaje': 'ok datos grabados'}
            else:
                context={'mensaje':'error, los cambos no pueden estar vacios'}

        if opcion=="Actualizar":
            username=request.POST["username"]
            email=request.POST["email"]
            nombre=request.POST["nombre"]
            apellido=request.POST["apellido"]

            if username !="" and email !="" and nombre !="" and apellido !="":
                usuario = Usuario(username, email, nombre, apellido)
                usuario.save()
                context={'mensaje':'ok datos actualizados'}

            else:
                context={'mensaje':'error los cambos no deben estar vacios'}
            return render(request,"personas/editarUsuarios.html", context)


#views carrito

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.agregar(producto)
    return redirect("/personas/carrito/")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.eliminar(producto)
    return redirect("personas/carrito/")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.restar(producto)
    return redirect("/personas/carrito/")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("/personas/carrito/")


#api rest
@csrf_exempt
@api_view(['GET','POST'])
def lista_productos(request):
    if request.method == 'GET':
        producto = Producto.objects.all()
        serializer = ProductoSerializer(producto, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def detalle_producto(request, producto_id):
    try:
        producto = Producto.objects.get(idProducto=producto_id)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProductoSerializer(producto, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

