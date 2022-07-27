from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post, Comment, Category
from .forms import CommentForm

def detail(request, slug,  category_slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    if request.method == 'POST':
        form_comment = CommentForm(request.POST)

        if form_comment.is_valid():
            comment = form_comment.save(commit=False)
            # check if ForeignKey is same
            comment.post = post
            comment.save()

            return redirect('post_detail', slug=slug)
    else:
        form_comment = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form_comment':form_comment})


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)
    return render(request, 'blog/category.html', {'category': category,'posts':posts})


def search(request):
    query= request.GET.get('query', '')
    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    return render(request, 'blog/search.html', {'posts':posts, 'query':query})
