from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Post, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def menu(templates):
    objAsMenu = Category.objects.all()
    data = {
        'templates':[templates,'core/includes/navbar.html'],
        'objAsMenu': objAsMenu
        }
    return data

# def frontpage(request):
#     latestPost = Post.objects.filter(status=Post.ACTIVE).order_by('-id')
#     posts = Post.objects.filter(status=Post.ACTIVE)
#     template = 'core/frontpage.html'
#     mixData = menu(template)
#     getTemplates = mixData.get('templates')
#     getObjeMenu = mixData.get('objAsMenu')

#     return render(request, getTemplates , {'posts':posts, 'getObjeMenu':getObjeMenu, 'latestPost':latestPost})


def frontpage(request):
    latestPost = Post.objects.filter(status=Post.ACTIVE).order_by('-id')[:2]
    numbers_list = Post.objects.filter(status=Post.ACTIVE)
    page = request.GET.get('page', 10)
    paginator = Paginator(numbers_list, 1)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    template = 'core/frontpage.html'
    mixData = menu(template)
    getTemplates = mixData.get('templates')
    getObjeMenu = mixData.get('objAsMenu')

    return render(request, getTemplates , {'getObjeMenu':getObjeMenu, 'latestPost':latestPost, 'numbers':numbers})

def about(request):
    return render(request, 'core/about.html')

def robots_txt(request):
    text = [
        "User-Agent: *",
        "Dissalow:/admin/",
    ]

    return HttpResponse("\n".join(text), content_type="text/plain")
