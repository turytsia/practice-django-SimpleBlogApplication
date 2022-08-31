from django.urls import path
from . import views

urlpatterns = [
    path('', views.Feed.as_view(), name='feed'),
    path('blogs/', views.BlogList.as_view(), name='blog-list'),
    path('blogs/favourites',views.BlogFavourites.as_view(),name = "favourites"),
    path('blogs/<slug:slug>', views.Blog.as_view(), name='blog')
]
