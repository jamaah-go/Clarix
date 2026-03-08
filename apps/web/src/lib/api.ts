import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface ApiResponse<T> {
  data?: T
  error?: string
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  }

  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    })

    const data = await response.json()

    if (!response.ok) {
      return { error: data.message || 'An error occurred' }
    }

    return { data }
  } catch (error) {
    return { error: 'Network error' }
  }
}

// Auth
export const authApi = {
  login: (email: string, password: string) =>
    fetchApi<{ access_token: string; user: any }>('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  register: (email: string, password: string, full_name?: string, tenant_name?: string) =>
    fetchApi<{ access_token: string; user: any }>('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, full_name, tenant_name }),
    }),

  logout: () => fetchApi('/api/v1/auth/logout', { method: 'POST' }),
}

// Documents
export const documentsApi = {
  list: (params?: { page?: number; page_size?: number; status?: string; search?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString()
    return fetchApi<any>(`/api/v1/documents?${query}`)
  },

  get: (id: string) => fetchApi<any>(`/api/v1/documents/${id}`),

  create: (name: string, storage_path: string, content_hash: string, document_type?: string) =>
    fetchApi<any>('/api/v1/documents', {
      method: 'POST',
      body: JSON.stringify({ name, storage_path, content_hash, document_type }),
    }),

  delete: (id: string) => fetchApi(`/api/v1/documents/${id}`, { method: 'DELETE' }),

  reprocess: (id: string) =>
    fetchApi(`/api/v1/documents/${id}/reprocess`, { method: 'POST' }),

  getUploadUrl: (filename: string, content_type: string) =>
    fetchApi<{ upload_url: string; storage_path: string }>('/api/v1/documents/upload-url', {
      method: 'POST',
      body: JSON.stringify({ filename, content_type }),
    }),
}

// Clauses
export const clausesApi = {
  list: (params?: { document_id?: string; category?: string; min_confidence?: number; page?: number }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString()
    return fetchApi<any>(`/api/v1/clauses?${query}`)
  },

  get: (id: string) => fetchApi<any>(`/api/v1/clauses/${id}`),

  verify: (id: string, verified: boolean, corrected_text?: string, corrected_category?: string) =>
    fetchApi(`/api/v1/clauses/${id}`, {
      method: 'PATCH',
      body: JSON.stringify({ verified, corrected_text, corrected_category }),
    }),

  getCategories: () => fetchApi<any>('/api/v1/clauses/categories/list'),
}

// Playbooks
export const playbooksApi = {
  list: () => fetchApi<any[]>('/api/v1/playbooks'),

  get: (id: string) => fetchApi<any>(`/api/v1/playbooks/${id}`),

  create: (name: string, description?: string, is_default?: boolean) =>
    fetchApi<any>('/api/v1/playbooks', {
      method: 'POST',
      body: JSON.stringify({ name, description, is_default }),
    }),

  update: (id: string, data: any) =>
    fetchApi<any>(`/api/v1/playbooks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  delete: (id: string) => fetchApi(`/api/v1/playbooks/${id}`, { method: 'DELETE' }),

  listRules: (playbookId: string, category?: string) => {
    const query = category ? `?category=${category}` : ''
    return fetchApi<any[]>(`/api/v1/playbooks/${playbookId}/rules${query}`)
  },

  createRule: (playbookId: string, data: any) =>
    fetchApi<any>(`/api/v1/playbooks/${playbookId}/rules`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateRule: (playbookId: string, ruleId: string, data: any) =>
    fetchApi<any>(`/api/v1/playbooks/${playbookId}/rules/${ruleId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  deleteRule: (playbookId: string, ruleId: string) =>
    fetchApi(`/api/v1/playbooks/${playbookId}/rules/${ruleId}`, { method: 'DELETE' }),
}

// Redlines
export const redlinesApi = {
  list: (params?: { document_id?: string; status?: string; risk_level?: string; page?: number }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString()
    return fetchApi<any>(`/api/v1/redlines?${query}`)
  },

  get: (id: string) => fetchApi<any>(`/api/v1/redlines/${id}`),

  generate: (document_id: string, clause_ids?: string[]) =>
    fetchApi<any>('/api/v1/redlines', {
      method: 'POST',
      body: JSON.stringify({ document_id, clause_ids }),
    }),

  feedback: (id: string, accepted: boolean, modified_text?: string, rationale?: string) =>
    fetchApi(`/api/v1/redlines/${id}/feedback`, {
      method: 'POST',
      body: JSON.stringify({ accepted, modified_text, rationale }),
    }),

  regenerate: (id: string) =>
    fetchApi(`/api/v1/redlines/${id}/regenerate`, { method: 'POST' }),
}

// Subscriptions
export const subscriptionsApi = {
  get: () => fetchApi<any>('/api/v1/subscriptions'),

  create: (plan_tier: string, payment_method_id: string) =>
    fetchApi<any>('/api/v1/subscriptions', {
      method: 'POST',
      body: JSON.stringify({ plan_tier, payment_method_id }),
    }),

  update: (plan_tier: string) =>
    fetchApi<any>('/api/v1/subscriptions', {
      method: 'PATCH',
      body: JSON.stringify({ plan_tier }),
    }),

  cancel: () => fetchApi('/api/v1/subscriptions', { method: 'DELETE' }),

  getUsage: () => fetchApi<any>('/api/v1/subscriptions/usage'),

  getInvoices: () => fetchApi<any[]>('/api/v1/subscriptions/invoices'),
}

// Users
export const usersApi = {
  list: () => fetchApi<any[]>('/api/v1/users'),

  getCurrent: () => fetchApi<any>('/api/v1/users/me'),

  update: (data: any) =>
    fetchApi<any>('/api/v1/users/me', {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  invite: (email: string, full_name?: string, role?: string) =>
    fetchApi<any>('/api/v1/users/invite', {
      method: 'POST',
      body: JSON.stringify({ email, full_name, role }),
    }),
}

// Events
export const eventsApi = {
  list: (params?: { event_type?: string; entity_type?: string; page?: number }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString()
    return fetchApi<any>(`/api/v1/events?${query}`)
  },
}
