from datetime import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Project, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        )
    
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


# Shows in task details
class ProjectSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']
        
        
class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSummarySerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source='project',
        write_only=True,
    )
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )
    class Meta:
        model = Task
        fields = ['id', 'title', 'description',
                  'project', 'project_id',
                  'assigned_to', 'assigned_to_id',
                  'status', 'priority', 'due_date',
                  'created_at', 'updated_at',
                  ]
        read_only_fields = ['created_at', 'updated_at']
        
    def validate_title(self, value):
        """Validate Task title"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        
        return value.strip()
    
    def validate_due_date(self, value):
        """Validate due date is not in the past."""
        if value and value < timezone.now().date(): # type: ignore
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    
    def validate_project(self, value):
        """Validate user owns the project."""
        request = self.context.get('request')
        if request and value.created_by != request.user:
            raise serializers.ValidationError('You can only create tasks in your own project.')
        return value
    
    
class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()
    pending_tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description',
                  'created_by',
                  'tasks', 'task_count', 'completed_tasks', 'pending_tasks',
                  'created_at', 'updated_at',
                  ]
        
        read_only_fields = ['created_at', 'updated_at']
        
    def get_task_count(self, obj):
        """Total numbers of tasks in project"""
        return obj.tasks.count()
    
    def get_completed_tasks(self, obj):
        """Number of completed tasks"""
        return obj.tasks.filter(status='done').count()
    
    def get_pending_tasks(self, obj):
        """Number of pending tasks"""
        return obj.tasks.exclude(status='done').count()
    
    def validate_title(self, value):
        """Validate Project title"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        
        request = self.context.get('request')
        if request:
            existing = Project.objects.filter(
                created_by=request.user,
                name__iexact=value.strip()
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing.exists():
                raise serializers.ValidationError("You already have a project with this title.")
        
        return value.strip()
        
        
# Lighter Project list serializer        
class ProjectListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    task_count = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 
                  'created_by',
                  'task_count', 'completed_tasks',
                  'created_at', 'updated_at',
                  ]
        
        read_only_fields = ['created_at', 'updated_at']
        
    def get_task_count(self, obj):
        """Total numbers of tasks in project"""
        project = Project.objects.get(id=1)
        return obj.tasks.count()
    
    def get_completed_tasks(self, obj):
        """Number of completed tasks"""
        return obj.tasks.filter(status='done').count()
