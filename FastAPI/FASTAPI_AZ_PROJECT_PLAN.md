# FastAPI A-Z Foundation Project Plan

## Project Name

TaskForge API

## Project Purpose

This project is a single-app FastAPI backend designed to teach FastAPI from foundation to advanced production-style backend engineering.

The goal is not to build a toy CRUD app. The goal is to build one coherent backend that forces you to touch the concepts a serious FastAPI/backend engineer needs:

- API design
- FastAPI routing and dependency injection
- Pydantic models and validation
- Authentication and authorization
- Database design with Postgres
- SQLAlchemy async patterns
- Alembic migrations
- Middleware and request lifecycle
- Error handling
- Background jobs
- File uploads
- WebSockets
- Testing
- Docker and local development
- Observability
- Security basics
- FastAPI internals and ASGI mental models

This is intentionally a single deployable backend app for now. Microservices should come later, after the monolith is well understood.

## Product Concept

TaskForge API is a multi-user project and task management backend.

Users can:

- Register and login
- Create organizations
- Invite other users into organizations
- Create projects inside organizations
- Create tasks inside projects
- Assign tasks to users
- Comment on tasks
- Upload attachments to tasks
- Track task activity history
- Receive simulated notifications
- Stream task updates over WebSockets
- View audit logs for sensitive actions

This domain is simple enough to reason about and rich enough to cover real backend concepts.

## Scope

### In Scope

- One FastAPI app
- REST API
- Postgres
- SQLAlchemy async
- Alembic migrations
- Docker and Docker Compose
- Token-based authentication
- Role-based and resource-based authorization
- Background task simulation
- WebSocket endpoint
- File upload endpoint
- API tests and integration tests
- Structured logging
- OpenAPI documentation

### Out of Scope For Now

- Microservices
- Kubernetes
- Real payment integration
- Real email/SMS provider
- Complex Postgres internals
- Frontend UI
- Production cloud deployment
- Event brokers like Kafka or RabbitMQ

These can be added later after the foundation app is solid.

## Recommended Tech Stack

- Python 3.14, based on the current `.python-version`
- `uv` for dependency and environment management
- FastAPI with `fastapi[standard]`
- Pydantic v2
- SQLAlchemy 2.x async
- Alembic
- Postgres
- `asyncpg`
- `pytest`
- `httpx`
- `pytest-asyncio` or `anyio`
- `ruff`
- `mypy`
- `python-multipart` for file uploads, if not already pulled by FastAPI standard
- Password hashing library such as Argon2 or bcrypt
- JWT or opaque token library, depending on the chosen auth style
- Docker and Docker Compose

## Architecture

Start with a modular monolith:

```text
Client
  |
  v
FastAPI App
  |
  +--> Middleware
  |     +--> request id
  |     +--> logging
  |     +--> timing
  |     +--> CORS
  |
  +--> API Routers
  |     +--> auth
  |     +--> users
  |     +--> organizations
  |     +--> projects
  |     +--> tasks
  |     +--> comments
  |     +--> attachments
  |     +--> notifications
  |     +--> audit
  |
  +--> Dependencies
  |     +--> settings
  |     +--> db session
  |     +--> current user
  |     +--> permissions
  |
  +--> Services
  |
  +--> Repositories
  |
  +--> SQLAlchemy Models
  |
  v
Postgres
```

Request lifecycle mental model:

```text
HTTP request
  |
  v
ASGI server
  |
  v
FastAPI / Starlette middleware
  |
  v
Route matching
  |
  v
Dependency graph resolution
  |
  v
Pydantic validation
  |
  v
Endpoint function
  |
  v
Service layer
  |
  v
Repository / database
  |
  v
Response serialization
  |
  v
HTTP response
```

## Suggested Package Layout

```text
fastapi_app/
  __init__.py
  main.py
  app.py

  core/
    config.py
    security.py
    errors.py
    logging.py
    pagination.py
    responses.py

  db/
    base.py
    session.py
    migrations/

  api/
    __init__.py
    router.py
    deps.py
    v1/
      router.py
      auth.py
      users.py
      organizations.py
      projects.py
      tasks.py
      comments.py
      attachments.py
      notifications.py
      audit.py

  modules/
    users/
      models.py
      schemas.py
      service.py
      repository.py
    organizations/
      models.py
      schemas.py
      service.py
      repository.py
    projects/
      models.py
      schemas.py
      service.py
      repository.py
    tasks/
      models.py
      schemas.py
      service.py
      repository.py
    audit/
      models.py
      schemas.py
      service.py

  tests/
    conftest.py
    api/
    unit/
    integration/
```

## Database Model, Light Version

Keep Postgres learning practical for now.

Core entities:

- `users`
- `organizations`
- `organization_members`
- `projects`
- `tasks`
- `task_comments`
- `task_attachments`
- `task_activity_events`
- `notifications`
- `audit_logs`

Important database ideas to learn:

- Primary keys
- Foreign keys
- Unique constraints
- Nullable vs non-nullable columns
- Enum-like status fields
- Created and updated timestamps
- Soft delete vs hard delete
- Basic indexes
- Join tables
- Transaction boundaries
- Migration history

Do not go deep yet into partitioning, replication, advanced query planning, or tuning.

## API Style Guide

Use consistent REST naming:

```text
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout

GET    /api/v1/users/me
PATCH  /api/v1/users/me

POST   /api/v1/organizations
GET    /api/v1/organizations
GET    /api/v1/organizations/{organization_id}
PATCH  /api/v1/organizations/{organization_id}
DELETE /api/v1/organizations/{organization_id}

POST   /api/v1/organizations/{organization_id}/projects
GET    /api/v1/organizations/{organization_id}/projects
GET    /api/v1/projects/{project_id}
PATCH  /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}

POST   /api/v1/projects/{project_id}/tasks
GET    /api/v1/projects/{project_id}/tasks
GET    /api/v1/tasks/{task_id}
PATCH  /api/v1/tasks/{task_id}
DELETE /api/v1/tasks/{task_id}

POST   /api/v1/tasks/{task_id}/comments
GET    /api/v1/tasks/{task_id}/comments

POST   /api/v1/tasks/{task_id}/attachments
GET    /api/v1/tasks/{task_id}/attachments

GET    /api/v1/tasks/{task_id}/activity
GET    /api/v1/audit-logs

WS     /api/v1/ws/tasks/{task_id}
```

API design principles:

- Use nouns for resources.
- Use HTTP methods for actions.
- Use clear status codes.
- Use stable error response shape.
- Add pagination to list endpoints.
- Add filtering and sorting where it teaches useful design.
- Never expose internal database details in API responses.
- Keep request schemas and response schemas separate.
- Avoid returning raw ORM models directly.

## Error Response Shape

Use one consistent error format:

```json
{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task not found",
    "details": {}
  },
  "request_id": "..."
}
```

Learning goals:

- `HTTPException`
- Custom exception classes
- Global exception handlers
- Validation error formatting
- Request ID propagation

## Section 1: Project Foundation

### Task 1.1: Clean The Starter Project

Goal:

- Convert the current starter project into a real FastAPI backend package.

Learn:

- Python project structure
- `uv` workflow
- `pyproject.toml`
- package naming

Steps:

- Review current `pyproject.toml`.
- Decide whether to keep or remove the Typer demo.
- Create the main app package.
- Ensure the app can be started through FastAPI CLI or Uvicorn.

Acceptance criteria:

- Project has a clear package directory.
- README explains how to run the app.
- No unrelated demo code is in the main app path.

### Task 1.2: Add App Factory

Goal:

- Create a function that builds and returns the FastAPI app.

Learn:

- `FastAPI()`
- app metadata
- router inclusion
- testable app construction

Steps:

- Create `create_app()`.
- Set title, version, docs URL, OpenAPI URL.
- Include a top-level API router.
- Keep `main.py` small.

Acceptance criteria:

- The app starts successfully.
- Tests can import and create the app.
- App metadata appears in OpenAPI docs.

### Task 1.3: Add Health Endpoints

Goal:

- Add basic operational endpoints.

Learn:

- Simple routes
- response models
- status checks

Endpoints:

- `GET /health`
- `GET /ready`

Acceptance criteria:

- `/health` returns app status.
- `/ready` can later include DB readiness.
- Both endpoints are documented.

### Task 1.4: Add Settings Management

Goal:

- Centralize configuration.

Learn:

- Pydantic settings
- environment variables
- config validation
- test overrides

Settings to model:

- app name
- environment
- debug flag
- database URL
- allowed CORS origins
- token expiry values

Acceptance criteria:

- No secrets are hardcoded.
- Local config can come from environment.
- Tests can override settings.

## Section 2: Routing And API Basics

### Task 2.1: Create Versioned API Router

Goal:

- Establish `/api/v1` as the API root.

Learn:

- `APIRouter`
- prefixes
- tags
- route organization

Acceptance criteria:

- All business endpoints live under `/api/v1`.
- Internal operational endpoints remain outside if appropriate.

### Task 2.2: Build First Resource Without Database

Goal:

- Build a temporary in-memory tasks endpoint before adding DB complexity.

Learn:

- Path params
- query params
- request bodies
- response models
- status codes

Endpoints:

- `POST /api/v1/tasks`
- `GET /api/v1/tasks`
- `GET /api/v1/tasks/{task_id}`

Acceptance criteria:

- Input is validated.
- Response model is explicit.
- Invalid IDs return a clean error.

### Task 2.3: Add Pagination Model

Goal:

- Learn reusable response structures.

Learn:

- query parameter validation
- reusable schemas
- generic response patterns

Acceptance criteria:

- List endpoints support `limit` and `offset`.
- Limits have min and max validation.
- Response includes items and pagination metadata.

### Task 2.4: Add Filtering And Sorting

Goal:

- Learn API query design.

Learn:

- query params
- enums
- allow-listed sort fields

Acceptance criteria:

- Tasks can be filtered by status.
- Tasks can be sorted by created date or priority.
- Invalid sort fields are rejected.

## Section 3: Pydantic Deep Dive

### Task 3.1: Separate Create, Update, And Read Schemas

Goal:

- Avoid using one schema for every purpose.

Learn:

- request vs response contracts
- optional update fields
- schema reuse

Acceptance criteria:

- Create schemas require mandatory fields.
- Update schemas allow partial changes.
- Read schemas include server-generated fields.

### Task 3.2: Add Field Validation

Goal:

- Validate data at API boundaries.

Learn:

- field constraints
- string length constraints
- enum validation
- semantic validation

Acceptance criteria:

- Task title has length limits.
- Task status is constrained.
- Due date cannot violate business rules.

### Task 3.3: Add OpenAPI Examples

Goal:

- Make docs useful.

Learn:

- examples
- schema metadata
- tags
- response descriptions

Acceptance criteria:

- Key endpoints have example requests and responses.
- OpenAPI docs are readable.

## Section 4: Database Foundation

### Task 4.1: Add Postgres With Docker Compose

Goal:

- Run the database locally.

Learn:

- Docker Compose
- local service networking
- environment-based config

Acceptance criteria:

- Postgres runs locally.
- App can connect using a configured URL.
- Credentials are not committed as real secrets.

### Task 4.2: Add SQLAlchemy Async Setup

Goal:

- Create the async DB engine and session dependency.

Learn:

- async engine
- async session
- dependency injection
- transaction scope

Acceptance criteria:

- API endpoints can receive a DB session.
- Sessions are closed correctly.
- DB dependency can be overridden in tests.

### Task 4.3: Add Alembic

Goal:

- Manage schema changes with migrations.

Learn:

- migration generation
- migration execution
- model metadata

Acceptance criteria:

- Alembic can create and run migrations.
- Database schema is reproducible from migrations.

### Task 4.4: Model Users, Organizations, And Memberships

Goal:

- Add the first real relational model.

Learn:

- one-to-many relationships
- many-to-many through association table
- uniqueness constraints

Acceptance criteria:

- Users can belong to organizations.
- Organization membership stores role.
- Duplicate membership is prevented.

### Task 4.5: Model Projects And Tasks

Goal:

- Add core product data.

Learn:

- foreign keys
- indexes
- enum-like fields
- timestamps

Acceptance criteria:

- Projects belong to organizations.
- Tasks belong to projects.
- Tasks can be assigned to users.
- Common query paths have basic indexes.

## Section 5: Service And Repository Layers

### Task 5.1: Move Business Logic Out Of Routers

Goal:

- Keep route handlers thin.

Learn:

- service layer
- separation of concerns
- testable business logic

Acceptance criteria:

- Routers handle HTTP concerns.
- Services handle business rules.
- Repositories handle database operations.

### Task 5.2: Add Transaction Boundaries

Goal:

- Make write operations consistent.

Learn:

- commits
- rollbacks
- unit-of-work thinking

Acceptance criteria:

- Multi-step operations are atomic.
- Failed operations do not partially write data.

## Section 6: Authentication

### Task 6.1: Add Password Hashing

Goal:

- Store passwords safely.

Learn:

- password hashing
- salts
- verification
- why hashing is not encryption

Acceptance criteria:

- Plaintext passwords are never stored.
- Password verification works.
- Hashing uses a modern library and parameters.

### Task 6.2: Add Registration

Goal:

- Create users safely.

Learn:

- unique constraints
- conflict errors
- request validation

Endpoint:

- `POST /api/v1/auth/register`

Acceptance criteria:

- Duplicate emails are rejected.
- Response does not include password data.

### Task 6.3: Add Login

Goal:

- Authenticate users.

Learn:

- credential verification
- generic error messages
- token issuing

Endpoint:

- `POST /api/v1/auth/login`

Acceptance criteria:

- Invalid login returns a generic response.
- Valid login returns an access token or session token.
- No raw secrets are logged.

### Task 6.4: Add Current User Dependency

Goal:

- Protect endpoints.

Learn:

- security dependencies
- dependency composition
- token parsing

Acceptance criteria:

- Protected endpoints require authentication.
- `GET /api/v1/users/me` returns the current user.

## Section 7: Authorization

### Task 7.1: Add Organization Roles

Goal:

- Model access inside organizations.

Learn:

- RBAC
- resource scoping
- deny by default

Roles:

- owner
- admin
- member
- viewer

Acceptance criteria:

- Users only access organizations they belong to.
- Role is checked before sensitive actions.

### Task 7.2: Add Permission Dependencies

Goal:

- Make authorization reusable.

Learn:

- dependency factories
- route-level permissions
- resource lookup

Acceptance criteria:

- Permission logic is centralized.
- Unauthorized users receive 403 or 404 consistently.

### Task 7.3: Add Authorization Tests

Goal:

- Prove access control works.

Learn:

- negative tests
- auth test fixtures
- IDOR prevention

Acceptance criteria:

- A user cannot access another organization's project.
- A viewer cannot mutate protected resources.
- Admin-only endpoints reject normal members.

## Section 8: API Design Maturity

### Task 8.1: Standardize Error Codes

Goal:

- Make API failures predictable.

Learn:

- error taxonomy
- client-friendly errors
- global handlers

Acceptance criteria:

- Common errors use stable codes.
- Error responses include request ID.

### Task 8.2: Add PATCH Semantics

Goal:

- Support partial updates correctly.

Learn:

- optional fields
- unset vs null
- partial update logic

Acceptance criteria:

- Omitted fields are unchanged.
- Explicit null is handled intentionally.

### Task 8.3: Add Idempotency For Create Operations

Goal:

- Learn retry-safe API design.

Learn:

- idempotency keys
- duplicate request handling
- safe retries

Acceptance criteria:

- Repeated create request with same idempotency key does not duplicate data.
- Different keys create separate resources.

## Section 9: Middleware And Request Lifecycle

### Task 9.1: Add Request ID Middleware

Goal:

- Trace requests across logs and responses.

Learn:

- middleware
- request state
- response headers

Acceptance criteria:

- Every request gets a request ID.
- Response includes the request ID header.
- Logs include request ID.

### Task 9.2: Add Timing Middleware

Goal:

- Measure request latency.

Learn:

- middleware order
- response mutation
- monotonic time

Acceptance criteria:

- Response includes duration header in local/dev.
- Logs include request duration.

### Task 9.3: Add Security Headers

Goal:

- Add basic API hardening.

Learn:

- response headers
- browser-facing API concerns

Acceptance criteria:

- Common safe headers are added.
- Headers are configured centrally.

### Task 9.4: Add CORS Configuration

Goal:

- Understand cross-origin API access.

Learn:

- CORS middleware
- allowed origins
- credentials tradeoffs

Acceptance criteria:

- CORS is environment-driven.
- Wildcard origins are avoided for credentialed requests.

## Section 10: Lifespan And Runtime Resources

### Task 10.1: Add Lifespan Handler

Goal:

- Learn startup and shutdown hooks.

Learn:

- FastAPI lifespan
- resource initialization
- graceful cleanup

Acceptance criteria:

- Startup logs app configuration safely.
- Shutdown cleans up resources.

### Task 10.2: Add Readiness Check With DB

Goal:

- Distinguish alive from ready.

Learn:

- health checks
- DB ping
- operational readiness

Acceptance criteria:

- `/health` means process is alive.
- `/ready` means dependencies are reachable.

## Section 11: Background Work

### Task 11.1: Add Notification Simulation

Goal:

- Learn background task basics.

Learn:

- FastAPI `BackgroundTasks`
- request-response decoupling
- limitations of in-process work

Acceptance criteria:

- Creating a task schedules a notification simulation.
- The API response does not wait for the notification work.

### Task 11.2: Add Outbox-Like Table

Goal:

- Learn reliable background work design without adding a broker yet.

Learn:

- outbox pattern
- transactional event recording
- eventual processing

Acceptance criteria:

- Important domain events are recorded in DB.
- A simple worker command can process pending events later.

## Section 12: File Uploads

### Task 12.1: Add Task Attachments

Goal:

- Support file uploads safely.

Learn:

- `UploadFile`
- multipart requests
- file size limits
- metadata storage

Acceptance criteria:

- Users can attach a file to a task.
- File metadata is stored in DB.
- Upload requires task access.

### Task 12.2: Add Upload Validation

Goal:

- Avoid unsafe file handling.

Learn:

- filename safety
- extension allow-lists
- content type limitations
- storage outside web root

Acceptance criteria:

- Server generates storage names.
- Original filename is treated as untrusted metadata.
- Unsupported file types are rejected.

## Section 13: WebSockets

### Task 13.1: Add Task Activity WebSocket

Goal:

- Stream task updates to connected clients.

Learn:

- WebSocket routes
- accept/send/receive flow
- connection lifecycle

Endpoint:

- `WS /api/v1/ws/tasks/{task_id}`

Acceptance criteria:

- Client can connect to a task stream.
- Server can send basic activity events.
- Unauthorized users cannot connect to tasks they cannot access.

### Task 13.2: Understand WebSocket Limits

Goal:

- Learn what changes when HTTP becomes long-lived.

Learn:

- connection state
- authentication at connect time
- cleanup on disconnect
- scaling limits

Acceptance criteria:

- Code handles disconnects.
- Notes explain why multi-process WebSockets need shared pub/sub later.

## Section 14: Audit Logging

### Task 14.1: Add Audit Log Table

Goal:

- Record sensitive actions.

Learn:

- audit event design
- append-only records
- privacy-aware logging

Events to audit:

- user login
- organization creation
- membership changes
- project deletion
- role changes

Acceptance criteria:

- Audit logs include actor, action, resource type, resource ID, and timestamp.
- Audit logs do not include secrets or raw tokens.

### Task 14.2: Add Audit Log Endpoint

Goal:

- Expose audit data safely.

Learn:

- admin-only endpoints
- filtering
- pagination

Acceptance criteria:

- Only authorized users can view audit logs.
- Logs can be filtered by action or resource.

## Section 15: Testing

### Task 15.1: Add Test App Factory

Goal:

- Make tests isolated.

Learn:

- dependency overrides
- test config
- async test client

Acceptance criteria:

- Tests can create an app with test settings.
- DB dependency can be swapped.

### Task 15.2: Add Basic API Tests

Goal:

- Verify endpoint behavior.

Learn:

- `httpx` test client
- status assertions
- JSON assertions

Acceptance criteria:

- Health endpoint is tested.
- Task CRUD happy path is tested.
- Validation failure is tested.

### Task 15.3: Add Database Integration Tests

Goal:

- Test with a real database-like setup.

Learn:

- migration setup in tests
- transactions
- cleanup strategies

Acceptance criteria:

- Tests run against isolated test DB.
- Tests do not depend on local developer state.

### Task 15.4: Add Security Tests

Goal:

- Catch auth and authz regressions.

Learn:

- negative testing
- token fixtures
- forbidden access patterns

Acceptance criteria:

- Unauthenticated requests are rejected.
- Unauthorized resource access is rejected.
- Sensitive fields cannot be mass-assigned.

## Section 16: Docker And Local Dev

### Task 16.1: Add Dockerfile

Goal:

- Containerize the app.

Learn:

- Python container basics
- `uv` inside Docker
- non-root runtime user
- health checks

Acceptance criteria:

- Image builds successfully.
- App runs in a container.
- Container does not require root at runtime.

### Task 16.2: Add Docker Compose

Goal:

- Run app and Postgres together.

Learn:

- service dependencies
- local networking
- volumes
- environment configuration

Acceptance criteria:

- `docker compose up` starts the app and DB.
- App can reach Postgres.
- Local data persists in a named volume.

### Task 16.3: Add Developer Commands

Goal:

- Make common workflows easy.

Learn:

- repeatable local commands
- scripts
- developer ergonomics

Commands to support:

- run app
- run tests
- run lint
- run migrations
- create migration

Acceptance criteria:

- README documents all commands.
- Commands work from a clean checkout.

## Section 17: Observability

### Task 17.1: Add Structured Logging

Goal:

- Make logs useful.

Learn:

- structured logs
- log levels
- request context

Acceptance criteria:

- Logs include timestamp, level, message, request ID.
- Secrets and raw tokens are not logged.

### Task 17.2: Add Domain Event Logs

Goal:

- Understand business observability.

Learn:

- logging important events
- separating logs from audit records

Acceptance criteria:

- Important actions produce structured logs.
- Audit records remain authoritative for sensitive actions.

## Section 18: FastAPI Internals Study Track

This section should be studied while building, not after.

### Task 18.1: Understand ASGI

Questions to answer in notes:

- What is ASGI?
- What does Uvicorn do?
- What does FastAPI do?
- What does Starlette do?
- How does a request become a response?

Acceptance criteria:

- You can explain ASGI in your own words.
- You can describe where middleware fits.

### Task 18.2: Understand Dependency Injection

Questions to answer in notes:

- How does FastAPI inspect dependency function signatures?
- When are dependencies executed?
- How are nested dependencies resolved?
- How are yielded dependencies cleaned up?
- How do dependency overrides work in tests?

Acceptance criteria:

- You can explain the dependency graph for a protected route.

### Task 18.3: Understand Pydantic Validation

Questions to answer in notes:

- When is request validation executed?
- How are query/path/body params validated differently?
- How does response serialization work?
- Why should response schemas be explicit?

Acceptance criteria:

- You can predict what happens for invalid request input.

### Task 18.4: Understand Async Behavior

Questions to answer in notes:

- What does `async def` change?
- What happens if you call blocking IO in an async endpoint?
- When does FastAPI use a threadpool?
- How should DB and HTTP clients be used safely?

Acceptance criteria:

- You can explain when to use async vs sync endpoints.

### Task 18.5: Understand OpenAPI Generation

Questions to answer in notes:

- How does FastAPI generate OpenAPI docs?
- Where do Pydantic models appear?
- How do tags, summaries, descriptions, and response models affect docs?

Acceptance criteria:

- OpenAPI docs reflect the intended API contract.

## Section 19: Security Checklist

Apply this throughout the project.

Authentication:

- No plaintext password storage.
- Generic login failure messages.
- Short-lived access tokens.
- Refresh/logout behavior is explicit.

Authorization:

- Deny by default.
- Resource access is scoped by organization membership.
- Sensitive role changes require elevated permissions.
- Negative tests exist for IDOR-style access.

Secrets:

- No hardcoded secrets.
- Use environment variables or local ignored files for local development.
- Commit only placeholder examples.

Input validation:

- Validate request models with Pydantic.
- Bound string lengths.
- Bound pagination limits.
- Allow-list sort fields.

Files:

- Treat filenames as untrusted.
- Generate server-side storage names.
- Enforce size limits.
- Store uploaded files outside public paths.

Logging:

- Do not log passwords, tokens, or secrets.
- Include request IDs.
- Use structured logs.

Database:

- Use parameterized ORM queries.
- Avoid raw SQL unless necessary.
- Apply least privilege in real deployments.

Certificates:

- No certificate files are planned initially.
- If certificate files are added later, verify expiration, key strength, signature algorithm, and whether they are self-signed.

## Section 20: Definition Of Done

The project foundation is complete when:

- The app runs locally with `uv`.
- The app runs through Docker Compose.
- Postgres is connected.
- Alembic migrations work.
- CRUD exists for organizations, projects, tasks, and comments.
- Auth works.
- Authorization prevents cross-organization access.
- File uploads work with validation.
- Background task simulation works.
- WebSocket task stream works.
- OpenAPI docs are useful.
- Tests cover happy paths and failure paths.
- Logs are structured.
- README explains setup and workflows.
- Internals notes exist for ASGI, dependency injection, Pydantic, async, middleware, and OpenAPI.

## Suggested Implementation Order

Follow this order to avoid getting stuck:

1. Project cleanup
2. App factory
3. Health endpoint
4. Settings
5. Versioned router
6. In-memory tasks API
7. Pydantic schemas
8. Pagination
9. Error handling
10. Docker Compose with Postgres
11. SQLAlchemy async setup
12. Alembic
13. User model
14. Organization model
15. Project model
16. Task model
17. Repository layer
18. Service layer
19. Registration
20. Login
21. Current user dependency
22. Organization membership
23. Authorization dependency
24. Authz tests
25. Comments
26. Task activity events
27. Audit logs
28. Middleware
29. Background notifications
30. Attachments
31. WebSockets
32. Structured logging
33. Dockerfile
34. Final README
35. Internals notes

## Section 21: Granular OpenSpec-Style Task Breakdown

Use this section as the detailed execution checklist.

Each task is intentionally small. A good workflow is to pick one task ID, switch to Ask mode, and ask for implementation guidance for only that task.

Task format:

- `Goal`: what the task produces
- `Learn`: what concept the task teaches
- `Verify`: how to know the task is complete

### 0. Project Orientation

- [x] `ORIENT-001`: Read the current `pyproject.toml`.
  - Goal: Understand the existing package name, Python version, and dependencies.
  - Learn: How Python projects are declared for `uv`.
  - Verify: You can explain the project metadata and current dependencies.

- [x] `ORIENT-002`: Read the current `.python-version`.
  - Goal: Confirm the Python runtime version.
  - Learn: How local Python version pinning affects tooling.
  - Verify: You know which interpreter version the project expects.

- [x] `ORIENT-003`: Read the current demo files.
  - Goal: Identify whether `main.py`, `typer_demo.py`, and `starlette_demo.py` are learning demos or app code.
  - Learn: How to separate experiments from production app structure.
  - Verify: You can decide what should stay, move, or be removed later.

- [x] `ORIENT-004`: Read this roadmap fully once.
  - Goal: Understand the project direction before coding.
  - Learn: How larger backend projects are planned in phases.
  - Verify: You can describe the app goal in one paragraph.

### 1. Python And uv Foundation

- [x] `UV-001`: Decide the package import name.
  - Goal: Choose the final Python package name, likely `fastapi_app`.
  - Learn: Difference between distribution name and import package name.
  - Verify: The chosen name is consistent with `pyproject.toml`.

- [x] `UV-002`: Decide whether demo files should remain at project root.
  - Goal: Keep the app root clean.
  - Learn: Project hygiene and source organization.
  - Verify: You have a clear decision for `typer_demo.py` and `starlette_demo.py`.

- [x] `UV-003`: Define runtime dependencies.
  - Goal: List required app dependencies before installing them.
  - Learn: Difference between runtime and dev dependencies.
  - Verify: You know why each dependency is needed.

- [x] `UV-004`: Define development dependencies.
  - Goal: List tools for testing, linting, formatting, and typing.
  - Learn: Dev dependency grouping.
  - Verify: The future dependency list includes test and quality tools.

- [x] `UV-005`: Add or update project scripts.
  - Goal: Make app startup easier.
  - Learn: `pyproject.toml` script entry points.
  - Verify: There is a planned command for running the app.

- [x] `UV-006`: Document common `uv` commands.
  - Goal: Make local development repeatable.
  - Learn: `uv sync`, `uv add`, `uv run`, and lockfile workflow.
  - Verify: README will explain the common commands.

### 2. App Package Structure

- [x] `STRUCT-001`: Create the root app package.
  - Goal: Create `fastapi_app/`.
  - Learn: Python package layout.
  - Verify: The package can be imported.

- [x] `STRUCT-002`: Create `fastapi_app/main.py`.
  - Goal: Provide the app entry point.
  - Learn: Uvicorn import path conventions.
  - Verify: The app can be referenced as `fastapi_app.main:app`.

- [x] `STRUCT-003`: Create `fastapi_app/app.py`.
  - Goal: Hold the app factory.
  - Learn: Why app factories improve testing and configuration.
  - Verify: `create_app()` returns a FastAPI instance.

- [x] `STRUCT-004`: Create `fastapi_app/api/`.
  - Goal: Reserve a package for API routers.
  - Learn: API boundary organization.
  - Verify: API routers are not mixed with database or domain code.

- [x] `STRUCT-005`: Create `fastapi_app/core/`.
  - Goal: Reserve a package for shared app infrastructure.
  - Learn: Separation of cross-cutting concerns.
  - Verify: Settings, errors, logging, and security utilities have a home.

- [ ] `STRUCT-006`: Create `fastapi_app/db/`.
  - Goal: Reserve a package for database setup.
  - Learn: Separating persistence infrastructure.
  - Verify: DB engine/session/model base will live here.

- [x] `STRUCT-007`: Create `fastapi_app/modules/`.
  - Goal: Reserve a package for domain modules.
  - Learn: Modular monolith organization.
  - Verify: Users, organizations, projects, and tasks can each become modules.

- [x] `STRUCT-008`: Create `tests/`.
  - Goal: Establish test structure from the beginning.
  - Learn: Test organization.
  - Verify: Unit, API, and integration test folders are planned.

### 3. App Factory And Metadata

- [x] `APP-001`: Implement the minimal app factory.
  - Goal: Create a FastAPI app through `create_app()`.
  - Learn: FastAPI app construction.
  - Verify: Importing the app does not start external services.

- [x] `APP-002`: Add app title.
  - Goal: Set a useful API title.
  - Learn: FastAPI metadata.
  - Verify: The title appears in `/docs`.

- [x] `APP-003`: Add app version.
  - Goal: Expose project version.
  - Learn: API metadata and release identity.
  - Verify: The version appears in OpenAPI output.

- [x] `APP-004`: Add app description.
  - Goal: Explain TaskForge in API docs.
  - Learn: Documentation metadata.
  - Verify: The description appears in Swagger UI.

- [x] `APP-005`: Configure docs URLs.
  - Goal: Decide `/docs`, `/redoc`, and `/openapi.json` paths.
  - Learn: FastAPI documentation controls.
  - Verify: Docs and OpenAPI schema are reachable.

- [x] `APP-006`: Add top-level router inclusion.
  - Goal: Include a root API router from the app factory.
  - Learn: Router composition.
  - Verify: Routes can be registered from one place.

### 4. Health And Readiness

- [x] `HEALTH-001`: Add `/health`.
  - Goal: Return basic process health.
  - Learn: Simple route handlers.
  - Verify: Endpoint returns HTTP 200 with stable JSON.

- [x] `HEALTH-002`: Add `/ready`.
  - Goal: Prepare for dependency readiness checks.
  - Learn: Difference between liveness and readiness.
  - Verify: Endpoint exists even before DB integration.

- [x] `HEALTH-003`: Add health response schema.
  - Goal: Make health response explicit.
  - Learn: Response models.
  - Verify: OpenAPI shows the health schema.

- [x] `HEALTH-004`: Add health tests.
  - Goal: Protect the simplest operational endpoints.
  - Learn: FastAPI test client basics.
  - Verify: Tests assert status code and response body.

### 5. Settings And Configuration

- [x] `CONFIG-001`: Create settings model.
  - Goal: Define app configuration in one place.
  - Learn: Pydantic settings pattern.
  - Verify: Settings can be instantiated.

- [x] `CONFIG-002`: Add environment name.
  - Goal: Support local, test, and production-like modes.
  - Learn: Environment-aware behavior.
  - Verify: App can read environment name.

- [x] `CONFIG-003`: Add debug flag.
  - Goal: Control debug behavior.
  - Learn: Safe configuration defaults.
  - Verify: Debug can be disabled by default.

- [x] `CONFIG-004`: Add database URL setting.
  - Goal: Prepare DB configuration.
  - Learn: Configuring external dependencies.
  - Verify: App reads DB URL without hardcoding real credentials.

- [x] `CONFIG-005`: Add CORS origins setting.
  - Goal: Prepare browser client access safely.
  - Learn: List parsing from environment.
  - Verify: Allowed origins can be configured.

- [x] `CONFIG-006`: Add token expiry settings.
  - Goal: Prepare auth configuration.
  - Learn: Security-sensitive configuration.
  - Verify: Expiry values are explicit and testable.

- [x] `CONFIG-007`: Cache settings safely.
  - Goal: Avoid rebuilding settings repeatedly.
  - Learn: Dependency caching and config lifecycle.
  - Verify: Tests can still override settings.

- [x] `CONFIG-008`: Add config tests.
  - Goal: Validate expected defaults and overrides.
  - Learn: Testing configuration.
  - Verify: Tests cover local and test environment behavior.

### 6. API Versioning

- [x] `ROUTE-001`: Create root API router.
  - Goal: Centralize router registration.
  - Learn: Router composition.
  - Verify: `api/router.py` can include versioned routers.

- [x] `ROUTE-002`: Create v1 router.
  - Goal: Put app endpoints under `/api/v1`.
  - Learn: URL versioning.
  - Verify: v1 endpoints share one prefix.

- [x] `ROUTE-003`: Add route tags.
  - Goal: Improve API docs.
  - Learn: OpenAPI grouping.
  - Verify: Swagger UI groups endpoints clearly.

- [ ] `ROUTE-004`: Add route summaries.
  - Goal: Make docs readable.
  - Learn: OpenAPI endpoint metadata.
  - Verify: Each endpoint has a useful summary.

### 7. First In-Memory Resource

- [x] `MEMTASK-001`: Define task status enum.
  - Goal: Restrict task status values.
  - Learn: Enum validation.
  - Verify: Invalid status is rejected.

- [x] `MEMTASK-002`: Define task priority enum.
  - Goal: Restrict priority values.
  - Learn: API contracts with enums.
  - Verify: Invalid priority is rejected.

- [x] `MEMTASK-003`: Define task create schema.
  - Goal: Validate task creation input.
  - Learn: Required fields and field constraints.
  - Verify: Missing title fails validation.

- [x] `MEMTASK-004`: Define task update schema.
  - Goal: Support partial updates.
  - Learn: Optional fields and PATCH semantics.
  - Verify: Empty update behavior is intentionally decided.

- [x] `MEMTASK-005`: Define task read schema.
  - Goal: Shape API output.
  - Learn: Response models.
  - Verify: Response includes generated fields.

- [x] `MEMTASK-006`: Add in-memory task store.
  - Goal: Learn API behavior before DB.
  - Learn: Why storage can be swapped behind services later.
  - Verify: Created tasks can be retrieved while app is running.

- [x] `MEMTASK-007`: Add create task endpoint.
  - Goal: Implement first POST endpoint.
  - Learn: Request body validation and 201 responses.
  - Verify: Valid request creates a task.

- [x] `MEMTASK-008`: Add list tasks endpoint.
  - Goal: Implement first collection GET endpoint.
  - Learn: List response design.
  - Verify: Created tasks appear in list response.

- [x] `MEMTASK-009`: Add get task by ID endpoint.
  - Goal: Implement resource lookup.
  - Learn: Path parameter validation.
  - Verify: Unknown task ID returns a clean 404.

- [x] `MEMTASK-010`: Add update task endpoint.
  - Goal: Implement PATCH behavior.
  - Learn: Partial update handling.
  - Verify: Only provided fields change.

- [x] `MEMTASK-011`: Add delete task endpoint.
  - Goal: Implement DELETE behavior.
  - Learn: 204 vs response-body decisions.
  - Verify: Deleted task cannot be fetched.

- [x] `MEMTASK-012`: Add tests for in-memory task endpoints.
  - Goal: Lock in baseline API behavior.
  - Learn: API testing.
  - Verify: Create, list, get, update, delete, and 404 paths are tested.

### 8. Pydantic And Validation

- [x] `PYD-001`: Add title length validation.
  - Goal: Prevent meaningless or oversized task titles.
  - Learn: String constraints.
  - Verify: Too-short and too-long titles fail.

- [x] `PYD-002`: Add description length validation.
  - Goal: Bound free-form text.
  - Learn: Input size control.
  - Verify: Oversized descriptions fail.

- [x] `PYD-003`: Add due date validation.
  - Goal: Enforce a business rule.
  - Learn: Semantic validation.
  - Verify: Invalid due dates fail.

- [ ] `PYD-004`: Add nested response examples.
  - Goal: Improve docs.
  - Learn: Schema examples.
  - Verify: Examples appear in OpenAPI.

- [ ] `PYD-005`: Compare request and response schemas.
  - Goal: Understand why they should differ.
  - Learn: Avoiding accidental field exposure.
  - Verify: Internal-only fields are not returned.

### 9. Error Handling

- [x] `ERR-001`: Define base application error.
  - Goal: Avoid scattered raw exceptions.
  - Learn: Error taxonomy.
  - Verify: App errors have code and message.

- [x] `ERR-002`: Define not-found error.
  - Goal: Standardize missing resource behavior.
  - Learn: Domain errors to HTTP responses.
  - Verify: Unknown task returns standard error shape.

- [x] `ERR-003`: Define forbidden error.
  - Goal: Prepare authorization failures.
  - Learn: Security-conscious responses.
  - Verify: Error shape does not leak unnecessary details.

- [x] `ERR-004`: Add global app error handler.
  - Goal: Convert app errors to JSON responses.
  - Learn: FastAPI exception handlers.
  - Verify: App errors use the standard response format.

- [x] `ERR-005`: Add validation error handler.
  - Goal: Customize request validation failures.
  - Learn: Pydantic/FastAPI validation flow.
  - Verify: Invalid input returns consistent JSON.

- [ ] `ERR-006`: Add request ID to error responses.
  - Goal: Make failures traceable.
  - Learn: Request state and observability.
  - Verify: Error response includes request ID once middleware exists.

### 10. Pagination, Filtering, And Sorting

- [x] `LIST-001`: Create pagination query schema.
  - Goal: Reuse pagination rules.
  - Learn: Query param modeling.
  - Verify: `limit` and `offset` have bounds.

- [x] `LIST-002`: Create paginated response schema.
  - Goal: Standardize list responses.
  - Learn: Response envelope tradeoffs.
  - Verify: List response includes items and pagination metadata.

- [x] `LIST-003`: Add task status filter.
  - Goal: Filter by task status.
  - Learn: Optional query parameters.
  - Verify: Only matching tasks are returned.

- [x] `LIST-004`: Add task priority filter.
  - Goal: Filter by priority.
  - Learn: Multiple query filters.
  - Verify: Filters compose correctly.

- [x] `LIST-005`: Add allow-listed sort fields.
  - Goal: Avoid unsafe arbitrary sorting.
  - Learn: Input allow-lists.
  - Verify: Unknown sort field is rejected.

- [x] `LIST-006`: Add sort direction.
  - Goal: Support ascending and descending order.
  - Learn: Enum query params.
  - Verify: Invalid direction is rejected.

- [ ] `LIST-007`: Add tests for pagination and filtering.
  - Goal: Protect list behavior.
  - Learn: Test data setup.
  - Verify: Tests cover default and custom list queries.

### 11. Database Setup

- [ ] `DB-001`: Add database dependencies.
  - Goal: Prepare SQLAlchemy async with Postgres.
  - Learn: Choosing DB libraries.
  - Verify: Dependencies are recorded in `pyproject.toml` and lockfile.

- [ ] `DB-002`: Create SQLAlchemy base.
  - Goal: Define model metadata.
  - Learn: Declarative models.
  - Verify: Models can inherit from the base.

- [ ] `DB-003`: Create async engine factory.
  - Goal: Connect to Postgres.
  - Learn: Async SQLAlchemy engine.
  - Verify: Engine uses configured database URL.

- [ ] `DB-004`: Create async session factory.
  - Goal: Provide DB sessions to requests.
  - Learn: Session lifecycle.
  - Verify: A session can be opened and closed.

- [ ] `DB-005`: Create DB session dependency.
  - Goal: Inject session into endpoints and services.
  - Learn: Yield dependencies.
  - Verify: Dependency cleanup happens after request.

- [ ] `DB-006`: Add DB readiness check.
  - Goal: Make `/ready` verify DB access.
  - Learn: Operational checks.
  - Verify: `/ready` fails if DB is unavailable.

- [ ] `DB-007`: Add database tests for session dependency.
  - Goal: Confirm DB dependency behavior.
  - Learn: Test overrides and async fixtures.
  - Verify: Tests can use isolated sessions.

### 12. Alembic Migrations

- [ ] `MIG-001`: Initialize Alembic.
  - Goal: Add migration infrastructure.
  - Learn: Schema versioning.
  - Verify: Alembic config exists.

- [ ] `MIG-002`: Connect Alembic to app metadata.
  - Goal: Enable autogeneration.
  - Learn: Metadata discovery.
  - Verify: Alembic sees SQLAlchemy models.

- [ ] `MIG-003`: Configure database URL for migrations.
  - Goal: Avoid hardcoded DB config.
  - Learn: Environment-based migrations.
  - Verify: Alembic uses configured URL.

- [ ] `MIG-004`: Create first empty migration.
  - Goal: Prove migration workflow.
  - Learn: Migration revision structure.
  - Verify: Migration runs successfully.

- [ ] `MIG-005`: Document migration commands.
  - Goal: Make DB workflow repeatable.
  - Learn: Developer ergonomics.
  - Verify: README includes upgrade and revision commands.

### 13. User Module

- [ ] `USER-001`: Create user SQLAlchemy model.
  - Goal: Store user accounts.
  - Learn: Model fields and constraints.
  - Verify: User table has ID, email, password hash, timestamps.

- [ ] `USER-002`: Add unique email constraint.
  - Goal: Prevent duplicate accounts.
  - Learn: Database-level invariants.
  - Verify: Duplicate email insert fails.

- [ ] `USER-003`: Create user schemas.
  - Goal: Separate create, update, and read contracts.
  - Learn: Safe API boundaries.
  - Verify: Password hash never appears in read schema.

- [ ] `USER-004`: Create user repository.
  - Goal: Encapsulate user queries.
  - Learn: Repository pattern.
  - Verify: Repository can create and fetch user by email.

- [ ] `USER-005`: Create user service.
  - Goal: Encapsulate user business rules.
  - Learn: Service layer.
  - Verify: Service handles duplicate email case cleanly.

- [ ] `USER-006`: Add users migration.
  - Goal: Create user table.
  - Learn: Model-to-migration flow.
  - Verify: Migration applies successfully.

- [ ] `USER-007`: Add user tests.
  - Goal: Verify user persistence and service behavior.
  - Learn: Unit vs integration test boundaries.
  - Verify: Create, fetch, and duplicate cases are tested.

### 14. Auth Module

- [ ] `AUTH-001`: Choose token strategy.
  - Goal: Decide JWT vs opaque server-side tokens.
  - Learn: Auth architecture tradeoffs.
  - Verify: Decision is documented in notes.

- [ ] `AUTH-002`: Add password hashing utility.
  - Goal: Hash and verify passwords.
  - Learn: Secure password storage.
  - Verify: Plaintext passwords are never stored.

- [ ] `AUTH-003`: Add registration endpoint.
  - Goal: Create users through API.
  - Learn: Auth request flow.
  - Verify: `POST /auth/register` creates a user.

- [ ] `AUTH-004`: Add login endpoint.
  - Goal: Exchange credentials for token/session.
  - Learn: Authentication flow.
  - Verify: Valid credentials succeed and invalid credentials return generic error.

- [ ] `AUTH-005`: Add current user dependency.
  - Goal: Protect routes.
  - Learn: FastAPI security dependencies.
  - Verify: Protected route can access current user.

- [ ] `AUTH-006`: Add token expiry handling.
  - Goal: Prevent unlimited token validity.
  - Learn: Token lifetime design.
  - Verify: Expired tokens are rejected.

- [ ] `AUTH-007`: Add refresh or re-login decision.
  - Goal: Decide how sessions continue.
  - Learn: Token lifecycle.
  - Verify: Decision is documented and implemented consistently.

- [ ] `AUTH-008`: Add logout behavior.
  - Goal: Make session ending explicit.
  - Learn: Stateless vs stateful token tradeoffs.
  - Verify: Logout behavior matches chosen token strategy.

- [ ] `AUTH-009`: Add auth tests.
  - Goal: Verify auth correctness.
  - Learn: Security testing.
  - Verify: Register, login, invalid login, protected route, and expired token cases are tested.

### 15. Organization Module

- [ ] `ORG-001`: Create organization model.
  - Goal: Store organizations.
  - Learn: Ownership and tenancy.
  - Verify: Organization has ID, name, slug, timestamps.

- [ ] `ORG-002`: Create organization membership model.
  - Goal: Link users to organizations.
  - Learn: Association tables.
  - Verify: Membership includes user, organization, and role.

- [ ] `ORG-003`: Add membership uniqueness constraint.
  - Goal: Prevent duplicate memberships.
  - Learn: Composite uniqueness.
  - Verify: Same user cannot join same organization twice.

- [ ] `ORG-004`: Create organization schemas.
  - Goal: Define org API contracts.
  - Learn: Request/response separation.
  - Verify: Read schema includes current user's role when appropriate.

- [ ] `ORG-005`: Create organization repository.
  - Goal: Encapsulate org queries.
  - Learn: Tenant-scoped querying.
  - Verify: Repository can list organizations for a user.

- [ ] `ORG-006`: Create organization service.
  - Goal: Add org creation business logic.
  - Learn: Multi-write service operations.
  - Verify: Creating an org also creates owner membership.

- [ ] `ORG-007`: Add organization endpoints.
  - Goal: Expose org CRUD.
  - Learn: Protected resource endpoints.
  - Verify: Authenticated user can create and list orgs.

- [ ] `ORG-008`: Add org tests.
  - Goal: Verify org behavior.
  - Learn: Authenticated API tests.
  - Verify: Create/list/get/update/delete paths are covered.

### 16. Project Module

- [ ] `PROJ-001`: Create project model.
  - Goal: Store projects under organizations.
  - Learn: Foreign key relationships.
  - Verify: Project belongs to organization.

- [ ] `PROJ-002`: Add project uniqueness rule.
  - Goal: Avoid duplicate project slugs inside one organization.
  - Learn: Composite unique constraints.
  - Verify: Same slug is allowed across orgs but not within one org.

- [ ] `PROJ-003`: Create project schemas.
  - Goal: Define project API contracts.
  - Learn: Nested resource design.
  - Verify: Create schema does not accept organization ID from body when path owns it.

- [ ] `PROJ-004`: Create project repository.
  - Goal: Query projects by organization.
  - Learn: Scoped repositories.
  - Verify: Repository never fetches projects without tenant context unless intentional.

- [ ] `PROJ-005`: Create project service.
  - Goal: Enforce project business rules.
  - Learn: Service orchestration.
  - Verify: Service validates organization access before create.

- [ ] `PROJ-006`: Add project endpoints.
  - Goal: Expose project CRUD.
  - Learn: Nested and direct resource routes.
  - Verify: User can manage projects only in accessible orgs.

- [ ] `PROJ-007`: Add project tests.
  - Goal: Verify project access and behavior.
  - Learn: Resource authorization tests.
  - Verify: Cross-organization project access is rejected.

### 17. Task Module With Database

- [ ] `TASK-DB-001`: Create task model.
  - Goal: Persist tasks.
  - Learn: Model design for core resource.
  - Verify: Task belongs to project and optionally assignee.

- [ ] `TASK-DB-002`: Add task status and priority fields.
  - Goal: Store workflow state.
  - Learn: Enum-like database fields.
  - Verify: Invalid statuses cannot enter through API.

- [ ] `TASK-DB-003`: Add task indexes.
  - Goal: Support common list queries.
  - Learn: Basic indexing.
  - Verify: Indexes exist for project, status, assignee, and created date as needed.

- [ ] `TASK-DB-004`: Replace in-memory task store with repository.
  - Goal: Move task persistence to DB.
  - Learn: Swapping implementation behind stable API.
  - Verify: Existing task API tests still pass after adapting fixtures.

- [ ] `TASK-DB-005`: Create task service.
  - Goal: Enforce task rules.
  - Learn: Business logic placement.
  - Verify: Assigning a task validates assignee membership.

- [ ] `TASK-DB-006`: Add task create endpoint with DB.
  - Goal: Persist task creation.
  - Learn: DB-backed POST endpoint.
  - Verify: Created task survives process restart.

- [ ] `TASK-DB-007`: Add task list endpoint with DB filters.
  - Goal: Query tasks efficiently.
  - Learn: Translating API filters to DB queries.
  - Verify: Filtering and sorting work against DB.

- [ ] `TASK-DB-008`: Add task update endpoint with DB.
  - Goal: Update persisted tasks.
  - Learn: Partial updates and persistence.
  - Verify: Updated fields are saved.

- [ ] `TASK-DB-009`: Add task delete behavior.
  - Goal: Decide hard delete or soft delete.
  - Learn: Data lifecycle.
  - Verify: Delete behavior is documented and tested.

- [ ] `TASK-DB-010`: Add task DB tests.
  - Goal: Verify persistence behavior.
  - Learn: Integration test design.
  - Verify: CRUD, filtering, sorting, and authorization paths are tested.

### 18. Authorization And Tenancy

- [ ] `AUTHZ-001`: Define role permissions.
  - Goal: Document what owner, admin, member, and viewer can do.
  - Learn: Authorization matrix.
  - Verify: Matrix exists in notes or README.

- [ ] `AUTHZ-002`: Create organization access dependency.
  - Goal: Reuse org membership checks.
  - Learn: Dependency composition.
  - Verify: Endpoints can require org membership.

- [ ] `AUTHZ-003`: Create role-required dependency.
  - Goal: Enforce minimum role.
  - Learn: Dependency factories.
  - Verify: Routes can require admin or owner.

- [ ] `AUTHZ-004`: Add project access dependency.
  - Goal: Prevent cross-organization project access.
  - Learn: Resource-scoped authorization.
  - Verify: User cannot fetch project from unrelated org.

- [ ] `AUTHZ-005`: Add task access dependency.
  - Goal: Prevent task IDOR.
  - Learn: Object-level authorization.
  - Verify: User cannot fetch task from unrelated project/org.

- [ ] `AUTHZ-006`: Add authorization denial logging.
  - Goal: Observe suspicious access attempts.
  - Learn: Security logging.
  - Verify: Denials log non-sensitive context.

- [ ] `AUTHZ-007`: Add authorization matrix tests.
  - Goal: Test permissions systematically.
  - Learn: Table-driven tests.
  - Verify: Each role is tested for allowed and forbidden actions.

### 19. Comments And Activity

- [ ] `COMMENT-001`: Create task comment model.
  - Goal: Store comments on tasks.
  - Learn: Parent-child relationships.
  - Verify: Comment belongs to task and author.

- [ ] `COMMENT-002`: Create comment schemas.
  - Goal: Define comment contracts.
  - Learn: Text validation.
  - Verify: Empty comments are rejected.

- [ ] `COMMENT-003`: Add create comment endpoint.
  - Goal: Allow collaboration on tasks.
  - Learn: Nested resource POST.
  - Verify: Authorized user can comment.

- [ ] `COMMENT-004`: Add list comments endpoint.
  - Goal: Read comments for a task.
  - Learn: Ordered collection endpoints.
  - Verify: Comments return in expected order.

- [ ] `COMMENT-005`: Create task activity event model.
  - Goal: Track important task changes.
  - Learn: Event-style tables.
  - Verify: Event records action, actor, task, and timestamp.

- [ ] `COMMENT-006`: Write activity event on task creation.
  - Goal: Record lifecycle event.
  - Learn: Side effects inside transactions.
  - Verify: Creating task creates activity event.

- [ ] `COMMENT-007`: Write activity event on comment creation.
  - Goal: Record collaboration event.
  - Learn: Consistent event recording.
  - Verify: Creating comment creates activity event.

- [ ] `COMMENT-008`: Add task activity endpoint.
  - Goal: Expose activity timeline.
  - Learn: Timeline API design.
  - Verify: Activity endpoint returns ordered events.

### 20. Audit Logs

- [ ] `AUDIT-001`: Define audit event categories.
  - Goal: Decide what must be audited.
  - Learn: Difference between audit logs and app logs.
  - Verify: Sensitive actions are listed.

- [ ] `AUDIT-002`: Create audit log model.
  - Goal: Persist audit records.
  - Learn: Append-only data design.
  - Verify: Audit table has actor, action, resource, metadata, timestamp.

- [ ] `AUDIT-003`: Create audit service.
  - Goal: Centralize audit writes.
  - Learn: Cross-cutting services.
  - Verify: Code can record audit events through one interface.

- [ ] `AUDIT-004`: Audit login success and failure safely.
  - Goal: Track auth activity.
  - Learn: Security observability.
  - Verify: Logs do not include passwords or tokens.

- [ ] `AUDIT-005`: Audit membership changes.
  - Goal: Track permission-sensitive changes.
  - Learn: Admin action auditing.
  - Verify: Role changes create audit records.

- [ ] `AUDIT-006`: Add audit list endpoint.
  - Goal: Expose audit records to authorized users.
  - Learn: Admin-only list endpoints.
  - Verify: Only permitted roles can access audit logs.

- [ ] `AUDIT-007`: Add audit tests.
  - Goal: Verify audit behavior.
  - Learn: Side-effect testing.
  - Verify: Sensitive actions produce audit records.

### 21. Middleware

- [ ] `MW-001`: Add request ID middleware.
  - Goal: Assign ID to each request.
  - Learn: Middleware request flow.
  - Verify: Response includes request ID header.

- [ ] `MW-002`: Store request ID on request state.
  - Goal: Make request ID available to handlers.
  - Learn: `request.state`.
  - Verify: Error handler can read request ID.

- [ ] `MW-003`: Add request timing middleware.
  - Goal: Measure latency.
  - Learn: Middleware wrapping.
  - Verify: Logs include request duration.

- [ ] `MW-004`: Add structured access logs.
  - Goal: Log method, path, status, duration, and request ID.
  - Learn: Observability basics.
  - Verify: Each request emits one safe access log.

- [ ] `MW-005`: Add CORS middleware.
  - Goal: Configure browser access.
  - Learn: CORS rules.
  - Verify: Allowed origins come from settings.

- [ ] `MW-006`: Add security headers middleware.
  - Goal: Add conservative headers.
  - Learn: API hardening.
  - Verify: Responses include configured headers.

- [ ] `MW-007`: Document middleware order.
  - Goal: Understand execution order.
  - Learn: Starlette middleware stack.
  - Verify: Notes explain request and response traversal order.

### 22. Lifespan

- [ ] `LIFE-001`: Add lifespan function.
  - Goal: Manage startup and shutdown behavior.
  - Learn: FastAPI lifespan API.
  - Verify: Startup and shutdown messages are logged safely.

- [ ] `LIFE-002`: Move startup checks into lifespan.
  - Goal: Keep runtime initialization centralized.
  - Learn: Resource lifecycle.
  - Verify: App startup can verify required config.

- [ ] `LIFE-003`: Add DB engine cleanup on shutdown.
  - Goal: Close resources cleanly.
  - Learn: Async cleanup.
  - Verify: Shutdown disposes DB engine.

- [ ] `LIFE-004`: Add lifespan tests.
  - Goal: Verify lifecycle behavior.
  - Learn: Testing app lifespan.
  - Verify: Test client triggers startup and shutdown correctly.

### 23. Background Work

- [ ] `BG-001`: Add notification model.
  - Goal: Store notification records.
  - Learn: Async work data modeling.
  - Verify: Notification belongs to user and has status.

- [ ] `BG-002`: Add notification service.
  - Goal: Encapsulate notification creation.
  - Learn: Service side effects.
  - Verify: Service can create pending notification.

- [ ] `BG-003`: Use FastAPI `BackgroundTasks`.
  - Goal: Send simulated notification after response.
  - Learn: In-process background task limitations.
  - Verify: API responds before simulated work completes.

- [ ] `BG-004`: Add outbox table.
  - Goal: Record reliable events for later processing.
  - Learn: Outbox pattern.
  - Verify: Domain event is stored in same transaction as business change.

- [ ] `BG-005`: Add simple outbox processor command.
  - Goal: Process pending events manually.
  - Learn: Worker-style code without full broker.
  - Verify: Pending events can be marked processed.

- [ ] `BG-006`: Document when to replace this with a real worker.
  - Goal: Understand production tradeoffs.
  - Learn: In-process tasks vs external workers.
  - Verify: Notes explain limitations clearly.

### 24. File Attachments

- [ ] `FILE-001`: Add attachment model.
  - Goal: Store file metadata.
  - Learn: File metadata vs file content.
  - Verify: Attachment belongs to task and uploader.

- [ ] `FILE-002`: Choose local storage path.
  - Goal: Store files outside public route paths.
  - Learn: Safe file storage basics.
  - Verify: Storage path is configurable.

- [ ] `FILE-003`: Add upload endpoint.
  - Goal: Accept multipart file uploads.
  - Learn: `UploadFile`.
  - Verify: Authorized user can upload file to accessible task.

- [ ] `FILE-004`: Generate server-side file names.
  - Goal: Avoid trusting user filenames.
  - Learn: File handling security.
  - Verify: Stored file name is generated by server.

- [ ] `FILE-005`: Validate file size.
  - Goal: Prevent oversized uploads.
  - Learn: Request and file limits.
  - Verify: Oversized file is rejected.

- [ ] `FILE-006`: Validate allowed extensions.
  - Goal: Restrict supported file types.
  - Learn: Allow-list validation.
  - Verify: Unsupported extension is rejected.

- [ ] `FILE-007`: Add attachment list endpoint.
  - Goal: Show task attachments.
  - Learn: Nested resource lists.
  - Verify: User can list attachments for accessible task.

- [ ] `FILE-008`: Add attachment download endpoint.
  - Goal: Serve stored files safely.
  - Learn: File responses.
  - Verify: Unauthorized users cannot download files.

- [ ] `FILE-009`: Add file upload tests.
  - Goal: Verify file behavior.
  - Learn: Multipart testing.
  - Verify: Valid upload, invalid type, oversized file, and unauthorized access are tested.

### 25. WebSockets

- [ ] `WS-001`: Create WebSocket router.
  - Goal: Add a dedicated place for WebSocket endpoints.
  - Learn: HTTP route vs WebSocket route separation.
  - Verify: Router is included under `/api/v1/ws`.

- [ ] `WS-002`: Add task WebSocket endpoint.
  - Goal: Allow clients to connect to task activity stream.
  - Learn: WebSocket accept/send flow.
  - Verify: Client can connect to a task stream.

- [ ] `WS-003`: Authenticate WebSocket connection.
  - Goal: Prevent unauthorized streams.
  - Learn: Auth with long-lived connections.
  - Verify: Missing or invalid token is rejected.

- [ ] `WS-004`: Authorize task access on connect.
  - Goal: Prevent task activity IDOR.
  - Learn: Object-level auth for WebSockets.
  - Verify: User cannot connect to inaccessible task stream.

- [ ] `WS-005`: Add connection manager.
  - Goal: Track active task connections.
  - Learn: In-memory connection state.
  - Verify: Connections are added and removed safely.

- [ ] `WS-006`: Broadcast task activity events.
  - Goal: Notify connected clients.
  - Learn: Push-style backend behavior.
  - Verify: Task update emits message to connected clients.

- [ ] `WS-007`: Handle disconnects.
  - Goal: Avoid leaked connections.
  - Learn: WebSocket lifecycle.
  - Verify: Disconnect removes client from manager.

- [ ] `WS-008`: Document scaling limitation.
  - Goal: Understand why in-memory WebSockets do not scale across processes.
  - Learn: Multi-worker architecture.
  - Verify: Notes explain need for Redis pub/sub or similar later.

### 26. Idempotency

- [ ] `IDEMP-001`: Define idempotency key policy.
  - Goal: Decide where idempotency is required.
  - Learn: Retry-safe API design.
  - Verify: Policy says which endpoints require keys.

- [ ] `IDEMP-002`: Add idempotency table.
  - Goal: Store request keys and responses.
  - Learn: Persistence for retry behavior.
  - Verify: Table tracks key, user, route, and result.

- [ ] `IDEMP-003`: Add idempotency dependency.
  - Goal: Reuse idempotency handling.
  - Learn: Cross-cutting dependency design.
  - Verify: Create endpoints can use the dependency.

- [ ] `IDEMP-004`: Apply idempotency to task creation.
  - Goal: Prevent duplicate task creation on retries.
  - Learn: Exactly-once API behavior approximation.
  - Verify: Same key returns same outcome.

- [ ] `IDEMP-005`: Add idempotency tests.
  - Goal: Prove retry behavior.
  - Learn: Race and duplicate request testing basics.
  - Verify: Duplicate request does not create duplicate resource.

### 27. Testing Infrastructure

- [x] `TEST-001`: Add pytest dependencies.
  - Goal: Enable tests.
  - Learn: Test tooling.
  - Verify: `pytest` runs.

- [x] `TEST-002`: Add API test client fixture.
  - Goal: Reuse client setup.
  - Learn: FastAPI testing.
  - Verify: Tests can call app endpoints.

- [x] `TEST-003`: Add settings override fixture.
  - Goal: Run tests with test config.
  - Learn: Dependency override strategy.
  - Verify: Tests do not use local production-like config.

- [ ] `TEST-004`: Add database fixture.
  - Goal: Isolate DB tests.
  - Learn: Test database lifecycle.
  - Verify: Tests start from clean database state.

- [ ] `TEST-005`: Add authenticated user fixture.
  - Goal: Simplify protected endpoint tests.
  - Learn: Test data factories.
  - Verify: Tests can request as a logged-in user.

- [ ] `TEST-006`: Add organization fixture.
  - Goal: Reuse tenancy setup.
  - Learn: Fixture composition.
  - Verify: Tests can create org with membership.

- [ ] `TEST-007`: Add project fixture.
  - Goal: Reuse project setup.
  - Learn: Layered fixtures.
  - Verify: Tests can create project under org.

- [ ] `TEST-008`: Add task fixture.
  - Goal: Reuse task setup.
  - Learn: Factory-style testing.
  - Verify: Tests can create task under project.

- [ ] `TEST-009`: Add validation error tests.
  - Goal: Verify API rejects bad input.
  - Learn: Negative API testing.
  - Verify: Invalid payloads return expected errors.

- [ ] `TEST-010`: Add auth failure tests.
  - Goal: Verify protected endpoints.
  - Learn: Security regression testing.
  - Verify: Missing, invalid, and expired tokens are rejected.

- [ ] `TEST-011`: Add authorization failure tests.
  - Goal: Verify tenant isolation.
  - Learn: IDOR test design.
  - Verify: Cross-org access attempts fail.

- [ ] `TEST-012`: Add OpenAPI schema smoke test.
  - Goal: Ensure docs generation stays healthy.
  - Learn: Contract testing basics.
  - Verify: `/openapi.json` returns valid schema.

### 28. Docker And Compose

- [ ] `DOCKER-001`: Create `.dockerignore`.
  - Goal: Keep images clean.
  - Learn: Docker build context.
  - Verify: Virtualenvs, caches, and local files are excluded.

- [ ] `DOCKER-002`: Create Dockerfile.
  - Goal: Build app image.
  - Learn: Python container basics.
  - Verify: Image builds.

- [ ] `DOCKER-003`: Use `uv` in Docker build.
  - Goal: Install dependencies consistently.
  - Learn: Reproducible container builds.
  - Verify: Build uses lockfile workflow.

- [ ] `DOCKER-004`: Run as non-root user.
  - Goal: Harden runtime container.
  - Learn: Container least privilege.
  - Verify: Dockerfile sets non-root user.

- [ ] `DOCKER-005`: Add app health check.
  - Goal: Make container health observable.
  - Learn: Container health checks.
  - Verify: Health check calls `/health`.

- [ ] `COMPOSE-001`: Add Postgres service.
  - Goal: Run DB locally.
  - Learn: Compose services and volumes.
  - Verify: Postgres starts with named volume.

- [ ] `COMPOSE-002`: Add app service.
  - Goal: Run API with DB.
  - Learn: Compose networking.
  - Verify: App reaches DB service by service name.

- [ ] `COMPOSE-003`: Add environment file example.
  - Goal: Document required variables safely.
  - Learn: Secret handling basics.
  - Verify: Example file contains placeholders only, not real secrets.

- [ ] `COMPOSE-004`: Document compose commands.
  - Goal: Make local startup easy.
  - Learn: Developer onboarding.
  - Verify: README has start, stop, logs, and reset commands.

### 29. Developer Experience

- [ ] `DX-001`: Add lint command.
  - Goal: Make code style checks easy.
  - Learn: Ruff workflow.
  - Verify: One command runs linting.

- [ ] `DX-002`: Add format command.
  - Goal: Make formatting repeatable.
  - Learn: Automated formatting.
  - Verify: One command formats code.

- [ ] `DX-003`: Add type check command.
  - Goal: Catch type issues.
  - Learn: Static typing workflow.
  - Verify: One command runs type checks.

- [ ] `DX-004`: Add test command.
  - Goal: Make tests easy to run.
  - Learn: Test workflow.
  - Verify: One command runs all tests.

- [ ] `DX-005`: Add migration commands.
  - Goal: Make DB changes repeatable.
  - Learn: Alembic workflow.
  - Verify: Commands exist for creating and applying migrations.

- [ ] `DX-006`: Add README quickstart.
  - Goal: Let a new developer run the project.
  - Learn: Documentation discipline.
  - Verify: Quickstart works from clean checkout.

### 30. Documentation And Learning Notes

- [ ] `DOC-001`: Write project overview.
  - Goal: Explain what TaskForge is.
  - Learn: Communicating system purpose.
  - Verify: README has a short overview.

- [ ] `DOC-002`: Write architecture notes.
  - Goal: Explain app layers.
  - Learn: Architecture communication.
  - Verify: Notes include router, service, repository, DB flow.

- [ ] `DOC-003`: Write API design notes.
  - Goal: Explain API conventions.
  - Learn: API consistency.
  - Verify: Notes cover paths, status codes, errors, pagination.

- [ ] `DOC-004`: Write auth notes.
  - Goal: Explain auth decisions.
  - Learn: Security tradeoffs.
  - Verify: Notes cover password hashing and token/session strategy.

- [ ] `DOC-005`: Write authorization notes.
  - Goal: Explain tenancy and roles.
  - Learn: Access control communication.
  - Verify: Notes include role matrix.

- [ ] `DOC-006`: Write DB notes.
  - Goal: Explain schema design lightly.
  - Learn: Database reasoning.
  - Verify: Notes include entities, relationships, and key constraints.

- [ ] `DOC-007`: Write ASGI notes.
  - Goal: Explain request lifecycle.
  - Learn: FastAPI internals.
  - Verify: Notes describe ASGI, Uvicorn, Starlette, FastAPI responsibilities.

- [ ] `DOC-008`: Write dependency injection notes.
  - Goal: Explain FastAPI dependency resolution.
  - Learn: Internals of dependencies.
  - Verify: Notes trace one protected request dependency graph.

- [ ] `DOC-009`: Write Pydantic notes.
  - Goal: Explain validation and serialization.
  - Learn: Pydantic internals at practical level.
  - Verify: Notes cover request validation and response serialization.

- [ ] `DOC-010`: Write async notes.
  - Goal: Explain async backend behavior.
  - Learn: Event loop and blocking IO.
  - Verify: Notes explain when to use async and what to avoid.

- [ ] `DOC-011`: Write middleware notes.
  - Goal: Explain middleware order and purpose.
  - Learn: Request/response wrapping.
  - Verify: Notes include order of middleware execution.

- [ ] `DOC-012`: Write testing notes.
  - Goal: Explain the test strategy.
  - Learn: Test pyramid for APIs.
  - Verify: Notes distinguish unit, API, and integration tests.

### 31. Final Review

- [ ] `FINAL-001`: Run all tests.
  - Goal: Verify app behavior.
  - Learn: Regression safety.
  - Verify: Full test suite passes.

- [ ] `FINAL-002`: Run linting.
  - Goal: Verify code quality.
  - Learn: Static quality checks.
  - Verify: Lint command passes.

- [ ] `FINAL-003`: Run formatting check.
  - Goal: Verify formatting consistency.
  - Learn: Automated formatting discipline.
  - Verify: Format check passes.

- [ ] `FINAL-004`: Run type checks.
  - Goal: Verify type health.
  - Learn: Static typing.
  - Verify: Type check command passes or documented exceptions exist.

- [ ] `FINAL-005`: Run app locally with `uv`.
  - Goal: Verify local runtime.
  - Learn: App startup workflow.
  - Verify: App serves docs and health endpoint.

- [ ] `FINAL-006`: Run app through Docker Compose.
  - Goal: Verify containerized runtime.
  - Learn: Local production-like environment.
  - Verify: App and Postgres start together.

- [ ] `FINAL-007`: Apply migrations from scratch.
  - Goal: Verify DB reproducibility.
  - Learn: Migration discipline.
  - Verify: Empty DB can be migrated to current schema.

- [ ] `FINAL-008`: Walk through primary user flow.
  - Goal: Verify end-to-end behavior.
  - Learn: Product-level testing.
  - Verify: Register, login, create org, create project, create task, comment, upload, and view activity all work.

- [ ] `FINAL-009`: Review security checklist.
  - Goal: Catch obvious unsafe patterns.
  - Learn: Security review habit.
  - Verify: No hardcoded secrets, unsafe auth responses, or cross-tenant access gaps are found.

- [ ] `FINAL-010`: Review docs.
  - Goal: Make project understandable later.
  - Learn: Maintainable project handoff.
  - Verify: README and notes explain setup, architecture, API, and internals.

## How To Use This File

Use this file as the main project roadmap.

Recommended workflow:

1. Pick one task.
2. Switch to Ask mode if you want explanation first.
3. Ask for implementation guidance for that task.
4. Implement the task.
5. Add tests.
6. Update README or notes.
7. Move to the next task.

Do not rush through the tasks. The point of this project is to understand each layer deeply enough that you can explain the design, the tradeoffs, and the internals.
