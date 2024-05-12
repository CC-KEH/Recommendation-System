from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="rcs_home"),
    path("home", views.rcs_home, name="rcs_home"),
    path("movies", views.rcs, name="movies"),
    path("songs", views.rcs, name="songs"),
    path("books", views.rcs, name="books"),
    path("recommend_books", views.rcs_recommend, name="recommend_books"),
    path("recommend_movies", views.rcs_recommend, name="recommend_movies"),
    path("recommend_songs", views.rcs_recommend, name="recommend_songs"),
]