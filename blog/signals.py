from django.db.models.signals import post_save, post_delete
from django.urls import reverse
from django.contrib.redirects.models import Redirect
from django.dispatch import receiver
from .models import Post, Comment
from django.core.cache import cache

@receiver(post_save, sender=Post, weak=False)
def handle_post_save(sender, instance, **kwargs):
    '''This function will take two arguments: the sender (the Post model) and the instance (the post object that was saved).
    The function will check if the slug field of the post has changed, and if so, it will create a redirect object that will
    point the old URL to the new one. The function will also use the reverse function to get the URL of the post based on its slug:'''
    # Get the previous and current slug values
    prev_slug = instance._meta.get_field('slug').pre_save(instance, False)
    curr_slug = instance.slug

    # check if the slug has changed
    if prev_slug != curr_slug:
        # Get the previous and current slug values
        prev_url = reverse('post_detail', args=[prev_slug])
        curr_url = reverse('post_detail', args=[curr_slug])

        # create a redirect object
        redirect = Redirect(old_path=prev_url, new_path=curr_url)
        redirect.save()



# This way, whenever a comment is created or removed, the cache for that post’s comment section will be invalidated and regenerated on the next request

@receiver([post_save, post_delete], sender=Comment)
def clear_comment_cache(sender, instance, **kwargs):
    post = instance.post
    cache_key = f'comments-{post.pk}'
    cache.delete(cache_key)
