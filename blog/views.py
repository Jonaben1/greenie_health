from django.views.generic import ListView, DetailView
from .models import Post
from .forms import CommentForm, ContactForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page, cache_control
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property


class BlogList(ListView):
    template_name = 'home.html'
    paginate_by = 2

#    @cached_property
    def get_queryset(self):
        # get the base queryset
        queryset = Post.objects.filter(status=1).order_by('-created_on').select_related('author')
        # filter by category if provided
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(categories__name=category)
        # filter by date if provided
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(created_on__date=date)
        return queryset

    def get(self, request, *args, **kwargs):
        # check if the request is an AJAX request
        if is_ajax(request):
            # get the list of posts as a queryset
            posts = self.get_queryset()
            # convert the queryset into a list of dictionaries
            data = list(posts.values('title', 'image_url', 'detail_url'))
            # return a JSON response with the data
            return JsonResponse(data, safe=False)
        else:
            # otherwise, use the default get method of the ListView class
            return super().get(request, *args, **kwargs)


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



