# API Documentation

Complete reference for the Task Management REST API.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. For production, implement JWT or API keys.

## Response Format

All responses are in JSON format.

### Success Response
```json
{
  "id": 1,
  "title": "Task Title",
  "status": "pending",
  ...
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (successful deletion) |
| 400 | Bad Request (validation error) |
| 404 | Not Found |
| 422 | Unprocessable Entity (invalid data) |
| 500 | Internal Server Error |

---

## Endpoints

### Health Checks

#### GET /health
Basic health check.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-06T10:30:00"
}
```

#### GET /health/detailed
Detailed health check with database status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-06T10:30:00",
  "database": "connected",
  "version": "1.0.0"
}
```

---

### Tasks

#### POST /api/v1/tasks
Create a new task.

**Request Body:**
```json
{
  "title": "Complete documentation",
  "description": "Write API docs and README",
  "status": "pending",
  "priority": "high",
  "due_date": "2024-12-31"
}
```

**Required Fields:**
- `title` (string, 1-200 chars)

**Optional Fields:**
- `description` (string)
- `status` (enum: pending, in_progress, completed) - default: pending
- `priority` (enum: low, medium, high) - default: medium
- `due_date` (date: YYYY-MM-DD)

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Complete documentation",
  "description": "Write API docs and README",
  "status": "pending",
  "priority": "high",
  "due_date": "2024-12-31",
  "created_at": "2024-02-06T10:30:00",
  "updated_at": "2024-02-06T10:30:00"
}
```

---

#### GET /api/v1/tasks
Get all tasks with optional filtering.

**Query Parameters:**
- `skip` (int, default: 0) - Number of tasks to skip
- `limit` (int, default: 100, max: 1000) - Maximum tasks to return
- `status` (enum: pending, in_progress, completed) - Filter by status
- `priority` (enum: low, medium, high) - Filter by priority

**Examples:**
```bash
# Get all tasks
GET /api/v1/tasks

# Get high priority tasks
GET /api/v1/tasks?priority=high

# Get completed tasks
GET /api/v1/tasks?status=completed

# Pagination: skip first 10, get next 20
GET /api/v1/tasks?skip=10&limit=20

# Combined filters
GET /api/v1/tasks?status=in_progress&priority=high&limit=50
```

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Task 1",
      "description": "Description",
      "status": "pending",
      "priority": "high",
      "due_date": null,
      "created_at": "2024-02-06T10:30:00",
      "updated_at": "2024-02-06T10:30:00"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

---

#### GET /api/v1/tasks/{task_id}
Get a specific task by ID.

**Path Parameters:**
- `task_id` (int) - Task ID

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Specific Task",
  "description": "Task details",
  "status": "pending",
  "priority": "medium",
  "due_date": "2024-12-31",
  "created_at": "2024-02-06T10:30:00",
  "updated_at": "2024-02-06T10:30:00"
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Task with id 999 not found"
}
```

---

#### PUT /api/v1/tasks/{task_id}
Update a task (full update).

**Path Parameters:**
- `task_id` (int) - Task ID

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "status": "completed",
  "priority": "low",
  "due_date": "2024-12-31"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Updated description",
  "status": "completed",
  "priority": "low",
  "due_date": "2024-12-31",
  "created_at": "2024-02-06T10:30:00",
  "updated_at": "2024-02-06T11:00:00"
}
```

---

#### PATCH /api/v1/tasks/{task_id}
Partially update a task.

**Path Parameters:**
- `task_id` (int) - Task ID

**Request Body (all fields optional):**
```json
{
  "title": "New Title"
}
```

**Response (200 OK):**
Same as PUT response.

---

#### PATCH /api/v1/tasks/{task_id}/status
Update only the task status.

**Path Parameters:**
- `task_id` (int) - Task ID

**Request Body:**
```json
{
  "status": "completed"
}
```

**Allowed Values:**
- `pending`
- `in_progress`
- `completed`

**Response (200 OK):**
Full task object with updated status.

---

#### PATCH /api/v1/tasks/{task_id}/priority
Update only the task priority.

**Path Parameters:**
- `task_id` (int) - Task ID

**Request Body:**
```json
{
  "priority": "high"
}
```

**Allowed Values:**
- `low`
- `medium`
- `high`

**Response (200 OK):**
Full task object with updated priority.

---

#### DELETE /api/v1/tasks/{task_id}
Delete a task permanently.

**Path Parameters:**
- `task_id` (int) - Task ID

**Response (204 No Content):**
Empty response body.

**Error (404 Not Found):**
```json
{
  "detail": "Task with id 999 not found"
}
```

---

#### GET /api/v1/tasks/search
Search tasks by title or description.

**Query Parameters:**
- `q` (string, required) - Search query
- `skip` (int, default: 0) - Number to skip
- `limit` (int, default: 100) - Maximum to return

**Examples:**
```bash
GET /api/v1/tasks/search?q=documentation
GET /api/v1/tasks/search?q=meeting&limit=10
```

**Response (200 OK):**
Same format as GET /api/v1/tasks

---

#### GET /api/v1/tasks/statistics
Get task statistics.

**Response (200 OK):**
```json
{
  "total_tasks": 25,
  "by_status": {
    "pending": 10,
    "in_progress": 8,
    "completed": 7
  },
  "by_priority": {
    "high": 5,
    "medium": 12,
    "low": 8
  }
}
```

---

## Data Models

### Task

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | integer | Auto | - | Unique identifier |
| title | string | Yes | - | Task title (max 200) |
| description | string | No | null | Detailed description |
| status | enum | No | pending | Current status |
| priority | enum | No | medium | Priority level |
| due_date | date | No | null | Due date (YYYY-MM-DD) |
| created_at | datetime | Auto | now | Creation timestamp |
| updated_at | datetime | Auto | now | Last update timestamp |

### Enums

**TaskStatus:**
- `pending`
- `in_progress`
- `completed`

**TaskPriority:**
- `low`
- `medium`
- `high`

---

## Error Handling

### Validation Errors (422)
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Not Found (404)
```json
{
  "detail": "Task with id 123 not found"
}
```

### Bad Request (400)
```json
{
  "detail": "Invalid request parameters"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production:
- Implement rate limiting middleware
- Suggested: 100 requests per minute per IP

---

## Pagination

For endpoints returning lists:
- Default page size: 100
- Maximum page size: 1000
- Use `skip` and `limit` parameters

**Example:**
```bash
# Page 1 (first 20)
GET /api/v1/tasks?skip=0&limit=20

# Page 2 (next 20)
GET /api/v1/tasks?skip=20&limit=20

# Page 3 (next 20)
GET /api/v1/tasks?skip=40&limit=20
```

---

## Best Practices

1. **Always check the response status code**
2. **Handle 404 errors gracefully**
3. **Use appropriate HTTP methods** (POST for create, PUT/PATCH for update)
4. **Validate data client-side** before sending
5. **Use pagination** for large datasets
6. **Filter** when possible to reduce payload size

---

## Examples with cURL

### Create a task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review pull request",
    "priority": "high",
    "status": "pending"
  }'
```

### Get all pending tasks
```bash
curl "http://localhost:8000/api/v1/tasks?status=pending"
```

### Update task to completed
```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete a task
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1"
```

### Search for tasks
```bash
curl "http://localhost:8000/api/v1/tasks/search?q=meeting"
```

---

## SDK / Client Libraries

### Python
```python
import requests

BASE_URL = "http://localhost:8000"

# Create task
response = requests.post(
    f"{BASE_URL}/api/v1/tasks",
    json={"title": "New Task", "priority": "high"}
)
task = response.json()

# Get all tasks
response = requests.get(f"{BASE_URL}/api/v1/tasks")
tasks = response.json()["tasks"]

# Update task
requests.patch(
    f"{BASE_URL}/api/v1/tasks/1/status",
    json={"status": "completed"}
)

# Delete task
requests.delete(f"{BASE_URL}/api/v1/tasks/1")
```

### JavaScript (Fetch API)
```javascript
const BASE_URL = 'http://localhost:8000';

// Create task
const response = await fetch(`${BASE_URL}/api/v1/tasks`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    title: 'New Task',
    priority: 'high'
  })
});
const task = await response.json();

// Get all tasks
const tasksResponse = await fetch(`${BASE_URL}/api/v1/tasks`);
const data = await tasksResponse.json();
const tasks = data.tasks;

// Update task status
await fetch(`${BASE_URL}/api/v1/tasks/1/status`, {
  method: 'PATCH',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({status: 'completed'})
});

// Delete task
await fetch(`${BASE_URL}/api/v1/tasks/1`, {
  method: 'DELETE'
});
```

---

For interactive documentation, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
