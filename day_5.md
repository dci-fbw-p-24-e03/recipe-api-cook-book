### What is Swagger (drf-yasg)?

Swagger (or OpenAPI) is a toolset for designing, documenting, and testing REST APIs. It provides an interactive interface where developers can view API endpoints, their request and response formats, and try them out in real time. 

In Django, the **`drf-yasg`** library integrates Swagger/OpenAPI into Django Rest Framework (DRF) projects. It auto-generates API documentation from the codebase, making it easier for developers to:
1. Understand available endpoints.
2. Validate requests and responses.
3. Test APIs interactively.

---

### Why Swagger is Needed
- **Interactive Documentation**: Automatically generates and updates API documentation based on your code.
- **Ease of Use**: Allows users to test endpoints directly in the browser.
- **Standardized Format**: Follows the OpenAPI specification, ensuring compatibility with tools that support OpenAPI.
- **Improved Collaboration**: Helps frontend and backend teams communicate API structures.
- **Time-Saving**: Reduces the need for manually writing API documentation.

---

### Code

#### **`settings.py`**

```python
INSTALLED_APPS = [
    ...
    "drf_yasg"
]

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        'api_key': {
            "type": 'apiKey',
            "in": "headers",
            'name': 'Authorization'
        }
    }
}
```

1. **`INSTALLED_APPS`**: Adds `drf_yasg` to the project, enabling Swagger documentation features.
2. **`SWAGGER_SETTINGS`**:
   - Configures authentication for the Swagger UI.
   - The `"SECURITY_DEFINITIONS"` section defines how the API will handle authorization:
     - `"type": 'apiKey'` specifies token-based authentication.
     - `"in": "headers"` means the token is passed in the HTTP headers.
     - `'name': 'Authorization'` indicates the header key for the token.

---

#### **`urls.py`**

```python
schema_view = get_schema_view(
    openapi.Info(
        title="Your API for finding the best recipes and the best chefs",
        default_version="v1",
        description="Find and create recipes.",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
```

1. **`get_schema_view`**: Generates the Swagger schema based on the provided API information.
2. **`openapi.Info`**: Contains metadata for the API:
   - **`title`**: Name of the API.
   - **`default_version`**: Version of the API (e.g., `v1`).
   - **`description`**: Brief explanation of the API's purpose.
   - **`terms_of_service`**: Link to the terms and conditions.
   - **`contact`**: Developer or support email.
   - **`license`**: Licensing information (e.g., BSD License).

```python
urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-doc"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-doc"),
    ...
]
```

3. **`schema_view.with_ui`**:
   - **`"swagger"`**: Renders the Swagger UI (interactive API documentation).
   - **`"redoc"`**: Renders ReDoc, another documentation UI.
   - **`cache_timeout=0`**: Ensures the schema is always updated without caching.

---

#### **`views.py`**

##### CustomUserListView
```python
@swagger_auto_schema(
    operation_description="Get the list of all users",
    responses={'200': CustomUserSerializer(many=True)}
)
def get(self, request, *args, **kwargs):
    return super().get(request, *args, **kwargs)
```

1. **`swagger_auto_schema`**:
   - Adds Swagger-specific metadata to the API view.
   - **`operation_description`**: Describes the purpose of the endpoint.
   - **`responses`**: Specifies possible HTTP response codes and their associated serializers (or messages).

```python
@swagger_auto_schema(
    operation_description="Create new user according to validation",
    responses={
        '201': "New User was added",
        '400': "Bad request get out of here"
    }
)
def post(self, request, *args, **kwargs):
    return super().post(request, *args, **kwargs)
```

2. For the `POST` method:
   - **`201`**: Indicates a successful creation.
   - **`400`**: Describes a bad request.

---

##### LoginView
```python
@swagger_auto_schema(
    operation_description="Login and generate a new token",
    responses={
        '200': "User logged in",
        '400': "Invalid credentials",
    }
)
def post(self, request):
    username = request.data.get("username")
    password = request.data.get("password")
    ...
```

- This decorator provides Swagger documentation for the login endpoint:
  - Explains that it logs in a user and generates a token.
  - Details possible responses (`200` for success, `400` for invalid credentials).

---

##### LogoutView
```python
@swagger_auto_schema(
    operation_description="Logout and the token will be deleted",
    responses={'200': "User logged out"}
)
def post(self, request):
    request.user.auth_token.delete()
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
```

- **Purpose**: Adds documentation for the logout endpoint.
- **Response Example**:
  - **`200`**: User logged out successfully.

---

### How Swagger Works
1. **Auto-Generated Documentation**: 
   - `drf-yasg` uses the `swagger_auto_schema` decorator and DRF serializers to generate endpoint descriptions.
   - Endpoints without explicit documentation (decorators) still appear but lack detailed metadata.

2. **Interactive UI**:
   - Developers can interact with endpoints directly in the browser.
   - Test data can be sent in requests to verify functionality.

3. **API Requests**:
   - Each endpoint's parameters (e.g., headers, body, query parameters) are displayed in Swagger.
   - Swagger auto-generates example requests based on the serializers and fields.

---

### Example Workflow
1. Visit `/swagger/` in the browser.
2. See a list of all API endpoints with their details.
3. Expand an endpoint (e.g., `GET /api/v1/users/`) to view:
   - Parameters (e.g., query filters).
   - Request and response schemas.
4. Test the endpoint by entering parameters and clicking "Try it out."

---

This setup simplifies API testing and ensures the documentation is always up-to-date with the codebase.