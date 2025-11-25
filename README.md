# Cloud Tech Lab 10-15: PostgreSQL, Redis & Database Integration

This project extends the existing OpenF1 API application with cloud database capabilities, implementing PostgreSQL for persistent storage and Redis for caching.

## 📋 Table of Contents
- [Overview](#overview)
- [Features Implemented](#features-implemented)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Database Migrations](#database-migrations)
- [Deployment to Render](#deployment-to-render)
- [Testing](#testing)
- [Project Structure](#project-structure)

## 🎯 Overview

This implementation fulfills Lab 10-15 requirements by integrating:
- **PostgreSQL** - Cloud relational database for user management
- **Redis** - Cloud key-value store for caching API responses
- **Alembic** - Database migration tool for schema version control
- **SQLAlchemy** - Async ORM for database operations

## ✨ Features Implemented

### 1. PostgreSQL Integration
**Why**: Store user data persistently in a cloud database  
**How**: Using async SQLAlchemy with PostgreSQL on Render

- **User Model**: Defined with email, password, and active status
- **Repository Pattern**: Clean separation of data access logic
- **Async Operations**: Non-blocking database queries for better performance
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality

**Files**:
- `database.py` - Database connection and session management
- `models.py` - User ORM model definition
- `schemas.py` - Pydantic validation schemas
- `repository.py` - Database operations abstraction
- `user_router.py` - REST API endpoints

### 2. Database Migrations (Alembic)
**Why**: Version control for database schema changes  
**How**: Alembic configured for async SQLAlchemy

- Automatic migration generation based on model changes
- Tracks database schema history
- Allows rollback to previous versions
- Works seamlessly with cloud databases

**Files**:
- `alembic.ini` - Alembic configuration
- `migrations/env.py` - Migration environment setup
- `migrations/versions/` - Migration scripts

### 3. Redis Caching
**Why**: Reduce external API calls and improve response times  
**How**: Upstash Redis with async client

**Direct Cache Endpoints**:
- Store and retrieve arbitrary key-value pairs
- Useful for testing and direct cache management

**OpenF1 API Caching**:
- Automatically caches driver and meeting data
- 60-second TTL (configurable)
- 50%+ performance improvement on cached responses
- Cache keys based on query parameters

**Files**:
- `redis_client.py` - Redis connection factory
- `redis_router.py` - Cache management endpoints
- `external_api/service.py` - Modified to include caching logic

## 🏗️ Architecture

```
┌─────────────────┐
│   FastAPI App   │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼───┐ ┌──▼──┐  ┌────▼────┐ ┌──▼──────┐
│ F1 API│ │Users│  │  Cache  │ │ Root    │
│       │ │     │  │         │ │         │
└───┬───┘ └──┬──┘  └────┬────┘ └─────────┘
    │        │          │
┌───▼────┐ ┌▼────────┐ │
│OpenF1  │ │User Repo│ │
│Service │ │         │ │
│+Cache  │ └─┬───────┘ │
└───┬────┘   │         │
    │        │         │
    │     ┌──▼─────┐ ┌─▼────┐
    └────►│  PG    │ │Redis │
          │Database│ │Cache │
          └────────┘ └──────┘
```

## 📦 Prerequisites

1. **Python 3.11+**
2. **PostgreSQL Database** (Cloud)
   - Render PostgreSQL (Free tier)
   - Or any PostgreSQL provider
3. **Redis Instance** (Cloud)
   - Upstash Redis (Pay-as-you-go/Free)
   - Or any Redis provider
4. **Git** (for version control)

## 🚀 Installation & Setup

### Step 1: Clone and Navigate
```bash
cd cloud-tech-lab-7-9
git checkout lab-10-15
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:

```env
# PostgreSQL Connection
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database

# Redis Connection  
REDIS_URL=rediss://default:token@host:6379
```

**Getting Database URLs**:

**PostgreSQL (Render)**:
1. Go to Render Dashboard → New → PostgreSQL
2. Choose Free plan
3. After creation, go to Info tab → Connections
4. Copy **External Database URL**
5. Replace `postgresql://` with `postgresql+asyncpg://`

**Redis (Upstash)**:
1. Go to Upstash Console → Redis → Create Database
2. Choose Pay-as-you-go (free up to daily limits)
3. Copy the Redis URL from dashboard
4. Should look like: `rediss://default:token@host:6379`

### Step 5: Run Database Migrations
```bash
alembic upgrade head
```

This creates the `users` table in your PostgreSQL database.

## 🎮 Running the Application

### Development Mode
```bash
uvicorn main:app --reload --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Access the Application
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Root Endpoint**: http://localhost:8000/

## 📡 API Endpoints

### 1. User Management (`/users`)

#### Create User
```http
POST /users/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "is_active": true
}
```

#### Get All Users
```http
GET /users/?skip=0&limit=100
```

#### Get Specific User
```http
GET /users/{user_id}
```

#### Update User
```http
PUT /users/{user_id}
Content-Type: application/json

{
  "email": "newemail@example.com",
  "is_active": false
}
```

#### Delete User
```http
DELETE /users/{user_id}
```

### 2. Redis Cache (`/cache`)

#### Set Cache Value
```http
POST /cache/set?key=mykey&value=myvalue
```

#### Get Cache Value  
```http
GET /cache/get/{key}
```

### 3. Formula 1 Data (`/api/f1`)

These endpoints now include automatic caching!

#### Get Drivers (Cached)
```http
GET /api/f1/drivers?session_key=9158&driver_number=1
```

#### Get Meetings (Cached)
```http
GET /api/f1/meetings?year=2023&country_name=Singapore
```

#### Get Driver with Meeting Info
```http
GET /api/f1/driver-meetings?session_key=9158
```

## 🗄️ Database Migrations

### Why Migrations?
Migrations allow you to:
- Track database schema changes over time
- Deploy schema updates safely
- Rollback changes if needed
- Keep database in sync across environments

### Creating a New Migration
After modifying models in `models.py`:

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Applying Migrations
```bash
alembic upgrade head
```

### Viewing Migration History
```bash
alembic history
```

### Rolling Back
```bash
alembic downgrade -1  # Rollback one migration
```

## 🌐 Deployment to Render

### Step 1: Prepare Environment Variables
In Render Dashboard → Your Web Service → Environment:

Add:
```
DATABASE_URL=<Internal Database URL from Render PostgreSQL>
REDIS_URL=<Redis URL from Upstash>
```

**Important**: Use the **Internal Database URL** for Render deployments (not External).

### Step 2: Configure Build & Start Commands

**Build Command**:
```bash
pip install -r requirements.txt && alembic upgrade head
```

**Start Command**:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 3: Deploy
Push your changes to the `lab-10-15` branch and Render will automatically deploy.

### Step 4: Verify
Visit your deployed app's `/docs` endpoint to test the API.

## 🧪 Testing

### Automated Testing
Run the verification script:
```bash
python verify.py
```

This tests:
- ✅ PostgreSQL CRUD operations
- ✅ Redis cache set/get
- ✅ OpenF1 caching performance

### Manual Testing via Swagger UI
1. Navigate to http://localhost:8000/docs
2. Expand endpoint sections
3. Click "Try it out"
4. Fill in parameters
5. Execute and view response

### Testing Cache Performance
1. Call `/api/f1/drivers?session_key=9158` - Note the response time
2. Call the same endpoint again - Should be significantly faster (cached)
3. Wait 60 seconds (TTL expires)
4. Call again - Will be slower (fetches from API and re-caches)

## 📁 Project Structure

```
cloud-tech-lab-7-9/
├── external_api/              # OpenF1 API module
│   ├── __init__.py
│   ├── config.py             # App configuration (DB, Redis, API settings)
│   ├── dtos.py               # Data Transfer Objects
│   ├── router.py             # F1 endpoints
│   └── service.py            # Business logic + caching
│
├── migrations/               # Alembic migrations
│   ├── versions/
│   │   └── 7ba8a7c66d77_initial_migration.py
│   ├── env.py               # Migration environment
│   └── script.py.mako       # Migration template
│
├── database.py              # Database connection & session
├── models.py                # SQLAlchemy ORM models
├── schemas.py               # Pydantic schemas for validation
├── repository.py            # Data access layer
├── user_router.py           # User CRUD endpoints
│
├── redis_client.py          # Redis connection factory
├── redis_router.py          # Cache management endpoints
│
├── main.py                  # FastAPI application entry point
├── alembic.ini             # Alembic configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
├── .gitignore              # Git ignore rules
├── Dockerfile              # Docker configuration (legacy)
└── verify.py               # Automated test script
```

## 🔑 Key Concepts Explained

### Why Async?
- **Better Performance**: Non-blocking I/O allows handling multiple requests simultaneously
- **Database Operations**: PostgreSQL queries don't block the event loop
- **External APIs**: OpenF1 API calls don't freeze the application
- **Redis Operations**: Cache operations are lightning-fast and non-blocking

### Why Repository Pattern?
- **Separation of Concerns**: Database logic separated from business logic
- **Testability**: Easy to mock database operations in tests
- **Maintainability**: Changes to database queries don't affect routers
- **Flexibility**: Can swap database implementations without changing API

### Why Caching with Redis?
- **Performance**: Reduces response time by 50%+ for repeated queries
- **API Rate Limits**: Prevents hitting OpenF1 API limits
- **Cost Savings**: Fewer external API calls
- **Better UX**: Faster responses improve user experience

### Why Alembic?
- **Version Control**: Track database schema changes like code
- **Team Collaboration**: Everyone has the same database structure
- **Safe Deployments**: Apply schema changes without manual SQL
- **Rollback Capability**: Revert problematic changes easily

## 📊 Performance Metrics

Based on verification tests:

| Operation | Without Cache | With Cache | Improvement |
|-----------|--------------|------------|-------------|
| Get Drivers | ~470ms | ~220ms | **53% faster** |
| Get Meetings | ~500ms | ~230ms | **54% faster** |

## 🐛 Troubleshooting

### Database Connection Errors
- Verify `DATABASE_URL` is correct
- Check database is accessible from your IP
- For Render: Use **External URL** for local development, **Internal URL** for deployed apps

### Redis Connection Errors
- Verify `REDIS_URL` is correct and includes credentials
- Check Redis instance is running
- Ensure firewall allows connections

### Migration Errors
- Check models are imported in `migrations/env.py`
- Verify database user has CREATE TABLE permissions
- Try: `alembic downgrade -1` then `alembic upgrade head`

### Import Errors
- Activate virtual environment: `source .venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Redis Commands](https://redis.io/commands/)
- [Pydantic Models](https://docs.pydantic.dev/)

## 👤 Author

Lab 10-15 Implementation for Cloud Technologies Course

---

**Questions?** Check the Swagger UI documentation at `/docs` or the walkthrough.md file for more details.
