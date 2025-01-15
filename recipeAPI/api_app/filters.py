from .models import CustomUser,Recipe
import django_filters.rest_framework as filters
SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
MEAL_TYPE_CHOICES = [
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
    ]
class CustomUserFilter(filters.FilterSet):
    dob_gte=filters.DateFilter(field_name="birthdate",lookup_expr="gte")
    dob_lte=filters.DateFilter(field_name="birthdate",lookup_expr="lte")
    sex=filters.TypedChoiceFilter(field_name="sex",choices=SEX_CHOICES)
    class Meta:
        model = CustomUser
        fields ={
            "username":["exact","contains","startswith"],
            "bio":["exact","contains","startswith"]
        }

class RecipeFilter(filters.FilterSet):
    limit = filters.NumberFilter(method="limit_filter")
    chef = filters.CharFilter(field_name="chef__username",lookup_expr="contains")
    meal_type =filters.TypedChoiceFilter(field_name="meal_type",choices=MEAL_TYPE_CHOICES)
    class Meta:
        model = Recipe
        fields = {
            "title":["exact","contains","startswith"],
            "description":["exact","contains","startswith"]
        }

    def limit_filter(self,queryset,name,value):
        return queryset[:value]