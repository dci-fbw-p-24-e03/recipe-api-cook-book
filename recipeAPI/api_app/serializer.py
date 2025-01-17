from rest_framework import serializers
from .models import CustomUser,Recipe
from django.core.exceptions import ValidationError
from datetime import date
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import bleach 
from django.utils.text import slugify


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id","username","password","first_name","last_name","email","sex","birthdate","bio")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


    def validate_username(self,value):#validate_<field_name>
        restricted_words = ['admin', 'dog', 'cat']

        if any(word in value.lower() for word in restricted_words):
            raise serializers.ValidationError("username must not contain these words")
        return value
    
    def validate_bio(self,value):
        if len(value) < 20:
            raise serializers.ValidationError("bio must be at 20 characters")
        return value
    

    def validate_birthdate(self,value):
        today = date.today()
        age = today.year - value.year 
        if age < 15:
            raise serializers.ValidationError("User must be at least 15 years old.")
        

    def sanitize_html(self,value):
        allowed_tags = ['b', 'i', 'u', 'em', 'strong']
        return bleach.clean(value, tags=allowed_tags, strip=True)
    
    def slugify_username(self,value):
        return slugify(value)

    def slugify_bio(self,value):
        return slugify(value)
    
    def replace_dollar_sign(self,value):
        if "$" in value:
            value.replace("$","_")
        return value
    def validate(self, data):
        data['username']=self.slugify_username(data['username'])
        #data['first_name']=self.slugify_username(data['first_name'])
        data['bio'] = self.sanitize_html(data['bio'])
        data["bio"] = self.replace_dollar_sign(data["bio"])
        data['bio'] = self.slugify_bio(data['bio'])
        

        return data
        

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id","chef","title","description","meal_type","ingredients","created_at","image")

        #fields = "__all__"

    def validate_title(self,value):#validate_<field_name>
        restricted_words = ['uranium', 'python', 'iron']

        if any(word in value.lower() for word in restricted_words):
            raise serializers.ValidationError("title must not contain these words")
        return value

    def validate_description(self,value):
        if len(value) < 20:
            raise serializers.ValidationError("Description must be at least 20 characters long.")
        return value
    
    def resize_image(self,image_field):
        image = Image.open(image_field)
        image = image.resize((300, 300))
        
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        resized_image = ContentFile(image_io.getvalue(), name=image_field.name)
        return resized_image
    

    def slugify_data(self,value):
        return slugify(value)
    
    def sanitize_html(self,value):
        allowed_tags = ['b', 'i', 'u', 'em', 'strong']
        return bleach.clean(value, tags=allowed_tags, strip=True)
    
    def validate(self, validated_data):
        validated_data['title'] = self.slugify_data(validated_data.get("title",""))
        validated_data['description'] = self.slugify_data(validated_data.get("description",""))
        validated_data['description'] = self.sanitize_html(validated_data.get("description",""))

        if "image" in validated_data:
            validated_data["image"] = self.resize_image(validated_data["image"])

        return validated_data
