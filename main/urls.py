from django.urls import path
from main.views import (
    HomeView,
    DetailView,
    PostsList,
    AuthorView,
    AboutView,
    like_view,
    list_view,
    contact_view,
)
from main.views import (
    CategoryView,
    SearchView,
)

app_name = 'main'


urlpatterns = [

    path('', HomeView.as_view(), name='home'),

    path('post/<slug:slug>/<int:pk>/', DetailView.as_view(), name='detail'),

    path('list/', list_view, name='list'),

    path('author/<username>/', AuthorView.as_view(), name='author'),

    path('like/<slug:slug>/<int:pk>/', like_view, name='like_post'),

    path('about-us/', AboutView.as_view(), name='about'),

    path('contact-us/', contact_view, name='contact'),

    path('post/<category_slug>/', CategoryView.as_view(), name='category'),

    path('search/', SearchView.as_view(), name='search'),

    #tag
    path('postlist/', PostsList.as_view(), name='post_list'),

    path('tags/<slug:tag_slug>/', PostsList.as_view(), name='post_list_tag'),
]
