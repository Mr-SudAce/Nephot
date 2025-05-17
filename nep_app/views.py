import os
from django.contrib.auth.decorators import *
from django.contrib.auth import *
from django.contrib.auth.forms import *
from django.contrib import messages
from django.shortcuts import *
from django.conf import settings
from .models import *
from .forms import *
from django.urls import *
from handler.ViewHandler import *


# Create your views here.


# Authentication
# Login view
def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")  # Redirect if already logged in

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get("next", "/")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "User_Authentication/userlogin.html", {"form": form})


# Registration view
def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been created! You can log in now."
            )
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, "User_Authentication/userregister.html", {"form": form})


# Logout view
@login_required
def user_logout(request):
    logout(request)
    return redirect("/")


# Home
@login_required
def home(request):
    products = ProductModel.objects.all()
    context = get_common_context(request, products=products)
    return render(request, "home.html", context)


def get_common_context(request, products=None, extra_context=None):
    categories = CategoryModel.objects.prefetch_related("subcategories").all()
    sub_categories = Sub_CategoryModel.objects.all()
    sliders = image_SliderModel.objects.all()
    header = HeaderModel.objects.last()
    otherdetails = OtherDetailModel.objects.last()
    advertisement = AdvertisementModel.objects.all()
    allcategory = CategoryModel.objects.all()

    if request.user.is_authenticated:
        cart = CartModel.objects.filter(user=request.user, is_paid=False).first()
        cart_items = CartItemModel.objects.filter(cart=cart) if cart else []
    else:
        cart_items = []

    cart_items = [item for item in cart_items if item.product]
    total_items_count = len(cart_items)
    grand_total = sum(float(item.total_price()) for item in cart_items)

    context = {
        "categories": categories,
        "sub_categories": sub_categories,
        "images": sliders,
        "cart_item": cart_items,
        "total_items_count": total_items_count,
        "grand_total": grand_total,
        "header": header,
        "otherdetails": otherdetails,
        "advertisement": advertisement,
        "allcategory": allcategory,
    }

    if products is not None:
        context["products"] = products

    if extra_context:
        context.update(extra_context)

    return context


def filter_by_subcategory(request, id):
    fltr_subcategory = get_object_or_404(Sub_CategoryModel, id=id)
    products = ProductModel.objects.filter(pro_sub_category=fltr_subcategory)
    context = get_common_context(
        request, products=products, extra_context={"fltr_subcategory": fltr_subcategory}
    )
    return render(request, "content/cards.html", context)


def filter_by_category(request, id):
    fltr_category = get_object_or_404(CategoryModel, id=id)
    products = ProductModel.objects.filter(product_category=fltr_category)
    context = get_common_context(
        request, products=products, extra_context={"fltr_category": fltr_category}
    )
    return render(request, "content/cards.html", context)


def show_allproducts(request, category_id=None):
    if category_id:
        fltr_category = get_object_or_404(CategoryModel, id=category_id)
        products = ProductModel.objects.filter(product_category=fltr_category)
        extra_context = {"fltr_category": fltr_category}
    else:
        products = ProductModel.objects.all()
        extra_context = {}

    context = get_common_context(
        request, products=products, extra_context=extra_context
    )
    return render(request, "content/cards.html", context)


# add to cart
@login_required
def add_to_cart(request, id):
    product = ProductModel.objects.get(id=id)

    if request.user.is_authenticated:
        cart, _ = CartModel.objects.get_or_create(user=request.user, is_paid=False)
        cart_item = CartItemModel.objects.filter(cart=cart, product=product).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItemModel.objects.create(cart=cart, product=product, quantity=1)
    else:
        cart = request.session.get("cart", {})

        if str(id) in cart:
            cart[str(id)]["quantity"] += 0
        else:
            cart[str(id)] = {
                "product_id": id,
                "quantity": 1,
            }
        request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER", "/"))


# def delete_cart_item(request, id):
#     if request.method == "POST":
#         cart_item = get_object_or_404(CartItemModel, id=id)
#         cart_item.delete()
#         return redirect(request.META.get("HTTP_REFERER", "/"))

def delete_cart_item(request, id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItemModel, id=id)
        cart_item.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))
    return HttpResponseNotAllowed(["POST"])


def cartdetail_delete(request, cart_det_id):
    try:
        cart_item = get_object_or_404(CartItemModel, id=cart_det_id)
        cart_item.delete()
        return redirect("cart_Detail")
    except CartItemModel.DoesNotExist:
        return HttpResponse("Cart item not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


# cart_detail
def cart_detail(request):
    cart_det = CartItemModel.objects.all()

    if request.user.is_authenticated:
        cart = CartModel.objects.filter(user=request.user, is_paid=False).first()
        cart_items = CartItemModel.objects.filter(cart=cart) if cart else []
    else:
        cart_items = []

    # total_items_count = cart_items.count()
    total_items_count = (
        len(cart_items) if isinstance(cart_items, list) else cart_items.count()
    )
    grand_total = sum(
        float(item.total_price()) if item.product else 0 for item in cart_items
    )
    context = {
        "cartdet": cart_det,
        "total_items_count": total_items_count,
        "grand_total": grand_total,
    }
    return render(request, "content/cart_detail.html", context)


def update_all_cart_details(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("quantity_"):
                cart_item_id = key.split("_")[1]
                quantity = int(value)
                cart_item = get_object_or_404(CartItemModel, id=cart_item_id)
                cart_item.quantity = quantity
                cart_item.total_price = cart_item.product.product_price * quantity
                cart_item.save()

        return redirect("cart_Detail")


# Search
def search_query(request):
    if request.method == "GET":
        query = request.GET.get("search_query", "").strip()
        if query:
            product = ProductModel.objects.all()
            products = ProductModel.objects.filter(product_name__icontains=query)
            context = {"products": products, "product": product, "query": query}
            return render(request, "content/search.html", context)
        else:
            return render(
                request, "content/search.html", {"error": "Please enter a search query"}
            )
    else:
        return redirect("home")


# productDetail
def product_itemView_detail(request, id):
    product_itemView_detail = ProductModel.objects.get(id=id)
    products = ProductModel.objects.exclude(id=id)
    cart_itm = CartItemModel.objects.all()
    header = HeaderModel.objects.last()
    cart = CartModel.objects.get(user=request.user)
    product_in_cart = CartItemModel.objects.filter(
        cart=cart, product=product_itemView_detail
    ).exists()
    context = {
        "product_detailV": product_itemView_detail,
        "product_in_cart": product_in_cart,
        "similarproduct": products,
        "header": header,
        "cart_itm": cart_itm,
    }
    return render(request, "content/product_detail.html", context)


def update_cart_quantity(request, id):
    product = get_object_or_404(ProductModel, id=id)
    cart = CartModel.objects.filter(user=request.user, is_paid=False).first()

    if cart:
        cart_item = CartItemModel.objects.filter(cart=cart, product=product).first()
        if cart_item:
            quantity = int(request.POST.get("quantity", 1))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            return redirect("product_itemView_detail", id=id)


# Dashboard
def dashboard(request):
    return render(request, "Dashboard/dashboard.html")


# Dashboard > D_Content
#
#
# Add/Create
def add_product(request):
    return handle_create(
        request=request,
        model=ProductModel,
        formname=ProductForm,
        redirect_url="add_product",
        template_url="Dashboard/D_Content/add_product.html",
        action_url="add_product",
    )


def add_category(request):
    return handle_create(
        request=request,
        model=CategoryModel,
        formname=CategoryForm,
        redirect_url="add_category",
        template_url="Dashboard/D_Content/add_category.html",
        action_url="add_category",
    )


def add_sub_category(request):
    return handle_create(
        request=request,
        model=Sub_CategoryModel,
        formname=SubCategoryForm,
        redirect_url="add_sub_category",
        template_url="Dashboard/D_Content/add_sub_category.html",
        action_url="add_sub_category",
    )


def add_image_slider(request):
    return handle_create(
        request=request,
        model=image_SliderModel,
        formname=ImageSliderForm,
        redirect_url="add_image_slider",
        template_url="Dashboard/D_Content/add_image_slider.html",
        action_url="add_image_slider",
    )


def add_cart(request):
    return handle_create(
        request=request,
        model=CartModel,
        formname=CartForm,
        redirect_url="add_cart",
        template_url="Dashboard/D_Content/add_cart.html",
        action_url="add_cart",
    )


def add_cart_item(request):
    return handle_create(
        request=request,
        model=CartItemModel,
        formname=CartItemForm,
        redirect_url="add_cart_item",
        template_url="Dashboard/D_Content/add_cart_item.html",
        action_url="add_cart_item",
    )


def add_header(request):
    return handle_create(
        request=request,
        model=HeaderModel,
        formname=HeaderForm,
        redirect_url="add_header",
        template_url="Dashboard/D_Content/add_header.html",
        action_url="add_header",
    )


def add_otherdetail(request):
    return handle_create(
        request=request,
        model=OtherDetailModel,
        formname=OtherDetailForm,
        redirect_url="add_otherdetail",
        template_url="Dashboard/D_Content/add_otherdetail.html",
        action_url="add_otherdetail",
    )


def add_advertisement(request):
    return handle_create(
        request=request,
        model=AdvertisementModel,
        formname=AdvertisementForm,
        redirect_url="add_advertisement",
        template_url="Dashboard/D_Content/add_advertisement.html",
        action_url="add_advertisement",
    )


#
#
# Update
def update_product(request, id):
    return handle_update(
        request=request,
        id=id,
        model=ProductModel,
        formname=ProductForm,
        redirect_url="add_product",
        template_url="Dashboard/D_Content/add_product.html",
        action_url="update_product",
    )


def update_category(request, id):
    return handle_update(
        request=request,
        id=id,
        model=CategoryModel,
        formname=CategoryForm,
        redirect_url="add_category",
        template_url="Dashboard/D_Content/add_category.html",
        action_url="update_category",
    )


def update_sub_category(request, id):
    return handle_update(
        request=request,
        id=id,
        model=Sub_CategoryModel,
        formname=SubCategoryForm,
        redirect_url="add_sub_category",
        template_url="Dashboard/D_Content/add_sub_category.html",
        action_url="update_sub_category",
    )


def update_image_slider(request, id):
    return handle_update(
        request=request,
        id=id,
        model=image_SliderModel,
        formname=ImageSliderForm,
        redirect_url="add_image_slider",
        template_url="Dashboard/D_Content/add_image_slider.html",
        action_url="update_image_slider",
    )


def update_cart(request, id):
    return handle_update(
        request=request,
        id=id,
        model=CartModel,
        formname=CartForm,
        redirect_url="add_cart",
        template_url="Dashboard/D_Content/add_cart.html",
        action_url="update_cart",
    )


def update_cart_item(request, id):
    return handle_update(
        request=request,
        id=id,
        model=CartItemModel,
        formname=CartItemForm,
        redirect_url="add_cart_item",
        template_url="Dashboard/D_Content/add_cart_item.html",
        action_url="update_cart_item",
    )


def update_header(request, id):
    return handle_update(
        request=request,
        id=id,
        model=HeaderModel,
        formname=HeaderForm,
        redirect_url="add_header",
        template_url="Dashboard/D_Content/add_header.html",
        action_url="update_header",
    )


def update_otherdetail(request, id):
    return handle_update(
        request=request,
        id=id,
        model=OtherDetailModel,
        formname=OtherDetailForm,
        redirect_url="add_otherdetail",
        template_url="Dashboard/D_Content/add_otherdetail.html",
        action_url="update_otherdetail",
    )


def update_advertisement(request, id):
    return handle_update(
        request=request,
        id=id,
        model=AdvertisementModel,
        formname=AdvertisementForm,
        redirect_url="add_advertisement",
        template_url="Dashboard/D_Content/add_advertisement.html",
        action_url="update_advertisement",
    )


# delete functions
def del_product(request, id):
    return handle_delete(
        request=request,
        id=id,
        model=ProductModel,
        redirect_url="add_product",
        success_msg="Deleted Successfully :)",
    )


def del_category(request, id):
    return handle_delete(
        request=request,
        id=id,
        model=CategoryModel,
        redirect_url="add_category",
        success_msg="Category Deleted Successfully :)",
    )


def del_sub_category(request, id):
    return handle_delete(
        request=request,
        id=id,
        model=Sub_CategoryModel,
        redirect_url="add_sub_category",
        success_msg="Sub Category Deleted Successfully :)",
    )


def del_image_slider(request, id):
    return handle_delete(
        request=request,
        id=id,
        model=image_SliderModel,
        redirect_url="add_image_slider",
        success_msg="Image Slider Deleted Successfully :)",
    )


def del_cart(request, id):
    return handle_delete(
        request=request,
        id=id,
        model=CartModel,
        redirect_url="add_cart",
        success_msg="Cart Deleted Successfully :)",
    )


def del_cart_item(request, id):
    return handle_delete(
        request=request,
        id=id,
        model=CartItemModel,
        redirect_url="add_cart_item",
        success_msg="Cart Item Deleted Successfully :)",
    )


def del_header(request, id):
    return handle_delete(
        request=request,
        id=id,
        model=HeaderModel,  # Assuming the model name is `HeaderModel`
        redirect_url="add_header",
        success_msg="Header Deleted Successfully :)",
    )


def del_otherdetail(request, id):
    return handle_delete(
        request=request,
        id=id,
        model=OtherDetailModel,
        redirect_url="add_otherdetail",
        success_msg="Other Detail Deleted Successfully :)",
    )


def del_advertisement(request, id):
    return handle_delete(
        request=request,
        id=id,
        model=AdvertisementModel,
        redirect_url="add_advertisement",
        success_msg="Advertisement Deleted Successfully :)",
    )
