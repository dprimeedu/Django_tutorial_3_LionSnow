from django.shortcuts import render, redirect, get_object_or_404
from .models import ImagePost
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ImagePostForm
from django.http import JsonResponse



# 전체 이미지 갤러리 보여주기
def index(request):
    images = ImagePost.objects.all()
    context = {"images":images}
    return render(request, 'imageapp/index.html', context)

# detail
def  image_detail(request, image_id):
    image = get_object_or_404(ImagePost, pk=image_id)
    context = {'image':image, 'is_susbcribed':image.is_subscribed(request.user)}
    return render(request, 'imageapp/image_detail.html', context)
# 새 게시글
@login_required
def image_write(request):
    if request.method =="POST":
        # 전송된 데이터를 저장
        form = ImagePostForm(request.POST, request.FILES)
        if form.is_valid():
            image_post = form.save(commit=False)
            image_post.author=request.user
            image_post.save()
            return redirect('imageapp:index')
    else:
        # 폼 생성
        form = ImagePostForm()
        return render(request, 'imageapp/image_form.html', {"form":form})

# 수정
@login_required
def image_edit(request, image_id):
    image_post = get_object_or_404(ImagePost, pk=image_id)
    if request.method =="POST":
        # 전송된 데이터를 저장
        form = ImagePostForm(request.POST, request.FILES, instance=image_post)
        if form.is_valid():
            image_post = form.save(commit=False)
            image_post.author=request.user
            image_post.save()
            return redirect('imageapp:index')
    else:
        # 폼 생성        
        form = ImagePostForm(instance=image_post)
        return render(request, 'imageapp/image_form.html', {"form":form})
# 삭제
@login_required
def image_delete(request, image_id):
    image_post = get_object_or_404(ImagePost, pk=image_id)
    image_post.delete()
    return redirect('imageapp:index')


# 구독
@login_required
@require_POST
def toggle_subscription(request, image_id):
    post = ImagePost.objects.get(pk=image_id)
    user = request.user
    if post.is_subscribed(user):
        post.unsubscribe(user)
        status = "unsubscribed"
    else:
        post.unsubscribe(user)
        status = "subscribed"
    context = {
        'status':status,
        'subscriber_count':post.get_subscriber_count()
    }
    return JsonResponse(context)