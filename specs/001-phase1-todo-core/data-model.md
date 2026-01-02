# Data Model: Phase I - Console Todo Application

**Feature**: 001-phase1-todo-core
**Date**: 2026-01-02
**Purpose**: Define data structures, validation rules, and state transitions

---

## Overview

Phase I data model consists of a single entity (Task) stored in-memory during application session. No persistence, relationships, or complex state machines required.

**Design Principles**:
- Simple, flat structure (no relationships)
- Type-safe with Python dataclasses
- Forward-compatible with SQLModel (Phase II)
- Validation at creation and modification
- Immutable IDs, mutable descriptions and status

---

## Entity: Task

### Purpose

Represents a single todo item in the system with unique identifier, text description, and completion status.

### Attributes

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `id` | int | Yes | Auto-assigned | Unique, > 0, immutable | Sequential identifier starting from 1 |
| `description` | str | Yes | None | 1-500 chars, non-empty | Task description text, whitespace trimmed |
| `completed` | bool | Yes | False | True/False | Completion status flag |
| `created_at` | int | Yes | Auto-assigned | ≥ 0, immutable | Creation order counter for sorting |

### Detailed Field Specifications

#### id: int
- **Purpose**: Unique identifier for task lookup and user reference
- **Generation**: Auto-assigned by TaskManager using sequential counter
- **Range**: 1, 2, 3, ... (positive integers)
- **Mutability**: Immutable after creation
- **User Input**: Never provided by user (system-generated)
- **Phase II Migration**: Maps to SQLModel integer primary key with auto-increment

#### description: str
- **Purpose**: Human-readable task description
- **Length**: Minimum 1 character, maximum 500 characters (after trimming)
- **Whitespace**: Leading/trailing whitespace automatically stripped on create/update
- **Empty Check**: Empty strings and whitespace-only strings rejected
- **Validation**: Performed in Task.__post_init__ and TaskManager methods
- **Phase II Migration**: SQLModel Field(min_length=1, max_length=500)
- **Examples**:
  - Valid: "Buy groceries"
  - Valid: "Review PR #456 - authentication module"
  - Invalid: "" (empty)
  - Invalid: "   " (whitespace only)
  - Invalid: (501-character string)

#### completed: bool
- **Purpose**: Track whether task has been completed
- **Values**: True (complete) or False (incomplete)
- **Default**: False (new tasks are incomplete)
- **Display**: `[X]` for True, `[ ]` for False in CLI
- **Transition**: One-way in Phase I (False → True only, no toggle back)
- **Idempotent**: Can mark complete multiple times (no error)
- **Phase II Migration**: Boolean column in database

#### created_at: int
- **Purpose**: Maintain creation order for display sorting
- **Generation**: Auto-assigned by TaskManager using counter
- **Value**: Sequential integers (1, 2, 3, ...) independent of task IDs
- **Mutability**: Immutable after creation
- **Usage**: Sort tasks by created_at to show oldest first (FR-015)
- **Note**: Separate from ID to handle potential future gaps in ID sequence
- **Phase II Migration**: Replace with timestamp (datetime.utcnow())

### Validation Rules

#### At Creation (Task.__post_init__)
1. **Description not empty**: After stripping, length must be > 0
2. **Description length**: After stripping, length must be ≤ 500
3. **Whitespace trimming**: description = description.strip()

#### At Update (TaskManager.update_task)
1. **Same validation as creation**: Apply all creation rules to new description
2. **Task exists**: Task ID must exist in collection
3. **Description changed**: (Optional validation, not enforced)

#### At Mark Complete (TaskManager.mark_complete)
1. **Task exists**: Task ID must exist in collection
2. **Already complete**: No error, idempotent operation

#### At Delete (TaskManager.delete_task)
1. **Task exists**: Task ID must exist in collection
2. **No confirmation**: Delete immediately (no "are you sure?" prompt)

### State Transitions

```
┌─────────────────────────────────────────────────────────┐
│                     Task Lifecycle                      │
└─────────────────────────────────────────────────────────┘

[Creation]
    │
    ↓
┌─────────────────┐
│  New Task       │  id: auto, description: validated
│  completed:     │  created_at: auto, completed: False
│    False        │
└────────┬────────┘
         │
         ├──→ [Update Description] ──→ Same state, description changed
         │
         ├──→ [Mark Complete] ──────→ Transition to Complete
         │
         └──→ [Delete] ──────────────→ [Removed from collection]

┌─────────────────┐
│  Complete Task  │  All fields unchanged except:
│  completed:     │  completed: True
│    True         │
└────────┬────────┘
         │
         ├──→ [Update Description] ──→ Same state, description changed
         │
         ├──→ [Mark Complete] ──────→ Same state (idempotent, no error)
         │
         └──→ [Delete] ──────────────→ [Removed from collection]
```

**State Rules**:
- **New → Complete**: Via mark_complete() method
- **Complete → Incomplete**: NOT SUPPORTED in Phase I (deferred to Phase II)
- **Any State → Deleted**: Via delete_task() method (irreversible)
- **Update Description**: Allowed in any state (does not change completed status)

### Data Structure Implementation

#### Python Dataclass (Phase I)

```python
from dataclasses import dataclass, field

@dataclass
class Task:
    """
    Represents a todo task with description and completion status.

    Attributes:
        id: Unique sequential identifier (auto-assigned)
        description: Task description text (1-500 characters)
        completed: Completion status (default: False)
        created_at: Creation order counter (auto-assigned)

    Raises:
        ValueError: If description is empty or exceeds 500 characters
    """
    id: int
    description: str
    completed: bool = False
    created_at: int = field(default=0, compare=False)

    def __post_init__(self):
        """Validate task data after initialization."""
        # Strip whitespace
        if isinstance(self.description, str):
            self.description = self.description.strip()

        # Validate description not empty
        if not self.description:
            raise ValueError("Task description cannot be empty")

        # Validate description length
        if len(self.description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")

    def __str__(self) -> str:
        """Human-readable string representation."""
        status = "[X]" if self.completed else "[ ]"
        return f"[{self.id}] {status} {self.description}"
```

#### SQLModel Migration (Phase II)

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Task(SQLModel, table=True):
    """
    Task entity for SQLModel/database storage.

    Phase II adds: persistence, primary key, table mapping
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(min_length=1, max_length=500)
    completed: bool = Field(default=False)
    created_at: int = Field(default_factory=lambda: int(time.time()))

    # Future Phase III+ fields (example):
    # user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    # priority: Optional[int] = Field(default=0, ge=0, le=5)
    # due_date: Optional[datetime] = None
```

---

## Storage Model

### Phase I: In-Memory List

**Structure**: `List[Task]` in TaskManager class

**Operations**:
- **Add**: Append to list, O(1)
- **Read All**: Iterate list, O(n)
- **Find by ID**: Linear search, O(n)
- **Update**: Find + modify in-place, O(n)
- **Delete**: Find + remove, O(n)

**Ordering**: Maintained by created_at field (oldest first)

**Persistence**: None (data lost on exit)

### Phase II: PostgreSQL with SQLModel

**Structure**: Relational table with auto-increment primary key

**Operations**:
- **Add**: INSERT INTO tasks, O(1)
- **Read All**: SELECT * FROM tasks ORDER BY created_at, O(n)
- **Find by ID**: SELECT * FROM tasks WHERE id = ?, O(1) with index
- **Update**: UPDATE tasks SET description = ? WHERE id = ?, O(1)
- **Delete**: DELETE FROM tasks WHERE id = ?, O(1)

**Ordering**: ORDER BY created_at in query

**Persistence**: Durable storage with ACID guarantees

---

## Validation Error Messages

| Error Condition | Message | HTTP Status (Phase II) |
|----------------|---------|------------------------|
| Description empty | "Task description cannot be empty" | 400 Bad Request |
| Description too long | "Task description cannot exceed 500 characters" | 400 Bad Request |
| Task not found (update) | "Task #{id} not found" | 404 Not Found |
| Task not found (complete) | "Task #{id} not found" | 404 Not Found |
| Task not found (delete) | "Task #{id} not found" | 404 Not Found |

---

## Example Data

### Valid Tasks

```python
Task(id=1, description="Buy groceries", completed=False, created_at=1)
Task(id=2, description="Review PR #456", completed=True, created_at=2)
Task(id=3, description="Write documentation for API endpoints", completed=False, created_at=3)
```

### Invalid Tasks (Raise ValueError)

```python
Task(id=1, description="", completed=False, created_at=1)
# ValueError: Task description cannot be empty

Task(id=2, description="   ", completed=False, created_at=2)
# ValueError: Task description cannot be empty (after strip)

Task(id=3, description="a" * 501, completed=False, created_at=3)
# ValueError: Task description cannot exceed 500 characters
```

---

## Forward Compatibility Checklist

- ✅ Task dataclass → SQLModel migration path clear
- ✅ Field types compatible with database columns
- ✅ Validation rules portable to SQLModel constraints
- ✅ ID generation strategy (sequential int) maps to auto-increment
- ✅ No hardcoded relationships blocking future foreign keys
- ✅ created_at can be replaced with timestamp in Phase II
- ✅ completed boolean works for both in-memory and database

---

## References

- Feature Specification: `specs/001-phase1-todo-core/spec.md`
- Implementation Plan: `specs/001-phase1-todo-core/plan.md`
- Research Document: `specs/001-phase1-todo-core/research.md`
- Functional Requirements: FR-002, FR-003, FR-004, FR-009
- Key Entities Section: spec.md lines 127-133
