from django.shortcuts import render
from .serializer import CustomUserSerializer,RecipeSerializer
# Create your views here.
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView
from .models import Recipe,CustomUser
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from .permission import IsAdminOrReadOnly,IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CustomUserFilter,RecipeFilter


class CustomUserListView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    filter_backends =[DjangoFilterBackend]
    filterset_class =CustomUserFilter

class CustomUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    

class RecipeListView(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes=[IsOwnerOrReadOnly]
    authentication_classes =[TokenAuthentication]
    filter_backends =[DjangoFilterBackend]
    filterset_class =RecipeFilter
    

class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes=[IsOwnerOrReadOnly]
    authentication_classes =[TokenAuthentication]


class LoginView(GenericAPIView):
    serializer_class = CustomUserSerializer
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = CustomUser.objects.filter(username=username).first()
        if user and user.check_password(password):
            login(request,user)
            token = Token.objects.create(user=user)
            return Response({'message':'user logged in','token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        



class LogoutView(GenericAPIView):
    permission_classes =[IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)