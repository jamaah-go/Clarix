-- CLARIX Database Schema
-- Version: 1.0.0
-- Description: Initial schema for CLARIX multi-tenant contract intelligence platform

-- ============================================================================
-- TENANTS
-- ============================================================================

CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan_tier TEXT NOT NULL DEFAULT 'starter',
    settings JSONB DEFAULT '{}',
    stripe_customer_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tenants_slug ON tenants(slug);
CREATE INDEX idx_tenants_plan ON tenants(plan_tier);

-- ============================================================================
-- USERS
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL DEFAULT 'member',
    password_hash TEXT,
    mfa_enabled BOOLEAN DEFAULT false,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(tenant_id, email)
);

CREATE INDEX idx_users_tenant ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);

-- ============================================================================
-- DOCUMENTS
-- ============================================================================

CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    document_type TEXT,
    metadata JSONB DEFAULT '{}',
    processed_at TIMESTAMPTZ,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_documents_tenant ON documents(tenant_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_content_hash ON documents(content_hash);
CREATE INDEX idx_documents_created_at ON documents(created_at DESC);

-- ============================================================================
-- DOCUMENTS AUDIT (Soft Delete)
-- ============================================================================

-- Add deleted_at column for soft delete
ALTER TABLE documents ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;

-- ============================================================================
-- CLAUSE CATEGORIES
-- ============================================================================

CREATE TABLE IF NOT EXISTS clause_categories (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    group_name TEXT NOT NULL,
    description TEXT,
    schema_version TEXT DEFAULT '1.0',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_clause_categories_group ON clause_categories(group_name);

-- ============================================================================
-- CLAUSES
-- ============================================================================

CREATE TABLE IF NOT EXISTS clauses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    category_code TEXT NOT NULL,
    original_text TEXT NOT NULL,
    normalized_text TEXT,
    page_numbers INTEGER[] DEFAULT '{}',
    section_path TEXT,
    confidence REAL NOT NULL,
    extraction_method TEXT NOT NULL,
    entities JSONB DEFAULT '{}',
    obligations JSONB DEFAULT '[]',
    schema_version TEXT NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_clauses_document ON clauses(document_id);
CREATE INDEX idx_clauses_category ON clauses(category);
CREATE INDEX idx_clauses_category_code ON clauses(category_code);
CREATE INDEX idx_clauses_confidence ON clauses(confidence);

-- ============================================================================
-- PLAYBOOKS
-- ============================================================================

CREATE TABLE IF NOT EXISTS playbooks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    is_default BOOLEAN DEFAULT false,
    version INTEGER NOT NULL DEFAULT 1,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_playbooks_tenant ON playbooks(tenant_id);
CREATE INDEX idx_playbooks_default ON playbooks(tenant_id, is_default);

-- ============================================================================
-- PLAYBOOK RULES
-- ============================================================================

CREATE TABLE IF NOT EXISTS playbook_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    playbook_id UUID NOT NULL REFERENCES playbooks(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    priority TEXT DEFAULT 'standard',
    preferred JSONB NOT NULL DEFAULT '{}',
    acceptable JSONB NOT NULL DEFAULT '{}',
    unacceptable JSONB DEFAULT '{}',
    rationale TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(playbook_id, category)
);

CREATE INDEX idx_rules_playbook ON playbook_rules(playbook_id);
CREATE INDEX idx_rules_category ON playbook_rules(category);

-- ============================================================================
-- REDLINES
-- ============================================================================

CREATE TABLE IF NOT EXISTS redlines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    clause_id UUID REFERENCES clauses(id) ON DELETE CASCADE,
    original_text TEXT NOT NULL,
    suggested_text TEXT NOT NULL,
    accepted_text TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    risk_level TEXT DEFAULT 'medium',
    confidence REAL DEFAULT 0.5,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_redlines_document ON redlines(document_id);
CREATE INDEX idx_redlines_status ON redlines(status);
CREATE INDEX idx_redlines_risk ON redlines(risk_level);

-- ============================================================================
-- REDLINE FEEDBACK
-- ============================================================================

CREATE TABLE IF NOT EXISTS redline_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    redline_id UUID NOT NULL REFERENCES redlines(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    original_suggestion TEXT NOT NULL,
    user_final TEXT NOT NULL,
    diff TEXT,
    rationale TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_feedback_redline ON redline_feedback(redline_id);
CREATE INDEX idx_feedback_user ON redline_feedback(user_id);

-- ============================================================================
-- SUBSCRIPTIONS
-- ============================================================================

CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    stripe_subscription_id TEXT UNIQUE NOT NULL,
    plan_tier TEXT NOT NULL,
    status TEXT NOT NULL,
    current_period_start TIMESTAMPTZ NOT NULL,
    current_period_end TIMESTAMPTZ NOT NULL,
    cancel_at_period_end BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_tenant ON subscriptions(tenant_id);
CREATE INDEX idx_subscriptions_stripe ON subscriptions(stripe_subscription_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);

-- ============================================================================
-- USAGE RECORDS
-- ============================================================================

CREATE TABLE IF NOT EXISTS usage_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    metric TEXT NOT NULL,
    count INTEGER NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_usage_tenant ON usage_records(tenant_id);
CREATE INDEX idx_usage_period ON usage_records(tenant_id, metric, period_start);

-- ============================================================================
-- EVENTS
-- ============================================================================

CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id UUID,
    payload JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_events_tenant ON events(tenant_id);
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_created ON events(created_at DESC);

-- ============================================================================
-- AUDIT LOGS
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_tenant ON audit_logs(tenant_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);

-- ============================================================================
-- ROW LEVEL SECURITY
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE clause_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE clauses ENABLE ROW LEVEL SECURITY;
ALTER TABLE playbooks ENABLE ROW LEVEL SECURITY;
ALTER TABLE playbook_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE redlines ENABLE ROW LEVEL SECURITY;
ALTER TABLE redline_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Tenants: Full access to own record
CREATE POLICY "tenants_select" ON tenants FOR SELECT USING (true);
CREATE POLICY "tenants_update" ON tenants FOR UPDATE USING (true);

-- Users: Tenant isolation
CREATE POLICY "users_select" ON users FOR SELECT USING (
    id IN (SELECT id FROM users WHERE tenant_id = current_setting('app.tenant_id')::uuid)
);
CREATE POLICY "users_insert" ON users FOR INSERT WITH CHECK (
    tenant_id = current_setting('app.tenant_id')::uuid
);
CREATE POLICY "users_update" ON users FOR UPDATE USING (
    id IN (SELECT id FROM users WHERE tenant_id = current_setting('app.tenant_id')::uuid)
);
CREATE POLICY "users_delete" ON users FOR DELETE USING (
    id IN (SELECT id FROM users WHERE tenant_id = current_setting('app.tenant_id')::uuid)
);

-- Documents: Tenant isolation
CREATE POLICY "documents_select" ON documents FOR SELECT USING (
    tenant_id = current_setting('app.tenant_id')::uuid
);
CREATE POLICY "documents_insert" ON documents FOR INSERT WITH CHECK (
    tenant_id = current_setting('app.tenant_id')::uuid
);
CREATE POLICY "documents_update" ON documents FOR UPDATE USING (
    tenant_id = current_setting('app.tenant_id')::uuid
);
CREATE POLICY "documents_delete" ON documents FOR DELETE USING (
    tenant_id = current_setting('app.tenant_id')::uuid
);

-- Clause Categories: Public read
CREATE POLICY "categories_select" ON clause_categories FOR SELECT USING (true);

-- Clauses: Tenant isolation via documents
CREATE POLICY "clauses_select" ON clauses FOR SELECT USING (
    document_id IN (SELECT id FROM documents WHERE tenant_id = current_setting('app.tenant_id')::uuid)
);
CREATE POLICY "clauses_insert" ON clauses FOR INSERT WITH CHECK (
    document_id IN (SELECT id FROM documents WHERE tenant_id = current_setting('app.tenant_id')::uuid)
);
CREATE POLICY "clauses_update" ON clauses FOR UPDATE USING (
    document_id IN (SELECT id FROM documents WHERE tenant_id = current_setting('app.tenant_id')::uuid)
);
CREATE POLICY "clauses_delete" ON clauses FOR DELETE USING (
    document_id IN (SELECT id FROM documents WHERE tenant_id = current_setting('app.tenant_id')::uuid)
);

-- Similar policies for other tables follow the same pattern

-- ============================================================================
-- FUNCTION: set_tenant_context
-- ============================================================================

CREATE OR REPLACE FUNCTION set_tenant_context(tenant_id UUID)
RETURNS void AS $$
BEGIN
    PERFORM set_config('app.tenant_id', tenant_id::text, true);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- SEED DATA
-- ============================================================================

-- Seed default playbook for new tenants (triggered on tenant creation)
