import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer
from .permissions import IsTaskAssignee, IsAdmin  # Custom permissions

from singletons.logger_singleton import LoggerSingleton

from factories.task_factory import TaskFactory
from rest_framework import status
from factories.post_factory import PostFactory


# Retrieve all users (GET)
def get_users(request):
    try:
        users = list(User.objects.values('id', 'username', 'email', 'date_joined'))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Create a new user (POST)
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get("username")
            
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists!"}, status=400)
            
            # Create a new user with a hashed password
            user = User.objects.create_user(
                username=username, 
                email=data.get("email", ""),  # Optional email field
                password=data.get("password")  # Secure password hashing
            )
            return JsonResponse({"message": "User created successfully!", "user_id": user.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# Retrieve all posts (GET)
def get_posts(request):
    try:
        posts = list(Post.objects.values('id', 'content', 'author', 'created_at'))
        return JsonResponse(posts, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Create a new post (POST)
@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            author = User.objects.get(id=data['author'])  # Ensure the user exists
            post = Post.objects.create(content=data['content'], author=author)
            return JsonResponse({'id': post.id, 'message': 'Post created successfully'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Delete a user (DELETE)
@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Update a user (PUT)
@csrf_exempt
def update_user(request, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=user_id)
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.save()
            return JsonResponse({'message': 'User updated successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated, IsTaskAssignee]

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        self.check_object_permissions(request, task)
        return Response({"title": task.title, "description": task.description})

    
class SecureView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        return Response({"message": "Secure endpoint accessed!"})
    

# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful!"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials!"}, status=400)

# Restrict access to admins only
class AdminPostEditView(APIView):
    permission_classes = [IsAdmin]  # Ensures only admins can edit

    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)  # Check if post exists
        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post updated successfully", "post": serializer.data}, status=200)
        return Response(serializer.errors, status=400)
        
# Custom permission class to check if the user is an admin
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class PostListCreate(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# singletons logger
logger = LoggerSingleton().get_logger()


def some_view(request):
    logger.info("Processing request...")
    return Response({"message": "Request processed"})

# singletons config_manager???
logger = LoggerSingleton().get_logger()
logger.info("API initialized successfully.")


# factory
class CreateTaskView(APIView):
    def post(self, request):
        data = request.data
        try:
            task = TaskFactory.create_task(
                task_type=data['task_type'],
                title=data['title'],
                description=data.get('description', ''),
                assigned_to=data['assigned_to'],
                metadata=data.get('metadata', {})
            )
            return Response({'message': 'Task created successfully!', 'task_id': task.id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# another factory?
class CreatePostView(APIView):
    def post(self, request):
        data = request.data
        try:
            post = PostFactory.create_post(
                post_type=data['post_type'],
                title=data['title'],
                content=data.get('content', ''),
                metadata=data.get('metadata', {})
            )
            return Response({'message': 'Post created successfully!', 'post_id': post.id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
