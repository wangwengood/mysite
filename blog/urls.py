from django.urls import path
from . import views
urlpatterns = [
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_with_type>', views.blogs_with_type, name='blog_with_type'),
]