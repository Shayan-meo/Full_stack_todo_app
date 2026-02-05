# Quickstart Guide: Phase II Full-Stack Web Application

**Feature**: 002-fullstack-web-app
**Created**: 2026-01-05
**Purpose**: Step-by-step setup instructions for local development

## Prerequisites

Before starting, ensure you have:

- [x] **Python 3.11+** installed (`python --version`)
- [x] **Node.js 20+** installed (`node --version`)
- [x] **uv** package manager installed (`uv --version`)
- [x] **Git** for version control
- [x] **Neon PostgreSQL** account (sign up at https://neon.tech)
- [x] Code editor (VS Code recommended)

---

## Part 1: Database Setup (Neon PostgreSQL)

### Step 1: Create Neon Database

1. Visit https://neon.tech and sign in
2. Click "New Project"
3. Configure:
   - **Project Name**: `todo-app-phase2`
   - **Region**: Choose closest to your location
   - **PostgreSQL Version**: 15+ (default)
4. Click "Create Project"
5. **Copy the connection string** from dashboard:
   ```
   postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
   ```

### Step 2: Test Database Connection

```bash
# Install psql client (if not already installed)
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql-client
# Windows: Download from https://www.postgresql.org/download/windows/

# Test connection (replace with your connection string)
psql "postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require"

# If connected successfully, you'll see:
# neondb=>

# Exit with \q
```

---

## Part 2: Monorepo Setup

### Step 3: Clone Repository and Checkout Branch

```bash
# Navigate to project directory
cd "C:\Users\SHAYAN\OneDrive\Desktop\Hackathon Two\Todo-list"

# Ensure you're on the correct branch
git checkout 002-fullstack-web-app

# Verify branch
git branch
# Should show: * 002-fullstack-web-app
```

### Step 4: Create Environment Configuration

Create a `.env` file at the **repository root** (not in backend/ or frontend/):

```bash
# Create .env file
touch .env  # macOS/Linux
# or manually create on Windows
```

Add the following content to `.env`:

```env
# Shared Secret (generate with: openssl rand -hex 32)
BETTER_AUTH_SECRET=your-secret-key-here-replace-with-random-32-char-hex

# Neon PostgreSQL Connection String
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require

# Backend Configuration
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Frontend Configuration (for backend CORS)
FRONTEND_URL=http://localhost:3000
```

**Important**: Replace placeholder values:
1. Generate `BETTER_AUTH_SECRET`:
   ```bash
   # Generate random 32-character hex string
   openssl rand -hex 32
   ```
2. Replace `DATABASE_URL` with your Neon connection string from Step 1

### Step 5: Create Backend Environment File

```bash
# Navigate to backend
cd backend

# Create .env file (symlink to root .env)
# macOS/Linux:
ln -s ../.env .env

# Windows (run as administrator):
mklink .env ..\.env

# Or manually copy ../. env content to backend/.env
```

### Step 6: Create Frontend Environment File

```bash
# Navigate to frontend
cd ../frontend

# Create .env.local file
touch .env.local  # macOS/Linux or create manually on Windows
```

Add the following to `frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration (must match backend)
BETTER_AUTH_SECRET=your-secret-key-here-same-as-root-env

# Database URL (for Better Auth)
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

**Important**: Use the **same** `BETTER_AUTH_SECRET` value from root `.env`

---

## Part 3: Backend Setup

### Step 7: Install Backend Dependencies

```bash
# Navigate to backend folder
cd ../backend

# Create virtual environment and install dependencies
uv venv
uv pip install -e .

# Verify installation
uv pip list
# Should show: fastapi, sqlmodel, pyjwt, passlib, uvicorn, etc.
```

### Step 8: Create Database Tables

```bash
# Run database migration script
uv run python scripts/create_tables.py

# Expected output:
# ✓ Tables created successfully
```

### Step 9: (Optional) Seed Test Data

```bash
# Create sample user and tasks for testing
uv run python scripts/seed_data.py

# Expected output:
# ✓ Created user: test@example.com with 3 tasks
```

**Test Credentials**:
- Email: `test@example.com`
- Password: `password123`

### Step 10: Start Backend Server

```bash
# Start FastAPI development server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
# INFO:     Started server process
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

**Verify Backend**:
1. Open browser: http://localhost:8000/docs
2. You should see FastAPI Swagger UI with all API endpoints
3. Test health check: http://localhost:8000/health (should return `{"status": "ok"}`)

**Leave this terminal running** and open a new terminal for frontend setup.

---

## Part 4: Frontend Setup

### Step 11: Install Frontend Dependencies

```bash
# Navigate to frontend folder (in new terminal)
cd "C:\Users\SHAYAN\OneDrive\Desktop\Hackathon Two\Todo-list\frontend"

# Install dependencies
npm install

# Verify installation
npm list --depth=0
# Should show: next, react, tailwindcss, better-auth, etc.
```

### Step 12: Start Frontend Development Server

```bash
# Start Next.js development server
npm run dev

# Expected output:
# - ready started server on 0.0.0.0:3000, url: http://localhost:3000
# - info  Loaded env from .env.local
# - event compiled client and server successfully
```

**Verify Frontend**:
1. Open browser: http://localhost:3000
2. You should see the landing page with "Sign In" and "Sign Up" buttons

**Leave this terminal running**. You now have both backend and frontend running!

---

## Part 5: Verify Full Stack Integration

### Step 13: Test Authentication Flow

1. **Navigate to Signup**:
   - Click "Sign Up" button on landing page
   - Or visit http://localhost:3000/signup

2. **Create Account**:
   - Email: `yourname@example.com`
   - Password: `testpass123` (minimum 8 characters)
   - Click "Sign Up"

3. **Verify Success**:
   - Should redirect to http://localhost:3000/dashboard
   - Should see empty task list message: "No tasks yet. Create your first task!"

### Step 14: Test Task CRUD Operations

1. **Create Task**:
   - Click "Add Task" button
   - Enter: "Test task from quickstart"
   - Click "Create"
   - Task should appear in list

2. **Toggle Completion**:
   - Click checkbox next to task
   - Task description should get strikethrough style
   - Click again to mark incomplete

3. **Update Task**:
   - Click "Edit" button on task
   - Change description to "Updated test task"
   - Click "Save"
   - Task description should update

4. **Delete Task**:
   - Click "Delete" button (trash icon)
   - Confirm deletion
   - Task should disappear from list

5. **Verify Persistence**:
   - Refresh browser (F5)
   - Tasks should still be there (loaded from database)

### Step 15: Test User Isolation

1. **Open Incognito Window**:
   - Open http://localhost:3000 in incognito/private browsing mode

2. **Create Second User**:
   - Sign up with different email: `user2@example.com`
   - Password: `password456`

3. **Create Different Tasks**:
   - Create 2-3 tasks with different descriptions

4. **Verify Isolation**:
   - User 2 should NOT see User 1's tasks
   - Switch back to original browser window
   - User 1 should NOT see User 2's tasks

✅ **Success!** User isolation is working correctly.

---

## Part 6: Development Workflow

### Running Both Services

**Terminal 1 - Backend**:
```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

### Useful Commands

**Backend**:
```bash
# Run tests
cd backend
uv run pytest

# Format code
uv run black app/

# Type checking
uv run mypy app/

# Database reset (WARNING: Deletes all data)
uv run python scripts/reset_database.py
```

**Frontend**:
```bash
# Run linter
npm run lint

# Type check
npm run type-check

# Build production bundle
npm run build

# Start production server
npm run start
```

### Viewing Logs

**Backend Logs**:
- Uvicorn outputs logs to console
- Check for SQL queries (if `echo=True` in database.py)
- Authentication failures logged automatically

**Frontend Logs**:
- Next.js logs in terminal
- Browser console (F12) for client-side errors
- Network tab (F12) to inspect API requests

---

## Part 7: Troubleshooting

### Common Issues

#### Issue 1: "Connection refused" when accessing backend

**Symptoms**: Frontend cannot reach http://localhost:8000

**Solutions**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local` matches backend URL
3. Ensure backend is bound to `0.0.0.0` not `127.0.0.1`
4. Check firewall/antivirus not blocking port 8000

#### Issue 2: "Invalid token" errors

**Symptoms**: 401 Unauthorized when accessing /api/tasks

**Solutions**:
1. Verify `BETTER_AUTH_SECRET` is **identical** in root `.env` and `frontend/.env.local`
2. Check token is being sent in Authorization header (inspect in browser Network tab)
3. Token might be expired (24h expiration) - try logging in again
4. Clear localStorage and cookies, then login again

#### Issue 3: Database connection errors

**Symptoms**: `could not connect to server` or `SSL error`

**Solutions**:
1. Verify `DATABASE_URL` is correct and includes `?sslmode=require`
2. Check Neon project is not hibernated (visit Neon dashboard to wake it)
3. Ensure your IP is not blocked (Neon allows all IPs by default)
4. Test connection with `psql` command from Step 2

#### Issue 4: "Email already registered" when signing up

**Symptoms**: Cannot create account with email used before

**Solutions**:
1. Use a different email address
2. Or delete the user from database:
   ```sql
   psql "your-connection-string"
   DELETE FROM "user" WHERE email = 'yourname@example.com';
   ```

#### Issue 5: Frontend shows "Network Error"

**Symptoms**: API requests fail with generic network error

**Solutions**:
1. Open browser DevTools (F12) → Network tab
2. Check if requests are reaching backend (should see requests to localhost:8000)
3. Verify CORS is configured correctly in backend
4. Check `FRONTEND_URL` in backend `.env` matches frontend URL

### Getting Help

If issues persist:
1. Check backend logs for detailed error messages
2. Check browser console (F12) for frontend errors
3. Review `/specs/002-fullstack-web-app/spec.md` for requirements
4. Review `/specs/002-fullstack-web-app/research.md` for architectural decisions

---

## Part 8: Next Steps

Now that Phase II is running locally:

1. **Explore the Code**:
   - Backend: `/backend/app/routers/tasks.py` (API endpoints)
   - Frontend: `/frontend/app/dashboard/page.tsx` (main UI)
   - Data models: `/backend/app/models/` (SQLModel classes)

2. **Review Documentation**:
   - API docs: http://localhost:8000/docs (FastAPI Swagger UI)
   - Specifications: `/specs/002-fullstack-web-app/spec.md`
   - Architecture plan: `/specs/002-fullstack-web-app/plan.md`

3. **Test Edge Cases**:
   - Try creating task with empty description (should fail)
   - Try creating task with 501 characters (should fail)
   - Try accessing another user's task ID directly (should fail)

4. **Prepare for Phase III**:
   - Read `/specs/003-ai-chatbot/` (when available)
   - Consider AI integration points (natural language task creation)

---

## Quick Reference

### Ports

| Service | Port | URL |
|---------|------|-----|
| Backend API | 8000 | http://localhost:8000 |
| API Documentation | 8000 | http://localhost:8000/docs |
| Frontend | 3000 | http://localhost:3000 |

### Test Credentials (if seeded)

| Email | Password |
|-------|----------|
| test@example.com | password123 |

### Key Files

| File | Purpose |
|------|---------|
| `/.env` | Shared secrets (root) |
| `/backend/.env` | Backend environment vars |
| `/frontend/.env.local` | Frontend environment vars |
| `/backend/app/main.py` | FastAPI application entry point |
| `/frontend/app/layout.tsx` | Next.js root layout |
| `/specs/002-fullstack-web-app/spec.md` | Feature specification |
| `/specs/002-fullstack-web-app/contracts/openapi.yaml` | API contract |

---

**Congratulations!** 🎉 You now have a fully functional full-stack web application with authentication, database persistence, and user isolation running locally.

Ready for Phase III (AI Chatbot Integration)?
