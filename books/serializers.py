from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "description", "created_at"]


class BookSearchSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "distance"]
