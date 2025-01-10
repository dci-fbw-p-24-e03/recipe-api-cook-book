### **What is Django REST Framework (DRF)?**

Django REST Framework (DRF) is a powerful and flexible toolkit for building Web APIs. While Django is primarily used for creating web applications, DRF extends Django to make it easier to build APIs that can be consumed by frontend frameworks (like React, Angular, or Vue) or mobile apps.

**Key Features of DRF:**
1. Serialization for converting complex data types (like querysets) to JSON or other content types.
2. Built-in support for common HTTP methods (GET, POST, PUT, DELETE).
3. Authentication and permission management for APIs.
4. Browsable API for testing and interacting with the API directly via a web interface.

### **Difference Between Django and Django REST Framework**

| Feature               | Django                                      | Django REST Framework                         |
|-----------------------|---------------------------------------------|----------------------------------------------|
| Purpose               | Builds web applications with HTML templates. | Builds APIs that return data (e.g., JSON).   |
| Response Type         | Typically HTML rendered using templates.    | JSON, XML, or other data formats.            |
| Data Serialization    | Not a primary feature.                      | Serializers handle converting models to JSON.|
| Interaction           | Meant for browsers.                        | Meant for API consumers like mobile apps.    |

---

### **What is a Serializer?**

In DRF, a **serializer** is used to convert complex data types, like Django models, into JSON or other data formats, and vice versa. For example:
- When sending data from the server to a client, serializers convert model instances into JSON.
- When receiving data from a client (e.g., via POST), serializers validate and convert the JSON into model instances.

---

### **Code Explanation**

#### **`settings.py`**
```python
INSTALLED_APPS = [
    ...
    "api_app",  # Your app containing API-related models, views, and serializers.
    "rest_framework",  # Enables DRF in the project.
]

AUTH_USER_MODEL = "api_app.CustomUser"  # Specifies the custom user model.
```

- **`api_app`**: Your Django app containing the models and logic for the API.
- **`rest_framework`**: Adds DRF functionality to your project.
- **`AUTH_USER_MODEL`**: Overrides the default Django `User` model with a custom one (`CustomUser`).

---

#### **`models.py`**
1. **`CustomUser` Model**:
   ```python
   class CustomUser(AbstractUser):
       bio = models.TextField(blank=True, null=True)
       birthdate = models.DateField(blank=True, null=True)
       SEX_CHOICES = [
           ('M', 'Male'),
           ('F', 'Female'),
           ('O', 'Other'),
       ]
       sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
   ```
   - Extends Django's default `User` model (`AbstractUser`).
   - Adds custom fields like `bio`, `birthdate`, and `sex` (with predefined choices).

2. **`Recipe` Model**:
   ```python
   class Recipe(models.Model):
       chef = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
       title = models.CharField(max_length=255)
       description = models.TextField()
       meal_type = models.CharField(max_length=1, choices=MEAL_TYPE_CHOICES)
       ingredients = models.TextField(help_text="Comma-separated list of ingredients")
       image = models.ImageField(upload_to='recipes/', blank=True, null=True)
       created_at = models.DateTimeField(auto_now_add=True)
   ```
   - Represents a recipe created by a `CustomUser`.
   - Fields:
     - **`chef`**: Foreign key linking a recipe to a user. Deletes the recipe if the user is deleted.
     - **`meal_type`**: Type of meal (breakfast, lunch, or dinner).
     - **`ingredients`**: A list of ingredients as a comma-separated string.
     - **`image`**: Optional image for the recipe.
     - **`created_at`**: Auto-populates with the current date and time.

---

#### **`serializer.py`**
1. **`CustomUserSerializer`**:
   ```python
   class CustomUserSerializer(serializers.ModelSerializer):
       class Meta:
           model = CustomUser
           fields = ("id", "username", "first_name", "last_name", "email", "sex", "birthdate", "bio")
   ```
   - Converts `CustomUser` model instances to/from JSON.
   - Fields include `id`, `username`, `bio`, etc.

2. **`RecipeSerializer`**:
   ```python
   class RecipeSerializer(serializers.ModelSerializer):
       class Meta:
           model = Recipe
           fields = ("id", "chef", "title", "description", "meal_type", "ingredients", "created_at", "image")
   ```
   - Serializes `Recipe` model instances.
   - Includes all relevant fields of the `Recipe` model.

---

#### **`views.py`**
1. **`CustomUserListView`**:
   ```python
   class CustomUserListView(ListCreateAPIView):
       queryset = CustomUser.objects.all()
       serializer_class = CustomUserSerializer
   ```
   - Handles listing all users (`GET`) and creating new users (`POST`).

2. **`CustomUserDetailView`**:
   ```python
   class CustomUserDetailView(RetrieveUpdateDestroyAPIView):
       queryset = CustomUser.objects.all()
       serializer_class = CustomUserSerializer
   ```
   - Handles retrieving, updating, and deleting a specific user by their ID.

3. **`RecipeListView`**:
   ```python
   class RecipeListView(ListCreateAPIView):
       queryset = Recipe.objects.all()
       serializer_class = RecipeSerializer
   ```
   - Handles listing all recipes (`GET`) and creating new recipes (`POST`).

4. **`RecipeDetailView`**:
   ```python
   class RecipeDetailView(RetrieveUpdateDestroyAPIView):
       queryset = Recipe.objects.all()
       serializer_class = RecipeSerializer
   ```
   - Handles retrieving, updating, and deleting a specific recipe by its ID.

---

#### **`urls.py`**
```python
urlpatterns = [
    path("users/", CustomUserListView.as_view(), name="users-list"),
    path("users/<int:pk>/", CustomUserDetailView.as_view(), name="user-details"),
    path('recipes/', RecipeListView.as_view(), name='recipes-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
]
```
- **`users/`**: Lists all users or allows creating a new user.
- **`users/<int:pk>/`**: Retrieves, updates, or deletes a specific user.
- **`recipes/`**: Lists all recipes or allows creating a new recipe.
- **`recipes/<int:pk>/`**: Retrieves, updates, or deletes a specific recipe.

---

### Summary

This code demonstrates a simple DRF API for managing users and recipes. Users can perform CRUD operations on `CustomUser` and `Recipe` models via the defined views and serializers. The serializers handle data conversion and validation, while the views provide the logic for handling API requests.


### **Class-Based APIView Equivalent**

The generic views (`ListCreateAPIView` and `RetrieveUpdateDestroyAPIView`) simplify common operations. Using `APIView`, we explicitly define the behavior for each HTTP method (`GET`, `POST`, `PUT`, `DELETE`).

#### **User Views**
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializer import CustomUserSerializer

class CustomUserListAPIView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetailAPIView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

#### **Recipe Views**
```python
from .models import Recipe
from .serializer import RecipeSerializer

class RecipeListAPIView(APIView):
    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailAPIView(APIView):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

---

### **Function-Based View (FBV) Equivalent**

FBVs explicitly define behavior for each HTTP method using conditional checks.

#### **User Views**
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializer import CustomUserSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
def custom_user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def custom_user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

#### **Recipe Views**
```python
@api_view(['GET', 'POST'])
def recipe_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

---

### **Summary of Differences**

| **Feature**               | **Generic Views**                  | **APIView**                     | **Function-Based Views**          |
|---------------------------|------------------------------------|----------------------------------|------------------------------------|
| **Code Complexity**       | Minimal (uses predefined logic).  | Moderate (explicit definitions).| High (manual method handling).    |
| **Customization**         | Limited (extend or override).     | Full customization.             | Full customization.               |
| **Ease of Use**           | Easiest (boilerplate).            | Moderate.                       | Can be verbose for complex logic. |

Each approach has its use case. Generic views are great for rapid development, while APIViews and FBVs provide more control when customizing behavior.