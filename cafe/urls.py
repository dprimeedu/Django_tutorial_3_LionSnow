from django.urls import path, include
from . import views
app_name="cafe"

urlpatterns = [
    path('', views.index_view, name='manager_home'),
    path('menu_list_url/', views.menu_list_url, name='menu_list_page'),
    path('menu_add_url/', views.menu_add_url, name='menu_add_page'),
    path('add_menu_data/', views.add_menu_data, name='add_menu_data'),
    path('detail/<int:menu_id>/', views.menu_detail, name='menu_detail'),
    path('add_option/<int:menu_id>/', views.add_option, name='add_option'),
    path('add_option_data/', views.add_option_data, name='add_option_data'),
    path('create/', views.create, name="menu_create"),
    path('/update/<int:pk>/', views.update, name="menu_update"),
    path('/delete/<int:pk>/', views.delete, name="menu_delete"),

]