from django.conf import settings
from django.conf.urls.static import *
from django.urls import path
from django.conf.urls import *
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("cart/", cart_detail, name="cart_Detail"),
    #
    #
    # cart
    path("add-to-cart/<int:id>/", add_to_cart, name="add_to_cart"),
    path("cart/update_all/", update_all_cart_details, name="update_all_cart_details"),
    path("cartdetail/delete/<int:cart_det_id>/",cartdetail_delete, name="cartdetail_delete"),
    #
    #
    # productdetail
    path("product-detail/<int:id>/",product_itemView_detail, name="product_itemView_detail"),
    path("update-cart/<int:id>/", update_cart_quantity, name="update_cart_quantity"),
    path("delete-crt/<int:id>/", delete_cart_item, name="delete_cart_item"),
    #
    #
    #
    path('all-products/', show_allproducts, name='allproduct'),
    path('all-products/category/<int:category_id>/', show_allproducts, name='allproduct_by_category'),
    path('all-products/', show_allproducts, name='allproduct'),
    # 
    # 
    # 
    path('products/<int:id>/', filter_by_subcategory, name='filterbysubcate'),
    path('category/<int:id>/', filter_by_category, name='filter_by_category'),   
    # 
    #
    #
    #
    # D_Content [add function]
    path("add-product/", add_product, name="add_product"),
    path("add-category/", add_category, name="add_category"),
    path("add-sub-category/", add_sub_category, name="add_sub_category"),
    path("add-image-slider/", add_image_slider, name="add_image_slider"),
    path("add-cart/", add_cart, name="add_cart"),
    path("add-cart-item/", add_cart_item, name="add_cart_item"),
    path("add_header/", add_header, name="add_header"),
    path("add_otherdetail/", add_otherdetail, name="add_otherdetail"),
    path("add_advertisement/", add_advertisement, name="add_advertisement"),
    #
    #
    # D_Content [update function]
    path('update-product/<int:id>', update_product, name='update_product'),
    path('update-category/<int:id>', update_category, name='update_category'),
    path('update-sub-category/<int:id>', update_sub_category, name='update_sub_category'),
    path('update-image-slider/<int:id>', update_image_slider, name='update_image_slider'),
    path('update-cart/<int:id>', update_cart, name='update_cart'),
    path('update-cart-item/<int:id>', update_cart_item, name='update_cart_item'),
    path('update-header/<int:id>', update_header, name='update_header'),
    path('update-otherdetail/<int:id>', update_otherdetail, name='update_otherdetail'),
    path('update-advertisement/<int:id>', update_advertisement, name='update_advertisement'),
    # 
    # 
    # 
    # D_Content [delete function]
    path("delete-product/<int:id>", del_product, name="del_product"),
    path("delete-category/<int:id>", del_category, name="del_category"),
    path("delete-sub-category/<int:id>", del_sub_category, name="del_sub_category"),
    path("delete-image-slider/<int:id>", del_image_slider, name="del_image_slider"),
    path("delete-cart/<int:id>", del_cart, name="del_cart"),
    path("delete-cart-item/<int:id>", del_cart_item, name="del_cart_item"),
    path("delete-header/<int:id>", del_header, name="del_header"),
    path("delete-otherdetail/<int:id>", del_otherdetail, name="del_otherdetail"),
    path("delete-advertisement/<int:id>", del_advertisement, name="del_advertisement"),
    #
    #
    # search
    path("search/", search_query, name="search_query"),
    #
    #
    # dashboard
    path("dashboard/", dashboard, name="dashboard"),
    #
    #
    # authentication
    path("accounts/login/", user_login, name="login"),
    path("accounts/register/", user_register, name="register"),
    path("logout/", user_logout, name="logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
