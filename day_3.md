### **Authentication and Permissions in the Code**


---

### **Authentication**
Authentication ensures that the user accessing the API is valid and can be identified. It answers the question, **"Who is the user?"**

#### **Key Parts**
1. **`settings.py`**
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.TokenAuthentication',
           'rest_framework.authentication.SessionAuthentication',
           'rest_framework.authentication.BasicAuthentication',
       ],
       ...
   }
   ```
   - **`TokenAuthentication`**: Validates requests using tokens. Users must include a valid token in the `Authorization` header (e.g., `Authorization: Token <token>`).
   - **`SessionAuthentication`**: Relies on Django sessions for authentication. It is commonly used for web browsers.
   - **`BasicAuthentication`**: Allows basic username/password authentication for simpler use cases (mainly for testing).

2. **Token Creation**
   In the shell:
   ```python
   from rest_framework.authtoken.models import Token
   user = CustomUser.objects.get(username='your_username')
   token = Token.objects.create(user=user)
   ```
   - A unique token is created for a specific user. This token must be included in the header of API requests to authenticate the user.

3. **Header Example**
   ```
   Authorization: Token 8951a608c193c5e6bb1b600c77520538aa477bba
   ```
   - The token is passed in the `Authorization` header for authenticated requests.

4. **Authentication in Views**
   ```python
   authentication_classes = [TokenAuthentication]
   ```
   - Each view specifies that `TokenAuthentication` is required to validate users. If a user doesn't provide a valid token, they won't be able to access the view.

---

### **Permissions**
Permissions define what authenticated users can or cannot do. It answers the question, **"Is this user allowed to perform this action?"**

#### **Key Parts**
1. **Default Permissions**
   ```python
   'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.IsAuthenticated',
   ],
   ```
   - The default permission class ensures that all views require users to be authenticated by default.

2. **Custom Permissions**
   - **`IsAdminOrReadOnly`**
     ```python
     class IsAdminOrReadOnly(BasePermission):
         def has_permission(self, request, view):
             if request.method in SAFE_METHODS:
                 return True
             return request.user.is_staff
     ```
     - **SAFE_METHODS**: Includes HTTP methods like `GET`, `HEAD`, and `OPTIONS` (read-only).
     - Admin users (`user.is_staff == True`) can perform write operations (e.g., `POST`, `PUT`, `DELETE`).
     - Regular users can only perform read operations.

   - **`IsOwnerOrReadOnly`**
     ```python
     class IsOwnerOrReadOnly(BasePermission):
         def has_object_permission(self, request, view, obj):
             if request.method in SAFE_METHODS:
                 return True
             return obj.chef == request.user
     ```
     - For object-level permissions:
       - Read operations (`SAFE_METHODS`) are allowed for everyone.
       - Write operations (e.g., `PUT`, `DELETE`) are restricted to the object's owner (`obj.chef` matches the current user).

3. **Permissions in Views**
   - **CustomUser Views**
     ```python
     permission_classes = [AllowAny]  # CustomUserListView
     permission_classes = [IsAdminOrReadOnly]  # CustomUserDetailView
     ```
     - `AllowAny`: No restrictions; anyone can access.
     - `IsAdminOrReadOnly`: Only admins can modify, but everyone can read.

   - **Recipe Views**
     ```python
     permission_classes = [IsOwnerOrReadOnly]
     ```
     - `IsOwnerOrReadOnly`: Ensures that only the owner (`chef`) of the recipe can modify it. Others can only read.

---

### **How It Works in Practice**
1. A client sends an API request with an `Authorization` header containing a valid token.
2. Django Rest Framework (DRF) checks the `TokenAuthentication` to validate the token and identify the user.
3. After authentication, DRF evaluates the permissions:
   - If the request is a `SAFE_METHOD` (like `GET`), read permissions are usually granted.
   - For write operations (like `POST`, `PUT`, `DELETE`), DRF checks if the user satisfies the conditions defined in the `permission_classes` of the view.
4. If both authentication and permission checks pass, the request is processed. Otherwise, a `403 Forbidden` or `401 Unauthorized` error is returned.

---

This layered approach ensures secure and flexible access to the API while accommodating various user roles and scenarios.

### **Difference Between Authentication and Permission**

| Aspect              | **Authentication**                              | **Permission**                              |
|---------------------|------------------------------------------------|--------------------------------------------|
| **Definition**       | Identifies who the user is.                    | Determines what the authenticated user can do. |
| **Purpose**          | Ensures the user is valid and logged in.        | Ensures the user has access rights to a specific action or resource. |
| **Scope**            | User-wide: Applies to the entire request.       | Resource-specific: Applies to actions on specific resources or objects. |
| **Example**          | Checking if the provided token is valid.        | Allowing only the object owner to update a recipe. |
| **Failure Response** | Returns `401 Unauthorized`.                     | Returns `403 Forbidden`.                   |

---

### **Different Authentication Types**

1. **Token Authentication**
   - **Description**: Each user is issued a unique token upon authentication. This token must be sent in the request header for subsequent API calls.
   - **Header Example**: 
     ```
     Authorization: Token <token_value>
     ```
   - **Use Cases**: Common in simple setups and when APIs are consumed by a limited number of clients.
   - **Advantages**: Easy to implement.
   - **Disadvantages**: Tokens don’t expire by default (unless managed explicitly), leading to potential security risks.

2. **JWT (JSON Web Token) Authentication**
   - **Description**: Uses a self-contained token (JSON structure) that includes encoded user data and a signature to ensure integrity.
   - **Header Example**: 
     ```
     Authorization: Bearer <jwt_token>
     ```
   - **Structure**:
     - **Header**: Algorithm and token type (e.g., HS256, JWT).
     - **Payload**: User data and claims (e.g., user ID, role, expiration).
     - **Signature**: Verifies that the token hasn't been tampered with.
   - **Advantages**:
     - Stateless: No need to store tokens on the server.
     - Includes user claims in the token for fast access.
   - **Disadvantages**:
     - Tokens are often longer.
     - Requires additional steps for secure storage and management (e.g., token expiration, refresh tokens).

3. **Session Authentication**
   - **Description**: Relies on Django's session framework. After login, the server creates a session and sends a session ID to the client via a cookie.
   - **Use Cases**: Suitable for browser-based applications.
   - **Advantages**: Seamlessly integrates with Django's session management.
   - **Disadvantages**: Requires server-side session storage.

4. **Basic Authentication**
   - **Description**: Sends the username and password with every request (Base64 encoded).
   - **Header Example**: 
     ```
     Authorization: Basic <base64_encoded_credentials>
     ```
   - **Advantages**: Simple to implement.
   - **Disadvantages**:
     - Less secure as credentials are sent in every request.
     - Not suitable for production without HTTPS.

---

### **Difference Between `has_permission` and `has_object_permission`**

| Aspect                  | **`has_permission`**                             | **`has_object_permission`**                      |
|-------------------------|--------------------------------------------------|-------------------------------------------------|
| **Purpose**             | Evaluates if the user has general access to the view. | Evaluates if the user has access to a specific object. |
| **Scope**               | Applied at the view level (general access).       | Applied at the object level (specific instance). |
| **When Used**           | Checked before accessing the view.               | Checked during actions on specific objects (e.g., `PUT`, `DELETE`). |
| **Example Use Case**    | Allow all users to access the list view.          | Allow only the owner of a recipe to update it.  |
| **Code Example**        | ```python def has_permission(self, request, view): return request.user.is_authenticated ``` | ```python def has_object_permission(self, request, view, obj): return obj.owner == request.user ``` |

---

### **Example in Practice**

#### View-Level Permission (`has_permission`)
- A user must be authenticated to access the `RecipeListView`.
- Example:
  ```python
  class RecipeListView(ListCreateAPIView):
      permission_classes = [IsAuthenticated]  # Ensures only logged-in users can access.
  ```

#### Object-Level Permission (`has_object_permission`)
- A user can only edit or delete their own recipe.
- Example:
  ```python
  class IsOwnerOrReadOnly(BasePermission):
      def has_object_permission(self, request, view, obj):
          if request.method in SAFE_METHODS:
              return True
          return obj.owner == request.user
  ```

---

### **Summary**
- **Authentication** determines **who** the user is.
- **Permission** determines **what** the user can do.
- **Token Authentication** is simpler but requires manual expiration management, while **JWT** is stateless and more scalable.
- `has_permission` checks access to a view, while `has_object_permission` ensures the user can interact with a specific object.