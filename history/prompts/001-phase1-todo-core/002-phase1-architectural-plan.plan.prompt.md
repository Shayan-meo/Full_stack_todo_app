---
id: 002
title: Phase I Architectural Plan
stage: plan
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-phase1-todo-core
branch: 001-phase1-todo-core
user: SHAYAN
command: /sp.plan
labels: ["phase1", "architecture", "planning", "design", "console-app"]
links:
  spec: specs/001-phase1-todo-core/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase1-todo-core/plan.md
  - specs/001-phase1-todo-core/research.md
  - specs/001-phase1-todo-core/data-model.md
  - specs/001-phase1-todo-core/quickstart.md
  - specs/001-phase1-todo-core/contracts/task-manager.md
tests:
  - Constitution compliance check (all gates passed)
  - Forward compatibility analysis for Phase II-V
---

## Prompt

Prompt for Claude Code: "Claude, based on our Specification and Clarifications, generate a detailed /specs/plan-phase1.md file. Use the following structured approach to guide the development:"

1) Architecture Sketch & Structure:

Modular Design: Separate the project into models.py (data structure), logic.py (CRUD operations), and cli.py (user interface).

Entry Point: Use main.py to initialize the app and run the main loop.

Data Flow: CLI → Logic Manager → List/Dict (In-memory storage).

2) Research-Concurrent Approach (Tech Discovery):

Dependency Check: Use uv to manage Python 3.13 environment.

UI Enhancement: Briefly research and implement basic ANSI colors or simple text formatting to make the CLI readable (Success/Error messages).

Future-Proofing: Ensure the Logic layer is clean so it can be wrapped in a FastAPI app for Phase II.

3) Decisions & Tradeoffs (Documentation):

Storage Choice: Use a Python List of Dicts vs Classes. (Tradeoff: Classes offer better type-hinting for future phases).

Unique IDs: Use simple incremental integers (1, 2, 3) for ease of CLI input, but keep logic flexible for UUIDs later.

Sync vs Async: Stay Synchronous for Phase I to keep it simple, but use a Service-Repository pattern.

4) Testing & Quality Validation Strategy:

Manual Gate 1: Verify Add Task correctly updates the in-memory list.

Manual Gate 2: Verify Delete Task handles non-existent IDs without crashing.

Manual Gate 3: Verify List View displays "No tasks found" when the list is empty.

Final Gate: Ensure CLAUDE.md is updated with run commands.

5) Phase-wise Execution:

Phase A (Foundation): Setup uv project and define the Task model.

Phase B (Logic): Implement Add, Delete, and Update functions.

Phase C (Interface): Build the CLI loop and menu system.

Phase D (Synthesis): Integrated testing and final spec-compliance check.

## Response snapshot

Generated comprehensive architectural plan for Phase I Console Todo Application following spec-driven development principles and project constitution.

**Files Created**:
1. **plan.md** (680 lines): Complete implementation plan with technical context, architecture, phases, and risk assessment
2. **research.md**: 8 technology decisions with rationale, alternatives, and forward compatibility analysis
3. **data-model.md**: Task entity specification, validation rules, state transitions, and SQLModel migration path
4. **quickstart.md**: Complete setup, installation, usage instructions, and testing guide
5. **contracts/task-manager.md**: TaskManager API contract with 6 methods, error handling, and Phase II REST mapping

**Plan Structure**:
- **Technical Context**: Python 3.13+, stdlib only, in-memory storage, 300-500 LOC, <1s operations
- **Constitution Check**: All gates passed, zero violations, full compliance
- **Project Structure**: Single project (todo_app/ package) with models, manager, cli, main modules
- **Phase 0 Research**: 8 decisions resolved (dataclasses, sequential IDs, numbered menu, centralized validation, exceptions, ANSI colors, List storage, dedicated complete action)
- **Phase 1 Design**: Task entity, TaskManager interface, quickstart guide, API contracts
- **Phase 2 Architecture**: 3-layer design (CLI → Manager → Models), error handling strategy, I/O specifications, testing strategy
- **Implementation Phases**: A (Foundation), B (Business Logic), C (CLI), D (Integration)

**Key Architectural Decisions**:
1. **Data Model**: @dataclass Task with id, description, completed, created_at fields
2. **Storage**: List[Task] with O(n) operations (sufficient for <1000 tasks)
3. **IDs**: Sequential integers starting from 1 (CLI-friendly)
4. **Validation**: Centralized in TaskManager (reusable for Phase II API)
5. **Error Handling**: ValueError exceptions with descriptive messages
6. **CLI Pattern**: Numbered menu with input validation loop
7. **Colors**: Optional ANSI codes with graceful fallback
8. **Completion**: Dedicated "Mark Complete" menu option (one-way: incomplete → complete)

**Forward Compatibility**:
- TaskManager → FastAPI endpoints (6 REST routes)
- Task dataclass → SQLModel migration (add table=True)
- Validation logic → API request validation
- Error messages → HTTP status codes (404, 400)
- Sequential IDs → auto-increment primary keys

**Module Design**:
- `models.py`: Task dataclass with validation (~30 LOC)
- `manager.py`: TaskManager service with 6 CRUD methods (~120 LOC)
- `cli.py`: Interactive menu and I/O handling (~150 LOC)
- `main.py`: Application entry point (~20 LOC)

**Testing Strategy**:
- Manual acceptance testing (5 test suites, 20 test cases)
- Pytest infrastructure prepared for Phase II
- Verification gates at each implementation phase

**Performance Guarantees**:
- Menu operations: <100ms
- CRUD operations: <1 second
- View tasks: <2 seconds for 1000 tasks
- O(1) add, O(n) search/update/delete

**Estimated Effort**: ~4 hours total (30min foundation + 1h logic + 1.5h CLI + 1h integration)

## Outcome

- ✅ Impact: Complete architectural plan ready for task generation (/sp.tasks command)
- 🧪 Tests: Constitution compliance verified, all quality gates passed
- 📁 Files: 5 documentation files created (plan, research, data-model, quickstart, contract)
- 🔁 Next prompts: `/sp.tasks` to generate atomic implementation tasks from this plan
- 🧠 Reflection: Plan provides clear implementation path with forward compatibility to Phase II-V. All technical unknowns resolved through research phase. Architecture follows constitutional principles: spec-driven, separated concerns, quality over speed, iterative evolution. Ready for task breakdown and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan generated successfully with complete research and design
- Graders run and results (PASS/FAIL): Constitution Check - ALL GATES PASSED
- Prompt variant (if applicable): Standard /sp.plan flow with user-provided structural guidance
- Next experiment (smallest change to try): Generate tasks.md with /sp.tasks to validate plan granularity
