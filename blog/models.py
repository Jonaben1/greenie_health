from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.utils.safestring import mark_safe
from PIL import Image

# Create your models here.


STATUS = (
    ('0', 'Draft'),
    ('1', 'Publish')
)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    author = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        db_index=True
    )
    title = models.CharField(
        max_length=255,
        unique=True
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True
    )
    body = RichTextUploadingField()
    created_on = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    last_modified = models.DateTimeField(
        auto_now=True
    )
    image = models.ImageField(upload_to='images', blank=True)
    keywords = models.TextField(max_length=300, default='Some keywords')
    description = models.TextField(max_length=300, default='Article description')
    categories = models.ManyToManyField(
        'Category', related_name='post'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS, default=0,
        db_index=True,
    )


    class Meta:
        ordering = ['-created_on']
        constraints = [
            models.CheckConstraint(
                name='status_in_choices',
                check=Q(status__in=['0','1']),
           ),
        ]

    def read_time(self):
        return round(len(self.body.split(' ')) / 200)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs=({'slug': self.slug}))

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="150" height="150">')
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'


class Comment(models.Model):
    name = models.CharField(max_length=80)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body  = models.TextField()
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment {self.content} by {self.name}'




class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name




'''# models.py
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Post(models.Model):
    # other fields
    images = ProcessedImageField(
        upload_to='images', # where to save the images
        processors=[ResizeToFill(300, 300)], # resize the images to 300x300 pixels
        format='JPEG', # save the images as JPEG format
        options={'quality': 60}, # adjust the quality as needed
    )
'''
