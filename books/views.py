from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pgvector.django import CosineDistance

from .models import Book
from .serializers import BookSerializer, BookSearchSerializer
from .embeddings import generate_embedding


@api_view(["GET", "POST"])
def book_list_create(request):
    """
    GET  /api/books/ -> List all books (excluding embeddings)
    POST /api/books/ -> Create a book, generate and store embedding
    """
    if request.method == "GET":
        books = Book.objects.all().order_by("-created_at")
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()

        # Generate and save vector embedding from the book's description
        book.embedding = generate_embedding(book.description)
        book.save(update_fields=["embedding"])

        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def semantic_search(request):
    """
    GET /api/books/search/?q=<query>
    Returns the top 3 semantically closest books by cosine distance.
    """
    query = request.query_params.get("q", "").strip()
    if not query:
        return Response(
            {"error": "Query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    query_embedding = generate_embedding(query)

    results = (
        Book.objects.annotate(distance=CosineDistance(
            "embedding", query_embedding))
        .order_by("distance")[:3]
    )

    serializer = BookSearchSerializer(results, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def keyword_search(request):
    """
    GET /api/books/keyword-search/?q=<query>
    Returns the top 3 books matching title or description via ILIKE.
    """
    query = request.query_params.get("q", "").strip()
    if not query:
        return Response(
            {"error": "Query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    results = Book.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )[:3]

    serializer = BookSerializer(results, many=True)
    return Response(serializer.data)
