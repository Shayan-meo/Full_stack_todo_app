---
id: 002
title: Phase 2 Implementation Planning
stage: plan
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-fullstack-web-app
branch: 002-fullstack-web-app
user: SHAYAN
command: /sp.plan
labels: ["phase2", "architecture", "fullstack", "planning", "monorepo", "jwt-auth", "postgresql"]
links:
  spec: specs/002-fullstack-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-fullstack-web-app/research.md
  - specs/002-fullstack-web-app/data-model.md
  - specs/002-fullstack-web-app/contracts/openapi.yaml
  - specs/002-fullstack-web-app/quickstart.md
  - specs/002-fullstack-web-app/plan.md
tests:
  - Constitution compliance check: PASS (all 5 principles verified)
  - Technology standards compliance: PASS (Python 3.11+, FastAPI, SQLModel, Next.js)
---

## Prompt

User requested Phase 2 implementation planning via /sp.plan with comprehensive architectural requirements:

"Based on Phase II Specification at specs/002-fullstack-web-app/spec.md, generate comprehensive implementation plan for full-stack web application. Architecture: Monorepo with /backend (FastAPI + SQLModel + Neon PostgreSQL) and /frontend (Next.js 16+ App Router + TypeScript + Tailwind CSS + Better Auth). Key planning areas: (1) Monorepo structure with shared .env for BETTER_AUTH_SECRET and DATABASE_URL, (2) Backend database schema (User and Task SQLModel classes with foreign key relationship), (3) Backend auth middleware to extract/verify JWT and enforce user isolation, (4) Backend REST API endpoints (GET/POST/PUT/PATCH/DELETE /api/tasks with user_id filtering from JWT claims not URL), (5) Frontend Better Auth JWT plugin setup, (6) Frontend API client (lib/api.ts) auto-attaching JWT to all requests, (7) Frontend Tailwind UI components for dashboard (empty states, loading states, CRUD modals/inline forms), (8) Quality gates (401 for missing token, user isolation blocking cross-user access, DB persistence verification in Neon dashboard), (9) Phase-wise execution: Phase A (Neon DB + Backend models), Phase B (Better Auth + JWT verification middleware), Phase C (Frontend-Backend API integration), Phase D (Tailwind styling + final verification). Security critical: user_id extracted from JWT claims only, never from URL parameters. All task endpoints protected with JWT authentication returning 401 for unauthorized requests."

## Response snapshot

Created comprehensive Phase 2 implementation plan with 5 key artifacts:

### 1. **research.md** - Technology Decisions (7 major areas)
- Monorepo structure (single repo with /backend and /frontend)
- JWT Authentication (Better Auth + FastAPI manual verification with shared secret)
- Neon PostgreSQL Integration (SQLModel ORM)
- Next.js 16 App Router Architecture
- Tailwind CSS Responsive Design Strategy
- User Isolation Security Pattern (JWT payload extraction, zero trust)
- Error Handling & User Experience patterns

**Key Decision**: Single monorepo simplifies development, shared .env for BETTER_AUTH_SECRET, user_id from JWT claims only

### 2. **data-model.md** - Database Schema
- Entity Relationship Diagram (User 1:N Task)
- User entity: id, email (unique), hashed_password, created_at
- Task entity: id, description (1-500 chars), completed, created_at, user_id (FK)
- Validation rules (VR-U001 to VR-T004)
- Business rules (BR-U001 to BR-T005)
- State transitions (Task completion toggle)
- Migration scripts (create_tables.py, seed_data.py)

### 3. **contracts/openapi.yaml** - API Contract (OpenAPI 3.1)
- 7 endpoints documented: 2 auth (signup, signin) + 5 task operations
- Request/response schemas with examples
- Security scheme (BearerAuth JWT)
- Error responses (400, 401, 404, 500)
- Validation rules in schema constraints

### 4. **quickstart.md** - Setup Guide (8 parts, 15 steps)
- Part 1: Neon database provisioning
- Part 2: Monorepo setup (.env configuration)
- Part 3: Backend setup (uv install, create tables, seed data)
- Part 4: Frontend setup (npm install, Better Auth config)
- Part 5: Full-stack integration verification
- Part 6: Development workflow commands
- Part 7: Troubleshooting guide (5 common issues)
- Part 8: Next steps and quick reference

### 5. **plan.md** - Implementation Plan (10 phases A-J)

**Phase A**: Foundation (backend core, database models)
**Phase B**: Security (JWT auth middleware, signup/signin endpoints)
**Phase C**: API Implementation (5 task CRUD endpoints with user isolation)
**Phase D**: Frontend Foundation (Next.js setup, Better Auth, API client)
**Phase E**: Authentication UI (signup/signin pages)
**Phase F**: Dashboard UI (task management interface)
**Phase G**: Responsive Design (mobile/tablet/desktop)
**Phase H**: Error Handling & UX Polish
**Phase I**: Testing & Quality Assurance (all 20 FRs, 7 SCs)
**Phase J**: Documentation & Deployment Prep

**Architecture Highlights**:
- Monorepo structure with /backend and /frontend at root
- JWT shared secret (BETTER_AUTH_SECRET) in root .env
- User isolation via JWT claims extraction (get_current_user_id dependency)
- CORS configured to allow frontend origin only
- Neon PostgreSQL with SQLModel ORM
- Next.js App Router with TypeScript + Tailwind CSS
- FastAPI Swagger UI at /docs for API documentation

**Critical Success Factors**:
1. User Isolation Security (JWT payload filtering, return 404 not 403)
2. JWT Security & Shared Secret (HS256, 24h expiration)
3. Database Persistence (Neon serverless, connection pooling)
4. CORS Configuration (allow frontend origin)
5. Responsive Design (mobile-first Tailwind approach)

**Risk Mitigation**:
- JWT expiration (24h limit, redirect on 401)
- Neon hibernation (first request slow, document limitation)
- Frontend-backend version mismatch (monorepo prevents)
- BETTER_AUTH_SECRET mismatch (validation script)

## Outcome

- ✅ Impact: Complete Phase 2 architecture designed, ready for `/sp.tasks` task generation
- 🧪 Tests: Constitution compliance PASS (5/5 principles), Technology standards PASS (6/6 requirements)
- 📁 Files: Created 5 files (research.md, data-model.md, openapi.yaml, quickstart.md, plan.md)
- 🔁 Next prompts: User should run `/sp.tasks` to generate implementation tasks breakdown
- 🧠 Reflection: Successfully translated business requirements into technical architecture with clear phase-wise execution strategy. Monorepo structure simplifies development while maintaining service separation. JWT-based user isolation pattern is security-critical and well-documented across all planning artifacts.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all required artifacts
- Graders run and results (PASS/FAIL):
  - Constitution Compliance: PASS (all 5 principles met)
  - Technology Standards: PASS (all 6 standards met)
  - Planning Completeness: PASS (10 phases defined with acceptance criteria)
  - Security Review: PASS (user isolation, JWT verification, no secrets in code)
- Prompt variant (if applicable): Standard /sp.plan workflow with comprehensive user requirements
- Next experiment (smallest change to try): Consider adding architecture decision records (ADRs) for significant technical decisions (JWT vs OAuth2, Neon vs self-hosted PostgreSQL, monorepo vs multi-repo) to capture rationale for future reference
