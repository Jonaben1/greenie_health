from .views import *
from django.urls import path
from .sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView


sitemaps = {
    'blog': PostSitemap
}



urlpatterns = [
    path('', BlogList.as_view(), name='home'),
    path('blog-list/', blog_list, name='blog_list'),
    path('<slug:slug>/', blog_detail, name='blog_detail'),
    path('ckeditor/new_post/', CreateBlogPost, name='create'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('about',  about, name='about'),
    path('contact', contact, name='contact'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]
