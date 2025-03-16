from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Library, Book, Loan, User
from django.db.models import Count

def lista_bibliotecas(request):
    bibliotecas = list(Library.objects.values("id","nombre", "direccion", "telefono"))
    return JsonResponse(bibliotecas, safe=False)

@csrf_exempt
def listar_registrar_biblioteca(request):
    if request.method == 'GET':
        bibliotecas = list(Library.objects.values("id","nombre", "direccion", "telefono"))
        return JsonResponse(bibliotecas, safe=False)
    
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            biblioteca = Library.objects.create(
                nombre=data['nombre'],
                telefono=data['telefono'],
                direccion=data['direccion']
            )
            return JsonResponse({"mensaje": "Biblioteca registrada con éxito", "biblioteca_id": biblioteca.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)




@csrf_exempt
def consultar_biblioteca(request, biblioteca_id):
    
    try:
        biblioteca = Library.objects.values("id","nombre", "direccion", "telefono").get(id=biblioteca_id)
        return JsonResponse(biblioteca)
    except Library.DoesNotExist:
        return JsonResponse({"error": "Biblioteca no registrada en el sistema"}, status=404)
    
@csrf_exempt    
def registrar_libro(request):
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            biblioteca = Library.objects.get(id=data['biblioteca_id'])
            nombreLibro = data['titulo']
            
            
            if data['titulo'] == "" or data['titulo'].strip() == "":
                return JsonResponse({"mensaje": "No puedes añadir un libro con titulo vacio"}, status=400)
            if Book.objects.filter(titulo=nombreLibro).exists():
                return JsonResponse({"mensaje": "El libro con ese titulo ya existe"}, status=400)
            
            
            
            libro = Book.objects.create(
                biblioteca = biblioteca,
                titulo=data['titulo'],
                autor=data['autor'],
                editorial=data['editorial']
            )
            
            return JsonResponse({"mensaje": "Libro registrado con éxito", "libro_id": libro.id})
        
        
            
        
        except Library.DoesNotExist:
            return JsonResponse({"error": "Biblioteca no registrada en el sistema"}, status=404)
        
        
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        
    return JsonResponse({"error": "Método no permitido"}, status=405)
 

@csrf_exempt
def listar_libros_de_biblioteca(request, biblioteca_id):
    try:
        libros = list(Book.objects.filter(biblioteca_id=biblioteca_id).values("id", "titulo", "autor", "editorial"))
        biblioteca = Library.objects.values("id","nombre", "direccion", "telefono").get(id=biblioteca_id)
        return JsonResponse(libros, safe=False)
    except Library.DoesNotExist:
        return JsonResponse({"error": "Biblioteca no existe"}, status=404)
    
@csrf_exempt    
def listar_modificar_borrar_libro(request, libro_id):
    if request.method == 'GET':     
        try:
            libro = Book.objects.values("id","titulo", "autor", "editorial", "biblioteca").get(id=libro_id)
            return JsonResponse(libro)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Libro no registrado en el sistema"}, status=404)
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            
            libro = Book.objects.get(id=libro_id)
            data = json.loads(request.body)
            libro.titulo = data.get('titulo', libro.titulo)  
            libro.autor = data.get('autor', libro.autor)
            libro.editorial = data.get('editorial', libro.editorial)
            biblioteca = Library.objects.values("id","nombre", "direccion", "telefono").get(id=data['biblioteca_id'])
            

            if 'biblioteca_id' in data:
                libro.biblioteca_id = data['biblioteca_id']
            
                libro.save()
            
            return JsonResponse({'Libro modificado con id:': libro.id})
            
            

        except Book.DoesNotExist:
            return JsonResponse({"error": "Libro no registrado en el sistema"}, status=404)

        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        
        except Library.DoesNotExist:
            return JsonResponse({"error": "Biblioteca no existe"}, status=400)
    
    
    if request.method == 'DELETE':     
        try:
            libro = Book.objects.get(id=libro_id)
            libro.delete()
            return JsonResponse({"message": "Libro ha sido borrado"})
        
        except Book.DoesNotExist:
            return JsonResponse({"error": "Libro no registrado en el sistema"}, status=404)
        
    
        
@csrf_exempt        
def listar_registrar_usuario(request):
    if request.method == 'GET':
        ususarios = list(User.objects.values("id","nombre", "email", "telefono"))
        return JsonResponse(ususarios, safe=False)
    
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ususario = User.objects.create(
                nombre=data['nombre'],
                email=data['email'],
                telefono=data['telefono']
            )
            return JsonResponse({"mensaje": "Usuario registrado con éxito", "usuario_id": ususario.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt 
def listar_usuario(request, usuario_id):
    
    if request.method == 'GET':     
        try:
            usuario = User.objects.values("id","nombre", "email", "telefono").get(id=usuario_id)
            return JsonResponse(usuario)
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no registrado en el sistema"}, status=404)
@csrf_exempt         
def listar_registrar_prestamos(request):
    if request.method == 'GET':     
    
        prestamos = list(Loan.objects.filter(devuelto=False)
                         .values("usuario__nombre", "libro__titulo", "fecha", "devuelto"))
        return JsonResponse(prestamos, safe=False)
    
    if request.method == 'POST':     
        try:
            data = json.loads(request.body)
            libro = Book.objects.get(id=data['libro_id'])
            usuario = User.objects.get(id=data['usuario_id'])
            if Loan.objects.filter(libro=libro, devuelto=False).exists():
                return JsonResponse({"error": "El libro ya está prestado y no ha sido devuelto."}, status=400)
            prestamo = Loan.objects.create(
                libro = libro,
                usuario = usuario
            )
            return JsonResponse({"mensaje": "Prestamo registrado con éxito", "prestamo_id": prestamo.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Libro no registrado en el sistema"}, status=404)
        except User.DoesNotExist:
            return JsonResponse({"error": "usuario no registrado en el sistema"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)   

@csrf_exempt
def ver_prestamos_usuario(request, usuario_id):
    if request.method == 'GET':
        try:
            usuario = User.objects.values("id","nombre", "email", "telefono").get(id=usuario_id)
            prestamos = list(Loan.objects.filter(usuario_id=usuario_id).values("id", "usuario", "libro", "fecha", "devuelto"))
            return JsonResponse(prestamos, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)
        
@csrf_exempt
def devolver_libro(request, prestamo_id):
    if request.method == 'PUT':
        try:
            """data = json.loads(request.body)"""
            prestamo = Loan.objects.get(id=prestamo_id)
            if prestamo.devuelto == True:
                return JsonResponse({"error": "El préstamo ya ha sido devuelto."}, status=400)
            prestamo.devuelto = True  
            
            
            prestamo.save()
            
            return JsonResponse({'Prestamo devuelto con id:': prestamo_id})

        except Loan.DoesNotExist:
            return JsonResponse({"error": "Prestamo no registrado en el sistema"}, status=404)

        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)     
        
@csrf_exempt    
def libros_biblioteca_disponible(request, biblioteca_id):
        if request.method == 'GET':
            try:
            # Filtra los libros de la biblioteca
                libros = Book.objects.filter(biblioteca_id=biblioteca_id)
                biblioteca = Library.objects.values("id","nombre", "direccion", "telefono").get(id=biblioteca_id)

                libros_disponibles = libros.exclude(
                id__in=Loan.objects.filter(devuelto=False).values('libro_id')
                )

    
                libros_data = list(libros_disponibles.values("id", "titulo", "autor", "editorial"))
    
                return JsonResponse(libros_data, safe=False)

            except Library.DoesNotExist:
                return JsonResponse({"error": "Biblioteca no encontrada"}, status=404)
    