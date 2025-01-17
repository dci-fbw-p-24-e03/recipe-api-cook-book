from django.test import TestCase
from rest_framework.test import APIClient
from api_app.models import CustomUser,Recipe
from django.urls import reverse
from rest_framework import status
# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'bio': 'This is a test bio that is sufficiently long.',
            'sex': 'M',
            'birthdate': '2000-01-01',
        }
        user=CustomUser.objects.create(**self.test_user)
        user.set_password(self.test_user['password'])
        user.save()


    def test_user_creation(self):
        self.test_user_1 = {
            'username': 'testusers',
            'email': 'testuser_1@example.com',
            'password': 'testpassword123',
            'bio': 'This is a test bio that is sufficiently long.',
            'sex': 'M',
            'birthdate': '1995-01-01',
        }
        response =self.client.post(reverse("users-list"),self.test_user_1)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(),2)

    def test_get_all_users(self):
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_login_user(self):
        response = self.client.post(reverse('user-login'), data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_logout_user(self):
        response = self.client.post(reverse('user-login'), data={'username': 'testuser', 'password': 'testpassword'})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(reverse('user-logout'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["message"],"Logged out successfully")
        self.assertNotIn('token',response.data)

    def test_create_invalid_user(self):
        self.test_user_1 = {
            'username': 'adminusers',
            'email': 'testuser_1@example.com',
            'password': 'testpassword123',
            'bio': 'This is a test bio that is sufficiently long.',
            'sex': 'M',
            'birthdate': '1995-01-01',
        }
        response =self.client.post(reverse("users-list"),self.test_user_1)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


class TestRecipes(TestCase):
    def setUp(self):
        
        self.client = APIClient()
        self.test_user = {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'testpassword',
                'bio': 'This is a test bio that is sufficiently long.',
                'sex': 'M',
                'birthdate': '2000-01-01',
            }
        self.user=CustomUser.objects.create(**self.test_user)
        self.user.set_password(self.test_user['password'])
        self.user.save()
        self.client.login(username='testuser', password='password123')

        self.recipe_data={
            "chef": self.user.id,
            "title": "testrecipe",
            "description": "a description long enough to pass the test",
            "meal_type": "D",
            "ingredients": "Test Ingredients to pass the test",
            "created_at": "2025-01-10T09:13:48.808495Z",
        }
    def test_recipe_creation(self):
        response = self.client.post(reverse("recipes-list"),self.recipe_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(),1)

    def test_get_all_recipes(self):
        response = self.client.post(reverse("recipes-list"),self.recipe_data)
        response_get = self.client.get(reverse('recipes-list'))
        self.assertEqual(response_get.status_code,status.HTTP_200_OK)

    def test_create_invalid_recipe(self):
        recipe_data={
            "chef": self.user.id,
            "title": "testrecipewith uranium",
            "description": "a description long enough to pass the test",
            "meal_type": "D",
            "ingredients": "Test Ingredients to pass the test",
            "created_at": "2025-01-10T09:13:48.808495Z",
        }
        response = self.client.post(reverse("recipes-list"),recipe_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_update_recipe_without_login(self):
        response = self.client.post(reverse("recipes-list"),self.recipe_data)
        recipe_title={
            "title": "testrecipeforupdate",
        }
        response = self.client.patch(reverse("recipe-detail",kwargs={"pk":1}),data=recipe_title)

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    def test_update_recipe(self):
        response = self.client.post(reverse("recipes-list"),self.recipe_data)
        login_response = self.client.post(reverse("user-login"),{
                'username': 'testuser',
                'password': 'testpassword'})
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        recipe_title={
           
            "title": "testrecipeforupdate",
            
        }
        response = self.client.patch(reverse("recipe-detail",kwargs={"pk":1}),data=recipe_title)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    