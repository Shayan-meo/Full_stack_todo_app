# Implementation Plan: Phase I - Console Todo Application

**Branch**: `001-phase1-todo-core` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase1-todo-core/spec.md`

## Summary

Build a lightweight, terminal-based task management system with core CRUD functionality (Create, Read, Update, Delete, Mark Complete). The application provides an interactive CLI menu for managing tasks stored in-memory during the session. Architecture separates business logic (TaskManager) from user interface (CLI) to support future evolution to Phase II web application. No persistence, external dependencies, or authentication required in Phase I.

**Technical Approach**: Modular Python architecture with dataclass-based Task model, service-layer TaskManager for business logic, and CLI module for user interaction. Use Python standard library only with type hints and comprehensive validation.

## Technical Context

**Language/Version**: Python 3.13+ (backward compatible to 3.11+)
**Primary Dependencies**: Python Standard Library only (no third-party packages)
**Storage**: In-memory List of Task objects (no persistence)
**Testing**: Manual testing against acceptance criteria; pytest infrastructure prepared for Phase II
**Target Platform**: Cross-platform console (Windows/Linux/macOS terminals with UTF-8 support)
**Project Type**: Single project (console application)
**Performance Goals**:
- Menu operations: <100ms response time
- Task operations (CRUD): <1 second completion
- View tasks: <2 seconds for up to 1000 tasks
**Constraints**:
- No external dependencies beyond Python stdlib
- In-memory storage only (data lost on exit)
- Session-based operation (no multi-session support)
- 500-character limit on task descriptions
**Scale/Scope**:
- Single-user, single-session application
- Support 100+ tasks per session without degradation
- 5 core operations (Add, View, Update, Delete, Mark Complete)
- ~300-500 LOC total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Constitution Compliance

**Spec-Driven First**:
- ✅ All code will be generated from this plan and specification
- ✅ No manual coding permitted; refinements go through spec updates

**Architectural Thinking**:
- ✅ Clean separation: TaskManager (logic) vs CLI (interface)
- ✅ Forward-compatible design for Phase II FastAPI integration

**Iterative Evolution**:
- ✅ TaskManager designed as service layer for future API wrapping
- ✅ Data model (Task dataclass) compatible with SQLModel migration
- ✅ Business logic independent of CLI for web UI integration

**Quality Over Speed**:
- ✅ Comprehensive validation and error handling specified
- ✅ Clear acceptance criteria for all operations
- ✅ Type hints and docstrings required

**Technology Standards**:
- ✅ Python 3.11+ as specified in constitution
- ✅ Package management via uv with pyproject.toml
- ✅ Standard library only (Phase I constraint)

**Documentation Requirements**:
- ✅ README.md with setup and usage instructions
- ✅ Complete specs folder (spec.md, plan.md, tasks.md)
- ✅ CLAUDE.md for implementation guidance

**Verification Protocol**:
- ✅ Manual functional testing against acceptance scenarios
- ✅ All 15 functional requirements testable
- ✅ Error handling for edge cases specified

### No Violations

All constitutional requirements satisfied. No complexity justification needed.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-todo-core/
├── spec.md              # Requirements specification (completed)
├── plan.md              # This file - architectural plan
├── research.md          # Phase 0: Technology decisions and patterns
├── data-model.md        # Phase 1: Task entity and validation rules
├── quickstart.md        # Phase 1: Setup and run instructions
├── contracts/           # Phase 1: Internal API contracts (optional for Phase I)
│   └── task-manager.md  # TaskManager interface contract
└── tasks.md             # Phase 2: Implementation tasks (/sp.tasks output)
```

### Source Code (repository root)

```text
todo_app/                # Main application package
├── __init__.py          # Package initialization
├── models.py            # Task dataclass definition
├── manager.py           # TaskManager service (business logic)
├── cli.py               # CLI interface and menu system
└── main.py              # Application entry point

tests/                   # Test infrastructure (prepared for Phase II)
├── __init__.py
├── test_models.py       # Task model tests (manual Phase I)
├── test_manager.py      # TaskManager logic tests (manual Phase I)
└── test_cli.py          # CLI integration tests (manual Phase I)

pyproject.toml           # uv project configuration
README.md                # Project documentation
CLAUDE.md                # Claude Code implementation guidance
.gitignore               # Git ignore patterns
```

**Structure Decision**: Single project structure chosen for Phase I simplicity. Console application requires minimal complexity with clear separation of concerns: models (data), manager (logic), cli (interface), main (entry point). This structure supports future migration to web application by wrapping TaskManager with FastAPI endpoints.

## Complexity Tracking

No constitutional violations. This section is empty as all requirements align with constitution principles.

---

## Phase 0: Research & Decisions

### Research Topics

1. **Python Dataclasses vs Dictionary Storage**
   - **Decision**: Use `@dataclass` for Task model
   - **Rationale**: Better type safety, IDE support, forward compatibility with SQLModel
   - **Alternatives**: Dict storage (rejected - lacks type hints and validation)

2. **Task ID Generation Strategy**
   - **Decision**: Sequential integer IDs starting from 1
   - **Rationale**: Simple CLI input, predictable, meets Phase I requirements
   - **Alternatives**: UUIDs (rejected - overkill for in-memory, harder user input)

3. **CLI Menu System Pattern**
   - **Decision**: Numbered menu with input validation loop
   - **Rationale**: Industry standard, accessible, matches specification
   - **Alternatives**: Command-line args (rejected - less interactive for CRUD)

4. **Input Validation Approach**
   - **Decision**: Centralized validation in TaskManager methods
   - **Rationale**: Single source of truth, testable, reusable for Phase II API
   - **Alternatives**: CLI-only validation (rejected - duplicates logic in Phase II)

5. **Error Handling Strategy**
   - **Decision**: Exception-based with custom TaskError class
   - **Rationale**: Pythonic, clear error propagation, structured messages
   - **Alternatives**: Return codes (rejected - less idiomatic Python)

6. **ANSI Color Support for CLI**
   - **Decision**: Optional ANSI colors using standard library (no dependencies)
   - **Rationale**: Improves UX, cross-platform support via colorama-like detection
   - **Alternatives**: Third-party libraries (rejected - violates no-dependency constraint)

7. **Storage Pattern**
   - **Decision**: List[Task] in TaskManager with sequential search
   - **Rationale**: Simple, sufficient for <1000 tasks, no persistence needed
   - **Alternatives**: Dict by ID (rejected - unnecessary optimization for Phase I)

8. **Completion Toggle Behavior**
   - **Decision**: Dedicated "Mark Complete" menu option (one-way: incomplete → complete only)
   - **Rationale**: Simplest UX, aligns with user story priorities
   - **Alternatives**: Toggle complete/incomplete (deferred to Phase II based on user feedback)

### Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Language | Python | 3.13+ (3.11+ compatible) | Constitution requirement, modern features |
| Package Manager | uv | Latest | Constitution requirement, fast dependency management |
| Type Checking | Built-in type hints | Python 3.11+ | Static analysis, IDE support, documentation |
| Testing Framework | Manual + pytest setup | N/A | Manual for Phase I, pytest infrastructure for Phase II |
| CLI Framework | Python stdlib (input/print) | Built-in | No dependencies, sufficient for Phase I |
| Data Storage | In-memory List | Built-in | Phase I constraint, no persistence |

### Forward Compatibility Considerations

**Phase II (Web Application) Preparation**:
- TaskManager methods designed as service layer → easily wrapped by FastAPI endpoints
- Task dataclass → direct SQLModel migration path (add table metadata)
- Validation logic in manager → reusable for API request validation
- Error handling → maps to HTTP status codes (404 Not Found, 400 Bad Request)

**Phase III (AI Chatbot) Preparation**:
- Natural language → structured CRUD operations via TaskManager
- No UI coupling in business logic → agent can call TaskManager directly

**Phase IV/V (Cloud-Native) Preparation**:
- Stateless TaskManager → supports horizontal scaling with external storage
- Clear separation → containerization boundary at package level

---

## Phase 1: Data Model & Contracts

### Data Model Design

**File**: `data-model.md`

#### Task Entity

**Purpose**: Represents a single todo item in the system

**Attributes**:

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | int | Unique, auto-generated, > 0 | Auto-assigned | Sequential identifier starting from 1 |
| description | str | 1-500 chars, non-empty, stripped | None | Task description text |
| completed | bool | True/False | False | Completion status flag |
| created_at | int | Auto-generated, immutable | Current counter | Creation order tracking |

**Validation Rules**:
- Description must not be empty or whitespace-only after stripping
- Description length: 1 ≤ len(description) ≤ 500 characters
- ID assigned automatically by TaskManager (not user input)
- created_at used for implicit ordering (oldest first)

**State Transitions**:
```
[New Task] → completed=False (default)
[Incomplete Task] → completed=True (via Mark Complete)
[Completed Task] → completed=True (idempotent, no change)
[Any Task] → [Deleted] (removed from list)
```

**Implementation**:
```python
from dataclasses import dataclass, field

@dataclass
class Task:
    """Represents a todo task with description and completion status."""
    id: int
    description: str
    completed: bool = False
    created_at: int = field(default=0, compare=False)

    def __post_init__(self):
        """Validate task data after initialization."""
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty")
        if len(self.description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")
        self.description = self.description.strip()
```

### API Contracts

**File**: `contracts/task-manager.md`

#### TaskManager Interface

**Purpose**: Service layer providing CRUD operations for task management

**Methods**:

1. **add_task(description: str) → Task**
   - **Input**: Task description string
   - **Output**: Created Task object with assigned ID
   - **Errors**: ValueError if description empty/invalid
   - **Side Effects**: Increments next_id counter, appends to tasks list

2. **get_all_tasks() → List[Task]**
   - **Input**: None
   - **Output**: List of all tasks ordered by creation (oldest first)
   - **Errors**: None (returns empty list if no tasks)
   - **Side Effects**: None (read-only)

3. **get_task_by_id(task_id: int) → Task | None**
   - **Input**: Task ID integer
   - **Output**: Task object if found, None otherwise
   - **Errors**: None (returns None for not found)
   - **Side Effects**: None (read-only)

4. **update_task(task_id: int, description: str) → Task**
   - **Input**: Task ID and new description
   - **Output**: Updated Task object
   - **Errors**: ValueError if task not found or description invalid
   - **Side Effects**: Modifies task description in-place

5. **mark_complete(task_id: int) → Task**
   - **Input**: Task ID integer
   - **Output**: Task object with completed=True
   - **Errors**: ValueError if task not found
   - **Side Effects**: Sets completed flag to True (idempotent)

6. **delete_task(task_id: int) → bool**
   - **Input**: Task ID integer
   - **Output**: True if deleted, False if not found
   - **Errors**: None (returns False for not found)
   - **Side Effects**: Removes task from list

**Error Handling Contract**:
- All validation errors raise `ValueError` with descriptive messages
- Not found conditions: update/mark_complete raise ValueError, others return None/False
- All errors include context (e.g., "Task #42 not found")

**Thread Safety**: Not required for Phase I (single-user, single-session)

**Performance Contract**:
- add_task: O(1) amortized
- get_all_tasks: O(n) where n = number of tasks
- get_task_by_id: O(n) linear search
- update_task: O(n) search + O(1) update
- mark_complete: O(n) search + O(1) update
- delete_task: O(n) search + O(n) list removal

### Quickstart Guide

**File**: `quickstart.md`

#### Setup Instructions

**Prerequisites**:
- Python 3.11 or higher installed
- `uv` package manager installed

**Installation**:
```bash
# Clone repository
git clone <repository-url>
cd Todo-list

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install project in development mode
uv pip install -e .
```

**Running the Application**:
```bash
# From project root
python -m todo_app.main

# Or using uv directly
uv run python -m todo_app.main
```

**Usage**:
1. Select menu option by entering the corresponding number (1-6)
2. Follow prompts to enter task descriptions or IDs
3. View feedback messages for each operation
4. Select option 6 to exit application

**Menu Options**:
- `1` - Add Task: Create new task with description
- `2` - View Tasks: Display all tasks with IDs and status
- `3` - Update Task: Modify existing task description
- `4` - Mark Complete: Mark task as complete
- `5` - Delete Task: Remove task from list
- `6` - Exit: Terminate application

**Testing**:
```bash
# Run manual acceptance testing
# Follow test scenarios in spec.md User Stories section
python -m todo_app.main

# Verify each acceptance scenario manually
# - Add task with valid/invalid inputs
# - View tasks (empty list, populated list)
# - Update task (valid/invalid IDs)
# - Mark complete (valid/invalid IDs)
# - Delete task (valid/invalid IDs)
```

---

## Phase 2: Architecture & Design

### Component Architecture

```
┌─────────────────────────────────────────────────┐
│                    CLI Layer                    │
│  (cli.py + main.py)                             │
│  - User interaction                             │
│  - Menu display                                  │
│  - Input collection                              │
│  - Output formatting                             │
└───────────────┬─────────────────────────────────┘
                │
                │ Calls methods
                ↓
┌─────────────────────────────────────────────────┐
│              TaskManager Layer                   │
│  (manager.py)                                    │
│  - Business logic                                │
│  - Validation                                    │
│  - CRUD operations                               │
│  - Error handling                                │
└───────────────┬─────────────────────────────────┘
                │
                │ Manages collection
                ↓
┌─────────────────────────────────────────────────┐
│               Data Layer                         │
│  (models.py)                                     │
│  - Task dataclass                                │
│  - In-memory List[Task]                          │
│  - Data validation                               │
└─────────────────────────────────────────────────┘
```

### Module Design

#### models.py
**Responsibility**: Define Task data structure and validation
**Dependencies**: dataclasses (stdlib)
**Exports**: Task class
**Size Estimate**: ~30 lines

#### manager.py
**Responsibility**: Business logic for task CRUD operations
**Dependencies**: models.py
**Exports**: TaskManager class
**Size Estimate**: ~120 lines

#### cli.py
**Responsibility**: User interface and menu system
**Dependencies**: manager.py, models.py
**Exports**: CLI class with run() method
**Size Estimate**: ~150 lines

#### main.py
**Responsibility**: Application entry point
**Dependencies**: cli.py
**Exports**: None (entry point only)
**Size Estimate**: ~20 lines

### Key Design Patterns

**Service Layer Pattern**: TaskManager acts as service layer between CLI and data
**Data Transfer Object**: Task dataclass serves as DTO across layers
**Separation of Concerns**: CLI handles presentation, Manager handles logic, Model handles data
**Fail-Fast Validation**: Validate at entry points (Manager methods) before processing

### Error Handling Strategy

**Error Categories**:
1. **Validation Errors**: Empty descriptions, invalid length → ValueError with clear message
2. **Not Found Errors**: Invalid task IDs → ValueError with task ID in message
3. **Input Errors**: Invalid menu choices, non-integer IDs → Re-prompt without crash

**Error Flow**:
```
CLI (input) → Manager (validate) → raise ValueError
                                  ↓
CLI (catch) → Display error message → Return to menu
```

**Error Messages Format**:
- Validation: "Task description cannot be empty"
- Not Found: "Task #42 not found"
- Success: "Task #42 marked as complete"

### Input/Output Specifications

**Menu Display**:
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

**Task Display Format**:
```
[1] [ ] Buy groceries
[2] [X] Review pull request
[3] [ ] Write documentation

Legend: [ ] = Incomplete, [X] = Complete
```

**Empty List Display**:
```
No tasks found. Add a task to get started!
```

**Confirmation Messages**:
- Add: "✓ Task added successfully (ID: 1)"
- Update: "✓ Task #1 updated successfully"
- Complete: "✓ Task #1 marked as complete"
- Delete: "✓ Task #1 deleted successfully"

**Error Messages**:
- Empty input: "⚠ Task description cannot be empty"
- Not found: "⚠ Task #42 not found"
- Invalid choice: "⚠ Invalid choice. Please enter 1-6"

### Testing Strategy

**Manual Acceptance Testing** (Phase I):

1. **Test Suite 1: Add Task**
   - TC1.1: Add task with valid description → Success
   - TC1.2: Add task with empty description → Error message
   - TC1.3: Add task with whitespace only → Error message
   - TC1.4: Add task with 500 chars → Success
   - TC1.5: Add task with 501 chars → Error message

2. **Test Suite 2: View Tasks**
   - TC2.1: View empty list → "No tasks found" message
   - TC2.2: View 1 task → Display with correct format
   - TC2.3: View 10 tasks → Display in creation order
   - TC2.4: View tasks with mixed completion status → Correct indicators

3. **Test Suite 3: Update Task**
   - TC3.1: Update existing task → Success message
   - TC3.2: Update non-existent task → Error message
   - TC3.3: Update with empty description → Error message
   - TC3.4: Verify update in view → Description changed

4. **Test Suite 4: Mark Complete**
   - TC4.1: Mark incomplete task complete → Success message
   - TC4.2: Mark already complete task → Success (idempotent)
   - TC4.3: Mark non-existent task → Error message
   - TC4.4: Verify completion in view → Status indicator changed

5. **Test Suite 5: Delete Task**
   - TC5.1: Delete existing task → Success message
   - TC5.2: Delete non-existent task → Error message
   - TC5.3: Verify deletion in view → Task not displayed
   - TC5.4: Delete last task → Empty list message

**Automated Testing Infrastructure** (Prepared for Phase II):
- pytest configuration in pyproject.toml
- Unit tests for TaskManager methods
- Integration tests for CLI workflows
- Test fixtures for common scenarios

---

## Implementation Phases

### Phase A: Foundation (Setup & Models)

**Objective**: Initialize project structure and define data model

**Tasks**:
1. Create project structure (directories, __init__.py files)
2. Setup pyproject.toml with uv configuration
3. Implement Task dataclass in models.py with validation
4. Write README.md with project overview
5. Create .gitignore for Python project

**Deliverables**:
- Project skeleton with proper structure
- Working Task dataclass with validation
- Project documentation (README)

**Validation**:
- Import Task class successfully
- Create Task instances with valid data
- Task validation raises ValueError for invalid data

### Phase B: Business Logic (TaskManager)

**Objective**: Implement core CRUD operations

**Tasks**:
1. Implement TaskManager class skeleton
2. Implement add_task() with ID generation
3. Implement get_all_tasks() with ordering
4. Implement get_task_by_id() with search
5. Implement update_task() with validation
6. Implement mark_complete() with idempotency
7. Implement delete_task() with confirmation

**Deliverables**:
- Complete TaskManager class
- All CRUD operations functional
- Comprehensive error handling

**Validation**:
- Manual testing of each TaskManager method
- Verify validation logic catches invalid inputs
- Verify error messages are descriptive

### Phase C: User Interface (CLI)

**Objective**: Build interactive menu system

**Tasks**:
1. Implement CLI class skeleton
2. Implement main menu display loop
3. Implement Add Task flow with input collection
4. Implement View Tasks flow with formatting
5. Implement Update Task flow with ID input
6. Implement Mark Complete flow with confirmation
7. Implement Delete Task flow with confirmation
8. Implement Exit flow with clean termination
9. Add ANSI color support for success/error messages (optional)

**Deliverables**:
- Complete CLI class
- Interactive menu system
- User-friendly input/output
- Color-coded messages (optional)

**Validation**:
- Navigate all menu options successfully
- Verify input validation and re-prompting
- Verify output formatting matches specification

### Phase D: Integration & Testing

**Objective**: End-to-end integration and acceptance testing

**Tasks**:
1. Implement main.py entry point
2. Run complete test suite (5 test suites, ~20 test cases)
3. Fix any issues discovered during testing
4. Update CLAUDE.md with implementation notes
5. Update README.md with usage instructions
6. Verify all acceptance criteria from spec.md

**Deliverables**:
- Fully integrated application
- All acceptance tests passing
- Complete documentation
- CLAUDE.md implementation guide

**Validation**:
- All 15 functional requirements satisfied
- All 7 success criteria met
- All 5 user stories verified
- All edge cases handled gracefully

---

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Input validation edge cases missed | Medium | Low | Comprehensive test suite with boundary conditions |
| CLI UX confusing for users | Low | Low | Follow industry standard menu patterns |
| Performance degradation with large lists | Low | Low | Spec limits to 1000 tasks, sequential search sufficient |
| Forward compatibility issues | Medium | Low | Design review against Phase II requirements |
| Type hint errors in Python 3.11 | Low | Low | Test on Python 3.11 minimum version |

**Critical Path**: Phase B (TaskManager) → Phase C (CLI) → Phase D (Integration)
**Dependencies**: Models must be complete before Manager, Manager before CLI

---

## Next Steps

1. **Review and Approve Plan**: Engineer reviews this plan for architectural soundness
2. **Generate Tasks**: Run `/sp.tasks` to break down implementation into atomic tasks
3. **Implement Phase A**: Setup project structure and models
4. **Implement Phase B**: Build TaskManager with CRUD operations
5. **Implement Phase C**: Create CLI interface
6. **Implement Phase D**: Integration testing and documentation

**Estimated Effort**:
- Phase A: 30 minutes
- Phase B: 1 hour
- Phase C: 1.5 hours
- Phase D: 1 hour
- **Total**: ~4 hours for complete Phase I implementation

**Success Criteria for Plan Completion**:
- ✅ All technical unknowns resolved
- ✅ Architecture aligns with constitution
- ✅ Forward compatibility considered
- ✅ Clear implementation path defined
- ✅ Ready for `/sp.tasks` command
