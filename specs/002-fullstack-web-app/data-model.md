# Data Model: Full-Stack Web Application

**Feature**: 002-fullstack-web-app
**Created**: 2026-01-05
**Purpose**: Define database schema, entity relationships, and validation rules

## Overview

This data model supports a multi-user task management system with JWT-based authentication and user isolation. All data is persisted in Neon PostgreSQL database using SQLModel ORM.

## Entity Relationship Diagram

```
┌─────────────────────┐
│       User          │
├─────────────────────┤
│ id (PK)            │◄───────┐
│ email (UNIQUE)     │        │
│ hashed_password    │        │ 1
│ created_at         │        │
└─────────────────────┘        │
                               │
                               │ owns
                               │
                               │ N
                        ┌──────┴──────────┐
                        │      Task       │
                        ├─────────────────┤
                        │ id (PK)         │
                        │ description     │
                        │ completed       │
                        │ created_at      │
                        │ user_id (FK)    │
                        └─────────────────┘
```

**Relationship**: One User has many Tasks (1:N)
**Cascade Behavior**: When a User is deleted, all their Tasks should be deleted (ON DELETE CASCADE)

---

## Entity Definitions

### Entity 1: User

**Purpose**: Represents an authenticated individual who can create and manage tasks

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique identifier for the user |
| `email` | String (255) | UNIQUE, NOT NULL, Index | User's email address for login |
| `hashed_password` | String (255) | NOT NULL | Bcrypt-hashed password (never store plaintext) |
| `created_at` | DateTime | NOT NULL, Default: UTC NOW | Account creation timestamp |

**Validation Rules**:
- **VR-U001**: Email MUST be valid format (contains @, valid domain)
- **VR-U002**: Email MUST be unique across all users
- **VR-U003**: Password MUST be at least 8 characters before hashing (FR-001)
- **VR-U004**: Email MUST be case-insensitive for uniqueness check (normalize to lowercase)

**Business Rules**:
- **BR-U001**: Users cannot change their email after registration (Phase II scope)
- **BR-U002**: Password reset is NOT available in Phase II (out of scope)
- **BR-U003**: Deleted users' tasks are cascade-deleted (data cleanup)

**Indexes**:
- Primary index on `id` (automatic)
- Unique index on `email` (for fast login lookup)

**SQLModel Implementation**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    """User account with authentication credentials"""
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### Entity 2: Task

**Purpose**: Represents a single todo item owned by a user

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique identifier for the task |
| `description` | String (500) | NOT NULL, Length: 1-500 | Task description text |
| `completed` | Boolean | NOT NULL, Default: False | Completion status |
| `created_at` | DateTime | NOT NULL, Default: UTC NOW | Task creation timestamp |
| `user_id` | Integer | Foreign Key (User.id), NOT NULL, Index, ON DELETE CASCADE | Owner of the task |

**Validation Rules**:
- **VR-T001**: Description MUST NOT be empty (minimum 1 character) - (FR-012)
- **VR-T002**: Description MUST NOT exceed 500 characters - (FR-012)
- **VR-T003**: Description MUST be trimmed of leading/trailing whitespace before save
- **VR-T004**: user_id MUST reference an existing User.id (foreign key constraint)

**Business Rules**:
- **BR-T001**: Tasks are private - only the owning user can view/modify them (FR-005)
- **BR-T002**: Completed status defaults to False on creation
- **BR-T003**: Tasks are NOT soft-deleted - DELETE operation permanently removes them
- **BR-T004**: Task ordering defaults to newest-first (DESC created_at) - (research.md decision)
- **BR-T005**: No limit on number of tasks per user (database storage limits apply)

**Indexes**:
- Primary index on `id` (automatic)
- Index on `user_id` (for fast filtering by user - critical for performance)
- Composite index on `(user_id, created_at DESC)` (optional optimization for list queries)

**SQLModel Implementation**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class Task(SQLModel, table=True):
    """Todo item owned by a user"""
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field(min_length=1, max_length=500)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id", index=True)
```

---

## State Transitions

### Task Completion State Machine

```
┌──────────────┐
│  Incomplete  │
│ (completed = │
│    False)    │
└───────┬──────┘
        │
        │ PATCH /api/tasks/{id}/complete
        │ (toggle)
        ▼
┌──────────────┐
│   Complete   │
│ (completed = │
│    True)     │
└───────┬──────┘
        │
        │ PATCH /api/tasks/{id}/complete
        │ (toggle)
        │
        └──────► Back to Incomplete
```

**Valid Transitions**:
1. Incomplete → Complete (user marks task done)
2. Complete → Incomplete (user unmarks task)

**Invalid Operations**:
- Cannot transition to "In Progress" or "Archived" (not in Phase II scope)
- Cannot set completion status during creation (always starts as Incomplete)

---

## Database Constraints & Integrity

### Foreign Key Constraints

```sql
-- Task.user_id references User.id
ALTER TABLE task
ADD CONSTRAINT fk_task_user
FOREIGN KEY (user_id)
REFERENCES user(id)
ON DELETE CASCADE;  -- Delete all tasks when user is deleted
```

### Uniqueness Constraints

```sql
-- User.email must be unique (case-insensitive)
CREATE UNIQUE INDEX idx_user_email_lower
ON user (LOWER(email));
```

### Check Constraints

```sql
-- Task description must not be empty
ALTER TABLE task
ADD CONSTRAINT chk_description_not_empty
CHECK (LENGTH(TRIM(description)) > 0);

-- Task description must not exceed 500 characters
ALTER TABLE task
ADD CONSTRAINT chk_description_max_length
CHECK (LENGTH(description) <= 500);
```

---

## Migration Strategy

### Initial Schema Creation

```python
# backend/scripts/create_tables.py
from sqlmodel import SQLModel, create_engine
from app.models.user import User
from app.models.task import Task
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def create_all_tables():
    """Create all tables if they don't exist"""
    SQLModel.metadata.create_all(engine)
    print("✓ Tables created successfully")

if __name__ == "__main__":
    create_all_tables()
```

**Execution**: Run once before first application start:
```bash
cd backend
uv run python scripts/create_tables.py
```

### Sample Data (Development Only)

```python
# backend/scripts/seed_data.py
from sqlmodel import Session, create_engine
from app.models.user import User
from app.models.task import Task
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
engine = create_engine(os.getenv("DATABASE_URL"))

def seed_database():
    """Create sample users and tasks for testing"""
    with Session(engine) as session:
        # Create test user
        user = User(
            email="test@example.com",
            hashed_password=pwd_context.hash("password123")
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create sample tasks
        tasks = [
            Task(description="Buy groceries", user_id=user.id),
            Task(description="Finish hackathon project", completed=True, user_id=user.id),
            Task(description="Read documentation", user_id=user.id),
        ]
        session.add_all(tasks)
        session.commit()
        print(f"✓ Created user: {user.email} with {len(tasks)} tasks")

if __name__ == "__main__":
    seed_database()
```

---

## Data Model Validation Checklist

- [x] All entities have primary keys
- [x] Foreign key relationships defined with cascade behavior
- [x] Unique constraints applied where needed (email)
- [x] Indexes created for query performance (user_id)
- [x] Validation rules documented for all fields
- [x] Business rules defined for entity lifecycle
- [x] State transitions documented (task completion)
- [x] Migration scripts provided for schema creation
- [x] Sample data script available for development

---

## Notes

**Forward Compatibility**:
- Future phases can add fields like `task.due_date`, `task.priority`, `task.category_id` without breaking existing schema
- User table can be extended with `name`, `profile_image_url`, `preferences` in Phase III
- Schema supports adding `shared_tasks` table for collaboration features (Phase III)

**Performance Considerations**:
- Index on `task.user_id` critical for fast task listing (most common query)
- Consider adding composite index `(user_id, completed)` if filtering by status becomes common
- Neon PostgreSQL auto-scales, no manual connection pooling configuration needed for Phase II

**Security**:
- Never store plaintext passwords - always use bcrypt hashing
- Email addresses stored as-is but compared case-insensitively
- No PII beyond email - GDPR compliant for Phase II scope
