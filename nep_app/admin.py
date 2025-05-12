from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register([CategoryModel,Sub_CategoryModel, image_SliderModel, ProductModel, CartModel, CartItemModel, HeaderModel,])