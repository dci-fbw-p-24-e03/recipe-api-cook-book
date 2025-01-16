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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CustomUserListView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    filter_backends =[DjangoFilterBackend]
    filterset_class =CustomUserFilter

    @swagger_auto_schema(operation_description="Get the list of all users",
                         responses={
                             '200':CustomUserSerializer(many=True)
                         })
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="Create new user according to validation",
                         responses={
                             '201':"New User was added",
                             '400':"Bad request get out of here"
                         })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(operation_description="Get a single user by his id",
                         responses={
                             '200':CustomUserSerializer,
                             '404':"No user Found"
                         })
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    @swagger_auto_schema(operation_description="Update a user",
                         responses={
                             '200':CustomUserSerializer,
                             '400':"Bad request get out of here",
                             "401":"Unauthrized",
                             "403":"You are forbidden to do this"
                         })
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    @swagger_auto_schema(operation_description="Delete a user",
                         responses={
                             "204":"User was deleted and there is no content",
                             "401":"Unauthorized",
                             "403":"You are forbidden to do this"
                         })
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    

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
    permission_classes =[AllowAny]
    @swagger_auto_schema(operation_description="Login and generate a new token",
                         responses={
                             '200':"User logged in",
                             '400':"Invalid credentials",
                             
                         })
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
    @swagger_auto_schema(operation_description="Logout and the token will be deleted",
                         responses={
                             '200':"User logged out",
                             
                         })
    def post(self,request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)