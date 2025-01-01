from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Comments, Projects, Tasks

from .serializer import CommentSerializer, ProjectsSerializer, TaskSerializer, UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer

# Generating JWT
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# User Registration View
class UserRegistrationView(APIView):
    def post(self, request):
        users_data = request.data
        serializer = UserRegistrationSerializer(data=users_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                'data': serializer.data,
                'message': 'User registered successfully.'
            }
            return Response(response_data, status.HTTP_201_CREATED)
        

# User Login View
class UserLoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            user_data = get_user_model().objects.filter(email=email).values().first()
            response_data = {
                'data': user_data,
                'message': 'Login successfully!',
                'tokens': token
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# User Profile View
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user = get_object_or_404(get_user_model(), id=id)
        serializer = UserProfileSerializer(user)
        response_data = {
            'data': serializer.data,
            'message': f'User profile of id {user.id} fetched successfully.'
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        user = get_object_or_404(get_user_model(), id=id)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                'data': serializer.data,
                'message': f'User profile of id {user.id} updated successfully.'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        user = get_object_or_404(get_user_model(), id=id)
        user.delete()
        response_data = {      
            'message': f'User profile of id {id} deleted successfully.'
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
    
# Project View
class ProjectView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        projects = Projects.objects.all()
        if not projects.exists():
            return Response({'message': 'No projects found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectsSerializer(projects, many=True)
        response_data = {
            'data': serializer.data,
            'message': 'All projects fetched successfully.'
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        project_data = request.data
        serializer = ProjectsSerializer(data=project_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                'data': serializer.data,
                'message': 'Project created successfully.'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
    
    
# Project Detail View
class ProjectDetailView(APIView):
    def get(self, request, id):
        project = get_object_or_404(Projects, id=id)
        serializer = ProjectsSerializer(project)
        response_data = {
            'data': serializer.data,
            'message': f'Project of id {project.id} fetched successfully.'
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        project = get_object_or_404(Projects, id=id)
        serializer = ProjectsSerializer(project, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                'data': serializer.data,
                'message': f'Project of id {project.id} updated successfully.'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        project = get_object_or_404(Projects, id=id)
        project.delete()
        response_data = {
            'message': f'Project of id {id} deleted successfully.'
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
    
# Task View
class TasksView(APIView):
    def get(self, request, project_id):
        tasks = Tasks.objects.filter(project_id=project_id)
        if not tasks.exists():
            return Response({'message': 'No tasks found.'}, status=status.HTTP_404_NOT_FOUND)

        # serialize the tasks
        serializer = TaskSerializer(tasks, many=True)
        response_data = {
            'data': serializer.data,
            'message': f'All tasks for project {project_id} fetched successfully.'
        }
        return Response(response_data, status=status.HTTP_200_OK)


    def post(self, request, project_id):
        # Check if project exists
        if not Projects.objects.filter(id=project_id).exists():
            return Response({'message': f'Project {project_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        task_data = request.data
        task_data['project'] = project_id
        serializer = TaskSerializer(data=task_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                'data': serializer.data,
                'message': f'Task created successfully for project {project_id}.'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
# Get task by id
class TaskDetailView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Tasks, id=task_id)
        serializer = TaskSerializer(task)
        response_data = {
            'data': serializer.data,
            'message': f'Task of id {task_id} fetched successfully.'
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def patch(self, request, task_id):
        task = get_object_or_404(Tasks, id=task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                'data': serializer.data,
                'message': f'Task of id {task_id} updated successfully.'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id):
        task = get_object_or_404(Tasks, id=task_id)
        task.delete()
        response_data = {   
            'message': f'Task of id {task_id} deleted successfully.'
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        
        

# Comment View
class CommentDetailView(APIView):
    def get(self, request, task_id):

        # Ensure the task exists
        tasks = get_object_or_404(Tasks, id=task_id)
        
        # Filter comments by given task id
        comments = Comments.objects.filter(task_id=task_id)

        # check if comments exist
        if not comments.exists():
            return Response({'message': 'No comments found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # serialize and return the comments
        serializer = CommentSerializer(comments, many=True)
        response_data = {   
            'data': serializer.data,
            'message': f'All comments for task {task_id} fetched successfully.'
        }
        return Response(response_data, status=status.HTTP_200_OK)

    
    def post(self, request, task_id):
        # Check if task exists
        tasks = Tasks.objects.filter(id=task_id)
        if not tasks.exists():
            return Response({'message': f'Task {task_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        comment_data = request.data
        comment_data['task'] = task_id
        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                'data': serializer.data,
                'message': f'Comment created successfully for task {task_id}.'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
    
class UpdateCommentView(APIView):
    def patch(self, request, comment_id):
        comment = get_object_or_404(Comments, id=comment_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                'data': serializer.data,
                'message': f'Comment of id {comment_id} updated successfully.'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comments, id=comment_id)
        comment.delete()
        response_data = {   
            'message': f'Comment of id {comment_id} deleted successfully.'
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)