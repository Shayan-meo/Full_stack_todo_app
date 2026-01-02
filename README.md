# Todo App - Phase I Console Application

A lightweight, terminal-based task management system with core CRUD functionality.

## Features

- Add tasks with descriptions (1-500 characters)
- View all tasks with completion status
- Mark tasks as complete
- Update task descriptions (with validation)
- Delete tasks
- In-memory storage (session-based)
- **No limit on number of tasks** - add as many as you need!
- Automatic task list refresh after updates
- Shows current description before updating

## Prerequisites

- Python 3.11 or higher
- uv package manager

## Installation

```bash
# Clone repository
git clone <repository-url>
cd Todo-list

# Create virtual environment and install
uv venv
uv pip install -e .
```

## Usage

```bash
# Run the application
uv run python -m todo_app.main

# Or use the installed script
todo-app
```

## Menu Options

1. **Add Task** - Create new task with description
2. **View Tasks** - Display all tasks with IDs and status
3. **Update Task** - Modify existing task description
4. **Mark Complete** - Mark task as complete
5. **Delete Task** - Remove task from list
6. **Exit** - Terminate application

## Project Structure

```
todo_app/
├── __init__.py       # Package initialization
├── models.py         # Task dataclass
├── manager.py        # TaskManager (business logic)
├── cli.py            # CLI interface
└── main.py           # Application entry point

tests/                # Test infrastructure
specs/                # Feature specifications
```

## Development

This is Phase I (Console Application) of a multi-phase project:
- Phase I: Console Todo App (current)
- Phase II: Web Application with FastAPI
- Phase III: AI Chatbot Integration
- Phase IV: Local Kubernetes Deployment
- Phase V: Cloud Deployment

## License

Educational project for Hackathon II.
