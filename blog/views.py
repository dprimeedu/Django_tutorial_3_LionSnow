from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Post
from .forms import CategoryForm, PostForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    categories = Category.objects.all()
    posts = Post.objects.all()
    context = {'categories' :categories,
               'posts' :posts
               }
    return render(request, 'blog/index.html', context)

def category_list(request):
    categories = Category.objects.all()
    context = {'categories' :categories}
    return render(request, 'blog/category_list.html', context)

@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # 유효성 검증
        if form.is_valid():
            form.save()
            return redirect('blog:category_list')

    elif request.method == "GET": # form 입력하는 페이지는 표시
        categories = Category.objects.all()
        form = CategoryForm()  
    return render(request, 'blog/category_form.html', context={'form':form, 'categories':categories})

def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    posts = Post.objects.filter(category=post.category)
    categories = Category.objects.all()
    context = {'post':post,'categories' :categories, 'posts':posts}
    return render(request, 'blog/post_detail.html', context)

def category_post_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    categories = Category.objects.all()

    posts = Post.objects.filter(category=category)
    context = {'posts':posts, 'category':category, 'categories':categories}
    return render(request, 'blog/index.html', context)
@login_required
def post_write(request, category_id):
   
    if request.method == 'GET':
        category = Category.objects.get(pk=category_id)
        categories = Category.objects.all()
        form = PostForm()
        context={'form':form,'categories' :categories, 'category':category}
        return render(request=request, template_name='blog/post_form.html',context=context)
    
    else:
        form =PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            category = Category.objects.get(pk=category_id)
            post.category = category
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', post_id=post.id)
@login_required   
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'GET':
        form = PostForm(instance=post)
        context={'form':form}
        return render(request, 'blog/post_form.html', context)
    
    else:
        form =PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('blog:post_detail', post_id=post.id)

def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('blog:index')

    