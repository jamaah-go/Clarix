# CLARIX - AI Contract Intelligence Platform

Production-ready implementation of an AI-native SaaS platform for legal document intelligence.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                      │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     │
│  │  Web Browser    │     │  Mobile Web     │     │  API Consumers  │     │
│  │  (Next.js 14)   │     │  (Next.js 14)   │     │  (REST/GraphQL) │     │
│  └────────┬────────┘     └────────┬────────┘     └────────┬────────┘     │
└───────────┼───────────────────────┼───────────────────────┼───────────────┘
            │                       │                       │
            ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EDGE / GATEWAY LAYER                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Vercel Edge Network (Global CDN, DDoS Protection, Rate Limiting)  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Vercel Serverless Functions (API Routes, Auth Middleware)         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────┬─────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      APPLICATION SERVICES LAYER                             │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐ │
│  │  Next.js 14 App      │  │  Python FastAPI    │  │  Background      │ │
│  │  (User Interface)    │  │  (Business Logic)   │  │  Workers         │ │
│  │                      │  │                     │  │  (Celery/Redis)  │ │
│  └──────────┬───────────┘  └──────────┬───────────┘  └────────┬─────────┘ │
└─────────────┼──────────────────────────┼─────────────────────────┼───────────┘
              │                          │                         │
              ▼                          ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │  Supabase       │  │  Pinecone       │  │  Supabase       │            │
│  │  PostgreSQL     │  │  Vector Store   │  │  Storage        │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Technology | Justification |
|-----------|-----------|--------------|
| Frontend | Next.js 14 App Router | Production-ready React framework |
| Backend | Python FastAPI | Strong async support, excellent LLM libraries |
| Database | Supabase PostgreSQL | Managed PostgreSQL with RLS |
| Vector Store | Pinecone | Managed vector DB with good scalability |
| Queue | Celery + Redis | Proven task queue |
| Auth | Supabase Auth | Built-in MFA, SSO |
| Payments | Stripe | Industry-standard billing |
| Hosting | Vercel + Railway | Optimized for Next.js and containers |
| LLM | Anthropic Claude + OpenAI GPT | Best-in-class for legal reasoning |

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker & Docker Compose
- Supabase account
- Pinecone account
- OpenAI API key
- Anthropic API key

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/your-org/clarix.git
cd clarix
```

2. Copy environment variables:
```bash
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.local.example apps/web/.env.local
```

3. Configure environment variables in `.env`:
```
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_JWT_SECRET=your-jwt-secret

# LLM Providers
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Stripe (optional)
STRIPE_API_KEY=sk_test_...

# Security
SECRET_KEY=your-secret-key-min-32-chars
```

4. Start local infrastructure:
```bash
docker-compose up -d
```

5. Run database migrations:
```bash
cd apps/api
alembic upgrade head
```

6. Start the development servers:
```bash
# Backend (Terminal 1)
cd apps/api
uvicorn src.main:app --reload

# Frontend (Terminal 2)
cd apps/web
npm run dev

# Celery Worker (Terminal 3)
cd apps/api
celery -A src.celery_app worker --loglevel=info
```

7. Access the application:
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Project Structure

```
clarix/
├── apps/
│   ├── api/                 # FastAPI backend
│   │   ├── src/
│   │   │   ├── config.py   # Configuration
│   │   │   ├── main.py     # App entry point
│   │   │   ├── routers/    # API routes
│   │   │   ├── services/   # Business logic
│   │   │   ├── tasks/      # Celery tasks
│   │   │   ├── middleware/ # Custom middleware
│   │   │   └── database/   # DB session management
│   │   └── migrations/     # Alembic migrations
│   │
│   └── web/                 # Next.js frontend
│       ├── src/
│       │   ├── app/        # App Router pages
│       │   ├── components/ # React components
│       │   ├── lib/        # Utilities
│       │   └── stores/     # State management
│       └── public/         # Static assets
│
├── packages/
│   ├── shared-types/       # Shared TypeScript types
│   ├── llm-orchestrator/   # LLM service
│   ├── clause-engine/      # Clause extraction
│   └── playbook-engine/    # Playbook service
│
├── infra/                  # Infrastructure as code
│   ├── terraform/          # Terraform configs
│   └── ansible/           # Ansible playbooks
│
├── scripts/               # Utility scripts
├── .github/workflows/     # CI/CD pipelines
├── turbo.json            # Turborepo config
└── docker-compose.yml     # Local development
```

## Key Features

### Document Ingestion
- Multi-format support (PDF, DOCX, TXT)
- OCR for scanned documents (AWS Textract)
- Layout-aware parsing (Unstructured.io)
- Sentence-aware chunking
- Content hashing for deduplication

### Clause Extraction
- 80+ clause categories
- LLM-powered extraction
- Confidence scoring
- Entity extraction (dates, amounts, parties)
- Cross-clause relationship modeling

### Redline Generation
- Diff-aware comparison
- Risk-based ranking
- Playbook integration
- Feedback loop for learning

### Monitoring
- Deadline tracking
- Obligation extraction
- Alert notifications
- Regulatory change monitoring

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user/tenant
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout

### Documents
- `GET /api/v1/documents` - List documents
- `POST /api/v1/documents` - Create document
- `GET /api/v1/documents/{id}` - Get document
- `DELETE /api/v1/documents/{id}` - Delete document

### Clauses
- `GET /api/v1/clauses` - List clauses
- `GET /api/v1/clauses/{id}` - Get clause
- `PATCH /api/v1/clauses/{id}` - Verify clause

### Playbooks
- `GET /api/v1/playbooks` - List playbooks
- `POST /api/v1/playbooks` - Create playbook
- `POST /api/v1/playbooks/{id}/rules` - Add rule

### Redlines
- `GET /api/v1/redlines` - List redlines
- `POST /api/v1/redlines` - Generate redlines
- `POST /api/v1/redlines/{id}/feedback` - Submit feedback

### Subscriptions
- `GET /api/v1/subscriptions` - Get subscription
- `POST /api/v1/subscriptions` - Create subscription
- `GET /api/v1/subscriptions/usage` - Get usage

## Deployment

### Production Deployment

1. **Vercel (Frontend)**
```bash
cd apps/web
vercel deploy --production
```

2. **Railway (Backend)**
```bash
railway deploy
```

3. **Environment Variables**
Set all required environment variables in your hosting platform.

### Docker Production Build

```bash
docker build -t clarix/api -f apps/api/Dockerfile apps/api/
docker build -t clarix/web -f apps/web/Dockerfile apps/web/
```

## Configuration

### Plan Tiers

| Feature | Starter | Professional | Enterprise |
|---------|---------|-------------|------------|
| Documents/month | 50 | 500 | Unlimited |
| Pages/month | 1,000 | 10,000 | Unlimited |
| Users | 5 | 25 | Unlimited |
| API Access | - | ✓ | ✓ |
| Custom Playbooks | - | ✓ | ✓ |
| SSO | - | - | ✓ |
| Support | Email | Priority | Dedicated |

## Security

- Row-level security (RLS) for tenant isolation
- JWT-based authentication
- Encrypted data at rest and in transit
- Audit logging for all operations
- SOC 2 compliance-ready architecture

## Monitoring

- Structured logging with structlog
- Error tracking with Sentry
- Metrics with Prometheus
- Distributed tracing with OpenTelemetry

## License

Proprietary - All rights reserved
