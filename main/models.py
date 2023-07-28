from django.db import models
from account.models import User
from django.urls import reverse
from django.db.models import Q
from extentions.utils import jalali_converter
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
import readtime
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
# from django.utils.text import slugify
from django.template.defaultfilters import slugify
from django_ckeditor_5.fields import CKEditor5Field



class Manager(models.Manager):
    def get_post_by_category(self, category_slug):
        return self.get_queryset().filter(categories__category_slug__iexact=category_slug, status=True)

    def get_post_by_search(self, query):
        TD = Q(title__icontains=query) | Q(description__icontains=query)
        return self.get_queryset().filter(TD, status=True).distinct()



class IPAdress(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.ip_address



class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100,  allow_unicode=True, unique=True)
    image = models.ImageField(upload_to='ImageCategory')

    def __str__(self):
        return self.category_name


def create_slug(title): # new
    slug = slugify(title)
    qs = Post.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        slug = "%s-%s" %(slug, qs.first().id)
    return slug


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=200, verbose_name='آدرس مقاله',  allow_unicode=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now=True)
    intro_image = models.ImageField(upload_to='ImagePosts', verbose_name='بارگذاری تصویر')
    description = RichTextField(verbose_name='متن مقاله', blank=True, null=True)
    status = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, verbose_name='دسته بندی')
    likes = models.ManyToManyField(User, related_name='blog_post', null=True, blank=True)
    hits = models.ManyToManyField(IPAdress, through='PostHit', blank=True, related_query_name='hits', null=True)
    objects = Manager()
    tags = TaggableManager()
    comments = GenericRelation(Comment)

    def total_likes(self):
        return self.likes.count()

    def absolute_url_post(self):
        return reverse('main:detail', args=[self.slug, self.id])

    def absolut_url_author(self):
        return reverse('main:author', args=[self.author])

    def absolute_url_tags(self):
        return  reverse("main:post_list_tag", args=[self.slug])

    def get_abolute_url(self):
        return reverse('account:home')

    def jcreated(self):
        return jalali_converter(self.created)

    def absolute_url_tag(self):
        return reverse('main:post_by_tag', args=[self.slug, self.id])

    def readtime(self):
        results = readtime.of_text(self.description)
        return results.minutes

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = create_slug(self.title)
    #     return super().save(*args, **kwargs)



# posts in 1 month
class PostHit(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAdress, on_delete=models.CASCADE)
    created = models.DateField(auto_now=True)

