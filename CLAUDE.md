# Claude Code Implementation Guide

## Project Overview

**Phase I Console Todo Application** - A lightweight, terminal-based task management system.

## How to Run

```bash
# Method 1: Using Python module
uv run python -m todo_app.main

# Method 2: Using installed script
uv run todo-app

# Method 3: Direct Python (after activating venv)
python -m todo_app.main
```

## Project Structure

```
todo_app/
├── __init__.py       # Package initialization
├── models.py         # Task dataclass with validation
├── manager.py        # TaskManager service (business logic)
├── cli.py            # CLI interface with menu system
└── main.py           # Application entry point
```

## Architecture

### 3-Layer Design

```
CLI Layer (cli.py + main.py)
    ↓ calls methods
TaskManager Layer (manager.py)
    ↓ manages collection
Data Layer (models.py)
```

### Key Components

**1. Task (models.py)**
- Dataclass with id, description, completed, created_at
- Validation: non-empty, ≤500 chars, whitespace stripped
- Display format: `[id] [status] description`

**2. TaskManager (manager.py)**
- `add_task(description)` → creates task with auto ID
- `get_all_tasks()` → returns all tasks in creation order
- `get_task_by_id(id)` → finds task by ID
- `update_task(id, description)` → updates description
- `mark_complete(id)` → marks task complete (idempotent)
- `delete_task(id)` → removes task from list

**3. CLI (cli.py)**
- Interactive menu with 6 options
- Input validation and error handling
- ANSI color support (graceful fallback)
- User-friendly error messages

## Features

✅ **Add Task**: Create tasks with descriptions (1-500 chars)
✅ **View Tasks**: Display all with IDs and status `[ ]` or `[X]`
✅ **Update Task**: Modify task descriptions
✅ **Mark Complete**: Toggle completion status
✅ **Delete Task**: Remove tasks from list
✅ **Exit**: Clean termination

## Technical Details

**Language**: Python 3.11+ (tested on 3.14)
**Package Manager**: uv
**Dependencies**: Python standard library only
**Storage**: In-memory (no persistence)
**Testing**: Manual testing (Phase I)

## Development Commands

```bash
# Install in development mode
uv pip install -e .

# Run application
uv run python -m todo_app.main

# Test Task model
uv run python -c "from todo_app.models import Task; print(Task(1, 'Test', False, 1))"

# Test TaskManager
uv run python -c "from todo_app.manager import TaskManager; m = TaskManager(); t = m.add_task('Test'); print(t)"
```

## Error Handling

- Empty descriptions → "Task description cannot be empty"
- >500 chars → "Task description cannot exceed 500 characters"
- Invalid task ID → "Task #X not found"
- Invalid menu choice → "Invalid choice. Please enter 1-6"
- Non-integer ID → "Task ID must be a number"

## Forward Compatibility (Phase II+)

- **Phase II**: TaskManager → FastAPI endpoints
- **Phase II**: Task dataclass → SQLModel (add `table=True`)
- **Phase III**: Natural language → TaskManager calls
- **Phase IV/V**: Horizontal scaling with external DB

## Limitations (Phase I)

- ❌ No persistence (data lost on exit)
- ❌ No database (in-memory only)
- ❌ Single session (no multi-user)
- ❌ No authentication
- ❌ No advanced features (priorities, due dates, tags)

## Constitution Compliance

✅ **Spec-Driven**: All code generated from specifications
✅ **Clean Architecture**: Separation of concerns (CLI/Manager/Models)
✅ **Quality**: Type hints, docstrings, validation
✅ **Forward-Compatible**: Designed for Phase II migration

## Manual Testing Checklist

### Add Task
- [X] Add valid task → Success
- [X] Empty description → Error
- [X] >500 chars → Error

### View Tasks
- [X] Empty list → "No tasks found"
- [X] Multiple tasks → All displayed
- [X] Status indicators → `[ ]` and `[X]` correct

### Update Task
- [X] Update existing → Success
- [X] Invalid ID → Error
- [X] Empty description → Error

### Mark Complete
- [X] Mark incomplete → Success
- [X] Mark again → Idempotent (no error)
- [X] Invalid ID → Error

### Delete Task
- [X] Delete existing → Success
- [X] Invalid ID → Error
- [X] View after delete → Task gone

## Performance

- Menu operations: <100ms
- CRUD operations: <1 second
- View tasks: <2 seconds (up to 1000 tasks)

## Implementation Status

**✅ Phase 1**: Setup complete
**✅ Phase 2**: Task model complete
**✅ Phase 3**: Add task complete
**✅ Phase 4**: View tasks complete
**✅ Phase 5**: Mark complete complete
**✅ Phase 6**: Update task complete
**✅ Phase 7**: Delete task complete
**✅ Phase 8**: CLI integration complete
**✅ Phase 9**: Error handling complete
**✅ Phase 10**: ANSI colors complete
**✅ Phase 11**: Documentation complete

## Success Criteria Met

✅ SC-001: Task operations <5 seconds
✅ SC-002: View tasks <2 seconds
✅ SC-003: 100% error messages displayed
✅ SC-004: Full lifecycle <30 seconds
✅ SC-005: Data integrity maintained
✅ SC-006: Handles 100+ tasks
✅ SC-007: All confirmations displayed

**Phase I Complete!** 🎉
