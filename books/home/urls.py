from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout", views.logout_view, name="logout"),
    path("search", views.search, name="search"),
    path("search/results", views.results_view, name="results"),
    path("search/<str:bookId>", views.book_page_view, name="book_page")
]