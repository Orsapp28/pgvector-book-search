from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list_create, name="book-list-create"),
    path("books/search/", views.semantic_search, name="book-semantic-search"),
    path(
        "books/keyword-search/",
        views.keyword_search,
        name="book-keyword-search",
    ),
]
