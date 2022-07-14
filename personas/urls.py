from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from personas.views import ListarUsuarios,RegistrarUsuario, agregar_producto, eliminar_producto, restar_producto, limpiar_carrito, lista_productos, detalle_producto
from django.contrib.auth.views import LogoutView,LoginView


from . import views

urlpatterns=[  
    path("productos", views.productos_crud, name="productos_crud" ),
    path("productosAdd", views.productosAdd, name="productosAdd" ),
    path('productos_del/<str:pk>', views.productos_del, name='productos_del'),
    path('productos_edit/<str:pk>', views.productos_edit, name='productos_edit'),
    path('productos_list/<str:pk>', views.productos_list, name='productos_list'),
    path('listadoProductos', views.tienda, name="listado"),

    path('indexNormal', views.indexNormal, name='indexNormal'),
    path('indexUsuario', views.indexUsuario, name='indexUsuario'),
    path('indexAdmin', views.indexAdmin, name='indexAdmin'),
    path('carrito/', views.carrito, name="carrito"),

    path('registrarUsuarios', (RegistrarUsuario.as_view()), name='registrarUsuarios'),
    path('usuarios_del/<str:pk>', views.usuarios_del, name='usuarios_del'),
    path('usuarios_edit/<str:pk>', views.usuarios_edit, name="usuarios_edit"),
    path('editarUsuarios', views.editarUsuarios, name="editarUsuarios"),
    path('listarUsuarios/', login_required(ListarUsuarios.as_view()), name='listarUsuarios'),

    path('login', LoginView.as_view(template_name='personas/login.html'),name="login"),
    path('logout/', LogoutView.as_view(template_name='personas/logout.html'), name='logout'),
    path('loginAdministrador', LoginView.as_view(template_name='personas/loginAdministrador.html'), name='loginAdministrador'),

    path('agregar/<int:producto_id>', agregar_producto, name="agregar"),
    path('eliminar/<int:producto_id>', eliminar_producto, name="eliminar"),
    path('restar/<int:producto_id>', restar_producto, name="restar"),
    path('limpiar/', limpiar_carrito, name="limpiar"),

    path('lista_productos', lista_productos, name="lista_productos"),
    path('detalle_producto/<producto_id>', detalle_producto, name="detalle_producto"),

]