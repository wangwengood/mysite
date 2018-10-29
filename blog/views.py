from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType
# Create your views here.

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, 4)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)

    page_range = (x for x in range(int(page_num)-3,int(page_num)+4) if 0<x<= paginator.num_pages)
    context = {}
    context['blogs_all_list'] = blogs_all_list
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html', context)
def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render_to_response('blog/blog_detail.html', context)
def blogs_with_type(request, blog_with_type):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_with_type)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_all_list, 4)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    page_range = (x for x in range(int(page_num) - 3, int(page_num) + 4) if 0 < x <= paginator.num_pages)
    context['blogs_all_list'] = blogs_all_list
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    context['blogs'] = page_of_blogs
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html', context)