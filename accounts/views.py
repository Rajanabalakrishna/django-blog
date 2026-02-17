import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserToken


def get_user_data(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }


@csrf_exempt
def signup(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()

    if not username or not email or not password:
        return JsonResponse({'error': 'username, email and password are required'}, status=400)

    if len(password) < 6:
        return JsonResponse({'error': 'Password must be at least 6 characters'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already taken'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already registered'}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    token = UserToken.objects.create(user=user)

    return JsonResponse({
        'message': 'Account created successfully',
        'token': str(token.token),
        'user': get_user_data(user),
    }, status=201)


@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    username = data.get('username', '')
    password = data.get('password', '')

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'error': 'Invalid username or password'}, status=401)

    token, _ = UserToken.objects.get_or_create(user=user)

    return JsonResponse({
        'message': 'Login successful',
        'token': str(token.token),
        'user': get_user_data(user),
    })


def get_profile(request):
    auth_header = request.headers.get('Authorization', '')

    if not auth_header.startswith('Token '):
        return JsonResponse({'error': 'Authorization header required'}, status=401)

    token_str = auth_header.replace('Token ', '')

    try:
        user_token = UserToken.objects.select_related('user').get(token=token_str)
    except UserToken.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    return JsonResponse({'user': get_user_data(user_token.user)})
