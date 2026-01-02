# Quickstart Guide: Phase I - Console Todo Application

**Feature**: 001-phase1-todo-core
**Date**: 2026-01-02
**Purpose**: Setup, installation, and usage instructions

---

## Prerequisites

Before running the application, ensure you have:

- **Python 3.11 or higher** installed
  - Check version: `python --version` or `python3 --version`
  - Download from: https://www.python.org/downloads/

- **uv package manager** installed
  - Check if installed: `uv --version`
  - Install: `pip install uv` or `pipx install uv`
  - Documentation: https://github.com/astral-sh/uv

- **Git** installed (for cloning repository)
  - Check version: `git --version`
  - Download from: https://git-scm.com/downloads

- **UTF-8 compatible terminal** (most modern terminals)

---

## Installation

### Step 1: Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd Todo-list

# Verify you're on the correct branch
git branch --show-current
# Should show: 001-phase1-todo-core
```

### Step 2: Setup Virtual Environment

```bash
# Create virtual environment with uv
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Verify activation (prompt should show (.venv))
```

### Step 3: Install Project

```bash
# Install project in development mode
uv pip install -e .

# Verify installation
python -c "from todo_app.models import Task; print('✓ Installation successful')"
```

---

## Running the Application

### Method 1: Using Python Module

```bash
# From project root directory
python -m todo_app.main
```

### Method 2: Using uv Run

```bash
# From project root directory
uv run python -m todo_app.main
```

### Method 3: Direct Entry Point (if configured in pyproject.toml)

```bash
# If entry point is configured
todo-app
```

---

## Application Usage

### Main Menu

Upon launching, you'll see the main menu:

```
=== Todo List Manager ===
1. Add Task
2. View Tasks
3. Update Task
4. Mark Complete
5. Delete Task
6. Exit

Enter choice (1-6): _
```

### Menu Options

#### 1. Add Task

Create a new task with description.

**Steps**:
1. Enter `1` at main menu
2. Enter task description (1-500 characters)
3. Receive confirmation with task ID

**Example**:
```
Enter choice (1-6): 1
Enter task description: Buy groceries
✓ Task added successfully (ID: 1)
```

**Error Handling**:
- Empty description: "⚠ Task description cannot be empty"
- Description too long (>500 chars): "⚠ Task description cannot exceed 500 characters"

---

#### 2. View Tasks

Display all tasks with IDs, descriptions, and completion status.

**Steps**:
1. Enter `2` at main menu
2. View formatted task list

**Example (with tasks)**:
```
Enter choice (1-6): 2

Your Tasks:
[1] [ ] Buy groceries
[2] [X] Review pull request
[3] [ ] Write documentation

Legend: [ ] = Incomplete, [X] = Complete
```

**Example (empty list)**:
```
Enter choice (1-6): 2
No tasks found. Add a task to get started!
```

---

#### 3. Update Task

Modify the description of an existing task.

**Steps**:
1. Enter `3` at main menu
2. Enter task ID to update
3. Enter new description
4. Receive confirmation

**Example**:
```
Enter choice (1-6): 3
Enter task ID to update: 1
Enter new description: Buy groceries and milk
✓ Task #1 updated successfully
```

**Error Handling**:
- Task not found: "⚠ Task #42 not found"
- Empty new description: "⚠ Task description cannot be empty"

---

#### 4. Mark Complete

Mark a task as complete.

**Steps**:
1. Enter `4` at main menu
2. Enter task ID to mark complete
3. Receive confirmation

**Example**:
```
Enter choice (1-6): 4
Enter task ID to mark complete: 1
✓ Task #1 marked as complete
```

**Notes**:
- Marking an already complete task is allowed (idempotent, no error)
- Cannot mark incomplete in Phase I (one-way operation)

**Error Handling**:
- Task not found: "⚠ Task #42 not found"

---

#### 5. Delete Task

Remove a task from the list.

**Steps**:
1. Enter `5` at main menu
2. Enter task ID to delete
3. Receive confirmation

**Example**:
```
Enter choice (1-6): 5
Enter task ID to delete: 1
✓ Task #1 deleted successfully
```

**Notes**:
- Deletion is immediate (no confirmation prompt)
- Deleted tasks cannot be recovered

**Error Handling**:
- Task not found: "⚠ Task #42 not found"

---

#### 6. Exit

Terminate the application cleanly.

**Steps**:
1. Enter `6` at main menu
2. Application exits

**Example**:
```
Enter choice (1-6): 6
Goodbye!
```

**Note**: All task data is lost on exit (in-memory only, no persistence in Phase I)

---

## Common Workflows

### Workflow 1: Add and View Tasks

```bash
# Start application
python -m todo_app.main

# Add first task
> 1
> Buy groceries

# Add second task
> 1
> Review PR #456

# View all tasks
> 2
# Output:
# [1] [ ] Buy groceries
# [2] [ ] Review PR #456

# Exit
> 6
```

### Workflow 2: Complete Task Lifecycle

```bash
# Start application
python -m todo_app.main

# Add task
> 1
> Write documentation

# View task
> 2
# [1] [ ] Write documentation

# Mark complete
> 4
> 1

# View updated task
> 2
# [1] [X] Write documentation

# Delete task
> 5
> 1

# Verify deletion
> 2
# No tasks found

# Exit
> 6
```

### Workflow 3: Update Task Description

```bash
# Start application
python -m todo_app.main

# Add task with typo
> 1
> Reviw pull request

# View task
> 2
# [1] [ ] Reviw pull request

# Update to fix typo
> 3
> 1
> Review pull request

# View corrected task
> 2
# [1] [ ] Review pull request

# Exit
> 6
```

---

## Troubleshooting

### Issue: "Module not found: todo_app"

**Cause**: Project not installed or virtual environment not activated

**Solution**:
```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Reinstall project
uv pip install -e .
```

### Issue: "Python version too old"

**Cause**: Python 3.10 or earlier installed

**Solution**:
- Download and install Python 3.11+ from python.org
- Verify version: `python --version`

### Issue: "uv: command not found"

**Cause**: uv package manager not installed

**Solution**:
```bash
# Install uv
pip install uv

# Or using pipx (recommended)
pipx install uv
```

### Issue: Colors not displaying correctly

**Cause**: Terminal does not support ANSI color codes

**Solution**:
- Application automatically falls back to plain text
- Use a modern terminal (Windows Terminal, iTerm2, GNOME Terminal)

### Issue: Tasks disappear after restarting

**Expected Behavior**: Phase I stores tasks in-memory only (no persistence)

**Explanation**: This is by design for Phase I. Tasks persist only during the current session. Phase II will add database persistence.

---

## Testing Guide

### Manual Acceptance Testing

Follow these test scenarios to verify all functionality:

#### Test Suite 1: Add Task

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| TC1.1 | Add task "Buy groceries" | Success, ID assigned, confirmation shown |
| TC1.2 | Add task with empty description | Error: "Task description cannot be empty" |
| TC1.3 | Add task with whitespace only | Error: "Task description cannot be empty" |
| TC1.4 | Add task with 500 characters | Success, full description saved |
| TC1.5 | Add task with 501 characters | Error: "Task description cannot exceed 500 characters" |

#### Test Suite 2: View Tasks

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| TC2.1 | View tasks with empty list | "No tasks found" message |
| TC2.2 | Add 1 task, then view | Task displayed with ID, status, description |
| TC2.3 | Add 10 tasks, then view | All tasks displayed in creation order |
| TC2.4 | Add and complete tasks, then view | Complete tasks show [X], incomplete show [ ] |

#### Test Suite 3: Update Task

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| TC3.1 | Update existing task description | Success, confirmation shown |
| TC3.2 | Update non-existent task (ID 999) | Error: "Task #999 not found" |
| TC3.3 | Update with empty description | Error: "Task description cannot be empty" |
| TC3.4 | View task after update | New description displayed |

#### Test Suite 4: Mark Complete

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| TC4.1 | Mark incomplete task complete | Success, confirmation shown |
| TC4.2 | Mark already complete task | Success (idempotent, no error) |
| TC4.3 | Mark non-existent task (ID 999) | Error: "Task #999 not found" |
| TC4.4 | View task after marking complete | Status shows [X] |

#### Test Suite 5: Delete Task

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| TC5.1 | Delete existing task | Success, confirmation shown |
| TC5.2 | Delete non-existent task (ID 999) | Error: "Task #999 not found" |
| TC5.3 | View tasks after deletion | Deleted task not displayed |
| TC5.4 | Delete last task, then view | "No tasks found" message |

---

## Development Commands

### Run Application

```bash
python -m todo_app.main
```

### Run Tests (Phase II)

```bash
# Unit tests
pytest tests/test_models.py
pytest tests/test_manager.py

# Integration tests
pytest tests/test_cli.py

# All tests
pytest
```

### Check Code Quality

```bash
# Type checking (if mypy installed)
mypy todo_app/

# Linting (if ruff installed)
ruff check todo_app/

# Formatting (if black installed)
black todo_app/
```

---

## Project Structure Reference

```
Todo-list/
├── todo_app/              # Main application package
│   ├── __init__.py        # Package initialization
│   ├── models.py          # Task dataclass
│   ├── manager.py         # TaskManager (business logic)
│   ├── cli.py             # CLI interface
│   └── main.py            # Application entry point
├── tests/                 # Test suite (Phase II)
│   ├── test_models.py
│   ├── test_manager.py
│   └── test_cli.py
├── specs/                 # Feature specifications
│   └── 001-phase1-todo-core/
│       ├── spec.md        # Requirements
│       ├── plan.md        # Architecture
│       └── tasks.md       # Implementation tasks
├── pyproject.toml         # Project configuration
├── README.md              # Project overview
└── CLAUDE.md              # Implementation guidance
```

---

## Next Steps

After successfully running the application:

1. **Review Specification**: Read `specs/001-phase1-todo-core/spec.md` for requirements
2. **Review Plan**: Read `specs/001-phase1-todo-core/plan.md` for architecture
3. **Generate Tasks**: Run `/sp.tasks` to create implementation task list
4. **Begin Implementation**: Follow tasks.md for development workflow

---

## Support

For issues or questions:

1. Check this quickstart guide
2. Review `README.md` in project root
3. Consult `specs/001-phase1-todo-core/spec.md` for requirements
4. Review `specs/001-phase1-todo-core/plan.md` for architecture details

---

## References

- Feature Specification: `specs/001-phase1-todo-core/spec.md`
- Implementation Plan: `specs/001-phase1-todo-core/plan.md`
- Data Model: `specs/001-phase1-todo-core/data-model.md`
- Project README: `README.md`
- Constitution: `.specify/memory/constitution.md`
