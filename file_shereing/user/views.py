from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework import response
from .serializer import UserSerializer, loginserializer, OTPTokenSerializer, fileserializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
import random
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import FileResponse

@swagger_auto_schema(
    method='post',
    operation_description="Create a new user",
    request_body=UserSerializer,
    responses={201: UserSerializer, 400: 'Bad Request'}
)
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        email = request.data.get('email')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data.get('username'))
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            encrypted_url = f"http://127.0.0.1:8000/signup/{token}"
            try:
                otp = str(random.randint(100000, 999999))
                otp_token = OTPToken.objects.create(token=otp)

                subject = 'Verification OTP'
                message = f"Your verification OTP is {otp}"
                send_mail(subject, message, 'rohit6398.iimt@gmail.com', email)
                if response.status_code == 200:
                    return Response({'success': True, 'message': 'email sent successfully'})
            except Exception as e:
                return Response({'message': otp, 'url': encrypted_url}, status=status.HTTP_201_CREATED)
            return Response({'message': otp}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="login",
    request_body=loginserializer,
    responses={201: UserSerializer, 400: 'Bad Request'}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    print(user)
    if user == None:
        return Response({'error': "invalid username or password"}, status=400)
    elif not user.is_staff:
        return Response({'message': "client user"}, status=200)
    elif user.is_staff:
        return Response({'message': 'ops user'}, status=200)
    else:
        return Response({'error': 'Invalid credentials'}, status=400)


@swagger_auto_schema(method='post', request_body=OTPTokenSerializer)
@api_view(['POST'])
def otp_ver(request):
    token = request.data.get('token')
    try:
        otp_token = OTPToken.objects.get(token=token)
        otp_token.delete()
        return Response({'detail': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
    except OTPToken.DoesNotExist:
        return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(generics.ListCreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = fileserializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        files = self.get_queryset()
        serializer = self.get_serializer(files, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def download_file(request, file_id):
    try:
        file_obj = UploadedFile.objects.get(id=file_id)
        file_path = file_obj.file.path
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    except UploadedFile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)