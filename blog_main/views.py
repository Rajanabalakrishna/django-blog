from django.http import JsonResponse
from blogs.models import category, Blog


def home(request):
    categories = list(category.objects.all().values(
        'id', 'category_name', 'created_at', 'updated_at'
    ))

    featured_qs = Blog.objects.filter(
        is_featured=True, status='Published'
    ).select_related('category', 'author').order_by('-created_at')[:10]

    featured_posts = []
    for post in featured_qs:
        # Build the FULL image URL using request
        image_url = None
        if post.featured_image:
            image_url = request.build_absolute_uri(post.featured_image.url)

        featured_posts.append({
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'short_description': post.short_description,
            'status': post.status,
            'is_featured': post.is_featured,
            'created_at': post.created_at.isoformat(),
            'category_name': post.category.category_name,
            'author_username': post.author.username,
            'author_id': post.author_id,
            'featured_image': image_url,   # ← Full URL, not relative
        })

    return JsonResponse({
        "categories": categories,
        "featured_posts": featured_posts,
    })
