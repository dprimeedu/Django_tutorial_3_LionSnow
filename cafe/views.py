from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Menu, Option
from django.urls import reverse

# Create your views here.
def index_view(request):
    return render(request, 'cafe/index.html')

def menu_list_url(request):
    menus=Menu.objects.all()
    context = {
        "menus_to_page" :menus,
        "cafe_name":"사나리아"
    }
    return render(request, 'cafe/menu_list_page.html',context)

def menu_add_url(request):
    return render(request, 'cafe/menu_add_page.html')

def add_menu_data(request):
    menu_name_from_form = request.POST['menu_name']
    menu_price_from_form = request.POST['menu_price']
    Menu.objects.create(menu_name=menu_name_from_form, menu_price=menu_price_from_form)

    return render(request, 'cafe/menu_add_page.html')

def menu_detail(request,menu_id):
    menu = Menu.objects.get(pk=menu_id)
    context = {
        "menu_to_page" : menu
    }
    return render(request, 'cafe/menu_detail.html', context)

def add_option(request,menu_id):
    menu=Menu.objects.get(pk=menu_id)
    context = {"menu":menu}
    return render(request, 'cafe/add_option.html', context)

def add_option_data(request):
    menu_id_from_form = request.POST['menu_id']
    option_name_from_form = request.POST['option_name']
    option_price_from_form = request.POST['option_price']
    menu=Menu.objects.get(pk=menu_id_from_form)
    Option.objects.create(menu=menu, option_name=option_name_from_form, option_price=option_price_from_form)
    context = {"menu":menu}
    return render(request, 'cafe/add_option.html', context)

def create(request):
    if request.method =="POST":
        menu_name=request.POST['menu_name']
        menu_price=request.POST['menu_price']
        Menu.objects.create(menu_name=menu_name, menu_price=menu_price)
        return HttpResponseRedirect(reverse('cafe:cafe_home'))
    # model = menu
    # success_url = reverse('cafe:cafe_home')
    
    elif request.method =="GET":
        return render(request, 'cafe/create.html')
    # templates_name = 'cafe/create.html'

def update(request,pk): #pk로 구분대는 대상이 있음
    if request.method =="POST":
            return HttpResponseRedirect(reverse('cafe:cafe_home'))
    # model = menu
    # success_url = reverse('cafe:cafe_home')
    
    elif request.method =="GET":          #원래내용
        menu = Menu.objects.get(pk=pk)
        context = {
             "menu_name":menu.menu_name,
             "menu_price":menu.menu_price
        }
        return render(request, 'update.html', context)

def delete(request, pk):
    menu = Menu.objects.get(pk=pk)
    menu.delete()
    return HttpResponseRedirect(reverse('cafe:menu_list_page'))