from django.urls import path

from .views import CustomUserListView,CustomUserDetailView,RecipeListView,RecipeDetailView


urlpatterns = [
    path("users/",CustomUserListView.as_view(),name="users-list"),
    path("users/<int:pk>/",CustomUserDetailView.as_view(),name="user-details"),
     path('recipes/', RecipeListView.as_view(), name='recipes-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
]