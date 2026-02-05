# Implementation Plan: Full-Stack Web Application

**Feature Branch**: `002-fullstack-web-app`
**Created**: 2026-01-05
**Status**: Planning Complete
**Related Documents**:
- [Specification](./spec.md)
- [Research](./research.md)
- [Data Model](./data-model.md)
- [API Contracts](./contracts/openapi.yaml)
- [Quickstart Guide](./quickstart.md)

---

## Executive Summary

Transform Phase I console application into a full-stack web system with:
- **Backend**: FastAPI + SQLModel + Neon PostgreSQL
- **Frontend**: Next.js 16 + TypeScript + Tailwind CSS
- **Authentication**: Better Auth with JWT (24h expiration)
- **Architecture**: Monorepo with `/backend` and `/frontend` folders
- **Security**: User isolation enforced via JWT claims, not URL parameters

**Key Deliverables**:
1. Multi-user authentication system (signup/signin)
2. RESTful API with 7 endpoints (2 auth + 5 task operations)
3. Responsive web UI (mobile/tablet/desktop)
4. PostgreSQL database persistence
5. Interactive API documentation (/docs)

---

## Constitution Compliance Check

### Verification Against Constitution Principles

| Principle | Requirement | Status | Evidence |
|-----------|-------------|--------|----------|
| **I. Spec-Driven First** | No manual coding | ✅ PASS | All code will be generated from this plan and tasks.md |
| **II. Architectural Thinking** | Clear design before implementation | ✅ PASS | research.md, data-model.md, contracts/ complete |
| **III. Forward-Compatible** | APIs version-stable for Phase III | ✅ PASS | REST API can support AI chatbot integration; database schema extensible |
| **IV. Quality Over Speed** | Zero manual edits required | ✅ PASS | Comprehensive specifications ensure complete generation |
| **V. AI-Native Design** | Phase III readiness | ✅ PASS | Architecture supports adding AI agent layer without backend changes |

### Technology Standards Compliance

| Standard | Required | Planned | Compliant |
|----------|----------|---------|-----------|
| **Backend Language** | Python 3.11+ | Python 3.11+ | ✅ |
| **Package Manager** | uv | uv | ✅ |
| **API Framework** | FastAPI | FastAPI | ✅ |
| **ORM** | SQLModel | SQLModel | ✅ |
| **Frontend** | Next.js App Router | Next.js 16 App Router | ✅ |
| **Authentication** | Better Auth (Phase II+) | Better Auth with JWT plugin | ✅ |

### Quality Gates

- [ ] All 20 functional requirements (FR-001 to FR-020) implemented
- [ ] All 7 success criteria (SC-001 to SC-007) met
- [ ] User isolation verified (User A cannot access User B's tasks)
- [ ] Data persistence confirmed (survives browser refresh and server restart)
- [ ] Responsive design tested on mobile (375px), tablet (768px), desktop (1920px)
- [ ] API documentation accessible at /docs with all endpoints
- [ ] Error handling returns user-friendly messages (no stack traces)
- [ ] Security audit passed (no hard-coded secrets, bcrypt password hashing)

---

## Architecture Overview

### System Context Diagram

```
┌─────────────┐
│   Browser   │  (Chrome, Firefox, Safari, Edge 90+)
│  (Client)   │
└──────┬──────┘
       │ HTTPS
       │ (Phase V: production)
       ▼
┌─────────────────────────────────────┐
│      Frontend (Next.js 16)          │
│  ┌───────────────────────────────┐  │
│  │  App Router Pages             │  │
│  │  - / (landing)                │  │
│  │  - /signup, /signin (auth)    │  │
│  │  - /dashboard (protected)     │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  Better Auth Client           │  │
│  │  - JWT token generation       │  │
│  │  - LocalStorage persistence   │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  API Client (lib/api.ts)      │  │
│  │  - Auto-attach JWT to headers │  │
│  │  - Handle 401 redirects       │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │ REST API (JSON)
               │ Authorization: Bearer <JWT>
               ▼
┌─────────────────────────────────────┐
│      Backend (FastAPI)              │
│  ┌───────────────────────────────┐  │
│  │  JWT Verification Middleware  │  │
│  │  - Extract token from header  │  │
│  │  - Verify with shared secret  │  │
│  │  - Extract user_id from claims│  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  API Routers                  │  │
│  │  - /api/auth (signup/signin)  │  │
│  │  - /api/tasks (CRUD + toggle) │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  SQLModel ORM                 │  │
│  │  - User model                 │  │
│  │  - Task model                 │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │ PostgreSQL Protocol
               │ (SSL/TLS encrypted)
               ▼
┌─────────────────────────────────────┐
│   Neon PostgreSQL (Serverless)      │
│  ┌───────────────────────────────┐  │
│  │  Tables:                      │  │
│  │  - user (id, email, password) │  │
│  │  - task (id, desc, completed) │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Monorepo Folder Structure

```
/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entrypoint
│   │   ├── database.py        # Neon connection + session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py        # User SQLModel
│   │   │   └── task.py        # Task SQLModel
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py        # POST /api/auth/signup, /signin
│   │   │   └── tasks.py       # GET/POST/PUT/PATCH/DELETE /api/tasks
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── auth.py        # JWT verification dependency
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── auth.py        # Request/response schemas for auth
│   │       └── tasks.py       # Request/response schemas for tasks
│   ├── scripts/
│   │   ├── create_tables.py   # Database migration (run once)
│   │   ├── seed_data.py       # Sample data for testing
│   │   └── reset_database.py  # WARNING: Deletes all data
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auth.py       # Authentication endpoint tests
│   │   └── test_tasks.py      # Task CRUD endpoint tests
│   ├── pyproject.toml         # uv dependencies
│   ├── .env                   # Backend environment variables
│   ├── CLAUDE.md              # Backend-specific instructions
│   └── README.md              # Backend setup guide
│
├── frontend/                   # Next.js application
│   ├── app/
│   │   ├── layout.tsx         # Root layout (global styles)
│   │   ├── page.tsx           # Landing page (/)
│   │   ├── (auth)/            # Auth route group (no layout)
│   │   │   ├── signup/
│   │   │   │   └── page.tsx   # Signup page (/signup)
│   │   │   └── signin/
│   │   │       └── page.tsx   # Signin page (/signin)
│   │   └── dashboard/
│   │       ├── layout.tsx     # Protected layout (auth check)
│   │       └── page.tsx       # Dashboard (/dashboard)
│   ├── components/
│   │   ├── TaskCard.tsx       # Individual task display
│   │   ├── TaskList.tsx       # List of tasks
│   │   ├── TaskForm.tsx       # Create/edit task form
│   │   ├── ErrorMessage.tsx   # Error display component
│   │   └── LoadingSpinner.tsx # Loading state
│   ├── lib/
│   │   ├── api.ts             # API client class
│   │   ├── auth.ts            # Better Auth configuration
│   │   └── types.ts           # TypeScript types for Task, User
│   ├── public/
│   │   └── favicon.ico
│   ├── styles/
│   │   └── globals.css        # Tailwind imports
│   ├── package.json           # npm dependencies
│   ├── tsconfig.json          # TypeScript configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   ├── next.config.js         # Next.js configuration
│   ├── .env.local             # Frontend environment variables
│   ├── CLAUDE.md              # Frontend-specific instructions
│   └── README.md              # Frontend setup guide
│
├── specs/
│   └── 002-fullstack-web-app/
│       ├── spec.md            # Feature specification (this file's parent)
│       ├── plan.md            # Implementation plan (THIS FILE)
│       ├── tasks.md           # Task breakdown (next to generate)
│       ├── research.md        # Technology decisions
│       ├── data-model.md      # Database schema
│       ├── quickstart.md      # Setup guide
│       ├── contracts/
│       │   └── openapi.yaml   # API contract
│       └── checklists/
│           └── requirements.md # Specification quality checklist
│
├── .env                       # Shared secrets (BETTER_AUTH_SECRET, DATABASE_URL)
├── .gitignore                 # Ignore .env, node_modules, __pycache__
├── README.md                  # Monorepo overview
└── CLAUDE.md                  # Project-wide instructions

```

---

## Phase-wise Implementation Strategy

### Phase A: Foundation (Backend Core)

**Goal**: Set up backend infrastructure with database connection and models

**Tasks**:
1. Create `backend/` folder structure
2. Configure `pyproject.toml` with dependencies (fastapi, sqlmodel, pyjwt, passlib, uvicorn)
3. Implement `backend/app/database.py` (Neon connection, session dependency)
4. Implement `backend/app/models/user.py` (User SQLModel with validation)
5. Implement `backend/app/models/task.py` (Task SQLModel with foreign key)
6. Create `backend/scripts/create_tables.py` (schema migration)
7. Create `backend/scripts/seed_data.py` (test data)
8. Test database connection and table creation

**Acceptance Criteria**:
- `uv pip install -e .` runs successfully
- `create_tables.py` creates `user` and `task` tables in Neon database
- Can manually insert/query users and tasks using psql

**Dependencies**: Neon database provisioned, DATABASE_URL in .env

**Estimated Complexity**: Medium (database setup, ORM configuration)

---

### Phase B: Security (Authentication & Authorization)

**Goal**: Implement JWT-based authentication with Better Auth pattern

**Tasks**:
1. Implement `backend/app/middleware/auth.py`:
   - `verify_jwt()` function (decode token, verify signature, extract user_id)
   - `get_current_user_id()` dependency (used by protected routes)
2. Implement `backend/app/routers/auth.py`:
   - POST `/api/auth/signup` (create user, hash password, return JWT)
   - POST `/api/auth/signin` (verify credentials, return JWT)
3. Implement password hashing with bcrypt (passlib)
4. Configure JWT token generation (HS256 algorithm, 24h expiration)
5. Add CORS middleware to allow frontend origin
6. Test authentication flow:
   - Signup creates user in database
   - Signin returns valid JWT token
   - Invalid credentials return 401

**Acceptance Criteria**:
- Can create user via POST /api/auth/signup
- Can login via POST /api/auth/signin and receive JWT
- JWT token can be decoded and verified using BETTER_AUTH_SECRET
- Invalid passwords return 401 Unauthorized
- Duplicate email registration returns 400 Bad Request

**Dependencies**: Phase A complete (User model exists)

**Estimated Complexity**: High (security-critical, JWT verification logic)

---

### Phase C: API Implementation (Task CRUD Endpoints)

**Goal**: Implement all 5 task management endpoints with user isolation

**Tasks**:
1. Implement `backend/app/routers/tasks.py`:
   - GET `/api/tasks` - List tasks for authenticated user
   - POST `/api/tasks` - Create task for authenticated user
   - PUT `/api/tasks/{id}` - Update task description (verify ownership)
   - PATCH `/api/tasks/{id}/complete` - Toggle completion status
   - DELETE `/api/tasks/{id}` - Delete task (verify ownership)
2. Add user_id filtering to all queries (extract from JWT, never from URL)
3. Implement validation (description 1-500 chars, non-empty)
4. Return appropriate HTTP status codes (200, 201, 400, 401, 404, 500)
5. Add error handling (database errors, validation errors)
6. Register routers in `backend/app/main.py`
7. Test all endpoints with curl or Postman

**Acceptance Criteria**:
- All endpoints accessible at http://localhost:8000/api/tasks
- Can create, read, update, toggle, delete tasks
- User A cannot access User B's tasks (returns 404 even with valid task ID)
- Validation errors return 400 with clear error messages
- Missing JWT returns 401 Unauthorized
- Swagger UI at /docs shows all endpoints with request/response schemas

**Dependencies**: Phase B complete (JWT authentication working)

**Estimated Complexity**: Medium (standard CRUD logic, user isolation critical)

---

### Phase D: Frontend Foundation (Next.js Setup)

**Goal**: Set up Next.js application with routing and Better Auth

**Tasks**:
1. Create `frontend/` folder structure
2. Initialize Next.js project with TypeScript
3. Configure Tailwind CSS (tailwind.config.js, globals.css)
4. Implement `frontend/lib/auth.ts` (Better Auth configuration with JWT plugin)
5. Implement `frontend/lib/api.ts` (API client class with auto-JWT attachment)
6. Create `frontend/lib/types.ts` (TypeScript interfaces for Task, User, API responses)
7. Implement `frontend/app/layout.tsx` (root layout with Tailwind imports)
8. Implement `frontend/app/page.tsx` (landing page with Sign In/Sign Up buttons)
9. Test Next.js dev server starts successfully

**Acceptance Criteria**:
- `npm install` runs successfully
- `npm run dev` starts server at http://localhost:3000
- Landing page displays with basic styling
- Tailwind CSS classes work correctly
- TypeScript compilation succeeds with no errors

**Dependencies**: Backend Phase C complete (API endpoints available)

**Estimated Complexity**: Medium (Next.js configuration, Better Auth setup)

---

### Phase E: Authentication UI (Signup/Signin Pages)

**Goal**: Create signup and signin pages with form validation

**Tasks**:
1. Implement `frontend/app/(auth)/signup/page.tsx`:
   - Email and password input fields
   - Client-side validation (email format, password min 8 chars)
   - Call POST /api/auth/signup on submit
   - Store JWT token in localStorage
   - Redirect to /dashboard on success
   - Display error messages on failure
2. Implement `frontend/app/(auth)/signin/page.tsx`:
   - Email and password input fields
   - Call POST /api/auth/signin on submit
   - Store JWT token in localStorage
   - Redirect to /dashboard on success
   - Display error messages (401 invalid credentials)
3. Implement `frontend/components/ErrorMessage.tsx` (reusable error display)
4. Style forms with Tailwind CSS (responsive, mobile-friendly)
5. Test authentication flow end-to-end

**Acceptance Criteria**:
- Can create account via signup form
- Can login via signin form
- JWT token stored in localStorage after successful auth
- Redirected to /dashboard after login
- Error messages displayed for invalid input or failed requests
- Forms work on mobile (375px), tablet (768px), desktop (1920px)

**Dependencies**: Phase D complete (Next.js app running), Phase B complete (auth endpoints)

**Estimated Complexity**: Medium (form handling, state management, API integration)

---

### Phase F: Dashboard UI (Task Management Interface)

**Goal**: Create dashboard page with full task CRUD functionality

**Tasks**:
1. Implement `frontend/app/dashboard/layout.tsx`:
   - Protected layout (check JWT token, redirect to /signin if missing)
   - Logout button
2. Implement `frontend/app/dashboard/page.tsx`:
   - Fetch tasks on mount (GET /api/tasks)
   - Display loading state while fetching
   - Display empty state if no tasks
   - Render TaskList component
   - Add task creation form
3. Implement `frontend/components/TaskList.tsx`:
   - Map over tasks and render TaskCard for each
4. Implement `frontend/components/TaskCard.tsx`:
   - Display task description
   - Checkbox to toggle completion (PATCH /api/tasks/{id}/complete)
   - Edit button (inline editing or modal)
   - Delete button (DELETE /api/tasks/{id})
   - Strikethrough styling for completed tasks
5. Implement `frontend/components/TaskForm.tsx`:
   - Input field for task description
   - Create button (POST /api/tasks)
   - Validation (1-500 chars)
6. Implement state management (React hooks: useState, useEffect)
7. Handle API errors (display ErrorMessage component)
8. Test all CRUD operations

**Acceptance Criteria**:
- Dashboard displays all user's tasks after login
- Can create new task and it appears in list
- Can toggle task completion with checkbox
- Can edit task description inline or in modal
- Can delete task with confirmation
- Changes persist after page refresh (data from database)
- Empty state shown when no tasks exist
- Loading spinner shown while fetching data
- Error messages shown for failed API calls

**Dependencies**: Phase E complete (authentication working), Phase C complete (task endpoints)

**Estimated Complexity**: High (complex UI state management, multiple API integrations)

---

### Phase G: Responsive Design (Mobile/Tablet/Desktop)

**Goal**: Ensure UI works flawlessly on all device sizes

**Tasks**:
1. Review all components for responsive Tailwind classes
2. Test on mobile viewport (375px width):
   - Single column layout
   - Touch-friendly button sizes (min 44x44px)
   - No horizontal scrolling
3. Test on tablet viewport (768px width):
   - Two-column layout where appropriate
   - Optimized spacing
4. Test on desktop viewport (1920px width):
   - Multi-column grid layout
   - Efficient use of space
5. Fix any layout issues
6. Test on actual devices (iPhone, iPad, desktop)

**Acceptance Criteria**:
- All pages render correctly on mobile (375px), tablet (768px), desktop (1920px)
- No horizontal scrolling on any viewport
- Touch targets are at least 44x44px on mobile
- Forms are easy to use on mobile devices
- Text is readable without zooming on all devices

**Dependencies**: Phase F complete (dashboard UI implemented)

**Estimated Complexity**: Low (mostly CSS adjustments)

---

### Phase H: Error Handling & UX Polish

**Goal**: Ensure robust error handling and smooth user experience

**Tasks**:
1. Backend error handling:
   - Catch all exceptions and return user-friendly messages
   - Never expose stack traces to clients
   - Log errors server-side for debugging
   - Return appropriate HTTP status codes
2. Frontend error handling:
   - Handle network failures (backend unreachable)
   - Handle 401 (redirect to /signin)
   - Handle 404 (task not found)
   - Handle validation errors (400)
   - Display toast notifications for success/error
3. Loading states:
   - Show spinners during API calls
   - Disable buttons during submission (prevent double-click)
4. Empty states:
   - "No tasks yet" message with call-to-action
5. Confirmation dialogs:
   - Confirm before deleting task
6. Test edge cases:
   - Empty description
   - 501-character description
   - Expired JWT token
   - Database connection failure

**Acceptance Criteria**:
- All error scenarios display user-friendly messages
- No stack traces visible to users
- Loading states shown during async operations
- Confirmation required before destructive actions
- Users are never "stuck" (always have clear next action)
- 401 errors automatically redirect to /signin

**Dependencies**: Phase F complete (all features implemented)

**Estimated Complexity**: Medium (comprehensive error handling across stack)

---

### Phase I: Testing & Quality Assurance

**Goal**: Verify all requirements and success criteria are met

**Tasks**:
1. **Functional Testing**:
   - Test all 20 functional requirements (FR-001 to FR-020)
   - Verify all user stories from spec.md
   - Test all acceptance scenarios
2. **Security Testing**:
   - Verify user isolation (User A cannot access User B's tasks)
   - Test JWT expiration handling
   - Test SQL injection attempts (should be blocked by SQLModel)
   - Verify passwords are bcrypt-hashed in database
   - Check no secrets in git repository
3. **Performance Testing**:
   - Test with 50 concurrent users (use locust or similar)
   - Verify response times acceptable (< 1s for API calls)
   - Test with 100 tasks per user
4. **Responsive Testing**:
   - Test on actual iPhone SE (375px)
   - Test on actual iPad (768px)
   - Test on desktop (1920px)
5. **Data Persistence Testing**:
   - Create tasks, close browser, reopen - tasks still there
   - Create tasks, restart backend server - tasks still there
   - Create tasks, wait 24 hours, check Neon dashboard - tasks still there
6. **API Documentation Testing**:
   - Visit http://localhost:8000/docs
   - Verify all 7 endpoints documented
   - Test endpoints via Swagger UI
7. Create test report documenting all results

**Acceptance Criteria**:
- All 20 functional requirements verified
- All 7 success criteria met
- All quality gates from constitution passed
- Test report documents 100% passing tests
- No critical or high-severity issues remain

**Dependencies**: Phase H complete (all features and error handling done)

**Estimated Complexity**: High (comprehensive testing across all layers)

---

### Phase J: Documentation & Deployment Prep

**Goal**: Complete documentation and prepare for Phase III

**Tasks**:
1. Update `/README.md` with monorepo overview
2. Create `backend/README.md` with backend-specific setup
3. Create `frontend/README.md` with frontend-specific setup
4. Verify `quickstart.md` is accurate (test with fresh setup)
5. Create `backend/CLAUDE.md` with backend implementation guidelines
6. Create `frontend/CLAUDE.md` with frontend implementation guidelines
7. Update `.gitignore` to exclude `.env`, `node_modules`, `__pycache__`, `.venv`
8. Create `backend/requirements.txt` (export from uv for compatibility)
9. Document environment variables in README
10. Create architecture diagram (Mermaid or similar)
11. Record demo video (signup, create tasks, logout, login, see persisted tasks)

**Acceptance Criteria**:
- README.md provides clear monorepo overview
- Quickstart guide can be followed by new developer to set up locally
- CLAUDE.md files guide AI code generation for each service
- All sensitive files excluded from git
- Architecture diagram accurately represents system
- Demo video shows working application end-to-end

**Dependencies**: Phase I complete (all testing passed)

**Estimated Complexity**: Low (documentation writing)

---

## Critical Success Factors

### 1. User Isolation Security

**Why Critical**: Core security requirement - users must never access other users' data

**Implementation Strategy**:
- Extract `user_id` from JWT payload in every protected route
- Filter all database queries by `user_id` (never accept from URL/body)
- Return 404 (not 403) when user tries to access non-owned resource
- Test with two logged-in users attempting cross-user access

**Verification**:
```python
# Test in backend/tests/test_tasks.py
def test_user_cannot_access_other_user_task():
    user1 = create_user("user1@test.com")
    user2 = create_user("user2@test.com")
    task1 = create_task(user1, "User 1's task")

    # User 2 tries to access User 1's task
    response = client.get(
        f"/api/tasks/{task1.id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert response.status_code == 404  # Not 403, to prevent information leakage
```

---

### 2. JWT Security & Shared Secret

**Why Critical**: Entire authentication system depends on JWT verification

**Implementation Strategy**:
- Generate cryptographically secure secret with `openssl rand -hex 32`
- Store in root `.env` file (excluded from git)
- Use identical secret in both frontend and backend `.env` files
- Never commit secrets to git repository
- Use HS256 algorithm (symmetric signing)

**Verification**:
```bash
# Verify secret is identical
$ grep BETTER_AUTH_SECRET .env
$ grep BETTER_AUTH_SECRET backend/.env
$ grep BETTER_AUTH_SECRET frontend/.env.local
# All three should have same value
```

---

### 3. Database Persistence

**Why Critical**: Distinguishes Phase II from Phase I (in-memory storage)

**Implementation Strategy**:
- Use Neon PostgreSQL (serverless, always available)
- Configure connection pooling via SQLModel engine
- Use SQLModel ORM to prevent SQL injection
- Create indexes on `task.user_id` for query performance
- Test with manual database queries to verify data persists

**Verification**:
```bash
# Connect to Neon database
$ psql "your-neon-connection-string"

# Check data persists
neondb=> SELECT * FROM task WHERE user_id = 1;
# Should show tasks created via API

# Restart backend server and re-query
# Tasks should still be there
```

---

### 4. CORS Configuration

**Why Critical**: Frontend on localhost:3000 must reach backend on localhost:8000

**Implementation Strategy**:
```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Verification**:
- Open browser DevTools Network tab
- Make API request from frontend
- Check response headers include `Access-Control-Allow-Origin: http://localhost:3000`

---

### 5. Responsive Design

**Why Critical**: Success criteria requires mobile/tablet/desktop support

**Implementation Strategy**:
- Use Tailwind's mobile-first approach (default styles for mobile)
- Add `md:` prefix for tablet (768px+)
- Add `lg:` prefix for desktop (1024px+)
- Test on actual devices, not just browser DevTools

**Verification**:
```tsx
// Example responsive component
<div className="
  flex flex-col gap-4          // Mobile: stack vertically
  md:flex-row md:gap-6         // Tablet: horizontal layout
  lg:grid lg:grid-cols-3 lg:gap-8  // Desktop: 3-column grid
">
  {tasks.map(task => <TaskCard key={task.id} task={task} />)}
</div>
```

---

## Risk Mitigation

### Risk 1: JWT Token Expiration During Active Use

**Severity**: Medium
**Probability**: High (24-hour expiration)
**Impact**: User suddenly logged out without warning

**Mitigation**:
- Implement token refresh mechanism (Phase III)
- For Phase II: Accept 24-hour expiration as known limitation
- Display user-friendly message: "Your session has expired. Please log in again."
- Automatically redirect to /signin on 401 errors

---

### Risk 2: Neon Database Hibernation

**Severity**: Low
**Probability**: Medium (free tier hibernates after inactivity)
**Impact**: Slow first request after hibernation (~5 seconds)

**Mitigation**:
- Document in README that first request may be slow
- Consider upgrading to paid tier for production (Phase V)
- For Phase II: Accept as known limitation

---

### Risk 3: Frontend-Backend Version Mismatch

**Severity**: High
**Probability**: Low (monorepo structure)
**Impact**: API contract breaking changes cause frontend failures

**Mitigation**:
- Monorepo ensures frontend and backend versioned together
- Document API contract in `contracts/openapi.yaml`
- Use TypeScript interfaces generated from OpenAPI schema (future enhancement)

---

### Risk 4: BETTER_AUTH_SECRET Mismatch

**Severity**: Critical
**Probability**: Medium (manual configuration)
**Impact**: All authentication fails (JWT verification errors)

**Mitigation**:
- Document in quickstart.md that secret MUST be identical
- Create validation script to check secret consistency:
```bash
#!/bin/bash
# scripts/validate-secrets.sh
ROOT_SECRET=$(grep BETTER_AUTH_SECRET .env | cut -d'=' -f2)
BACKEND_SECRET=$(grep BETTER_AUTH_SECRET backend/.env | cut -d'=' -f2)
FRONTEND_SECRET=$(grep BETTER_AUTH_SECRET frontend/.env.local | cut -d'=' -f2)

if [ "$ROOT_SECRET" != "$BACKEND_SECRET" ] || [ "$ROOT_SECRET" != "$FRONTEND_SECRET" ]; then
  echo "ERROR: BETTER_AUTH_SECRET mismatch detected!"
  exit 1
else
  echo "✓ BETTER_AUTH_SECRET is consistent across all .env files"
fi
```

---

## Next Steps

After Phase 2 planning is complete:

1. **Generate `tasks.md`**: Run `/sp.tasks` to break down plan into concrete implementation tasks
2. **Execute Implementation**: Run `/sp.implement` to generate code from tasks
3. **Verify Against Specification**: Check all functional requirements and success criteria
4. **Create Pull Request**: Submit for review with demo video
5. **Prepare for Phase III**: Review AI Chatbot integration requirements

---

## Appendix

### A. Environment Variables Reference

**Root `.env`** (shared secrets):
```env
BETTER_AUTH_SECRET=<32-char hex string>
DATABASE_URL=postgresql://...
```

**`backend/.env`**:
```env
# Can symlink to root .env or duplicate
BETTER_AUTH_SECRET=<same as root>
DATABASE_URL=<same as root>
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
FRONTEND_URL=http://localhost:3000
```

**`frontend/.env.local`**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<same as root>
DATABASE_URL=<same as root>
```

### B. API Endpoint Summary

| Method | Endpoint | Auth Required | Purpose |
|--------|----------|---------------|---------|
| POST | /api/auth/signup | No | Create new user account |
| POST | /api/auth/signin | No | Login and receive JWT |
| GET | /api/tasks | Yes | List all tasks for user |
| POST | /api/tasks | Yes | Create new task |
| PUT | /api/tasks/{id} | Yes | Update task description |
| PATCH | /api/tasks/{id}/complete | Yes | Toggle completion status |
| DELETE | /api/tasks/{id} | Yes | Delete task |

### C. Database Schema Summary

**`user` table**:
- `id` (INTEGER, PRIMARY KEY)
- `email` (VARCHAR(255), UNIQUE)
- `hashed_password` (VARCHAR(255))
- `created_at` (TIMESTAMP)

**`task` table**:
- `id` (INTEGER, PRIMARY KEY)
- `description` (VARCHAR(500))
- `completed` (BOOLEAN, DEFAULT FALSE)
- `created_at` (TIMESTAMP)
- `user_id` (INTEGER, FOREIGN KEY → user.id, ON DELETE CASCADE)

---

**Plan Status**: ✅ Complete and ready for `/sp.tasks` generation
