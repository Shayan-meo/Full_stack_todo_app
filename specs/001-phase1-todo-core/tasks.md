---
description: "Implementation tasks for Phase I Console Todo Application"
---

# Tasks: Phase I - Console Todo Application

**Input**: Design documents from `/specs/001-phase1-todo-core/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/task-manager.md, research.md

**Tests**: Manual testing only (no automated tests in Phase I)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Project root**: `todo_app/` package
- **Tests**: `tests/` (infrastructure only, manual testing Phase I)
- **Documentation**: Root level (README.md, CLAUDE.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and structure per plan.md

- [ ] T001 Create project directory structure (todo_app/, tests/, specs/)
- [ ] T002 Initialize pyproject.toml with uv for Python 3.11+ project
- [ ] T003 [P] Create todo_app/__init__.py package initialization file
- [ ] T004 [P] Create tests/__init__.py for test infrastructure
- [ ] T005 [P] Create .gitignore for Python project (venv, __pycache__, .pyc files)
- [ ] T006 Verify uv environment setup by running: uv run python --version

**Verification**: Run `uv run python --version` - should show Python 3.11+

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Task entity that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Create todo_app/models.py with Task dataclass (id, description, completed, created_at fields)
- [ ] T008 Implement Task.__post_init__ validation (non-empty description, max 500 chars)
- [ ] T009 Implement Task.__str__ method for display formatting
- [ ] T010 Verify Task model by creating test instance: Task(id=1, description="Test", completed=False, created_at=1)

**Verification**: Create dummy Task object and print to verify validation works

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Quick Task Capture (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks with descriptions to in-memory list

**Independent Test**: Launch app, add task "Buy groceries", verify confirmation "Task added successfully (ID: 1)"

### Implementation for User Story 1

- [ ] T011 [US1] Create todo_app/manager.py with TaskManager class skeleton
- [ ] T012 [US1] Initialize TaskManager with empty _tasks list, _next_id=1, _creation_counter=1
- [ ] T013 [US1] Implement TaskManager.add_task(description: str) → Task method
- [ ] T014 [US1] Add validation in add_task: strip whitespace, check non-empty, check ≤500 chars
- [ ] T015 [US1] Implement ID generation: assign _next_id, increment counter
- [ ] T016 [US1] Implement creation order tracking: assign _creation_counter, increment
- [ ] T017 [US1] Append created task to _tasks list in add_task method
- [ ] T018 [US1] Return created Task object from add_task
- [ ] T019 [US1] Test add_task manually: manager.add_task("Test") should return Task with id=1

**Verification**: Create temporary test script, call manager.add_task("Test task"), verify list length increases

**Checkpoint**: At this point, users can add tasks to in-memory storage

---

## Phase 4: User Story 2 - Task Review and Status Check (Priority: P1)

**Goal**: Enable users to view all tasks with IDs, descriptions, and completion status

**Independent Test**: Add 3 tasks, select "View Tasks", verify all display with correct format

### Implementation for User Story 2

- [ ] T020 [US2] Implement TaskManager.get_all_tasks() → List[Task] method
- [ ] T021 [US2] Return copy of _tasks list maintaining creation order
- [ ] T022 [US2] Handle empty list case (return empty list, no error)
- [ ] T023 [US2] Test get_all_tasks: add 3 tasks, verify method returns all 3 in order
- [ ] T024 [US2] Create todo_app/cli.py with CLI class skeleton
- [ ] T025 [US2] Initialize CLI with TaskManager instance in __init__
- [ ] T026 [US2] Implement CLI.display_menu() method showing 6 numbered options
- [ ] T027 [US2] Implement CLI.view_tasks() method calling manager.get_all_tasks()
- [ ] T028 [US2] Format task display: "[id] [status] description" (e.g., "[1] [ ] Buy groceries")
- [ ] T029 [US2] Handle empty list: display "No tasks found. Add a task to get started!"
- [ ] T030 [US2] Add legend: "Legend: [ ] = Incomplete, [X] = Complete"
- [ ] T031 [US2] Test view_tasks: manually verify display format matches specification

**Verification**: Run CLI, add tasks, select View option, verify formatted output

**Checkpoint**: At this point, User Stories 1 AND 2 work (add + view = minimal workflow)

---

## Phase 5: User Story 3 - Task Completion Tracking (Priority: P2)

**Goal**: Enable users to mark tasks as complete with status persistence

**Independent Test**: Add task, mark complete, view tasks to verify [X] status indicator

### Implementation for User Story 3

- [ ] T032 [US3] Implement TaskManager.get_task_by_id(task_id: int) → Task | None method
- [ ] T033 [US3] Add linear search through _tasks list in get_task_by_id
- [ ] T034 [US3] Return None if task not found (no error raised)
- [ ] T035 [US3] Test get_task_by_id: verify returns task for valid ID, None for invalid
- [ ] T036 [US3] Implement TaskManager.mark_complete(task_id: int) → Task method
- [ ] T037 [US3] Find task by ID in mark_complete, raise ValueError if not found
- [ ] T038 [US3] Set task.completed = True (idempotent operation)
- [ ] T039 [US3] Return updated task from mark_complete
- [ ] T040 [US3] Test mark_complete: verify status changes, verify idempotent (no error if already complete)
- [ ] T041 [US3] Implement CLI.mark_task_complete() method
- [ ] T042 [US3] Prompt user for task ID input in mark_task_complete
- [ ] T043 [US3] Call manager.mark_complete(task_id) with error handling
- [ ] T044 [US3] Display success message: "✓ Task #X marked as complete"
- [ ] T045 [US3] Display error message if task not found: "⚠ Task #X not found"
- [ ] T046 [US3] Add menu option 4 "Mark Complete" to display_menu

**Verification**: Add task, mark complete, view tasks - status should show [X]

**Checkpoint**: All P1+P2 stories functional (add + view + complete)

---

## Phase 6: User Story 4 - Task Modification (Priority: P2)

**Goal**: Enable users to update task descriptions with validation

**Independent Test**: Add task "Review PR", update to "Review PR #456", verify change in view

### Implementation for User Story 4

- [ ] T047 [US4] Implement TaskManager.update_task(task_id: int, description: str) → Task method
- [ ] T048 [US4] Find task by ID in update_task, raise ValueError if not found
- [ ] T049 [US4] Validate new description (strip whitespace, non-empty, ≤500 chars)
- [ ] T050 [US4] Update task.description in-place with validated description
- [ ] T051 [US4] Return updated task from update_task
- [ ] T052 [US4] Test update_task: verify description changes, verify validation errors
- [ ] T053 [US4] Implement CLI.update_task() method
- [ ] T054 [US4] Prompt user for task ID and new description in update_task
- [ ] T055 [US4] Call manager.update_task(task_id, description) with error handling
- [ ] T056 [US4] Display success message: "✓ Task #X updated successfully"
- [ ] T057 [US4] Display error messages for not found and validation errors
- [ ] T058 [US4] Add menu option 3 "Update Task" to display_menu

**Verification**: Update existing task, verify description changes in view

**Checkpoint**: All P1+P2 stories complete with update functionality

---

## Phase 7: User Story 5 - Task Removal (Priority: P3)

**Goal**: Enable users to delete tasks from the list

**Independent Test**: Add 5 tasks, delete task #3, verify it no longer appears in list

### Implementation for User Story 5

- [ ] T059 [US5] Implement TaskManager.delete_task(task_id: int) → bool method
- [ ] T060 [US5] Find task by ID in delete_task
- [ ] T061 [US5] Remove task from _tasks list if found, return True
- [ ] T062 [US5] Return False if task not found (no error raised)
- [ ] T063 [US5] Test delete_task: verify task removed, verify returns False for invalid ID
- [ ] T064 [US5] Implement CLI.delete_task() method
- [ ] T065 [US5] Prompt user for task ID to delete
- [ ] T066 [US5] Call manager.delete_task(task_id)
- [ ] T067 [US5] Display success message if deleted: "✓ Task #X deleted successfully"
- [ ] T068 [US5] Display error if not found: "⚠ Task #X not found"
- [ ] T069 [US5] Add menu option 5 "Delete Task" to display_menu

**Verification**: Delete task, view list - task should not appear

**Checkpoint**: All 5 user stories complete (full CRUD + complete)

---

## Phase 8: CLI Integration & Main Loop

**Purpose**: Complete interactive menu system with all operations

- [ ] T070 Implement CLI.add_task() method for menu option 1
- [ ] T071 Prompt user for task description in add_task method
- [ ] T072 Call manager.add_task(description) with error handling
- [ ] T073 Display success message: "✓ Task added successfully (ID: X)"
- [ ] T074 Display error message for validation failures
- [ ] T075 Implement CLI.run() method with infinite menu loop
- [ ] T076 Display menu, get user choice input (1-6)
- [ ] T077 Route choice to appropriate method (add/view/update/complete/delete/exit)
- [ ] T078 Handle invalid menu choices with error message
- [ ] T079 Implement exit option (choice 6) to break loop and display "Goodbye!"
- [ ] T080 Add input validation: handle non-integer inputs gracefully
- [ ] T081 Create todo_app/main.py as application entry point
- [ ] T082 Import CLI class in main.py
- [ ] T083 Create CLI instance and call run() method in if __name__ == "__main__"
- [ ] T084 Test complete menu flow: navigate all 6 options

**Verification**: Run app, navigate all menu options, verify each operation works

---

## Phase 9: Error Handling & Input Validation

**Purpose**: Robust error handling across all operations

- [ ] T085 Add try-except blocks in CLI methods to catch ValueError from manager
- [ ] T086 Display user-friendly error messages for all validation failures
- [ ] T087 Handle empty input gracefully (re-prompt user)
- [ ] T088 Handle non-integer task IDs gracefully (re-prompt user)
- [ ] T089 Test error handling: try empty descriptions, invalid IDs, non-numeric inputs
- [ ] T090 Verify application never crashes on invalid input

**Verification**: Test all error scenarios - app should handle gracefully without crashing

---

## Phase 10: Optional ANSI Color Support

**Purpose**: Enhanced UX with color-coded messages (optional)

- [ ] T091 [P] Detect terminal capability using sys.stdout.isatty()
- [ ] T092 [P] Define ANSI color codes (GREEN for success, YELLOW for errors, RESET)
- [ ] T093 [P] Set colors to empty strings if terminal doesn't support ANSI
- [ ] T094 Apply GREEN color to success messages (✓ Task added, etc.)
- [ ] T095 Apply YELLOW color to error messages (⚠ Task not found, etc.)
- [ ] T096 Test colors in terminal - verify graceful fallback on unsupported terminals

**Verification**: Run in color-supporting terminal (colors appear) and plain terminal (no escape codes)

---

## Phase 11: Documentation & Polish

**Purpose**: Complete project documentation and final quality checks

- [ ] T097 [P] Create README.md with project overview and architecture summary
- [ ] T098 [P] Add setup instructions to README.md (prerequisites, installation steps)
- [ ] T099 [P] Add usage instructions to README.md (how to run, menu options)
- [ ] T100 [P] Add examples to README.md (sample workflows)
- [ ] T101 [P] Create CLAUDE.md with implementation guidance and run commands
- [ ] T102 [P] Document TaskManager interface contract in CLAUDE.md
- [ ] T103 [P] Add type hints to all function signatures (verify with mypy if available)
- [ ] T104 [P] Add docstrings to all classes and public methods
- [ ] T105 [P] Format code with black or follow PEP 8 guidelines
- [ ] T106 Run complete acceptance test suite from spec.md
- [ ] T107 Verify all 15 functional requirements (FR-001 through FR-015)
- [ ] T108 Verify all 7 success criteria (SC-001 through SC-007)
- [ ] T109 Test all 5 edge cases from spec.md
- [ ] T110 Run quickstart.md validation to ensure documentation is accurate

**Verification**: Follow README.md from scratch - should work without issues

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - US1 (P1): Can start after Foundational
  - US2 (P1): Depends on US1 (TaskManager.get_all_tasks + CLI.view_tasks)
  - US3 (P2): Depends on US2 (needs get_task_by_id)
  - US4 (P2): Depends on US3 (uses get_task_by_id)
  - US5 (P3): Independent of US3/US4, only depends on US2
- **CLI Integration (Phase 8)**: Depends on all user stories being complete
- **Error Handling (Phase 9)**: Depends on CLI Integration
- **Colors (Phase 10)**: Can be done anytime after CLI Integration (optional)
- **Documentation (Phase 11)**: Depends on complete implementation

### User Story Dependencies

- **User Story 1 (P1 - Add Task)**: No dependencies, foundational feature
- **User Story 2 (P1 - View Tasks)**: Depends on US1 (needs tasks to view)
- **User Story 3 (P2 - Mark Complete)**: Depends on US2 (needs get_task_by_id and view)
- **User Story 4 (P2 - Update Task)**: Depends on US3 (uses get_task_by_id)
- **User Story 5 (P3 - Delete Task)**: Depends on US2 (independent of US3/US4)

### Critical Path

1. Setup (Phase 1) → T001-T006
2. Foundational (Phase 2) → T007-T010
3. User Story 1 (Phase 3) → T011-T019
4. User Story 2 (Phase 4) → T020-T031
5. User Story 3 (Phase 5) → T032-T046
6. User Story 4 (Phase 6) → T047-T058
7. User Story 5 (Phase 7) → T059-T069
8. CLI Integration (Phase 8) → T070-T084
9. Error Handling (Phase 9) → T085-T090
10. Documentation (Phase 11) → T097-T110

### Parallel Opportunities

**Phase 1 (Setup)**:
- T003, T004, T005 can run in parallel (different files)

**Phase 2 (Foundational)**:
- T007, T008, T009 must be sequential (same file)

**Within User Stories**:
- Most tasks within a story are sequential (same files)
- Exception: Tests for managers can be separate from CLI work

**Phase 11 (Documentation)**:
- T097-T105 can all run in parallel (different files)

---

## Parallel Example: Setup Phase

```bash
# Launch these tasks together:
Task T003: "Create todo_app/__init__.py"
Task T004: "Create tests/__init__.py"
Task T005: "Create .gitignore"
```

## Parallel Example: Documentation Phase

```bash
# Launch these tasks together:
Task T097: "Create README.md overview"
Task T098: "Add setup instructions to README"
Task T099: "Add usage instructions to README"
Task T100: "Add examples to README"
Task T101: "Create CLAUDE.md"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

**Minimum Viable Product delivers: Add tasks + View tasks**

1. Complete Phase 1: Setup (T001-T006) - ~30 minutes
2. Complete Phase 2: Foundational (T007-T010) - ~15 minutes
3. Complete Phase 3: User Story 1 (T011-T019) - ~30 minutes
4. Complete Phase 4: User Story 2 (T020-T031) - ~45 minutes
5. **STOP and VALIDATE**: Test add + view workflow independently
6. **MVP Ready**: Users can capture and review tasks

**Total MVP Time**: ~2 hours

### Full Phase I Delivery

**Complete feature set: All CRUD + Mark Complete**

1. Complete MVP (Phases 1-4)
2. Add Phase 5: User Story 3 (T032-T046) - Mark Complete - ~30 minutes
3. Add Phase 6: User Story 4 (T047-T058) - Update - ~30 minutes
4. Add Phase 7: User Story 5 (T059-T069) - Delete - ~20 minutes
5. Complete Phase 8: CLI Integration (T070-T084) - ~30 minutes
6. Complete Phase 9: Error Handling (T085-T090) - ~20 minutes
7. Optional Phase 10: Colors (T091-T096) - ~10 minutes
8. Complete Phase 11: Documentation (T097-T110) - ~30 minutes

**Total Phase I Time**: ~4 hours

### Incremental Delivery Milestones

1. **Milestone 1**: Setup + Foundational → Project structure ready
2. **Milestone 2**: +US1 → Can add tasks (but can't see them yet)
3. **Milestone 3 (MVP)**: +US2 → Can add and view tasks (minimal workflow)
4. **Milestone 4**: +US3 → Can mark tasks complete
5. **Milestone 5**: +US4 → Can update task descriptions
6. **Milestone 6**: +US5 → Full CRUD complete
7. **Milestone 7**: +Integration → Interactive menu complete
8. **Milestone 8**: +Polish → Production-ready Phase I

---

## Manual Testing Checklist

### Test Suite 1: Add Task (US1)

- [ ] TC1.1: Add task "Buy groceries" → Success with ID 1
- [ ] TC1.2: Add task with empty description → Error message
- [ ] TC1.3: Add task with whitespace only → Error message
- [ ] TC1.4: Add task with 500 characters → Success
- [ ] TC1.5: Add task with 501 characters → Error message

### Test Suite 2: View Tasks (US2)

- [ ] TC2.1: View empty list → "No tasks found" message
- [ ] TC2.2: Add 1 task, view → Display with correct format
- [ ] TC2.3: Add 10 tasks, view → All displayed in creation order
- [ ] TC2.4: View with mixed complete/incomplete → Correct [ ] and [X] indicators

### Test Suite 3: Mark Complete (US3)

- [ ] TC3.1: Mark incomplete task complete → Success message
- [ ] TC3.2: Mark already complete task → Success (idempotent, no error)
- [ ] TC3.3: Mark non-existent task #999 → Error message
- [ ] TC3.4: View after marking complete → Status shows [X]

### Test Suite 4: Update Task (US4)

- [ ] TC4.1: Update existing task description → Success message
- [ ] TC4.2: Update non-existent task #999 → Error message
- [ ] TC4.3: Update with empty description → Error message
- [ ] TC4.4: View after update → Description changed

### Test Suite 5: Delete Task (US5)

- [ ] TC5.1: Delete existing task → Success message
- [ ] TC5.2: Delete non-existent task #999 → Error message
- [ ] TC5.3: View after deletion → Task not displayed
- [ ] TC5.4: Delete last task, view → "No tasks found" message

### Test Suite 6: Error Handling

- [ ] TC6.1: Invalid menu choice (0, 7, abc) → Error message, re-prompt
- [ ] TC6.2: Non-integer task ID → Error message, re-prompt
- [ ] TC6.3: Empty input when task ID expected → Error message, re-prompt

### Test Suite 7: Edge Cases

- [ ] TC7.1: Add 100 tasks → Performance acceptable (<2s view)
- [ ] TC7.2: Task with special characters → Displays correctly
- [ ] TC7.3: Task with unicode characters → Displays correctly
- [ ] TC7.4: Exit application → Clean termination, no errors

---

## Notes

- **[P] tasks**: Different files, can run in parallel
- **[Story] labels**: Map tasks to user stories for traceability
- **Independent stories**: Each story should be completable and testable alone
- **Manual testing**: No automated tests in Phase I (pytest infrastructure for Phase II)
- **Verification steps**: Every phase includes explicit verification commands
- **MVP strategy**: Focus on US1+US2 first for fastest value delivery
- **Commit frequency**: Commit after each phase or logical group of tasks
- **Stop at checkpoints**: Validate each user story independently before proceeding
- **Quality gates**: All 15 FR + 7 SC + 5 edge cases must pass before Phase I complete

---

## Task Summary

**Total Tasks**: 110 tasks across 11 phases
**Critical Path**: 11 phases (Setup → Foundation → 5 User Stories → Integration → Error Handling → Documentation)
**Parallel Opportunities**: 8 tasks can run in parallel (different files, no dependencies)
**MVP Scope**: Phases 1-4 (46 tasks, ~2 hours) delivers add + view workflow
**Full Phase I**: All 110 tasks (~4 hours) delivers complete CRUD + Mark Complete

**User Story Breakdown**:
- US1 (Add Task): 9 tasks
- US2 (View Tasks): 12 tasks
- US3 (Mark Complete): 15 tasks
- US4 (Update Task): 12 tasks
- US5 (Delete Task): 11 tasks
- Setup + Integration + Polish: 51 tasks

**Ready for Implementation**: All tasks defined with file paths, verification steps, and dependencies
