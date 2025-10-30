from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Project, Task
from .serializers import ProjectListSerializer, TaskSerializer, UserRegistrationSerializer, ProjectSerializer


class RegisterUserView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    
class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self): # type: ignore
        """Use different serializer for list and details"""
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self): # type: ignore
        """Users only see their own projects"""
        # query for getting projects owned by user
        queryset = Project.objects.filter(created_by=self.request.user)
        
        # optimize queryset by loading user in same query
        queryset = queryset.select_related('created_by')
        
        if self.action == 'retrive':
            # for detail view also load tasks
            queryset = queryset.prefetch_related('tasks__assigned_to')
        
        return queryset
    
    def perform_create(self, serializer):
        """Auto set created_by to current user"""
        serializer.save(created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'project', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']  # newest first
    
    
    def get_queryset(self): # type: ignore
        """Users only see tasks from their projects"""
        user_project = Project.objects.filter(created_by=self.request.user)
        
        return Task.objects.filter(
            project__in=user_project
            ).select_related(  # load project and assigned user in same query
                'project',
                'assigned_to'
            )

        
    