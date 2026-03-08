// ============================================================================
// CLARIX Shared Types - Database Models & API Schemas
// ============================================================================

// ============================================================================
// Tenant Types
// ============================================================================

export interface Tenant {
  id: string;
  name: string;
  slug: string;
  plan_tier: PlanTier;
  settings: TenantSettings;
  created_at: Date;
  updated_at: Date;
}

export type PlanTier = 'starter' | 'professional' | 'enterprise';

export interface TenantSettings {
  allow_signups?: boolean;
  default_notification_channels?: ('email' | 'slack' | 'sms')[];
  slack_webhook_url?: string;
  timezone?: string;
  retention_days?: number;
}

// ============================================================================
// User Types
// ============================================================================

export interface User {
  id: string;
  tenant_id: string;
  email: string;
  full_name: string | null;
  role: UserRole;
  mfa_enabled: boolean;
  last_login_at: Date | null;
  created_at: Date;
  updated_at: Date;
}

export type UserRole = 'admin' | 'manager' | 'member' | 'viewer';

export interface UserCreate {
  email: string;
  password: string;
  full_name?: string;
  tenant_id: string;
  role?: UserRole;
}

export interface UserUpdate {
  full_name?: string;
  role?: UserRole;
  mfa_enabled?: boolean;
}

// ============================================================================
// Document Types
// ============================================================================

export interface Document {
  id: string;
  tenant_id: string;
  name: string;
  storage_path: string;
  content_hash: string;
  status: DocumentStatus;
  document_type: DocumentType | null;
  metadata: DocumentMetadata;
  processed_at: Date | null;
  created_by: string | null;
  created_at: Date;
  updated_at: Date;
}

export type DocumentStatus =
  | 'pending'
  | 'processing'
  | 'completed'
  | 'failed'
  | 'quarantined';

export type DocumentType =
  | 'msa'
  | 'sow'
  | 'nda'
  | 'employment'
  | 'vendor'
  | 'lease'
  | 'license'
  | 'regulatory'
  | 'other';

export interface DocumentMetadata {
  parties?: string[];
  effective_date?: string;
  expiration_date?: string;
  deal_value?: number;
  jurisdiction?: string;
  governing_law?: string;
  page_count?: number;
  word_count?: number;
}

// ============================================================================
// Clause Types
// ============================================================================

export interface Clause {
  id: string;
  document_id: string;
  category: string;
  category_code: string;
  original_text: string;
  normalized_text: string | null;
  page_numbers: number[];
  section_path: string | null;
  confidence: number;
  extraction_method: ExtractionMethod;
  entities: ClauseEntities;
  obligations: Obligation[];
  schema_version: string;
  extracted_at: Date;
}

export type ExtractionMethod = 'llm' | 'pattern' | 'hybrid';

export interface ClauseEntities {
  dates?: ExtractedDate[];
  amounts?: ExtractedAmount[];
  parties?: string[];
  jurisdictions?: string[];
}

export interface ExtractedDate {
  value: string;
  type: 'effective' | 'expiration' | 'deadline' | 'notice' | 'renewal' | 'other';
  raw_text: string;
  confidence: number;
}

export interface ExtractedAmount {
  value: number;
  currency?: string;
  type: 'payment' | 'penalty' | 'liability' | 'revenue' | 'other';
  raw_text: string;
  confidence: number;
}

export interface Obligation {
  id: string;
  party: string;
  action: string;
  trigger: string | null;
  deadline: string | null;
  deadline_type: 'absolute' | 'relative' | 'conditional' | null;
  is_recurring: boolean;
  recurrence_pattern?: string;
}

// ============================================================================
// Clause Categories (80+ types)
// ============================================================================

export const CLAUSE_CATEGORIES = {
  // Obligations
  OBLIG_001: { name: 'Confidentiality', group: 'obligations' },
  OBLIG_002: { name: 'Non-Compete', group: 'obligations' },
  OBLIG_003: { name: 'Non-Solicitation', group: 'obligations' },
  OBLIG_004: { name: 'Non-Assignment', group: 'obligations' },
  OBLIG_005: { name: 'Performance Obligations', group: 'obligations' },
  OBLIG_006: { name: 'Reporting Requirements', group: 'obligations' },
  OBLIG_007: { name: 'Insurance Requirements', group: 'obligations' },
  OBLIG_008: { name: 'Compliance', group: 'obligations' },

  // Dates & Deadlines
  DATE_001: { name: 'Effective Date', group: 'dates' },
  DATE_002: { name: 'Expiration Date', group: 'dates' },
  DATE_003: { name: 'Renewal Date', group: 'dates' },
  DATE_004: { name: 'Notice Period', group: 'dates' },
  DATE_005: { name: 'Cure Period', group: 'dates' },
  DATE_006: { name: 'Survival Period', group: 'dates' },

  // Financial
  FIN_001: { name: 'Payment Terms', group: 'financial' },
  FIN_002: { name: 'Pricing', group: 'financial' },
  FIN_003: { name: 'Fees', group: 'financial' },
  FIN_004: { name: 'Expenses', group: 'financial' },
  FIN_005: { name: 'Taxes', group: 'financial' },
  FIN_006: { name: 'Revenue Sharing', group: 'financial' },
  FIN_007: { name: 'Invoicing', group: 'financial' },
  FIN_008: { name: 'Late Payment', group: 'financial' },

  // Termination
  TERM_001: { name: 'Termination for Cause', group: 'termination' },
  TERM_002: { name: 'Termination for Convenience', group: 'termination' },
  TERM_003: { name: 'Termination Notice', group: 'termination' },
  TERM_004: { name: 'Termination Effects', group: 'termination' },
  TERM_005: { name: 'Transition Services', group: 'termination' },

  // Intellectual Property
  IP_001: { name: 'IP Ownership', group: 'ip' },
  IP_002: { name: 'Licensing', group: 'ip' },
  IP_003: { name: 'Work-for-Hire', group: 'ip' },
  IP_004: { name: 'Derivative Works', group: 'ip' },
  IP_005: { name: 'Background IP', group: 'ip' },
  IP_006: { name: 'Foreground IP', group: 'ip' },
  IP_007: { name: 'IP Assignment', group: 'ip' },

  // Liability
  LIAB_001: { name: 'Limitation of Liability', group: 'liability' },
  LIAB_002: { name: 'Indemnification', group: 'liability' },
  LIAB_003: { name: 'Damages', group: 'liability' },
  LIAB_004: { name: 'Warranty Disclaimer', group: 'liability' },
  LIAB_005: { name: 'Consequential Damages', group: 'liability' },
  LIAB_006: { name: 'Mutual Indemnification', group: 'liability' },
  LIAB_007: { name: 'Insurance', group: 'liability' },

  // Regulatory
  REG_001: { name: 'Data Protection', group: 'regulatory' },
  REG_002: { name: 'Privacy', group: 'regulatory' },
  REG_003: { name: 'Security', group: 'regulatory' },
  REG_004: { name: 'Audit Rights', group: 'regulatory' },
  REG_005: { name: 'Regulatory Compliance', group: 'regulatory' },
  REG_006: { name: 'GDPR', group: 'regulatory' },
  REG_007: { name: 'CCPA', group: 'regulatory' },

  // General
  GEN_001: { name: 'Governing Law', group: 'general' },
  GEN_002: { name: 'Dispute Resolution', group: 'general' },
  GEN_003: { name: 'Arbitration', group: 'general' },
  GEN_004: { name: 'Venue', group: 'general' },
  GEN_005: { name: 'Entire Agreement', group: 'general' },
  GEN_006: { name: 'Amendment', group: 'general' },
  GEN_007: { name: 'Waiver', group: 'general' },
  GEN_008: { name: 'Severability', group: 'general' },
  GEN_009: { name: 'Counterparts', group: 'general' },
  GEN_010: { name: 'Assignment', group: 'general' },
  GEN_011: { name: 'Force Majeure', group: 'general' },
  GEN_012: { name: 'Notices', group: 'general' },
  GEN_013: { name: 'Relationship of Parties', group: 'general' },
  GEN_014: { name: 'Third Party Beneficiaries', group: 'general' },
  GEN_015: { name: 'Headings', group: 'general' },

  // Auto-Renewal
  RENEW_001: { name: 'Auto-Renewal', group: 'renewal' },
  RENEW_002: { name: 'Renewal Notice', group: 'renewal' },
  RENEW_003: { name: 'Renewal Terms', group: 'renewal' },

  // Representations
  REP_001: { name: 'Representations', group: 'representations' },
  REP_002: { name: 'Warranties', group: 'representations' },

  // Misc
  MISC_001: { name: 'Definition', group: 'misc' },
  MISC_002: { name: 'Exhibits', group: 'misc' },
  MISC_003: { name: 'Schedules', group: 'misc' },
  MISC_004: { name: 'Order of Precedence', group: 'misc' },
} as const;

// ============================================================================
// Playbook Types
// ============================================================================

export interface Playbook {
  id: string;
  tenant_id: string;
  name: string;
  description: string | null;
  is_default: boolean;
  version: number;
  created_by: string | null;
  created_at: Date;
  updated_at: Date;
}

export interface PlaybookRule {
  id: string;
  playbook_id: string;
  category: string;
  priority: RulePriority;
  preferred: RulePreference;
  acceptable: RulePreference;
  unacceptable: Record<string, unknown>;
  rationale: string | null;
  created_at: Date;
  updated_at: Date;
}

export type RulePriority = 'critical' | 'high' | 'standard' | 'low';

export interface RulePreference {
  max_liability?: string;
  carve_outs?: string[];
  notice_days?: number;
  renewal_terms?: string;
  // Add more fields as needed
}

// ============================================================================
// Redline Types
// ============================================================================

export interface Redline {
  id: string;
  document_id: string;
  clause_id: string;
  original_text: string;
  suggested_text: string;
  accepted_text: string | null;
  status: RedlineStatus;
  risk_level: RiskLevel;
  confidence: number;
  created_by: string;
  created_at: Date;
  updated_at: Date;
}

export type RedlineStatus = 'pending' | 'accepted' | 'rejected' | 'modified';
export type RiskLevel = 'critical' | 'high' | 'medium' | 'low';

export interface RedlineFeedback {
  id: string;
  redline_id: string;
  user_id: string;
  original_suggestion: string;
  user_final: string;
  diff: string;
  rationale: string | null;
  created_at: Date;
}

// ============================================================================
// Event Types
// ============================================================================

export interface Event {
  id: string;
  tenant_id: string | null;
  event_type: EventType;
  entity_type: string;
  entity_id: string | null;
  payload: Record<string, unknown>;
  created_at: Date;
}

export type EventType =
  | 'document.uploaded'
  | 'document.processing'
  | 'document.completed'
  | 'document.failed'
  | 'clause.extracted'
  | 'clause.verified'
  | 'clause.modified'
  | 'redline.created'
  | 'redline.accepted'
  | 'redline.rejected'
  | 'deadline.approaching'
  | 'deadline.passed'
  | 'regulation.changed';

// ============================================================================
// Audit Types
// ============================================================================

export interface AuditLog {
  id: string;
  tenant_id: string;
  user_id: string | null;
  action: string;
  entity_type: string;
  entity_id: string | null;
  old_values: Record<string, unknown> | null;
  new_values: Record<string, unknown> | null;
  ip_address: string | null;
  user_agent: string | null;
  created_at: Date;
}

// ============================================================================
// Subscription Types
// ============================================================================

export interface Subscription {
  id: string;
  tenant_id: string;
  stripe_subscription_id: string;
  plan_tier: PlanTier;
  status: SubscriptionStatus;
  current_period_start: Date;
  current_period_end: Date;
  cancel_at_period_end: boolean;
  created_at: Date;
  updated_at: Date;
}

export type SubscriptionStatus =
  | 'active'
  | 'trialing'
  | 'past_due'
  | 'canceled'
  | 'unpaid';

export interface UsageRecord {
  id: string;
  tenant_id: string;
  metric: UsageMetric;
  count: number;
  period_start: Date;
  period_end: Date;
  created_at: Date;
}

export type UsageMetric =
  | 'documents_processed'
  | 'pages_processed'
  | 'llm_tokens'
  | 'api_calls'
  | 'storage_gb';

// ============================================================================
// API Response Types
// ============================================================================

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
  request_id?: string;
}

export interface ApiSuccess<T> {
  data: T;
  message?: string;
}

// ============================================================================
// Tenant Context
// ============================================================================

export interface TenantContext {
  tenant_id: string;
  user_id: string;
  role: UserRole;
  plan_tier: PlanTier;
}

// ============================================================================
// LLM Types
// ============================================================================

export interface LLMRequest {
  model: LLMModel;
  messages: LLMMessage[];
  temperature?: number;
  max_tokens?: number;
  response_schema?: Record<string, unknown>;
}

export interface LLMMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export type LLMModel =
  | 'claude-opus-4-20250514'
  | 'claude-sonnet-4-20250514'
  | 'claude-haiku-3-20240307'
  | 'gpt-4o-2024-05-13'
  | 'gpt-4o-mini';

export interface LLMResponse {
  content: string;
  model: LLMModel;
  usage: {
    input_tokens: number;
    output_tokens: number;
    total_tokens: number;
  };
  finish_reason: string;
}

// ============================================================================
// Vector Types
// ============================================================================

export interface VectorRecord {
  id: string;
  values: number[];
  metadata: Record<string, unknown>;
  namespace?: string;
}

export interface VectorSearchResult {
  id: string;
  score: number;
  metadata: Record<string, unknown>;
}

// ============================================================================
// Export all types
// ============================================================================

export type {
  // Re-export with different names to avoid conflicts
  Clause as ClauseEntity,
  Document as DocumentEntity,
  User as UserEntity,
  Tenant as TenantEntity,
  Playbook as PlaybookEntity,
  PlaybookRule as PlaybookRuleEntity,
};
