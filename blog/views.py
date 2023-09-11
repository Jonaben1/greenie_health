from django.views.generic import ListView, DetailView
from .models import Post
from .forms import CommentForm, ContactForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page, cache_control
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property


class BlogList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on').select_related('author')
    template_name = 'home.html'
    paginate_by = 2


def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

#@cache_page(60 * 15)
def blog_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related('author'), slug=slug)
    comments = post.comments.filter(active=True)
    new_comments = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'new_comments': new_comments,
        'comment_form': comment_form
    }
    return render(request, 'blog_detail.html', context)





def CreateBlogPost(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('New blog successfully added!')
    else:
        form = BlogForm()
        context = {
            'form': form
        }
    return render(request, 'create_blog.html', context)


def about(request):
    return render(request, 'about.html')



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})



