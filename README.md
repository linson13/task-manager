# Task Management REST API 📋

A production-ready RESTful API for task management built with FastAPI, featuring request validation, error handling, health checks, and complete CRUD operations.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Features

- ✅ **Complete CRUD Operations** - Create, Read, Update, Delete tasks
- ✅ **RESTful Design** - Industry-standard API patterns
- ✅ **Request Validation** - Automatic validation using Pydantic models
- ✅ **Error Handling** - Comprehensive error responses with proper HTTP status codes
- ✅ **Health Checks** - Monitor API status and database connectivity
- ✅ **Modular Architecture** - Clean separation of concerns
- ✅ **SQLite Database** - Lightweight, serverless database with SQLAlchemy ORM
- ✅ **Auto-Documentation** - Interactive API docs with Swagger UI
- ✅ **Search & Filter** - Find tasks by status, priority, or text
- ✅ **Task Priorities** - Low, Medium, High priority levels
- ✅ **Status Tracking** - Pending, In Progress, Completed statuses
- ✅ **Due Dates** - Track task deadlines
- ✅ **Docker Support** - Containerized deployment ready
- ✅ **Production Ready** - CORS, logging, environment configuration

## 📁 Project Structure

```
task-management-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and settings
│   │
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── tasks.py        # Task CRUD endpoints
│   │   │   └── health.py       # Health check endpoints
│   │   └── dependencies.py     # Dependency injection
│   │
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   └── task.py            # Task model
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   └── task.py            # Request/Response schemas
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── task_service.py    # Task operations
│   │
│   ├── database/               # Database setup
│   │   ├── __init__.py
│   │   └── session.py         # Database connection
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── exceptions.py      # Custom exceptions
│
├── tests/                      # Unit and integration tests
│   ├── __init__.py
│   ├── test_tasks.py
│   └── test_health.py
│
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── pytest.ini                 # Pytest configuration
├── README.md                  # This file
└── run.py                     # Application runner
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Docker for containerized deployment

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (optional, defaults work fine)
```

5. **Run the application**
```bash
python run.py
```

The API will be available at **http://localhost:8000**

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop the container
docker-compose down
```

## 📖 API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 API Endpoints

### Health Checks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Basic health check |
| GET | `/health/detailed` | Detailed health with database status |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/tasks` | Get all tasks (with filters) |
| GET | `/api/v1/tasks/{task_id}` | Get specific task |
| POST | `/api/v1/tasks` | Create new task |
| PUT | `/api/v1/tasks/{task_id}` | Update task |
| PATCH | `/api/v1/tasks/{task_id}` | Partial update task |
| DELETE | `/api/v1/tasks/{task_id}` | Delete task |
| GET | `/api/v1/tasks/search` | Search tasks |
| PATCH | `/api/v1/tasks/{task_id}/status` | Update task status |
| PATCH | `/api/v1/tasks/{task_id}/priority` | Update task priority |

### Query Parameters (GET /api/v1/tasks)

- `status` - Filter by status (pending, in_progress, completed)
- `priority` - Filter by priority (low, medium, high)
- `skip` - Number of records to skip (pagination)
- `limit` - Maximum records to return (default: 100)

## 📝 Usage Examples

### Create a Task

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "priority": "high",
    "status": "in_progress",
    "due_date": "2024-12-31"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2024-12-31",
  "created_at": "2024-02-06T10:30:00",
  "updated_at": "2024-02-06T10:30:00"
}
```

### Get All Tasks

```bash
curl -X GET "http://localhost:8000/api/v1/tasks"
```

### Get Task by ID

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/1"
```

### Update Task

```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "status": "completed"
  }'
```

### Update Task Status

```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Search Tasks

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/search?q=documentation&status=in_progress"
```

### Delete Task

```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1"
```

### Filter Tasks

```bash
# Get high priority tasks
curl -X GET "http://localhost:8000/api/v1/tasks?priority=high"

# Get completed tasks
curl -X GET "http://localhost:8000/api/v1/tasks?status=completed"

# Pagination
curl -X GET "http://localhost:8000/api/v1/tasks?skip=10&limit=20"
```

## 🧪 Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_tasks.py -v
```

## 🏗️ Architecture

### Modular Design

The application follows a **layered architecture**:

1. **API Layer** (`app/api/routes/`) - HTTP endpoints and request handling
2. **Service Layer** (`app/services/`) - Business logic and orchestration
3. **Model Layer** (`app/models/`) - Database models and ORM
4. **Schema Layer** (`app/schemas/`) - Request/response validation

### Request Flow

```
Client Request
    ↓
API Route (Validation)
    ↓
Service Layer (Business Logic)
    ↓
Database Layer (Persistence)
    ↓
Response (Serialization)
    ↓
Client Response
```

### Error Handling

The API uses proper HTTP status codes:

- `200` - Success
- `201` - Created
- `204` - No Content (Delete)
- `400` - Bad Request (Validation error)
- `404` - Not Found
- `422` - Unprocessable Entity
- `500` - Internal Server Error

## 🔧 Configuration

Environment variables (`.env` file):

```env
# Application
APP_NAME=Task Management API
APP_VERSION=1.0.0
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=sqlite:///./tasks.db

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

## 🚢 Deployment

### Production Considerations

1. **Use PostgreSQL** instead of SQLite for production:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/taskdb
   ```

2. **Set DEBUG=False** in production

3. **Use a production ASGI server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

4. **Enable HTTPS** with reverse proxy (nginx/traefik)

5. **Set up monitoring** and logging

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-task-api

# Deploy
git push heroku main

# Open app
heroku open
```

### Deploy to Railway/Render

1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically on push

## 🛠️ Development

### Adding New Endpoints

1. Create route in `app/api/routes/`
2. Add business logic in `app/services/`
3. Update schemas in `app/schemas/`
4. Write tests in `tests/`

### Database Migrations

For production, use Alembic:

```bash
# Install Alembic
pip install alembic

# Initialize
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new field"

# Apply migration
alembic upgrade head
```

## 📊 Database Schema

**Task Table:**

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| title | String(200) | Task title (required) |
| description | Text | Task description (optional) |
| status | Enum | pending/in_progress/completed |
| priority | Enum | low/medium/high |
| due_date | Date | Due date (optional) |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
- [REST API Best Practices](https://restfulapi.net/)

---

⭐ **Star this repository if you find it helpful!**
