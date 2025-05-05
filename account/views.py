from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from django.shortcuts import render, redirect  
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Vista para el api rest del registro
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para el api rest del login
class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request, username=serializer.validated_data['username'], password=serializer.validated_data['password']
            )
            if user is not None:
                # Crear los tokens JWT
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                refresh.payload['username'] = user.username

                # Crear la respuesta de redirección
                response = JsonResponse({'message': 'Login successful'})  # Retornamos un JsonResponse primero

                # Establecer el token en una cookie segura
                response.set_cookie(
                    #aca se guarda el token en las cookies y redirigue al 
                    'access_token', access_token, httponly=False, secure=True, max_age=3600, samesite='Lax'
                ) 

                # Redirigir a la página de inicio (root)
                response['Location'] = '/'  # Redirigir a la raíz del sitio
                response.status_code = 302  # Establecemos un código de redirección

                return response

            # Si las credenciales son incorrectas
            return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Si el serializer no es válido
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para el frontend (ejemplo de una página de login con un formulario tradicional)
def Login_view(request):
    return render(request, 'account/login.html')


def Register_view(request):
    return render(request, 'account/register.html')


def logout_view(request):
    # Eliminar la cookie del access_token
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('access_token')  # Esto elimina la cookie 'access_token'
    
    return response

def get_username(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({'username':user.username})
    except User.DoesNotExist:
        return JsonResponse({'Error':'User not found'},status=404)