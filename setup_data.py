import os
import django

# 1. Initialize Django settings first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_search.settings")
django.setup()

# 2. Define the book list
sample_books = [
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "description": "A desert planet conflict involving noble houses, giant sandworms, spice harvesting, and galactic empire politics."
    },
    {
        "title": "The Martian",
        "author": "Andy Weir",
        "description": "An astronaut stranded on Mars relies on botanical science, mechanical ingenuity, and survival instincts to stay alive."
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "description": "Practical framework for improving daily routines, breaking bad behaviors, and mastering tiny incremental personal changes."
    },
    {
        "title": "Deep Work",
        "author": "Cal Newport",
        "description": "Rules for focused success in a distracted world, optimizing cognitive effort and eliminating workplace interruptions."
    },
    {
        "title": "The Hound of the Baskervilles",
        "author": "Arthur Conan Doyle",
        "description": "A gothic mystery set on the foggy moors of Devonshire featuring an elusive detective investigating a spectral hound."
    },
    {
        "title": "Murder on the Orient Express",
        "author": "Agatha Christie",
        "description": "A Belgian detective must solve an enigmatic murder aboard an opulent snowbound passenger train with twelve suspects."
    },
    {
        "title": "All Quiet on the Western Front",
        "author": "Erich Maria Remarque",
        "description": "A harrowing depiction of frontline trench warfare, soldier camaraderie, and the psychological trauma of global conflict."
    },
    {
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "description": "Exploration of evolutionary biology, cognitive revolutions, agriculture, and societal developments that shaped our species."
    },
    {
        "title": "Steve Jobs",
        "author": "Walter Isaacson",
        "description": "A detailed biography of the visionary technology pioneer who revolutionized computers, digital animation, music, and phones."
    },
    {
        "title": "Neuromancer",
        "author": "William Gibson",
        "description": "A washed-up computer hacker is hired for a perilous cyberspace heist involving artificial intelligence and multinational corporations."
    },
]


def seed_database():
    # Deferred imports: These only run AFTER django.setup() completes above
    from books.models import Book
    from books.embeddings import generate_embedding

    print("Clearing old books...")
    Book.objects.all().delete()

    print("Generating embeddings and seeding 10 books...")
    for item in sample_books:
        print(f"Embedding: {item['title']}...")
        vector = generate_embedding(item["description"])
        Book.objects.create(
            title=item["title"],
            author=item["author"],
            description=item["description"],
            embedding=vector
        )

    print("Done! Database successfully populated.")


if __name__ == "__main__":
    seed_database()
