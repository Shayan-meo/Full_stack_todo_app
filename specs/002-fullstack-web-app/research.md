# Phase II Research: Technology Decisions & Best Practices

**Feature**: 002-fullstack-web-app
**Created**: 2026-01-05
**Purpose**: Document research findings and technology decisions for Full-Stack Web Application implementation

## Overview

This document captures architectural research, technology decisions, and best practices for transforming the Phase I console application into a full-stack web system with authentication, database persistence, and responsive UI.

## Research Areas

### 1. Monorepo Structure for Full-Stack TypeScript/Python Applications

**Decision**: Single monorepo with `/frontend` and `/backend` folders at repository root

**Rationale**:
- **Simplified Development**: Developers can work on both frontend and backend in single clone/branch
- **Atomic Commits**: Related frontend/backend changes can be committed together
- **Shared Configuration**: Single `.env` file at root can contain shared secrets (BETTER_AUTH_SECRET, DATABASE_URL)
- **Easier CI/CD**: Single repository simplifies deployment pipelines
- **Version Coherence**: Frontend and backend versions stay synchronized

**Alternatives Considered**:
- **Multi-repo (separate git repositories)**: Rejected because it complicates local development setup, requires managing two branches/PRs for related changes, and makes it harder to maintain contract consistency
- **Workspace monorepo (Nx, Turborepo)**: Rejected as over-engineering for Hackathon scope - adds complexity without delivering value for 2-service architecture

**Implementation Pattern**:
```
/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── models/          # SQLModel classes
│   │   ├── routers/         # API endpoints
│   │   ├── middleware/      # JWT auth middleware
│   │   └── database.py      # Neon PostgreSQL connection
│   ├── pyproject.toml
│   ├── .env                 # Backend env vars
│   └── CLAUDE.md            # Backend-specific instructions
├── frontend/
│   ├── app/                 # Next.js App Router
│   │   ├── (auth)/         # Auth pages (signup, signin)
│   │   ├── dashboard/       # Protected dashboard
│   │   └── layout.tsx
│   ├── components/          # React components
│   ├── lib/
│   │   ├── api.ts          # API client with JWT
│   │   └── auth.ts         # Better Auth setup
│   ├── .env.local           # Frontend env vars
│   └── CLAUDE.md            # Frontend-specific instructions
├── .env                     # Shared secrets (root level)
├── README.md                # Monorepo setup guide
└── specs/                   # Specifications
```

**Best Practices**:
- Keep `BETTER_AUTH_SECRET` and `DATABASE_URL` in root `.env` file
- Use relative imports within each service
- Document cross-service contracts in `/specs/002-fullstack-web-app/contracts/`
- Each service (frontend/backend) has independent dependency management (package.json, pyproject.toml)

---

### 2. JWT Authentication with Better Auth + FastAPI Integration

**Decision**: Use Better Auth for JWT generation (frontend) and manual JWT verification in FastAPI (backend) using shared secret

**Rationale**:
- **Better Auth Simplicity**: Better Auth provides production-ready JWT generation with minimal configuration
- **Framework Agnostic**: JWT verification in FastAPI is straightforward using `pyjwt` library - no tight coupling to specific auth framework
- **Shared Secret Pattern**: Single `BETTER_AUTH_SECRET` environment variable enables both services to sign/verify tokens
- **Stateless**: JWT tokens eliminate need for session storage in database

**Alternatives Considered**:
- **NextAuth.js**: Rejected because Better Auth is specifically requested in requirements and provides cleaner JWT plugin architecture
- **FastAPI OAuth2PasswordBearer**: Rejected as it couples backend to OAuth2 flow - we need simple JWT verification, not full OAuth2 server
- **Custom JWT implementation**: Rejected due to security risks - using established libraries (Better Auth + pyjwt) is safer

**Implementation Pattern**:

**Frontend (Better Auth)**:
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  plugins: [
    jwt({
      expiresIn: "24h",
      algorithm: "HS256"
    })
  ],
  database: {
    provider: "neon",
    url: process.env.DATABASE_URL!
  }
});
```

**Backend (FastAPI JWT Verification)**:
```python
# backend/app/middleware/auth.py
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()

def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """Extract and verify JWT token, return user claims"""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )
        return payload  # Contains user_id, email, exp
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Best Practices**:
- Always extract `user_id` from JWT payload (payload["sub"] or payload["user_id"]), never from URL
- Set token expiration to 24 hours (acceptable for Phase II scope)
- Return 401 Unauthorized for expired/invalid tokens
- Log authentication failures for security auditing (FR-019)

---

### 3. Neon PostgreSQL Integration with SQLModel

**Decision**: Use Neon Serverless PostgreSQL with SQLModel ORM for database access

**Rationale**:
- **Serverless**: No database server management - automatic scaling and hibernation
- **Developer Experience**: Instant database provisioning via Neon dashboard
- **SQLModel**: Type-safe ORM that integrates FastAPI Pydantic models with database schemas
- **PostgreSQL Compatibility**: Full PostgreSQL feature set (ACID transactions, foreign keys, indexes)

**Alternatives Considered**:
- **SQLite**: Rejected because it doesn't support concurrent writes and isn't suitable for production web applications
- **Raw SQL with psycopg2**: Rejected due to lack of type safety and increased boilerplate
- **SQLAlchemy Core**: Rejected because SQLModel provides simpler API while maintaining full SQLAlchemy power

**Implementation Pattern**:

**Database Connection**:
```python
# backend/app/database.py
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # From Neon dashboard
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    """Dependency for FastAPI routes"""
    with Session(engine) as session:
        yield session
```

**SQLModel Classes**:
```python
# backend/app/models/user.py
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# backend/app/models/task.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field(max_length=500)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
```

**Best Practices**:
- Use connection pooling for production (SQLModel handles this via engine)
- Always use parameterized queries (SQLModel does this automatically)
- Create indexes on `user_id` foreign key for query performance
- Enable `echo=True` in development for SQL debugging, disable in production

**Migration Strategy**:
```python
# backend/app/create_tables.py
from sqlmodel import SQLModel
from app.database import engine
from app.models.user import User
from app.models.task import Task

def create_tables():
    """Run once to create database schema"""
    SQLModel.metadata.create_all(engine)
```

---

### 4. Next.js 16 App Router Architecture

**Decision**: Use Next.js App Router with TypeScript, React Server Components, and client-side data fetching

**Rationale**:
- **App Router**: Modern Next.js architecture with file-based routing, nested layouts, and server components
- **Type Safety**: TypeScript provides compile-time safety for API contracts
- **Server Components**: Reduce JavaScript bundle size by default (use "use client" only when needed)
- **Flexibility**: Easy to add SSR/SSG in Phase III if needed

**Alternatives Considered**:
- **Pages Router**: Rejected because App Router is recommended for new Next.js projects (v13+)
- **Remix**: Rejected because hackathon specifies Next.js
- **Create React App**: Rejected due to lack of SSR capabilities and framework obsolescence

**Implementation Pattern**:

**Route Structure**:
```
frontend/app/
├── (auth)/                    # Auth group (no layout)
│   ├── signup/
│   │   └── page.tsx          # /signup route
│   └── signin/
│       └── page.tsx          # /signin route
├── dashboard/
│   ├── layout.tsx            # Protected layout
│   └── page.tsx              # /dashboard route (main tasks page)
├── layout.tsx                # Root layout (global styles)
└── page.tsx                  # / route (landing page)
```

**API Client Pattern**:
```typescript
// frontend/lib/api.ts
export class APIClient {
  private baseURL: string;
  private getToken: () => string | null;

  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_API_URL!;
    this.getToken = () => localStorage.getItem("auth_token");
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();
    const headers = {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Redirect to login on unauthorized
        window.location.href = "/signin";
      }
      throw new Error(`API error: ${response.status}`);
    }

    return response.json();
  }

  // Task methods
  async getTasks() {
    return this.request<Task[]>("/api/tasks");
  }

  async createTask(description: string) {
    return this.request<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify({ description }),
    });
  }

  async updateTask(id: number, description: string) {
    return this.request<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify({ description }),
    });
  }

  async toggleTask(id: number) {
    return this.request<Task>(`/api/tasks/${id}/complete`, {
      method: "PATCH",
    });
  }

  async deleteTask(id: number) {
    return this.request<void>(`/api/tasks/${id}`, {
      method: "DELETE",
    });
  }
}

export const api = new APIClient();
```

**Best Practices**:
- Use "use client" directive only for components with interactivity (forms, buttons)
- Store JWT in httpOnly cookies (more secure) or localStorage (simpler for Phase II)
- Handle 401 responses globally by redirecting to /signin
- Use React Query or SWR for caching API responses (Phase III enhancement)

---

### 5. Tailwind CSS Responsive Design Strategy

**Decision**: Use Tailwind CSS utility-first approach with mobile-first responsive breakpoints

**Rationale**:
- **Utility-First**: Rapid UI development without writing custom CSS
- **Responsive Modifiers**: Built-in `sm:`, `md:`, `lg:` breakpoints align with requirements (< 768px, 768-1024px, > 1024px)
- **Design Consistency**: Tailwind's design system ensures consistent spacing, colors, and typography
- **Tree-Shaking**: Unused styles automatically removed in production build

**Alternatives Considered**:
- **CSS Modules**: Rejected due to verbosity and lack of built-in design system
- **Styled Components**: Rejected because it adds runtime overhead and requires client-side JavaScript
- **Bootstrap**: Rejected due to heavy bundle size and opinionated component styling

**Implementation Pattern**:

**Responsive Breakpoints** (match FR-017):
```tsx
// Mobile-first approach
<div className="
  flex flex-col gap-4           // Mobile (default): Stack vertically
  md:flex-row md:gap-6          // Tablet (768px+): Horizontal layout
  lg:grid lg:grid-cols-3 lg:gap-8  // Desktop (1024px+): 3-column grid
">
  {/* Content */}
</div>
```

**Component Example** (Task Card):
```tsx
// components/TaskCard.tsx
"use client";

interface TaskCardProps {
  task: Task;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
}

export function TaskCard({ task, onToggle, onDelete }: TaskCardProps) {
  return (
    <div className="
      flex items-center gap-3 p-4
      bg-white rounded-lg shadow-sm
      hover:shadow-md transition-shadow
      border border-gray-200
    ">
      <button
        onClick={() => onToggle(task.id)}
        className="flex-shrink-0 w-6 h-6 rounded border-2
                   border-gray-300 hover:border-blue-500
                   flex items-center justify-center"
        aria-label="Toggle complete"
      >
        {task.completed && (
          <svg className="w-4 h-4 text-blue-500" /* checkmark icon */ />
        )}
      </button>

      <span className={`
        flex-1 text-sm md:text-base
        ${task.completed ? 'line-through text-gray-400' : 'text-gray-900'}
      `}>
        {task.description}
      </span>

      <button
        onClick={() => onDelete(task.id)}
        className="flex-shrink-0 p-2 text-red-500 hover:bg-red-50 rounded"
        aria-label="Delete task"
      >
        <svg className="w-5 h-5" /* trash icon */ />
      </button>
    </div>
  );
}
```

**Best Practices**:
- Use mobile-first approach (default styles for mobile, then add `md:` and `lg:` modifiers)
- Ensure touch targets are at least 44x44px on mobile (accessibility)
- Use `hover:` states only on `md:` and above (avoid on mobile touch devices)
- Test on actual devices: iPhone SE (375px), iPad (768px), Desktop (1920px)

---

### 6. User Isolation Security Pattern

**Decision**: Extract `user_id` from JWT payload and filter all database queries by this user_id

**Rationale**:
- **Zero Trust**: Never trust user_id from URL parameters or request body
- **Single Source of Truth**: JWT is cryptographically signed, cannot be tampered with
- **Automatic Enforcement**: Middleware extracts user_id once, all routes use it for filtering

**Alternatives Considered**:
- **Session-based**: Rejected because JWT is stateless and aligns with Better Auth architecture
- **Row-Level Security (RLS) in PostgreSQL**: Rejected as over-engineering for Phase II - application-level filtering is sufficient

**Implementation Pattern**:

**Middleware** (extract user_id once):
```python
# backend/app/middleware/auth.py
from fastapi import Depends, HTTPException
from sqlmodel import Session

async def get_current_user_id(
    payload: dict = Depends(verify_jwt)
) -> int:
    """Extract user_id from JWT payload"""
    user_id = payload.get("sub") or payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token structure")
    return int(user_id)
```

**Route Protection** (automatically filter by user_id):
```python
# backend/app/routers/tasks.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.middleware.auth import get_current_user_id
from app.database import get_session
from app.models.task import Task

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/")
def list_tasks(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> list[Task]:
    """Get all tasks for authenticated user (FR-007)"""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

@router.post("/")
def create_task(
    description: str,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> Task:
    """Create task for authenticated user (FR-008)"""
    task = Task(description=description, user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.put("/{task_id}")
def update_task(
    task_id: int,
    description: str,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> Task:
    """Update task if owned by user (FR-009)"""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    task.description = description
    session.commit()
    session.refresh(task)
    return task
```

**Best Practices**:
- Always check `task.user_id == user_id` before any update/delete operation
- Return 404 (not 403) when user tries to access other user's task - prevents information leakage
- Log authorization failures for security auditing (FR-019)
- Never accept user_id from request body or URL - always from JWT

---

### 7. Error Handling & User Experience

**Decision**: Return user-friendly error messages with appropriate HTTP status codes, never expose stack traces

**Rationale**:
- **Security**: Stack traces leak implementation details that attackers can exploit
- **User Experience**: Users need actionable error messages (e.g., "Password must be at least 8 characters")
- **Standards Compliance**: Proper HTTP status codes enable clients to handle errors appropriately

**Implementation Pattern**:

**Backend (FastAPI)**:
```python
# backend/app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catch all exceptions and return user-friendly errors (FR-020)"""
    # Log full traceback for debugging
    import traceback
    print(traceback.format_exc())

    # Return generic error to user
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Return structured error responses (FR-013)"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

**Frontend (React)**:
```tsx
// components/ErrorMessage.tsx
interface ErrorMessageProps {
  error: string;
  onDismiss?: () => void;
}

export function ErrorMessage({ error, onDismiss }: ErrorMessageProps) {
  return (
    <div className="
      p-4 mb-4 bg-red-50 border border-red-200 rounded-lg
      flex items-center justify-between
    ">
      <div className="flex items-center gap-3">
        <svg className="w-5 h-5 text-red-500" /* error icon */ />
        <span className="text-sm text-red-700">{error}</span>
      </div>
      {onDismiss && (
        <button onClick={onDismiss} className="text-red-500 hover:text-red-700">
          <svg className="w-4 h-4" /* close icon */ />
        </button>
      )}
    </div>
  );
}
```

**HTTP Status Code Standards** (FR-013):
- **200 OK**: Successful GET/PUT/PATCH request
- **201 Created**: Successful POST request (task created)
- **204 No Content**: Successful DELETE request
- **400 Bad Request**: Invalid input (empty description, too long, etc.)
- **401 Unauthorized**: Missing/invalid JWT token
- **404 Not Found**: Task doesn't exist or doesn't belong to user
- **500 Internal Server Error**: Database connection failure, unexpected errors

**Best Practices**:
- Log all errors server-side with full stack traces
- Return user-friendly messages client-side (no technical jargon)
- Use Toast notifications for transient errors
- Use Error boundaries in React for component-level error handling

---

## Summary of Key Decisions

| Area | Decision | Primary Rationale |
|------|----------|------------------|
| **Repository Structure** | Single monorepo with /frontend and /backend | Simplifies development, atomic commits, shared env vars |
| **Authentication** | Better Auth (JWT generation) + FastAPI manual verification | Framework agnostic, shared secret pattern, stateless |
| **Database** | Neon PostgreSQL + SQLModel ORM | Serverless, type-safe ORM, PostgreSQL compatibility |
| **Frontend Framework** | Next.js 16 App Router + TypeScript | Modern architecture, type safety, SSR capabilities |
| **Styling** | Tailwind CSS utility-first | Rapid development, built-in responsive system, tree-shaking |
| **User Isolation** | JWT payload extraction + query filtering | Zero trust, single source of truth, automatic enforcement |
| **Error Handling** | User-friendly messages + standard HTTP codes | Security, UX, standards compliance |

## Next Steps

With research complete, proceed to:
1. **Phase 1**: Create `data-model.md` (User and Task entities)
2. **Phase 1**: Generate API contracts in `/contracts/` (OpenAPI schema)
3. **Phase 1**: Write `quickstart.md` (local development setup guide)
4. **Phase 2**: Finalize `plan.md` with phase-wise implementation tasks
