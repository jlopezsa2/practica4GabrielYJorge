from django.urls import path
from .views import(
    listar_registrar_biblioteca, consultar_biblioteca, 
    registrar_libro, listar_libros_de_biblioteca, listar_modificar_borrar_libro, listar_registrar_usuario,listar_registrar_prestamos,
    listar_usuario, ver_prestamos_usuario, devolver_libro, libros_biblioteca_disponible
    
)

urlpatterns = [
    
    path('libraries/', listar_registrar_biblioteca, name='listar_registrar_biblioteca'),
    path('libraries/<int:biblioteca_id>/', consultar_biblioteca, name='consultar_biblioteca'),
    path('books/', registrar_libro, name='registrar_libro'),
    path('libraries/<int:biblioteca_id>/books/', listar_libros_de_biblioteca, name='listar_libros_de_biblioteca'),
    path('books/<int:libro_id>', listar_modificar_borrar_libro, name='listar_modificar_borrar_libro'),
    path('users/', listar_registrar_usuario, name='listar_registrar_usuario'),
    path('users/<int:usuario_id>', listar_usuario, name='listar_libro'),
    path('loans/', listar_registrar_prestamos, name='listar_registrar_prestamos'),
    path('users/<int:usuario_id>/loans/', ver_prestamos_usuario, name='ver_prestamos_usuario'),
    path('loans/<int:prestamo_id>/', devolver_libro, name='devolver_libro'),
    path('books/<int:biblioteca_id>/avaliable/', libros_biblioteca_disponible, name='libros_biblioteca_disponible'),
     
]




