from django.urls import path
from . views import CommentDetailView, ProjectDetailView, ProjectView,TasksView, TaskDetailView, UpdateCommentView, UserRegistrationView, UserLoginView, UserProfileView

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='register'),
    path('users/login/', UserLoginView.as_view(), name='login'),
    path('users/<int:id>/', UserProfileView.as_view(), name='profile'),
    path('projects/', ProjectView.as_view(), name='projects'),
    path('projects/<int:id>/', ProjectDetailView.as_view(), name='project'),
    path('projects/<int:project_id>/tasks/', TasksView.as_view(), name='tasks'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:task_id>/comments/', CommentDetailView.as_view(), name='comments'),
    path('comments/<int:comment_id>/', UpdateCommentView.as_view(), name='update-comment'),
]