from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from api.handlers.auth_handler import AuthHandler
from api.serializers import RegisterSerializer, UserDetailSerializer, CustomTokenObtainPairSerializer

class RegisterController(APIView):
    authentication_classes = []
    permission_classes = []
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_handler = AuthHandler()
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = self.auth_handler.register_user(
                name=data['name'],
                phone_number=data['phone_number'],
                email=data.get('email'),
                password=data['password']
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response_serializer = UserDetailSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)



class LoginController(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer