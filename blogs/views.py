from django.http import JsonResponse
from blogs.models import Blog, category


def _serialize_posts(posts, request):
    result = []
    for post in posts:
        image_url = None
        if post.featured_image:
            image_url = request.build_absolute_uri(post.featured_image.url)

        data = {
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'short_description': post.short_description,
            'blog_body': post.blog_body,
            'status': post.status,
            'is_featured': post.is_featured,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat(),
            'category_name': post.category.category_name,
            'category_id': post.category_id,
            'author_username': post.author.username,
            'author_first_name': post.author.first_name,
            'author_last_name': post.author.last_name,
            'author_id': post.author_id,
            'featured_image': image_url,   # ← Full URL
        }
        result.append(data)
    return result



def posts_by_category(request, category_id):
    posts = Blog.objects.filter(
        status='Published', category_id=category_id
    ).select_related('category', 'author').order_by('-created_at')
    return JsonResponse({"posts": _serialize_posts(posts, request)})


def posts_by_author(request, author_id):
    posts = Blog.objects.filter(
        author_id=author_id
    ).select_related('category', 'author').order_by('-created_at')
    return JsonResponse({"posts": _serialize_posts(posts, request)})


def post_detail(request, slug):
    try:
        post = Blog.objects.select_related('category', 'author').get(slug=slug)
        data = _serialize_posts([post], request)[0]
        return JsonResponse({"post": data})
    except Blog.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
