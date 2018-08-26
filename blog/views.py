from django.shortcuts import render
from django.utils import timezone
from .models import Post,Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm,CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

'''def post_detail(request,pk):                                            #muchas cosas nuevas aquí copiando estructura de nuevo y mezclando con la de post_detail
    post=get_object_or_404(Post, pk=pk)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form=CommentForm()
        return render(request, 'blog/post_detail.html', {'post':post}, {'form':form})
'''

def post_detail(request,pk):                                            #muchas cosas nuevas aquí copiando estructura de nuevo y mezclando con la de post_detail
    post=get_object_or_404(Post, pk=pk)                                 # por alguna razon no me funciona hacer         comments=post.comments.order_by('created_date')
    return render(request, 'blog/post_detail.html', {'post':post})      # con                                   ....   ... {'comments':comments}   y en el post_detail {%for comment in comments%}

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def post_new(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.published_date = timezone.now()
            post.save()                                                         #accediendo a la función de la clase Post. Influye en la published_date
            return redirect('post_detail', pk=post.pk)
    else:
        form=PostForm()
        return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)          #por alguna razón el post con el save faltaba antes de que me decidiera a trackear x q faltaba la published_date tambn
            post.author = request.user               #la publishd date la quitamos de aquí para crear primeor el draft. Y lugo con la post_publish view ya nos encargamos de eso
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
