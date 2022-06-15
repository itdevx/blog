from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from extentions.utils import jalali_converter
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import Count, Q
from django.views import View
from main.models import Post, Category
from account.models import User
from taggit.models import Tag
from datetime import datetime, timedelta
from django.core.paginator import Paginator




class HomeView(View):
    def get(self, request):
        first_post = Post.objects.filter(status=True).order_by('-id')[:1]
        other_post = Post.objects.filter(status=True).order_by('-id')[1:7]
        mega_menu = Post.objects.filter(status=True)[:4]
        category = Category.objects.all()   
        # posts_by_views = Post.objects.filter(status=True).annotate(likes_count=Count('likes')).order_by('-likes').distinct()[:5]
        posts_by_views = Post.objects.filter(status=True).annotate(count=Count('hits')).distinct()[:5]

        # posts in month
        last_month = datetime.today() - timedelta(days=7)
        post_by_hits_count = Post.objects.filter(status=True).annotate(count=Count('likes', filter=Q(posthit__created__gt=last_month))).order_by('-count', 'created')[:3]

        c = {
            'fp':first_post,
            'op':other_post,
            'lm':post_by_hits_count,
            'category':category,
            'mega_menu':mega_menu,
            'hits':posts_by_views,
            'date':jalali_converter(datetime.date(datetime.now()))
        }
        
        return render(request, 'ViewsMain/home-tech-blog.html', c)



class PostsList(View):
    def get(self, request, tag_slug=None):
        posts = Post.objects.filter(status=True)
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        last_month = datetime.today() - timedelta(days=30)
        tag = None
        if tag_slug:
            tag = Tag.objects.get(slug=tag_slug)
            posts = posts.filter(tags__in=[tag])


        c = {
            'posts':page_obj,
            'tag':tag,
            'date':jalali_converter(datetime.date(datetime.now())),
            'last_month':Post.objects.filter(status=True).annotate(count=Count('likes', filter=Q(posthit__created__gt=last_month))).order_by('-count', 'created')[:3],
            'category':Category.objects.all()
        }
        return render(request, 'ViewsMain/post-list-tags.html', c)



class DetailView(View):
    def get(self, request, slug, pk):
        # print(request.resolver_match)
        post = get_object_or_404(Post, slug=slug, id=pk, status=True)
        related_posts = Post.objects.get_queryset().filter(categories__post=post, status=True).distinct()[:4]
        category = Category.objects.all()
        posts_by_views = Post.objects.filter(status=True).order_by('hits').distinct()[:3]
        new_posts = Post.objects.filter(status=True).order_by('-id')[:3]

        # posts in month
        last_month = datetime.today() - timedelta(days=30)
        post_by_hits_count = Post.objects.filter(status=True).annotate(count=Count('likes', filter=Q(posthit__created__gt=last_month))).order_by('-count', 'created')[:3]

        ip_address = request.user.ip_address
        if ip_address not in post.hits.all():
            post.hits.add(ip_address)

        c = {
            'post':post,
            'lm':post_by_hits_count,
            'related_post':related_posts,
            'category':category,
            'hits':posts_by_views,
            'new':new_posts,
            'date':jalali_converter(datetime.date(datetime.now()))
        }

        return render(request, 'ViewsMain/post-layout-5.html', c)



@login_required(login_url='account:login')
def like_view(request, slug, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('main:detail',args=[slug,int(pk)]))



class AuthorView(View):
    def get(self, request, username):
        user = User.objects.filter(username=username)
        if not user.exists():
            raise Http404('این کاربر وجود ندارد')

        post = Post.objects.filter(author__username=username)
        author = Post.objects.get_queryset().filter(author__username=username).first()

        paginator = Paginator(post, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # posts in month
        last_month = datetime.today() - timedelta(days=30)
        post_by_hits_count = Post.objects.filter(status=True).annotate(count=Count('likes', filter=Q(posthit__created__gt=last_month))).order_by('-count', 'created')[:3]


        c = {
            'post':page_obj,
            'User':author,
            'category':Category.objects.all(),
            'date':jalali_converter(datetime.date(datetime.now())),
            'last_month':post_by_hits_count
        }
        return render(request, 'ViewsMain/author.html', c)



class AboutView(View):
    def get(self, request):
        return render(request, 'ViewsMain/about.html', {'category':Category.objects.all(),'date': jalali_converter(datetime.date(datetime.now()))})



def contact_view(request):
    context = {
        'category': Category.objects.all(),
        'date': jalali_converter(datetime.date(datetime.now()))
    }
    return render(request,'ViewsMain/contact.html',context)



def list_view(request):
    return render(request, 'ViewsMain/post-list.html')



class CategoryView(ListView):
    template_name = 'ViewsMain/post-list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['date' ] = jalali_converter(datetime.date(datetime.now()))
        # posts in month
        last_month = datetime.today() - timedelta(days=30)
        context['last_month'] = Post.objects.filter(status=True).annotate(count=Count('likes', filter=Q(posthit__created__gt=last_month))).order_by('-count', 'created')[:3]
        return context        
    
    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = Category.objects.filter(category_name__iexact=category_slug).first()
        if category is None:
            pass
        return Post.objects.get_post_by_category(category_slug)



class SearchView(ListView):
    template_name = 'ViewsMain/post-list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        last_month = datetime.today() - timedelta(days=30)
        context['last_month'] = Post.objects.filter(status=True).annotate(count=Count('likes', filter=Q(posthit__created__gt=last_month))).order_by('-count', 'created')[:3]
        context['date' ] = jalali_converter(datetime.date(datetime.now()))
        return context 
    
    def get_queryset(self):
        request = self.request
        query = request.GET.get('query')
        if query is not None:
            return Post.objects.get_post_by_search(query)
        return Post.objects.filter(status=True)



def page_not_found_view(request, exception):
    return render(request, 'ViewsMain/404.html', status=404)
