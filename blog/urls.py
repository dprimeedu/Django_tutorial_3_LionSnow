from django.urls import path
from . import views

app_name='blog'
urlpatterns = [
    path('category/', views.category_list, name='category_list'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/<int:category_id>', views.category_post_list, name='category_post_list'), 
    
    path("", views.index, name='index'), 
    path('post/<int:post_id>', views.post_detail, name='post_detail'), 
    path('post/write/<int:category_id>/', views.post_write, name='post_write'), 
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete', views.post_delete, name='post_delete'),
    path('search/', views.search, name='search'),
    path('search/autocomplete/', views.search_autocomplete,name='search_autocomplete'),
]