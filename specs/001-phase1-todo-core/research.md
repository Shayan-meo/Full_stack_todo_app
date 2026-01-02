# Phase 0: Research & Technology Decisions

**Feature**: Phase I - Console Todo Application
**Date**: 2026-01-02
**Purpose**: Document technology choices, patterns, and architectural decisions

## Research Summary

All technical unknowns resolved through analysis of requirements, Python ecosystem best practices, and forward compatibility considerations for Phase II+ evolution.

---

## Decision 1: Python Dataclasses vs Dictionary Storage

**Context**: Need to represent Task entity in memory with ID, description, and completion status.

**Options Evaluated**:
1. **@dataclass** from standard library
2. Plain dictionary with string keys
3. NamedTuple from typing module
4. Custom class with __init__

**Decision**: Use `@dataclass` for Task model

**Rationale**:
- **Type Safety**: Full type hint support for static analysis
- **IDE Support**: Auto-completion, refactoring, inline documentation
- **Forward Compatibility**: Direct migration path to SQLModel (add table=True)
- **Validation**: __post_init__ hook for data validation
- **Immutability Options**: frozen=True available if needed
- **Standard Library**: No external dependencies required
- **Pythonic**: Modern Python 3.7+ standard for data containers

**Alternatives Considered**:
- **Dict storage**: Rejected - lacks type hints, prone to typos, no IDE support, harder to maintain
- **NamedTuple**: Rejected - immutable (need to update descriptions), no validation hooks
- **Custom class**: Rejected - verbose, dataclass provides same functionality with less code

**References**:
- PEP 557 – Data Classes
- SQLModel documentation (Phase II forward compatibility)

---

## Decision 2: Task ID Generation Strategy

**Context**: Need unique identifiers for tasks that are easy for CLI users to input.

**Options Evaluated**:
1. Sequential integers starting from 1
2. UUIDs (UUID4)
3. Timestamp-based IDs
4. User-assigned names/slugs

**Decision**: Sequential integer IDs starting from 1

**Rationale**:
- **CLI Usability**: Simple to type (1, 2, 3 vs UUID strings)
- **Predictable**: Users can remember IDs during session
- **Implementation Simplicity**: Counter increment in TaskManager
- **Meets Requirements**: FR-003 specifies "sequential integer IDs starting from 1"
- **Sufficient for Phase I**: In-memory, single-session, no distributed concerns

**Alternatives Considered**:
- **UUIDs**: Rejected - overkill for in-memory storage, poor CLI UX, 36-character strings
- **Timestamps**: Rejected - not guaranteed unique, harder to type, less intuitive
- **User names**: Rejected - validation complexity, uniqueness issues, longer input

**Forward Compatibility Note**:
- Phase II migration: SQLModel auto-increment integer primary key
- Phase IV/V: If distributed system needed, can migrate to UUIDs with ID translation layer

---

## Decision 3: CLI Menu System Pattern

**Context**: Interactive console interface for CRUD operations.

**Options Evaluated**:
1. Numbered menu with input loop
2. Command-line arguments (e.g., `todo add "task"`)
3. REPL with commands (e.g., `> add task`)
4. TUI framework (textual, rich)

**Decision**: Numbered menu with input validation loop

**Rationale**:
- **Industry Standard**: Familiar pattern (ATM machines, installation wizards)
- **Accessibility**: Clear numbered options, no memorization required
- **Specification Alignment**: FR-001 requires "interactive command-line menu"
- **Error Recovery**: Easy to handle invalid inputs and return to menu
- **No Dependencies**: Pure stdlib (input/print)
- **Simple Implementation**: ~150 LOC for complete CLI

**Alternatives Considered**:
- **CLI args**: Rejected - less interactive, doesn't meet "interactive menu" requirement
- **REPL**: Rejected - requires command parsing, more complex than needed
- **TUI framework**: Rejected - external dependency, overkill for Phase I simplicity

**Menu Structure**:
```
=== Todo List Manager ===
1. Add Task
2. View Tasks
3. Update Task
4. Mark Complete
5. Delete Task
6. Exit
```

---

## Decision 4: Input Validation Approach

**Context**: Need to validate task descriptions and IDs across CLI and future API layers.

**Options Evaluated**:
1. Centralized validation in TaskManager methods
2. Validation in CLI layer only
3. Validation in Task model only
4. Separate validator class/module

**Decision**: Centralized validation in TaskManager methods

**Rationale**:
- **Single Source of Truth**: Business rules in one location
- **Reusability**: Phase II API can reuse same validation logic
- **Testability**: Unit test validation independently of UI
- **Consistency**: Same error messages across interfaces
- **Encapsulation**: Business logic layer owns business rules

**Alternatives Considered**:
- **CLI-only validation**: Rejected - duplicates logic in Phase II, inconsistent errors
- **Model-only validation**: Rejected - Task is data container, validation is business rule
- **Separate validator**: Rejected - unnecessary abstraction for simple validation

**Validation Rules Implemented**:
- Description: non-empty, stripped whitespace, 1-500 characters
- Task ID: exists in collection, positive integer
- Operations: task exists before update/complete/delete

---

## Decision 5: Error Handling Strategy

**Context**: Need clear error communication for validation failures and not-found scenarios.

**Options Evaluated**:
1. Exception-based with ValueError
2. Return codes (success/failure integers)
3. Result objects (Ok/Err pattern)
4. Custom exception hierarchy

**Decision**: Exception-based with ValueError for validation, structured messages

**Rationale**:
- **Pythonic**: Exceptions are standard Python error handling idiom
- **Clear Flow**: Error path separate from success path (no if checks)
- **Descriptive**: Exception messages include context (e.g., "Task #42 not found")
- **Standard Library**: No external dependencies
- **Forward Compatible**: Maps cleanly to HTTP status codes in Phase II

**Alternatives Considered**:
- **Return codes**: Rejected - not idiomatic Python, requires constant checking
- **Result objects**: Rejected - requires external library or custom implementation
- **Custom exceptions**: Deferred - ValueError sufficient for Phase I, can refactor if needed

**Error Message Format**:
- Validation: "Task description cannot be empty"
- Not Found: "Task #42 not found"
- Context: Always include entity type and identifier

---

## Decision 6: ANSI Color Support for CLI

**Context**: Improve UX with color-coded success/error messages.

**Options Evaluated**:
1. ANSI escape codes with stdlib (no dependencies)
2. colorama library (cross-platform)
3. rich library (advanced formatting)
4. No colors (plain text only)

**Decision**: Optional ANSI colors using stdlib, fallback to plain text

**Rationale**:
- **No Dependencies**: Uses Python stdlib only (sys.stdout.isatty())
- **Cross-Platform Detection**: Check terminal capability before using colors
- **Graceful Degradation**: Falls back to plain text if unsupported
- **Improved UX**: Green checkmarks for success, yellow warnings for errors
- **Simple Implementation**: ~10 lines color utility functions

**Alternatives Considered**:
- **colorama**: Rejected - external dependency violates Phase I constraints
- **rich**: Rejected - heavy library, external dependency
- **No colors**: Viable fallback, less polished UX

**Implementation Approach**:
```python
# Detect terminal capability
if sys.stdout.isatty():
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
else:
    GREEN = YELLOW = RESET = ''
```

---

## Decision 7: Storage Pattern

**Context**: In-memory storage for Task objects during session.

**Options Evaluated**:
1. List[Task] with sequential search
2. Dict[int, Task] with ID lookup
3. OrderedDict for insertion order
4. Custom collection class

**Decision**: List[Task] with sequential search

**Rationale**:
- **Simplicity**: Straightforward append, remove, iterate operations
- **Sufficient Performance**: O(n) acceptable for <1000 tasks (spec limit)
- **Insertion Order**: List maintains creation order naturally
- **Memory Efficient**: No overhead of dict hash table
- **Specification Alignment**: FR-015 requires creation-time ordering

**Alternatives Considered**:
- **Dict by ID**: Rejected - O(1) lookup unnecessary optimization, loses order without OrderedDict
- **OrderedDict**: Rejected - overhead not justified, list sufficient
- **Custom collection**: Rejected - YAGNI, premature abstraction

**Performance Analysis**:
- Add: O(1) append
- View all: O(n) iteration (unavoidable)
- Find by ID: O(n) linear search (acceptable for n < 1000)
- Delete: O(n) search + O(n) removal (acceptable for phase I)

---

## Decision 8: Completion Toggle Behavior

**Context**: User Story 3 describes marking tasks complete, but behavior wasn't fully specified.

**Options Evaluated**:
1. Dedicated "Mark Complete" menu option (one-way: incomplete → complete)
2. Toggle menu option (complete ↔ incomplete)
3. Separate "Mark Complete" and "Mark Incomplete" options
4. Part of "Update Task" submenu

**Decision**: Dedicated "Mark Complete" menu option (one-way only)

**Rationale**:
- **Simplest UX**: Single action for most common use case
- **Meets Specification**: User Story 3 describes marking complete (no toggle mentioned)
- **Idempotent**: Can mark complete multiple times without error (graceful)
- **Focus**: Phase I prioritizes core workflow over edge cases
- **Extensible**: Can add "Mark Incomplete" in Phase II based on user feedback

**Alternatives Considered**:
- **Toggle**: Deferred to Phase II - adds complexity, not in requirements
- **Separate options**: Deferred - clutters menu, unlikely use case in Phase I
- **Update submenu**: Rejected - extra navigation step, separate concerns

**Implementation Notes**:
- mark_complete() method is idempotent (no error if already complete)
- Menu shows current status in task list view
- Future: Can add toggle if user feedback requests it

---

## Technology Stack Summary

| Component | Technology | Version | Justification |
|-----------|-----------|---------|---------------|
| **Language** | Python | 3.13+ (3.11+ compatible) | Constitution requirement, type hints, dataclasses |
| **Package Manager** | uv | Latest stable | Constitution requirement, fast, modern |
| **Type System** | Built-in type hints | Python 3.11+ | Static analysis, IDE support, documentation |
| **Data Structures** | dataclasses | stdlib | Type-safe, forward-compatible with SQLModel |
| **Storage** | List[Task] | stdlib | Simple, sufficient for in-memory Phase I |
| **CLI** | input/print | stdlib | No dependencies, meets requirements |
| **Error Handling** | ValueError exceptions | stdlib | Pythonic, clear error flow |
| **Testing** | Manual (pytest setup) | pytest 8.0+ | Manual Phase I, automated Phase II+ |
| **Colors** | ANSI codes (optional) | stdlib | Optional UX enhancement, no dependencies |

---

## Forward Compatibility Analysis

### Phase II: Web Application

**TaskManager → FastAPI Integration**:
- Each TaskManager method → API endpoint
- add_task() → POST /tasks
- get_all_tasks() → GET /tasks
- get_task_by_id() → GET /tasks/{id}
- update_task() → PUT /tasks/{id}
- mark_complete() → PATCH /tasks/{id}/complete
- delete_task() → DELETE /tasks/{id}

**Task Dataclass → SQLModel**:
```python
# Phase I
@dataclass
class Task:
    id: int
    description: str
    completed: bool = False

# Phase II migration
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(min_length=1, max_length=500)
    completed: bool = False
```

**Error Handling → HTTP Status Codes**:
- ValueError (validation) → 400 Bad Request
- ValueError (not found) → 404 Not Found
- Success → 200 OK / 201 Created

### Phase III: AI Chatbot

**Natural Language → Structured Operations**:
- "Add buy groceries" → add_task("buy groceries")
- "Show all tasks" → get_all_tasks()
- "Mark task 3 done" → mark_complete(3)

**Integration Point**: OpenAI Agents SDK calls TaskManager methods directly (no CLI coupling)

### Phase IV/V: Cloud-Native

**Stateless Design**:
- TaskManager has no state beyond method parameters
- In-memory list → external database (PostgreSQL with SQLModel)
- Each request independent → horizontal scaling support

**Containerization**:
- todo_app/ package → Docker container
- Clear boundaries for service deployment
- TaskManager → microservice or serverless function

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Type hint compatibility Python 3.11 | Low | Test on Python 3.11, use compatible syntax |
| ANSI colors fail on some terminals | Low | Graceful fallback to plain text, detect capability |
| Forward compatibility assumptions invalid | Medium | Design review by engineer, Phase II validation |
| Performance issues with large task lists | Low | Spec limits to 1000 tasks, O(n) acceptable |

---

## Validation Checklist

- ✅ All technology choices use Python stdlib only
- ✅ All decisions support forward compatibility to Phase II+
- ✅ Architecture aligns with constitution (separation of concerns)
- ✅ No external dependencies required
- ✅ Type hints for static analysis
- ✅ Clear error handling strategy
- ✅ UX patterns follow industry standards
- ✅ Performance adequate for Phase I scale (100-1000 tasks)

---

## References

- [PEP 557 – Data Classes](https://peps.python.org/pep-0557/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [Python Design Patterns](https://refactoring.guru/design-patterns/python)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/) (Phase II reference)
- Project Constitution: `.specify/memory/constitution.md`
- Feature Specification: `specs/001-phase1-todo-core/spec.md`
