from django.db import migrations, models
import pgvector.django
from pgvector.django import VectorExtension  # 1. Must import VectorExtension


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        VectorExtension(),  # 2. MUST be the first item in this list!
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "embedding",
                    pgvector.django.VectorField(
                        blank=True, dimensions=768, null=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
