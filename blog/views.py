from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Blog, BlogType
# Create your views here.

def get_blog_list_common_date(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, 4)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    page_range = (x for x in range(int(page_num) - 3, int(page_num) + 4) if 0 < x <= paginator.num_pages)
    context = {}
    context['blogs_all_list'] = blogs_all_list
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_date_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_date_dict[blog_date] = blog_count
    context['blog_date'] = blog_date_dict
    return context
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_date(request, blogs_all_list)
    return render_to_response('blog/blog_list.html', context)
def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get('blog_%s_read' % blog_pk):
        blog.read_num += 1
        blog.save()
    context['blog_previous'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['blog_next'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    response = render_to_response('blog/blog_detail.html', context)
    response.set_cookie('blog_%s_read' % blog_pk, 'true')
    return response
def blogs_with_type(request, blog_with_type):
    blog_type = get_object_or_404(BlogType, pk=blog_with_type)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_date(request, blogs_all_list)
    # 这是type类型
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html', context)
def blogs_with_date(request, year, month):

    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_date(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render_to_response('blog/blogs_date.html', context)