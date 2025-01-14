from django.shortcuts import render
from .serializer import CustomUserSerializer,RecipeSerializer
# Create your views here.
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Recipe,CustomUser
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from .permission import IsAdminOrReadOnly,IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication


class CustomUserListView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

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
    

class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes=[IsOwnerOrReadOnly]
    authentication_classes =[TokenAuthentication]