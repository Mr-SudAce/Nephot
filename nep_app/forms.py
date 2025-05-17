from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# user
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# Add Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = "__all__"


# Add Catgory
class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = "__all__"


# Add Cart Item
class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItemModel
        fields = "__all__"


# Add Cart
class CartForm(forms.ModelForm):
    class Meta:
        model = CartModel
        fields = "__all__"


# Add ImageSlider image
class ImageSliderForm(forms.ModelForm):
    class Meta:
        model = image_SliderModel
        fields = "__all__"


# Add Sub_Category
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_CategoryModel
        fields = "__all__"


class HeaderForm(forms.ModelForm):
    class Meta:
        model = HeaderModel
        fields = "__all__"


class OtherDetailForm(forms.ModelForm):
    class Meta:
        model = OtherDetailModel
        fields = "__all__"


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = AdvertisementModel
        fields = "__all__"

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingInfoModel
        fields = ['address', 'city', 'postal_code', 'phone_number']