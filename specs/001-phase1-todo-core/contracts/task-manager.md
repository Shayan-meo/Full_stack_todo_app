# API Contract: TaskManager

**Feature**: 001-phase1-todo-core
**Date**: 2026-01-02
**Purpose**: Define TaskManager interface, methods, and behavioral contracts

---

## Overview

TaskManager provides the service layer for todo task management, encapsulating business logic, validation, and data operations. Acts as boundary between user interface (CLI) and data layer (Task models).

**Design Principles**:
- Single Responsibility: Manages task collection operations only
- Stateless (except for task collection): No side effects beyond data manipulation
- Fail-Fast: Validate inputs immediately before processing
- Idempotent where possible: Safe to repeat operations

---

## Class: TaskManager

### Purpose

Service layer providing CRUD operations and business logic for task management.

### State

```python
class TaskManager:
    _tasks: List[Task]         # In-memory task collection
    _next_id: int              # Counter for sequential ID generation
    _creation_counter: int     # Counter for created_at timestamps
```

**State Invariants**:
- `_next_id` always increments (never decrements)
- `_creation_counter` always increments (never decrements)
- All tasks in `_tasks` have unique IDs
- Task IDs are sequential and start from 1

---

## Methods

### 1. add_task

**Signature**:
```python
def add_task(self, description: str) -> Task
```

**Purpose**: Create a new task with given description and add to collection.

**Parameters**:
- `description` (str): Task description text

**Returns**:
- `Task`: Newly created task with assigned ID

**Raises**:
- `ValueError`: If description is empty or whitespace-only after stripping
- `ValueError`: If description exceeds 500 characters

**Behavior**:
1. Validate description (non-empty, ≤500 chars)
2. Strip leading/trailing whitespace from description
3. Assign next available ID from `_next_id` counter
4. Assign creation order from `_creation_counter`
5. Create Task object with completed=False
6. Append task to `_tasks` list
7. Increment `_next_id` counter
8. Increment `_creation_counter`
9. Return created task

**Side Effects**:
- Increments `_next_id`
- Increments `_creation_counter`
- Appends to `_tasks` list

**Complexity**: O(1) amortized

**Example**:
```python
manager = TaskManager()
task = manager.add_task("Buy groceries")
# task.id == 1, task.description == "Buy groceries", task.completed == False
```

**Error Examples**:
```python
manager.add_task("")           # ValueError: Task description cannot be empty
manager.add_task("   ")        # ValueError: Task description cannot be empty
manager.add_task("a" * 501)    # ValueError: Task description cannot exceed 500 characters
```

---

### 2. get_all_tasks

**Signature**:
```python
def get_all_tasks(self) -> List[Task]
```

**Purpose**: Retrieve all tasks ordered by creation time (oldest first).

**Parameters**: None

**Returns**:
- `List[Task]`: All tasks in collection, ordered by `created_at` field
- Empty list if no tasks exist

**Raises**: None

**Behavior**:
1. Return copy of `_tasks` list (or sorted by created_at if needed)
2. Preserve original order (list maintains insertion order)

**Side Effects**: None (read-only operation)

**Complexity**: O(n) where n = number of tasks

**Example**:
```python
manager = TaskManager()
manager.add_task("Task 1")
manager.add_task("Task 2")
tasks = manager.get_all_tasks()
# tasks == [Task(id=1, ...), Task(id=2, ...)]
```

**Empty List Example**:
```python
manager = TaskManager()
tasks = manager.get_all_tasks()
# tasks == []
```

---

### 3. get_task_by_id

**Signature**:
```python
def get_task_by_id(self, task_id: int) -> Task | None
```

**Purpose**: Find and return task with specified ID.

**Parameters**:
- `task_id` (int): Task identifier to search for

**Returns**:
- `Task`: Task object if found
- `None`: If no task with given ID exists

**Raises**: None

**Behavior**:
1. Search `_tasks` list for task with matching ID
2. Return task if found, otherwise return None

**Side Effects**: None (read-only operation)

**Complexity**: O(n) linear search where n = number of tasks

**Example**:
```python
manager = TaskManager()
task = manager.add_task("Task 1")  # task.id == 1
found = manager.get_task_by_id(1)
# found == task

not_found = manager.get_task_by_id(999)
# not_found == None
```

---

### 4. update_task

**Signature**:
```python
def update_task(self, task_id: int, description: str) -> Task
```

**Purpose**: Update description of existing task.

**Parameters**:
- `task_id` (int): ID of task to update
- `description` (str): New task description

**Returns**:
- `Task`: Updated task object

**Raises**:
- `ValueError`: If task with given ID not found
- `ValueError`: If new description is empty or whitespace-only
- `ValueError`: If new description exceeds 500 characters

**Behavior**:
1. Find task by ID
2. If not found, raise ValueError with "Task #{task_id} not found"
3. Validate new description (same rules as add_task)
4. Strip whitespace from new description
5. Update task.description in-place
6. Return updated task

**Side Effects**:
- Modifies task description in `_tasks` list

**Complexity**: O(n) for search + O(1) for update

**Example**:
```python
manager = TaskManager()
task = manager.add_task("Old description")
updated = manager.update_task(task.id, "New description")
# updated.description == "New description"
```

**Error Examples**:
```python
manager.update_task(999, "New")      # ValueError: Task #999 not found
manager.update_task(1, "")           # ValueError: Task description cannot be empty
manager.update_task(1, "a" * 501)    # ValueError: Task description cannot exceed 500 characters
```

---

### 5. mark_complete

**Signature**:
```python
def mark_complete(self, task_id: int) -> Task
```

**Purpose**: Mark task as complete by setting completed flag to True.

**Parameters**:
- `task_id` (int): ID of task to mark complete

**Returns**:
- `Task`: Task object with completed=True

**Raises**:
- `ValueError`: If task with given ID not found

**Behavior**:
1. Find task by ID
2. If not found, raise ValueError with "Task #{task_id} not found"
3. Set task.completed = True
4. Return task (idempotent - no error if already complete)

**Side Effects**:
- Modifies task.completed in `_tasks` list

**Complexity**: O(n) for search + O(1) for update

**Idempotency**: Marking an already complete task is allowed and returns success

**Example**:
```python
manager = TaskManager()
task = manager.add_task("Task 1")  # task.completed == False
completed = manager.mark_complete(task.id)
# completed.completed == True

# Idempotent - can mark complete again
completed_again = manager.mark_complete(task.id)
# completed_again.completed == True (no error)
```

**Error Example**:
```python
manager.mark_complete(999)  # ValueError: Task #999 not found
```

**Phase I Limitation**: Cannot mark task as incomplete (no toggle). One-way operation: incomplete → complete only.

---

### 6. delete_task

**Signature**:
```python
def delete_task(self, task_id: int) -> bool
```

**Purpose**: Remove task from collection by ID.

**Parameters**:
- `task_id` (int): ID of task to delete

**Returns**:
- `bool`: True if task was found and deleted, False if not found

**Raises**: None

**Behavior**:
1. Find task by ID
2. If found:
   - Remove task from `_tasks` list
   - Return True
3. If not found:
   - Return False (no error)

**Side Effects**:
- Removes task from `_tasks` list if found

**Complexity**: O(n) for search + O(n) for list removal

**Example**:
```python
manager = TaskManager()
task = manager.add_task("Task 1")
deleted = manager.delete_task(task.id)
# deleted == True

deleted_again = manager.delete_task(task.id)
# deleted_again == False (already deleted)

not_found = manager.delete_task(999)
# not_found == False
```

**Note**: Unlike update/mark_complete, delete returns False instead of raising exception for not found.

---

## Error Handling Summary

| Operation | Condition | Response |
|-----------|-----------|----------|
| add_task | Empty description | ValueError: "Task description cannot be empty" |
| add_task | Description > 500 chars | ValueError: "Task description cannot exceed 500 characters" |
| update_task | Task not found | ValueError: "Task #{id} not found" |
| update_task | Empty description | ValueError: "Task description cannot be empty" |
| update_task | Description > 500 chars | ValueError: "Task description cannot exceed 500 characters" |
| mark_complete | Task not found | ValueError: "Task #{id} not found" |
| mark_complete | Already complete | Success (idempotent, no error) |
| delete_task | Task not found | Return False (no error) |
| get_task_by_id | Task not found | Return None (no error) |
| get_all_tasks | Empty list | Return [] (no error) |

---

## Thread Safety

**Phase I**: Not thread-safe (single-user, single-session application)

**Assumptions**:
- Single CLI process
- No concurrent access
- No need for locks or synchronization

**Phase II+**: Will require thread safety for web server (multiple concurrent requests)

---

## Performance Guarantees

| Method | Complexity | Notes |
|--------|-----------|-------|
| add_task | O(1) amortized | List append operation |
| get_all_tasks | O(n) | Must iterate all tasks |
| get_task_by_id | O(n) | Linear search (no index) |
| update_task | O(n) | Linear search + O(1) update |
| mark_complete | O(n) | Linear search + O(1) update |
| delete_task | O(n) | Linear search + O(n) removal |

**Scale Assumptions**: n < 1000 tasks (Phase I specification limit)

**Optimization Opportunities** (Phase II):
- Replace list with dict for O(1) ID lookup
- Use database index for O(1) primary key lookup

---

## Usage Example

```python
from todo_app.manager import TaskManager

# Initialize manager
manager = TaskManager()

# Add tasks
task1 = manager.add_task("Buy groceries")
task2 = manager.add_task("Review PR #456")
task3 = manager.add_task("Write documentation")

# View all tasks
all_tasks = manager.get_all_tasks()
for task in all_tasks:
    print(f"[{task.id}] {'[X]' if task.completed else '[ ]'} {task.description}")
# Output:
# [1] [ ] Buy groceries
# [2] [ ] Review PR #456
# [3] [ ] Write documentation

# Mark task complete
manager.mark_complete(1)

# Update task description
manager.update_task(2, "Review PR #456 - authentication module")

# Get specific task
task = manager.get_task_by_id(1)
print(task.completed)  # True

# Delete task
success = manager.delete_task(3)
print(success)  # True

# View final state
final_tasks = manager.get_all_tasks()
# [1] [X] Buy groceries
# [2] [ ] Review PR #456 - authentication module
```

---

## Phase II Migration: FastAPI Endpoints

TaskManager methods map directly to REST API endpoints:

| TaskManager Method | HTTP Method | Endpoint | Request Body | Response |
|-------------------|-------------|----------|--------------|----------|
| add_task | POST | /tasks | {"description": str} | Task JSON |
| get_all_tasks | GET | /tasks | None | List[Task] JSON |
| get_task_by_id | GET | /tasks/{id} | None | Task JSON or 404 |
| update_task | PUT | /tasks/{id} | {"description": str} | Task JSON or 404 |
| mark_complete | PATCH | /tasks/{id}/complete | None | Task JSON or 404 |
| delete_task | DELETE | /tasks/{id} | None | 204 No Content or 404 |

---

## Testing Contract

Each method requires:
1. **Happy Path Test**: Verify success case returns expected result
2. **Error Path Test**: Verify validation errors raise ValueError
3. **Not Found Test**: Verify behavior when task ID doesn't exist
4. **Edge Case Test**: Verify boundary conditions (empty list, last task, etc.)
5. **Idempotency Test** (where applicable): Verify repeated operations are safe

---

## References

- Feature Specification: `specs/001-phase1-todo-core/spec.md`
- Implementation Plan: `specs/001-phase1-todo-core/plan.md`
- Data Model: `specs/001-phase1-todo-core/data-model.md`
- Functional Requirements: FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012
