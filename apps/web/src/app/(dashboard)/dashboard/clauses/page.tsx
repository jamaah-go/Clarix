'use client'

import { useState } from 'react'
import { ScrollText, Filter, Search, ChevronDown } from 'lucide-react'
import { formatDate, truncate, getStatusColor } from '@/lib/utils'

export default function ClausesPage() {
  const [clauses] = useState<any[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Clauses</h1>
        <p className="text-muted-foreground">Review extracted contract clauses</p>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search clauses..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border rounded-md"
          />
        </div>

        <div className="relative">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="appearance-none pl-4 pr-10 py-2 border rounded-md bg-background"
          >
            <option value="">All Categories</option>
            <option value="LIAB_001">Limitation of Liability</option>
            <option value="LIAB_002">Indemnification</option>
            <option value="TERM_001">Termination for Cause</option>
            <option value="OBLIG_001">Confidentiality</option>
          </select>
          <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
        </div>
      </div>

      {/* Clauses List */}
      <div className="bg-background rounded-lg border">
        {clauses.length === 0 ? (
          <div className="p-8 text-center text-muted-foreground">
            <ScrollText className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>No clauses extracted yet</p>
            <p className="text-sm">Upload and process documents to see clauses</p>
          </div>
        ) : (
          <div className="divide-y">
            {clauses.map((clause) => (
              <div key={clause.id} className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <span className="font-medium">{clause.category}</span>
                    <span className="text-muted-foreground text-sm ml-2">
                      {clause.category_code}
                    </span>
                  </div>
                  <span className={`px-2 py-1 text-xs font-medium rounded ${getStatusColor(clause.status)}`}>
                    {clause.status}
                  </span>
                </div>

                <p className="text-sm text-muted-foreground mb-2">
                  Page {clause.page_numbers?.join(', ')}
                </p>

                <p className="text-sm line-clamp-3">
                  {truncate(clause.original_text, 200)}
                </p>

                <div className="flex items-center gap-2 mt-3">
                  <span className="text-xs text-muted-foreground">
                    Confidence: {Math.round(clause.confidence * 100)}%
                  </span>
                  <span className="text-xs text-muted-foreground">
                    • {formatDate(clause.extracted_at)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
