from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project, Task


class ProjectAPITestCase(TestCase):
    def setUp(self):
        """Setup test client & create task user"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_create_project(self):
        """Test creating a new project"""
        data = {
            'name': 'Test Project',
            'description': 'Test Description'
        }
        
        response = self.client.post('/api/projects/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().name, 'Test Project') # type: ignore
        
        
    def test_list_projects(self):
        """Test listing projects"""
        
        Project.objects.create(
            name='Project 1',
            created_by=self.user
        )
        
        Project.objects.create(
            name='Project 2',
            created_by=self.user
        )
        
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2) # type: ignore
        
    def test_user_can_only_see_own_projects(self):
        """Test users can't see others projects"""
        
        other_user = User.objects.create(username="otheruser", password='otherpass123')
        Project.objects.create(name='other project', created_by=other_user)
        Project.objects.create(name='my project', created_by=self.user)
        
        response = self.client.get('/api/projects/')
        self.assertEqual(len(response.data['results']), 1) # type: ignore
        self.assertEqual(response.data['results'][0]['name'], 'my project') # type: ignore
        
    
class TaskAPITestCase(TestCase):
    def setUp(self):
        """Setup API client & create user"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            name='test project',
            created_by=self.user
        )
    
    
    def test_create_task(self):
        """Test creating a task"""
        data = {
            'title': 'test task',
            'project_id': self.project.id, # type: ignore
            'status': 'todo'            
        }
        
        response = self.client.post('/api/tasks/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        
    def test_filter_tasks_by_status(self):
        """Test filtering tasks"""
        Task.objects.create(title='Task 1', project=self.project, status='todo')
        Task.objects.create(title='Task 2', project=self.project, status='done')
        
        response = self.client.get('/api/tasks/?status=done')
        self.assertEqual(len(response.data['results']), 1) # type: ignore
        self.assertEqual(response.data['results'][0]['title'], 'Task 2') # type: ignore