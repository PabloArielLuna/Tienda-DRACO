from django.shortcuts import render, redirect
from App1.models import *
from .forms import crear_Usuarios_forms, crear_Productos_forms, crear_Ventas_detalles_forms, UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import admin
from django.core.paginator import Paginator

# Create your views here.

def mostrar_index(request):
    return render(request, 'App1/index.html')

def mostrar_productos(request):
    producto = Productos.objects.all()
    
    context = {'producto': producto}
    
    return render(request, 'App1/productos.html', context=context)

def mostrar_usuarios(request):
    usuario = Usuarios.objects.all()
    
    context = {'usuario': usuario}
    
    return render(request, 'App1/usuarios.html', context=context)

def mostrar_ventas_detalles(request):
    venta_detalle = Ventas_detalles.objects.all()
    
    context = {'venta_detalle': venta_detalle}
    
    return render(request, 'App1/ventas_detalles.html', context=context)

def crear_Usuarios(request):
    if request.method == 'POST':
        form = crear_Usuarios_forms(request.POST)
        
        if form.is_valid():
            
            formulario_limpio  = form.cleaned_data

            usuarios = Usuarios(nombre_usuario=formulario_limpio['nombre_usuario'], email_usuario=formulario_limpio['email_usuario'])
            
            usuarios.save()
            
            return render(request, 'App1/usuarios.html')
    else:
        form = crear_Usuarios_forms()
    
    return render(request, 'App1/crear_usuarios.html', {'form': crear_Usuarios_forms})


def crear_Productos(request):
    if request.method == 'POST':
        form = crear_Productos_forms(request.POST)
        
        if form.is_valid():
            
            formulario_limpio  = form.cleaned_data
            
            productos = Productos(nombre_producto=formulario_limpio['nombre_producto'], marca_producto=formulario_limpio['marca_producto'])
            
            productos.save()
            
            return render(request, 'App1/productos.html')
    
    else:
        form = crear_Productos_forms()
    
    return render(request, 'App1/crear_productos.html', {'form': crear_Productos_forms})

def crear_Ventas_detalles(request):

    if request.method == 'POST':
        form = crear_Ventas_detalles_forms(request.POST)
        
        if form.is_valid():
            
            formulario_limpio  = form.cleaned_data
            
            ventas_detalles = Ventas_detalles(monto=formulario_limpio['monto'], fecha_venta=formulario_limpio['fecha_venta'], forma_de_pago=formulario_limpio['forma_de_pago'], producto=formulario_limpio['producto'], usuario=formulario_limpio['usuario'])
            
            ventas_detalles.save()
            
            return render(request, 'App1/ventas_detalles.html')
    
    else:
        form = crear_Ventas_detalles_forms()
    
    return render(request, 'App1/crear_ventas.html', {'form': crear_Ventas_detalles_forms})

def buscar_marca_producto(request):
    
    if request.GET.get('marca_producto', False):
        marca_producto = request.GET['marca_producto']
        Producto = Productos.objects.filter(marca_producto__icontains=marca_producto)
        
        return render(request, 'App1/buscar_marca_producto.html', {'Producto': Producto})
    else:
        respuesta = 'no hay datos'
    return render(request, 'App1/buscar_marca_producto.html', {'respuesta': respuesta})

def buscar_usuario(request):
    
    if request.GET.get('email_usuario', False):
        email = request.GET['email_usuario']
        usuario = Usuarios.objects.filter(email_usuario__icontains=email)
        
        return render(request, 'App1/buscar_usuarios.html', {'usuario': usuario})
    else:
        respuesta = 'no hay datos'
    return render(request, 'App1/buscar_usuarios.html', {'respuesta': respuesta})

def buscar_forma_de_pago(request):
    
    if request.GET.get('forma_de_pago', False):
        forma_de_pago = request.GET['forma_de_pago']
        ventas_detalles = Ventas_detalles.objects.filter(forma_de_pago__icontains=forma_de_pago)
        
        return render(request, 'App1/buscar_ventas_detalles.html', {'ventas_detalles': ventas_detalles})
    else:
        respuesta = 'no hay datos'
    return render(request, 'App1/buscar_ventas_detalles.html', {'respuesta': respuesta})

def eliminar_productos(request, productos_id):
    
    productos = Productos.objects.get(id=productos_id)
    #producto = get_object_or_404(Productos, id=productos_id)
    productos.delete()
    
    producto= productos.objects.all()
    
    context = {'producto': producto}
    
    return render(request, 'App1/index.html', context=context)


def actualizar_productos(request, productos_id):
    productos = Productos.objects.get(id=productos_id)
    if request.method == 'POST':
        form = crear_Productos_forms(request.POST)
        
        if form.is_valid():
            
            formulario_limpio  = form.cleaned_data

            productos.nombre_producto = formulario_limpio['nombre_producto']
            productos.marca_producto = formulario_limpio['marca_producto']
            productos.save()
            
            return render(request, 'App1/productos.html')
        
    else:
        form = crear_Productos_forms(initial={'nombre_producto': productos.nombre_producto, 'marca_producto': productos.marca_producto})
        
    return render(request, 'App1/actualizar_productos.html', {'form': crear_Productos_forms})


def eliminar_usuarios(request, usuarios_id):
    
    usuarios = Usuarios.objects.get(id=usuarios_id)
    usuarios.delete()
    
    usuario= usuarios.objects.all()
    
    context = {'usuario': usuario}
    
    return render(request, 'App1/usuarios.html', context=context)


def actualizar_usuarios(request,usuarios_id):
    usuario = Usuarios.objects.get(id=usuarios_id)
    if request.method == 'POST':
        form = crear_Usuarios_forms(request.POST)
        
        if form.is_valid():
            
            formulario_limpio  = form.cleaned_data
        
            usuario.nombre_usuario = formulario_limpio['nombre_usuario']
            usuario.email_usuario = formulario_limpio['email_usuario']
            usuario.save()
        
            return render(request, 'App1/usuarios.html')
    else:
        form = crear_Usuarios_forms(initial={'nombre_usuario': usuario.nombre_usuario, 'email_usuario': usuario.email_usuario})
        
    return render(request, 'App1/actualizar_usuarios.html' , {'form': crear_Usuarios_forms})

def eliminar_Ventas_detalles(request, ventas_detalles_id):
    
    ventas_detalles = Ventas_detalles.objects.get(id=ventas_detalles_id)
    ventas_detalles.delete()
    
    ventas_detalles= ventas_detalles.objects.all()
    
    context = {'ventas_detalles': ventas_detalles}
    
    return render(request, 'App1/ventas_detalles.html', context=context)


def actualizar_ventas_detalles(request, ventas_detalles_id):
    ventas_detalles = Ventas_detalles.objects.get(id=ventas_detalles_id)
    if request.method == 'POST':
        form = crear_Ventas_detalles_forms(request.POST)
        
        if form.is_valid():
            
            formulario_limpio  = form.cleaned_data
        
            ventas_detalles.monto = formulario_limpio['monto']
            ventas_detalles.fecha_venta = formulario_limpio['fecha_venta']
            ventas_detalles.forma_de_pago = formulario_limpio['forma_de_pago']
            ventas_detalles.producto = formulario_limpio['producto']
            ventas_detalles.usuario = formulario_limpio['usuario']
            
            ventas_detalles.save()
        
            return render(request, 'App1/ventas_detalles.html')
        
    else:
    
        form = crear_Ventas_detalles_forms(initial={'monto': ventas_detalles.monto, 'fecha_venta': ventas_detalles.fecha_venta, 'forma_de_pago': ventas_detalles.forma_de_pago, 'producto': ventas_detalles.producto, 'usuario': ventas_detalles.usuario})
        
        return render(request, 'App1/actualizar_ventas_detalles.html', {'form': crear_Ventas_detalles_forms}) 
     

def registro_usuario(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)         
        if form.is_valid():
            form.save() #Guardar el usuario sin asignarlo a una variable
            messages.success(request, '¡Registro exitoso! Bienvenido/a.')
            #Renderiza directamente el template de index después del registro exitoso           
            return render(request, 'App1/index.html')
        
    else:
            form = UserRegisterForm()
        
    return render(request,'App1/registro.html', {'form': form})

def login_request(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')
            
            user = authenticate(username=usuario, password=contra)
            
            
            if user is not None:
                    login(request, user)
                
                    return render(request, "App1/index.html", {"mensaje":f"Bienvenido {usuario}"})
        
            else:
                    return render(request, "App1/index.html",  {"mensaje":"Error, datos incorrectos"})
        
        else:
                return render(request, "App1/index.html", {"mensaje":"Error, formulario erroneo"})
    
    form = AuthenticationForm()
    
    return render(request, "App1/login.html", {"form": form})

def logout_request(request):
    logout(request)
    
    return render(request, "App1/index.html", {"mensaje":"Has cerrado sesión correctamente"})

def privacy_policy(request):
    return render(request, "App1/privacy_policy.html")

def terms_conditions(request):
    return render(request, "App1/terms_conditions.html")

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        
        if nombre and email and mensaje:
            # Guardar el mensaje en la base de datos
            MensajeContacto.objects.create(
                nombre=nombre,
                email=email,
                mensaje=mensaje,
            )
            
            # Enviar confirmación al usuario
            send_mail(
                'Gracias por contactarnos',
                f'Hola {nombre}, hemos recibido tu mensaje y te contactaremos pronto.',
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            
            messages.success(request, 'Mensaje enviado exitosamente.')
            return redirect('pagina_de_gracias')
        else:
            messages.error(request, 'Por favor, rellena todos los campos.')
            
    return render(request, 'App1/contacto.html')

def pagina_de_gracias(request):
    return render(request, 'App1/gracias.html')

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha_envio')
    search_fields = ('nombre', 'email')

def listar_mensajes(request):
    mensajes = MensajeContacto.objects.all().order_by('-fecha_envio')
    paginator = Paginator(mensajes, 10) # Mostrar 10 mensajes por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'App1/lista_mensajes.html', {'page_obj': page_obj} ) #{'mensajes': mensajes}