# Quick Start Guide - Task Management API

Get your Task Management API running in 5 minutes!

## 🚀 Option 1: Quick Run (Recommended)

### Prerequisites
- Python 3.8+ installed
- pip package manager

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python run.py
```

**That's it!** API is now running at http://localhost:8000

Visit http://localhost:8000/docs for interactive API documentation.

## 🐳 Option 2: Docker (Even Easier!)

### Prerequisites
- Docker installed
- Docker Compose installed

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api

# 2. Run with Docker Compose
docker-compose up
```

API is running at http://localhost:8000

## 📝 First Steps

### 1. Check API Health
```bash
curl http://localhost:8000/health
```

### 2. Create Your First Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Task",
    "description": "Learning the API",
    "priority": "high",
    "status": "pending"
  }'
```

### 3. Get All Tasks
```bash
curl http://localhost:8000/api/v1/tasks
```

### 4. Explore Interactive Docs
Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎮 Interactive Documentation

The Swagger UI allows you to:
- ✅ See all available endpoints
- ✅ Try out API calls directly in your browser
- ✅ See request/response examples
- ✅ View data models

## 🧪 Run Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📱 Common Operations

### Create a Task
```bash
POST /api/v1/tasks
{
  "title": "Complete project documentation",
  "description": "Write README and API docs",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2024-12-31"
}
```

### Get All Tasks (with filters)
```bash
GET /api/v1/tasks?status=pending&priority=high
```

### Update Task Status
```bash
PATCH /api/v1/tasks/1/status
{
  "status": "completed"
}
```

### Search Tasks
```bash
GET /api/v1/tasks/search?q=documentation
```

### Delete Task
```bash
DELETE /api/v1/tasks/1
```

## 🎯 Task Properties

| Property | Type | Required | Options |
|----------|------|----------|---------|
| title | string | Yes | Max 200 chars |
| description | string | No | Any text |
| status | enum | No | pending, in_progress, completed |
| priority | enum | No | low, medium, high |
| due_date | date | No | YYYY-MM-DD format |

## ⚙️ Configuration

Edit `.env` file (copy from `.env.example`):

```env
APP_NAME=Task Management API
DEBUG=True
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./tasks.db
```

## 🔍 Useful Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI |
| `/redoc` | GET | ReDoc documentation |
| `/api/v1/tasks` | GET | List all tasks |
| `/api/v1/tasks` | POST | Create task |
| `/api/v1/tasks/{id}` | GET | Get specific task |
| `/api/v1/tasks/{id}` | PUT | Update task |
| `/api/v1/tasks/{id}` | DELETE | Delete task |
| `/api/v1/tasks/search` | GET | Search tasks |

## 🐛 Troubleshooting

### Port Already in Use
Change port in `.env`:
```env
PORT=8001
```

### Database Issues
Delete `tasks.db` file and restart:
```bash
rm tasks.db
python run.py
```

### Import Errors
Make sure you're in the project root:
```bash
cd task-management-api
python run.py
```

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the [API Documentation](http://localhost:8000/docs)
3. Check out the code in `app/` directory
4. Run the tests with `pytest`
5. Customize for your needs!

## 🆘 Need Help?

- Check the [README.md](README.md) for comprehensive documentation
- Visit http://localhost:8000/docs for API reference
- Open an issue on GitHub

---

**Enjoy building with the Task Management API! 🎉**
