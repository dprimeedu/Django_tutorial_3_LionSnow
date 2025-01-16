from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Post
from .forms import CategoryForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
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

def search(request):
    """
    통합 검색 - 제목, 내용, 작성자, 카테고리를 검색
    """
    query = request.GET['query']
    posts = Post.objects.all()
    searched_posts = posts.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(author__username__icontains=query) |
        Q(category__name__icontains=query)
        )
    
    paginator = Paginator(searched_posts, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)


    context = {'searched_posts':searched_posts}
    return render(request,'blog/search.html', context)

def search_autocomplete(request):
    query= request.GET.get('query', '')
    # 2글자 이상 query가 전달되었을때 검색이 이루어지도록 함
    if query and len(query)>=2:
        posts = Post.objects.filter(
            Q(title__icontains=query)
        ).values_list('title', flat=True).distinct()[:5]
        # 최대 5개의 검색어를 제시함
        return JsonResponse(
            {
                'status':'success',
                'suggestions':list(posts)
            }
        )
    else:
        return JsonResponse(
            {
                'status':'error',
                'suggestions':[]
            }
        )