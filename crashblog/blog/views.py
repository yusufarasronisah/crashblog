from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post, Comment, Category
from .forms import CommentForm
from core.views import menu

def detail(request, slug,  category_slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    if request.method == 'POST':
        form_comment = CommentForm(request.POST)

        if form_comment.is_valid():
            comment = form_comment.save(commit=False)
            # check if ForeignKey is same
            comment.post = post
            comment.save()

            return redirect('post_detail', slug=slug, category_slug=category_slug)
    else:
        form_comment = CommentForm()

    template = 'blog/detail.html'
    mixData = menu(template)
    getTemplates = mixData.get('templates')
    getObjeMenu = mixData.get('objAsMenu')

    return render(request, getTemplates, {'post': post, 'form_comment':form_comment, 'getObjeMenu':getObjeMenu})


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)
    template = 'blog/category.html'
    mixData = menu(template)
    getTemplates = mixData.get('templates')
    getObjeMenu = mixData.get('objAsMenu')

    return render(request, getTemplates, {'category': category,'posts':posts, 'getObjeMenu':getObjeMenu})


def search(request):
    query= request.GET.get('query', '')
    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    return render(request, 'blog/search.html', {'posts':posts, 'query':query})





