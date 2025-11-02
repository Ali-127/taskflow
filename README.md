# Taskflow API 🚀

A professional REST API for project and task management built with Django REST Framework and PostgreSQL. Features JWT authentication, advanced filtering, auto-generated API documentation, and comprehensive test coverage.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0+-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14+-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)

## 🎯 Features

- **Authentication & Authorization**
  - JWT-based authentication with access and refresh tokens
  - User registration and login
  - Permission-based access control (users only see their own data)

- **Project Management**
  - Create, read, update, delete projects
  - Track project progress with task statistics
  - Search projects by name or description

- **Task Management**
  - Full CRUD operations on tasks
  - Task assignment to users
  - Status tracking (todo, in progress, done)
  - Priority levels (low, medium, high)
  - Due date management
  - Link tasks to projects

- **Advanced Features**
  - Filtering by status, priority, project, and assigned user
  - Full-text search across tasks and projects
  - Pagination for efficient data loading
  - Ordering/sorting capabilities
  - Optimized database queries (N+1 prevention)
  - Input validation and error handling

- **API Documentation**
  - Auto-generated interactive Swagger UI
  - ReDoc documentation
  - OpenAPI 3.0 schema

## 🛠️ Tech Stack

**Backend Framework:**
- Django 5.0+
- Django REST Framework 3.14+

**Database:**
- PostgreSQL 14+

**Authentication:**
- djangorestframework-simplejwt (JWT tokens)

**API Documentation:**
- drf-spectacular (OpenAPI/Swagger)

**Filtering & Search:**
- django-filter

**Environment Management:**
- python-decouple

## 📋 Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- pip (Python package manager)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Ali-127/taskflow.git
cd taskflow
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here-generate-a-strong-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=taskflow_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

**Generate a secure SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Create PostgreSQL Database
```bash
# Using psql
psql -U postgres
CREATE DATABASE taskflow_db;
\q

# Or using createdb command
createdb -U postgres taskflow_db
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI (Interactive):** http://localhost:8000/api/docs/
- **ReDoc (Clean Docs):** http://localhost:8000/api/redoc/
- **Admin Panel:** http://localhost:8000/admin/

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register/` | Register new user | No |
| POST | `/api/token/` | Login (get JWT tokens) | No |
| POST | `/api/token/refresh/` | Refresh access token | No |

### Projects

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/projects/` | List all user's projects | Yes |
| POST | `/api/projects/` | Create new project | Yes |
| GET | `/api/projects/{id}/` | Get project details | Yes |
| PUT | `/api/projects/{id}/` | Update project (full) | Yes |
| PATCH | `/api/projects/{id}/` | Update project (partial) | Yes |
| DELETE | `/api/projects/{id}/` | Delete project | Yes |

### Tasks

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks/` | List all tasks | Yes |
| POST | `/api/tasks/` | Create new task | Yes |
| GET | `/api/tasks/{id}/` | Get task details | Yes |
| PUT | `/api/tasks/{id}/` | Update task (full) | Yes |
| PATCH | `/api/tasks/{id}/` | Update task (partial) | Yes |
| DELETE | `/api/tasks/{id}/` | Delete task | Yes |

## 📖 Usage Examples

### 1. Register a New User
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe"
}
```

### 2. Login (Get JWT Tokens)
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Note:** Use the `access` token in subsequent requests.

### 3. Create a Project
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Website Redesign",
    "description": "Complete redesign of company website"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Website Redesign",
  "description": "Complete redesign of company website",
  "created_by": {
    "id": 1,
    "username": "john_doe"
  },
  "task_count": 0,
  "completed_tasks": 0,
  "created_at": "2024-11-02T10:30:00Z",
  "updated_at": "2024-11-02T10:30:00Z"
}
```

### 4. Create a Task
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Design homepage mockup",
    "description": "Create initial design concepts",
    "project": 1,
    "status": "todo",
    "priority": "high",
    "due_date": "2024-12-15"
  }'
```

### 5. Filter and Search

**Get all completed tasks:**
```bash
GET /api/tasks/?status=done
```

**Get high priority tasks:**
```bash
GET /api/tasks/?priority=high
```

**Search tasks by title:**
```bash
GET /api/tasks/?search=homepage
```

**Get tasks for specific project:**
```bash
GET /api/tasks/?project=1
```

**Combine filters:**
```bash
GET /api/tasks/?status=in_progress&priority=high&ordering=-due_date
```

**Pagination:**
```bash
GET /api/tasks/?page=2
GET /api/tasks/?page=2&page_size=20
```

## 🏗️ Project Structure
```
taskflow/
├── taskflow/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── api/                     # API application
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py            # Django admin configuration
│   ├── models.py           # Data models (Project, Task)
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API views and viewsets
│   ├── urls.py             # API URL routing
│   ├── permissions.py      # Custom permissions (if any)
│   └── tests.py            # Unit tests
├── .env                    # Environment variables (not in git)
├── .env.example            # Example environment file
├── .gitignore             # Git ignore rules
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🧪 Running Tests

Run all tests:
```bash
python manage.py test
```

Run specific test class:
```bash
python manage.py test api.tests.ProjectAPITestCase
```

Run with verbose output:
```bash
python manage.py test -v 2
```

Run with coverage (if installed):
```bash
coverage run --source='.' manage.py test
coverage report
```

## 🔒 Security Features

- **JWT Authentication:** Secure token-based authentication
- **Password Hashing:** Passwords stored using Django's built-in hashing
- **Permission Classes:** Users can only access their own data
- **Input Validation:** Comprehensive validation on all inputs
- **SQL Injection Prevention:** ORM-based queries prevent SQL injection
- **CORS Ready:** Easy to configure for frontend applications

## ⚡ Performance Optimizations

- **Query Optimization:** Uses `select_related()` and `prefetch_related()` to prevent N+1 queries
- **Pagination:** Default 10 items per page to reduce payload size
- **Database Indexing:** Proper indexes on foreign keys and frequently queried fields
- **Efficient Serialization:** Separate serializers for list and detail views

## 🚢 Deployment

### Environment Variables for Production

Update your `.env` file for production:
```env
SECRET_KEY=generate-a-new-strong-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=your_production_db
DB_USER=your_production_user
DB_PASSWORD=strong_production_password
DB_HOST=your_db_host
DB_PORT=5432
```

## 🐛 Troubleshooting

**Database connection error:**
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists: `createdb taskflow_db`

**Import errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Migration errors:**
- Delete migration files (except `__init__.py`)
- Drop and recreate database
- Run `python manage.py makemigrations` and `migrate`

**401 Unauthorized errors:**
- Check if access token is included in Authorization header
- Verify token hasn't expired (refresh if needed)
- Format: `Authorization: Bearer YOUR_ACCESS_TOKEN`

## 📝 What I Learned

Building this project helped me understand:

- **RESTful API Design:** Proper HTTP methods, status codes, and resource naming
- **Django REST Framework:** Serializers, viewsets, routers, and permissions
- **JWT Authentication:** Token-based authentication flow and security best practices
- **Database Design:** Relational database modeling, foreign keys, and query optimization
- **API Documentation:** Auto-generating documentation with OpenAPI/Swagger
- **Testing:** Writing unit tests for API endpoints
- **Environment Management:** Separating configuration from code
- **Git Workflow:** Version control, meaningful commits, and collaboration practices

## 🔮 Future Enhancements

Potential features to add:

- [ ] **Team Collaboration:** Share projects with other users
- [ ] **Task Comments:** Discussion threads on tasks
- [ ] **File Attachments:** Upload files to tasks/projects
- [ ] **Activity Log:** Track all changes and actions
- [ ] **Email Notifications:** Notify users of task assignments
- [ ] **Task Dependencies:** Link tasks that depend on each other
- [ ] **Time Tracking:** Log time spent on tasks
- [ ] **Dashboard Analytics:** Visualize project progress
- [ ] **Webhooks:** Integrate with external services
- [ ] **Mobile App:** iOS/Android clients
- [ ] **Real-time Updates:** WebSocket support for live collaboration

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Ali Mehdizadeh**

- GitHub: [@Ali-127](https://github.com/Ali-127)
- Email: alimehdizadeh127@gmail.com

## 🙏 Acknowledgments

- Built as a learning project to demonstrate REST API development skills
- Inspired by modern project management tools like Trello and Asana
- Thanks to the Django and DRF communities for excellent documentation

---

**⭐ If you found this project helpful, please consider giving it a star!**

Made with ❤️ and Django