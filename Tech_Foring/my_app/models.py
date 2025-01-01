from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, user_name, email, first_name, last_name, password=None, password2=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            user_name = user_name,
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_name, email, first_name, last_name, password=None):
        user = self.create_user(
            user_name, 
            email,
            first_name,
            last_name,
            password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    user_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

class Projects(models.Model):
    project_name = models.CharField(max_length=50)
    description = models.TextField()
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

class Project_Members(models.Model):
    ROLE_CHOICES = [('admin', 'admin'), ('member', 'member')]
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='member')

    def __str__(self):
        return self.user.username


class Tasks(models.Model):
    STATUS_CHOICES = [('to_do', 'to_do'), ('in_progress', 'in_progress'), ('done', 'done')]
    PRIOTITY_CHOICES = [(('low', 'low')), ('medium', 'medium'), ('high', 'high')]
    title = models.CharField(max_length=50)
    task_desc = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_do')
    priority = models.CharField(max_length=20, choices=PRIOTITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
class Comments(models.Model):
    content = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)