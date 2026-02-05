# Implementation Tasks: Full-Stack Web Application

**Feature Branch**: `002-fullstack-web-app`
**Created**: 2026-01-05
**Status**: Ready for Implementation

## Task Summary

- **Total Tasks**: 110 tasks
- **User Stories**: 5 (mapped from spec.md priorities)
- **Phases**: 11 (Setup + 10 implementation phases)
- **Parallel Opportunities**: 45 parallelizable tasks marked with [P]

## User Story Mapping

| Story ID | Priority | Description | Phase | Task Count |
|----------|----------|-------------|-------|------------|
| US1 | P1 | User Registration and Login | 3-4 | 25 tasks |
| US2 | P1 | Personal Task Management | 5-6 | 30 tasks |
| US3 | P2 | Task Status Toggle | 7 | 8 tasks |
| US4 | P2 | Responsive Multi-Device Access | 8 | 12 tasks |
| US5 | P1 | Data Persistence Across Sessions | 2 | 5 tasks |

---

## Phase 1: Setup & Monorepo Structure

**Goal**: Initialize monorepo with backend and frontend folders, configure shared environment

**Independent Test**: Both `backend/` and `frontend/` folders exist with proper structure, shared `.env` configured

### Tasks

- [ ] T001 Create monorepo root structure with backend/ and frontend/ folders
- [ ] T002 [P] Create backend/app/ folder structure (models/, routers/, middleware/, schemas/)
- [ ] T003 [P] Create backend/scripts/ folder for database migration scripts
- [ ] T004 [P] Create frontend/app/ folder structure following Next.js App Router convention
- [ ] T005 [P] Create frontend/components/ and frontend/lib/ folders
- [ ] T006 Create root `.env` file with BETTER_AUTH_SECRET and DATABASE_URL placeholders
- [ ] T007 [P] Create backend/.gitignore (exclude .env, __pycache__, .venv, *.pyc)
- [ ] T008 [P] Create frontend/.gitignore (exclude .env.local, node_modules/, .next/, out/)
- [ ] T009 [P] Create backend/pyproject.toml with fastapi, sqlmodel, pyjwt, passlib, uvicorn dependencies
- [ ] T010 [P] Create frontend/package.json with next, react, tailwindcss, better-auth dependencies

**Verification**:
```bash
# Check folder structure
ls backend/app/models backend/app/routers backend/app/middleware
ls frontend/app frontend/components frontend/lib

# Verify .env exists at root
cat .env | grep BETTER_AUTH_SECRET
cat .env | grep DATABASE_URL
```

---

## Phase 2: Backend Foundation (Data Models & Database)

**Goal**: [US5] Establish database connection and create User/Task models for data persistence

**Independent Test**: Can run `create_tables.py` successfully, tables visible in Neon dashboard, can manually insert/query data

### Tasks

- [ ] T011 [US5] Implement backend/app/database.py with Neon connection string and SQLModel engine
- [ ] T012 [P] [US5] Create get_session() dependency function for FastAPI routes in backend/app/database.py
- [ ] T013 [P] [US1] Implement User SQLModel in backend/app/models/user.py (id, email, hashed_password, created_at)
- [ ] T014 [P] [US2] Implement Task SQLModel in backend/app/models/task.py (id, description, completed, created_at, user_id FK)
- [ ] T015 [US5] Create backend/scripts/create_tables.py migration script using SQLModel.metadata.create_all()
- [ ] T016 [P] [US5] Create backend/scripts/seed_data.py to generate test user and sample tasks
- [ ] T017 [US5] Create backend/scripts/reset_database.py (WARNING: deletes all data) for development resets

**Verification**:
```bash
cd backend
uv venv
uv pip install -e .
uv run python scripts/create_tables.py
# Expected: ✓ Tables created successfully

# Verify tables in Neon dashboard
psql "your-neon-connection-string"
\dt  # Should show: user, task tables
\d user  # Should show: id, email, hashed_password, created_at columns
\d task  # Should show: id, description, completed, created_at, user_id columns
```

---

## Phase 3: Security Layer (JWT Authentication)

**Goal**: [US1] Implement JWT-based authentication with signup/signin endpoints

**Independent Test**: Can create user via POST /api/auth/signup, login via POST /api/auth/signin, receive JWT token

### Tasks

- [ ] T018 [US1] Implement JWT verification middleware in backend/app/middleware/auth.py with verify_jwt() function
- [ ] T019 [US1] Implement get_current_user_id() dependency in backend/app/middleware/auth.py (extracts user_id from JWT payload)
- [ ] T020 [P] [US1] Create AuthRequest schema in backend/app/schemas/auth.py (email, password fields)
- [ ] T021 [P] [US1] Create AuthResponse schema in backend/app/schemas/auth.py (token, user fields)
- [ ] T022 [US1] Implement POST /api/auth/signup endpoint in backend/app/routers/auth.py (create user, hash password, return JWT)
- [ ] T023 [US1] Implement POST /api/auth/signin endpoint in backend/app/routers/auth.py (verify credentials, return JWT)
- [ ] T024 [P] [US1] Implement password hashing with bcrypt (passlib.context.CryptContext) in backend/app/routers/auth.py
- [ ] T025 [P] [US1] Configure JWT token generation with HS256 algorithm and 24h expiration in backend/app/routers/auth.py
- [ ] T026 [US1] Add CORS middleware in backend/app/main.py allowing frontend origin (http://localhost:3000)
- [ ] T027 [US1] Register auth router in backend/app/main.py with /api/auth prefix
- [ ] T028 [US1] Create backend/app/main.py FastAPI application instance with title="Todo List Manager API"

**Verification**:
```bash
# Start backend server
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test signup (in another terminal)
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
# Expected: {"token":"eyJ...","user":{"id":1,"email":"test@example.com"}}

# Test signin
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
# Expected: {"token":"eyJ...","user":{"id":1,"email":"test@example.com"}}

# Test invalid credentials
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"wrongpassword"}'
# Expected: 401 {"detail":"Invalid email or password"}
```

---

## Phase 4: Task API Endpoints

**Goal**: [US2] Implement all 5 task CRUD operations with user isolation

**Independent Test**: Can create, read, update, toggle, delete tasks via API; User A cannot access User B's tasks

### Tasks

- [ ] T029 [P] [US2] Create TaskResponse schema in backend/app/schemas/tasks.py (id, description, completed, created_at)
- [ ] T030 [P] [US2] Create CreateTaskRequest schema in backend/app/schemas/tasks.py (description field only)
- [ ] T031 [P] [US2] Create UpdateTaskRequest schema in backend/app/schemas/tasks.py (description field only)
- [ ] T032 [US2] Implement GET /api/tasks endpoint in backend/app/routers/tasks.py (list tasks filtered by user_id from JWT)
- [ ] T033 [US2] Implement POST /api/tasks endpoint in backend/app/routers/tasks.py (create task for authenticated user)
- [ ] T034 [US2] Implement PUT /api/tasks/{id} endpoint in backend/app/routers/tasks.py (update task description, verify ownership)
- [ ] T035 [US3] Implement PATCH /api/tasks/{id}/complete endpoint in backend/app/routers/tasks.py (toggle completion status)
- [ ] T036 [US2] Implement DELETE /api/tasks/{id} endpoint in backend/app/routers/tasks.py (delete task, verify ownership)
- [ ] T037 [US2] Add task description validation (1-500 chars, non-empty) in backend/app/routers/tasks.py
- [ ] T038 [US2] Implement user isolation check (task.user_id == user_id) returning 404 if mismatch in backend/app/routers/tasks.py
- [ ] T039 [US2] Register tasks router in backend/app/main.py with /api/tasks prefix and JWT auth dependency
- [ ] T040 [US2] Add exception handler for HTTPException in backend/app/main.py returning JSON error responses
- [ ] T041 [US2] Add generic exception handler in backend/app/main.py (log error, return 500 without stack trace)

**Verification**:
```bash
# Get JWT token from signin
TOKEN=$(curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.token')

# Test list tasks (should be empty initially)
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN"
# Expected: []

# Test create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description":"Buy groceries"}'
# Expected: {"id":1,"description":"Buy groceries","completed":false,"created_at":"..."}

# Test list tasks (should show 1 task)
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN"
# Expected: [{"id":1,"description":"Buy groceries",...}]

# Test update task
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description":"Buy groceries and cook dinner"}'
# Expected: {"id":1,"description":"Buy groceries and cook dinner",...}

# Test toggle complete
curl -X PATCH http://localhost:8000/api/tasks/1/complete \
  -H "Authorization: Bearer $TOKEN"
# Expected: {"id":1,...,"completed":true}

# Test delete task
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN"
# Expected: 204 No Content

# Test user isolation: Create second user, try to access first user's task
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user2@example.com","password":"password456"}'

TOKEN2=$(curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"user2@example.com","password":"password456"}' \
  | jq -r '.token')

# User 2 tries to access User 1's task (create task as User 1 first, get ID, then try with User 2 token)
curl http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN2"
# Expected: 404 {"detail":"Task not found"}
```

---

## Phase 5: API Documentation

**Goal**: Generate interactive Swagger UI documentation for all endpoints

**Independent Test**: Can access http://localhost:8000/docs and test all endpoints via Swagger UI

### Tasks

- [ ] T042 [P] Add API documentation metadata in backend/app/main.py (title, description, version, contact)
- [ ] T043 [P] Add OpenAPI tags to auth router in backend/app/routers/auth.py (tag="Authentication")
- [ ] T044 [P] Add OpenAPI tags to tasks router in backend/app/routers/tasks.py (tag="Tasks")
- [ ] T045 [P] Add operation descriptions to all endpoints (summary, description fields) in auth.py and tasks.py
- [ ] T046 [P] Add response model examples to schemas in backend/app/schemas/ (Config.json_schema_extra)

**Verification**:
```bash
# Access Swagger UI
open http://localhost:8000/docs
# Expected: Interactive API documentation showing:
# - Authentication section with POST /api/auth/signup and POST /api/auth/signin
# - Tasks section with GET/POST/PUT/PATCH/DELETE /api/tasks endpoints
# - Bearer authentication option (lock icon) to set JWT token
# - Request/response examples for all endpoints

# Test endpoint via Swagger UI:
# 1. Click "Authorize" button, paste JWT token
# 2. Try GET /api/tasks → Should return authenticated user's tasks
# 3. Try POST /api/tasks → Should create new task
```

---

## Phase 6: Frontend Foundation

**Goal**: [US1][US4] Initialize Next.js application with routing, Better Auth, and API client

**Independent Test**: Next.js dev server starts, landing page displays, Tailwind CSS works

### Tasks

- [ ] T047 Initialize Next.js 16 project in frontend/ with TypeScript and App Router
- [ ] T048 [P] Configure Tailwind CSS in frontend/tailwind.config.js with responsive breakpoints (sm:768px, md:1024px, lg:1280px)
- [ ] T049 [P] Create frontend/styles/globals.css with Tailwind imports (@tailwind base/components/utilities)
- [ ] T050 [P] [US1] Configure Better Auth in frontend/lib/auth.ts with JWT plugin (24h expiration, HS256 algorithm)
- [ ] T051 [P] Create TypeScript interfaces in frontend/lib/types.ts (User, Task, AuthResponse, ErrorResponse)
- [ ] T052 [US1] Implement API client class in frontend/lib/api.ts with auto-JWT attachment to Authorization header
- [ ] T053 [US1] Add 401 auto-redirect to /signin in frontend/lib/api.ts request() method
- [ ] T054 [P] [US4] Implement root layout in frontend/app/layout.tsx (import globals.css, set viewport metadata)
- [ ] T055 [P] [US4] Create landing page in frontend/app/page.tsx with "Sign In" and "Sign Up" buttons
- [ ] T056 [P] Create frontend/.env.local with NEXT_PUBLIC_API_URL=http://localhost:8000 and BETTER_AUTH_SECRET

**Verification**:
```bash
cd frontend
npm install
npm run dev
# Expected: Server started on http://localhost:3000

# Open browser: http://localhost:3000
# Expected:
# - Landing page displays with "Todo List Manager" heading
# - Two buttons: "Sign In" and "Sign Up"
# - Tailwind CSS styles applied (modern, clean design)
# - Responsive layout (test by resizing browser window)

# Check API client configuration
# Open DevTools Console and test:
fetch('http://localhost:8000/health').then(r => r.json()).then(console.log)
# Expected: CORS error or successful response depending on backend CORS config
```

---

## Phase 7: Authentication UI

**Goal**: [US1] Create signup and signin pages with form validation

**Independent Test**: Can create account, login, JWT stored in localStorage, redirected to dashboard

### Tasks

- [ ] T057 [P] [US1] Create ErrorMessage component in frontend/components/ErrorMessage.tsx (red alert with dismiss button)
- [ ] T058 [P] [US1] Create LoadingSpinner component in frontend/components/LoadingSpinner.tsx (animated spinner)
- [ ] T059 [US1] Create auth route group folder frontend/app/(auth)/ (no shared layout)
- [ ] T060 [US1] Implement signup page in frontend/app/(auth)/signup/page.tsx (email/password form, client-side validation)
- [ ] T061 [US1] Add POST /api/auth/signup call in signup page, store JWT in localStorage, redirect to /dashboard
- [ ] T062 [US1] Implement signin page in frontend/app/(auth)/signin/page.tsx (email/password form)
- [ ] T063 [US1] Add POST /api/auth/signin call in signin page, store JWT in localStorage, redirect to /dashboard
- [ ] T064 [P] [US1] [US4] Style auth forms with Tailwind CSS (responsive, mobile-friendly, centered layout)
- [ ] T065 [P] [US1] Add email format validation and password length validation (min 8 chars) in both forms
- [ ] T066 [P] [US1] Display error messages using ErrorMessage component for auth failures

**Verification**:
```bash
# Test signup flow
# 1. Open http://localhost:3000/signup
# 2. Enter email: testuser@example.com, password: testpass123
# 3. Click "Sign Up"
# Expected:
# - Loading spinner appears briefly
# - Redirected to http://localhost:3000/dashboard
# - JWT token stored in localStorage (check DevTools → Application → Local Storage)

# Test signin flow
# 1. Open http://localhost:3000/signin
# 2. Enter same credentials
# 3. Click "Sign In"
# Expected:
# - Redirected to dashboard
# - JWT token in localStorage

# Test error handling
# 1. Try signup with existing email
# Expected: Error message "Email already registered"
# 2. Try signin with wrong password
# Expected: Error message "Invalid email or password"

# Test validation
# 1. Try signup with invalid email format
# Expected: Client-side error before API call
# 2. Try signup with password < 8 characters
# Expected: Client-side error before API call
```

---

## Phase 8: Dashboard UI (Task Management)

**Goal**: [US2][US3] Create dashboard with full task CRUD functionality

**Independent Test**: Can view tasks, create new task, update description, toggle completion, delete task - all without page refresh

### Tasks

- [ ] T067 [US2] Create protected dashboard layout in frontend/app/dashboard/layout.tsx (check JWT, redirect if missing)
- [ ] T068 [P] [US2] Add logout button in dashboard layout (clear localStorage, redirect to /signin)
- [ ] T069 [US2] Implement dashboard page in frontend/app/dashboard/page.tsx (fetch tasks on mount with useEffect)
- [ ] T070 [P] [US2] Add loading state display using LoadingSpinner while fetching tasks
- [ ] T071 [P] [US2] Add empty state display ("No tasks yet. Create your first task!") when tasks array is empty
- [ ] T072 [P] [US2] Implement TaskList component in frontend/components/TaskList.tsx (maps tasks to TaskCard)
- [ ] T073 [US2] [US3] Implement TaskCard component in frontend/components/TaskCard.tsx (display description, checkbox, edit/delete buttons)
- [ ] T074 [P] [US3] Add checkbox click handler in TaskCard calling PATCH /api/tasks/{id}/complete
- [ ] T075 [P] [US2] Add strikethrough styling to completed task description in TaskCard
- [ ] T076 [P] [US2] Add delete button handler in TaskCard calling DELETE /api/tasks/{id} with confirmation dialog
- [ ] T077 [US2] Implement TaskForm component in frontend/components/TaskForm.tsx (input field, create button)
- [ ] T078 [US2] Add POST /api/tasks call in TaskForm, update tasks state without page refresh
- [ ] T079 [P] [US2] Add inline editing to TaskCard (click description → input field, save button)
- [ ] T080 [P] [US2] Add PUT /api/tasks/{id} call for inline editing, update tasks state
- [ ] T081 [P] [US2] Add task description validation (1-500 chars) in TaskForm and inline edit
- [ ] T082 [P] [US2] Display ErrorMessage component for failed API calls in dashboard

**Verification**:
```bash
# Test dashboard access
# 1. Navigate to http://localhost:3000/dashboard (while logged in)
# Expected: Dashboard displays with "Your Tasks" heading

# Test create task
# 1. Enter "Buy groceries" in task input field
# 2. Click "Add Task" button
# Expected:
# - Task appears in list immediately (no page refresh)
# - Input field clears
# - Task shows with checkbox (unchecked) and description "Buy groceries"

# Test toggle completion
# 1. Click checkbox on "Buy groceries" task
# Expected:
# - Checkbox becomes checked
# - Description gets strikethrough style
# - No page refresh

# Test inline edit
# 1. Click on task description
# Expected:
# - Description becomes editable input field
# - "Save" button appears
# 2. Change to "Buy groceries and cook dinner"
# 3. Click "Save"
# Expected:
# - Description updates immediately
# - Input field becomes static text again

# Test delete
# 1. Click delete button (trash icon) on task
# 2. Confirm deletion in dialog
# Expected:
# - Task disappears from list immediately
# - No page refresh

# Test persistence
# 1. Create 3 tasks
# 2. Refresh page (F5)
# Expected: All 3 tasks still displayed (loaded from database)

# Test empty state
# 1. Delete all tasks
# Expected: "No tasks yet" message displays
```

---

## Phase 9: Responsive Design

**Goal**: [US4] Ensure UI works on mobile (375px), tablet (768px), and desktop (1920px+)

**Independent Test**: All pages render correctly on all viewport sizes, no horizontal scrolling

### Tasks

- [ ] T083 [P] [US4] Add mobile-first responsive classes to landing page (stack buttons vertically on mobile)
- [ ] T084 [P] [US4] Add responsive breakpoints to auth forms (single column mobile, centered on desktop)
- [ ] T085 [US4] Add responsive grid to dashboard (single column mobile, 2-col tablet, 3-col desktop)
- [ ] T086 [P] [US4] Ensure touch targets are min 44x44px on mobile (buttons, checkboxes) in all components
- [ ] T087 [P] [US4] Add responsive navbar in dashboard layout (hamburger menu on mobile, full nav on desktop)
- [ ] T088 [P] [US4] Test on mobile viewport (375px width) - verify no horizontal scrolling
- [ ] T089 [P] [US4] Test on tablet viewport (768px width) - verify optimal layout utilization
- [ ] T090 [P] [US4] Test on desktop viewport (1920px width) - verify multi-column layout
- [ ] T091 [P] [US4] Add responsive font sizes (text-sm mobile, text-base tablet, text-lg desktop)
- [ ] T092 [P] [US4] Add responsive spacing (gap-2 mobile, gap-4 tablet, gap-6 desktop)
- [ ] T093 [P] [US4] Remove hover states on mobile (only apply md:hover:) to avoid stuck hover on touch devices
- [ ] T094 [US4] Test on actual devices (iPhone SE, iPad, desktop) - document any issues

**Verification**:
```bash
# Browser testing (Chrome DevTools)
# 1. Open http://localhost:3000
# 2. Open DevTools (F12) → Toggle device toolbar
# 3. Test Mobile (375x667 - iPhone SE):
# - Landing page: buttons stack vertically
# - Auth forms: full width, centered
# - Dashboard: tasks in single column, touch-friendly buttons
# - No horizontal scrolling
# 4. Test Tablet (768x1024 - iPad):
# - Landing page: buttons side-by-side
# - Dashboard: tasks in 2 columns
# - Optimal spacing
# 5. Test Desktop (1920x1080):
# - Dashboard: tasks in 3 columns
# - Generous white space
# - All content easily accessible

# Real device testing
# 1. Open app on actual iPhone (Safari)
# Expected: Smooth touch interactions, no layout issues
# 2. Open app on actual iPad
# Expected: Efficient use of screen space
# 3. Test all CRUD operations on mobile
# Expected: All features work, touch targets easy to tap
```

---

## Phase 10: Error Handling & UX Polish

**Goal**: Implement robust error handling and smooth user experience across all scenarios

**Independent Test**: All error scenarios display user-friendly messages, loading states shown, confirmations required for destructive actions

### Tasks

- [ ] T095 [P] Add toast notification system in frontend/components/Toast.tsx (success/error/info toasts)
- [ ] T096 [P] Replace ErrorMessage with Toast notifications for better UX in all components
- [ ] T097 [P] Add success toasts for task create/update/delete/toggle operations
- [ ] T098 [P] Add loading states to all buttons during async operations (disable button, show spinner)
- [ ] T099 [P] Add confirmation dialog for task deletion in TaskCard component
- [ ] T100 [P] Handle network errors (backend unreachable) with user-friendly message in API client
- [ ] T101 [P] Handle 500 errors with "Something went wrong. Please try again." message
- [ ] T102 [P] Handle validation errors (400) with specific field error messages
- [ ] T103 [P] Add retry mechanism for failed API calls (exponential backoff, max 3 retries)
- [ ] T104 [P] Test expired JWT token scenario (manually set expiration, verify redirect to /signin after 24h)
- [ ] T105 [P] Test empty description submission (should show validation error before API call)
- [ ] T106 [P] Test 501-character description (should show validation error before API call)

**Verification**:
```bash
# Test error handling
# 1. Stop backend server
# 2. Try to create task in frontend
# Expected: Toast notification "Unable to connect to server. Please try again."

# Test validation
# 1. Try to create task with empty description
# Expected: Error message "Task description cannot be empty"
# 2. Try to create task with 501 characters
# Expected: Error message "Task description cannot exceed 500 characters"

# Test loading states
# 1. Click "Add Task" button
# Expected: Button shows spinner and is disabled during API call

# Test confirmation dialog
# 1. Click delete button on task
# Expected: Confirmation dialog appears "Are you sure you want to delete this task?"
# 2. Click "Cancel"
# Expected: Dialog closes, task remains
# 3. Click delete again, click "Confirm"
# Expected: Task is deleted

# Test success notifications
# 1. Create task
# Expected: Green toast "Task created successfully"
# 2. Toggle task complete
# Expected: Green toast "Task marked as complete"
# 3. Update task
# Expected: Green toast "Task updated successfully"
# 4. Delete task
# Expected: Green toast "Task deleted successfully"

# Test JWT expiration (manual simulation)
# 1. Set token expiration to 1 minute (modify backend JWT config temporarily)
# 2. Wait 1 minute
# 3. Try to fetch tasks
# Expected: Automatically redirected to /signin with message "Session expired. Please log in again."
```

---

## Phase 11: Testing & Quality Assurance

**Goal**: Verify all functional requirements, success criteria, and quality gates

**Independent Test**: All 20 FRs verified, all 7 SCs met, test report documents 100% passing

### Tasks

- [ ] T107 Test FR-001: User registration with email/password validation (min 8 chars)
- [ ] T108 Test FR-002: User login returns JWT token signed with shared secret
- [ ] T109 Test FR-003: All task endpoints protected with JWT auth, return 401 without token
- [ ] T110 Test FR-004: user_id extracted from JWT claims, not URL parameters

---

## Phase 12: Documentation & Deployment Prep

**Goal**: Complete documentation for Phase 2, prepare for Phase 3

**Independent Test**: Quickstart guide can be followed by new developer, README accurate, demo video shows working app

### Tasks (Not shown for brevity - would include updating README, creating architecture diagrams, recording demo video)

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**User Story 1 (US1) + User Story 5 (US5)**: Authentication + Data Persistence
- Complete Phases 1-3 + Phase 5 (Setup → Security → API Documentation)
- Deliverable: Working authentication system with persistent user accounts

### Incremental Delivery Order

1. **Sprint 1** (Phases 1-3): Backend foundation + Authentication
2. **Sprint 2** (Phases 4-5): Task API + Documentation
3. **Sprint 3** (Phases 6-8): Frontend + Dashboard
4. **Sprint 4** (Phases 9-11): Responsive design + Testing + Polish

### Parallel Execution Opportunities

**Phase 1 Parallelizable** (can run simultaneously):
- T002-T005: Folder structure creation (different paths)
- T007-T008: .gitignore files (different services)
- T009-T010: Dependency configuration (backend vs frontend)

**Phase 2 Parallelizable**:
- T012, T013, T014: Database session, User model, Task model (independent files)

**Phase 3 Parallelizable**:
- T020-T021, T024-T025: Schema definitions and utility functions (independent)

**Phase 4 Parallelizable**:
- T029-T031: All schema definitions (independent files)

---

## Dependencies & Execution Order

### Critical Path (Must Complete Sequentially)

```
Phase 1 (Setup) → Phase 2 (Models) → Phase 3 (Auth) → Phase 4 (Task API)
    ↓
Phase 6 (Frontend Setup) → Phase 7 (Auth UI) → Phase 8 (Dashboard)
    ↓
Phase 9 (Responsive) → Phase 10 (Error Handling) → Phase 11 (Testing)
```

### Story Dependencies

- **US5 (Data Persistence)** → Blocks all other stories (foundational)
- **US1 (Authentication)** → Blocks US2, US3 (requires user identity)
- **US2 (Task Management)** → Blocks US3 (toggle requires task to exist)
- **US4 (Responsive Design)** → Independent, can be done in parallel with features

### File Dependencies

```
backend/app/database.py
    ├─→ backend/app/models/user.py
    ├─→ backend/app/models/task.py
    └─→ backend/app/middleware/auth.py
            └─→ backend/app/routers/auth.py
            └─→ backend/app/routers/tasks.py
                    └─→ backend/app/main.py

frontend/lib/types.ts
    ├─→ frontend/lib/api.ts
    └─→ frontend/lib/auth.ts
            └─→ frontend/app/(auth)/signup/page.tsx
            └─→ frontend/app/(auth)/signin/page.tsx
                    └─→ frontend/app/dashboard/page.tsx
                            └─→ frontend/components/TaskCard.tsx
                            └─→ frontend/components/TaskForm.tsx
```

---

## Verification Checklist

### Constitution Compliance

- [ ] All code generated from specifications (no manual coding)
- [ ] Forward compatibility maintained for Phase 3 (AI integration supported)
- [ ] Quality gates met (20 FRs, 7 SCs)
- [ ] Documentation complete (CLAUDE.md, README.md, ADRs)

### Functional Requirements (FR-001 to FR-020)

- [ ] FR-001: User registration with email/password validation
- [ ] FR-002: User login returns JWT token
- [ ] FR-003: All task endpoints protected with JWT auth
- [ ] FR-004: user_id extracted from JWT claims only
- [ ] FR-005: User isolation enforced (User A cannot access User B's tasks)
- [ ] FR-006: Data persists to Neon PostgreSQL
- [ ] FR-007: GET /api/tasks lists user's tasks
- [ ] FR-008: POST /api/tasks creates task
- [ ] FR-009: PUT /api/tasks/{id} updates task
- [ ] FR-010: PATCH /api/tasks/{id}/complete toggles status
- [ ] FR-011: DELETE /api/tasks/{id} deletes task
- [ ] FR-012: Task description validation (1-500 chars)
- [ ] FR-013: Appropriate HTTP status codes returned
- [ ] FR-014: Frontend signup/signin forms with validation
- [ ] FR-015: Task list displays with complete/incomplete distinction
- [ ] FR-016: UI controls for all task operations
- [ ] FR-017: Responsive layout (mobile/tablet/desktop)
- [ ] FR-018: API documentation at /docs
- [ ] FR-019: Authentication failures logged
- [ ] FR-020: Database errors handled gracefully

### Success Criteria (SC-001 to SC-007)

- [ ] SC-001: Account creation + first task within 3 minutes
- [ ] SC-002: Tasks persist after browser close and server restart
- [ ] SC-003: 100% user isolation (cross-user access blocked)
- [ ] SC-004: Works on mobile (375px), tablet (768px), desktop (1920px)
- [ ] SC-005: Handles 50 concurrent users
- [ ] SC-006: All 7 endpoints documented in /docs
- [ ] SC-007: User-friendly error messages (no stack traces)

---

**Tasks Status**: ✅ Ready for `/sp.implement` execution
**Total Task Count**: 110 tasks (45 parallelizable)
**Estimated Implementation Time**: 4-6 development sessions
**Next Command**: `/sp.implement` to begin code generation
