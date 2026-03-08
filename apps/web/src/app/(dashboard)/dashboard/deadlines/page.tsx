'use client'

import { useState } from 'react'
import { Bell, Calendar, AlertTriangle, CheckCircle } from 'lucide-react'
import { formatDate } from '@/lib/utils'

interface Deadline {
  id: string
  event: string
  document_name: string
  category: string
  deadline_date: string
  days_left: number
  status: 'upcoming' | 'urgent' | 'passed'
}

export default function DeadlinesPage() {
  const [deadlines] = useState<Deadline[]>([
    { id: '1', event: 'License Renewal', document_name: 'Software-License-2024.pdf', category: 'Auto-Renewal', deadline_date: '2026-03-15', days_left: 10, status: 'upcoming' },
    { id: '2', event: 'Notice Period', document_name: 'MSA-Vendor.pdf', category: 'Termination', deadline_date: '2026-03-20', days_left: 15, status: 'upcoming' },
    { id: '3', event: 'Compliance Review', document_name: 'Data-Processing-Agreement.pdf', category: 'Regulatory', deadline_date: '2026-04-01', days_left: 27, status: 'upcoming' },
  ])

  const statusColors = {
    upcoming: 'bg-blue-100 text-blue-800',
    urgent: 'bg-red-100 text-red-800',
    passed: 'bg-gray-100 text-gray-800',
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Deadlines</h1>
        <p className="text-muted-foreground">Track important contract deadlines and obligations</p>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-3 mb-8">
        <div className="p-4 bg-background rounded-lg border">
          <div className="flex items-center gap-3">
            <Bell className="w-8 h-8 text-blue-500" />
            <div>
              <p className="text-sm text-muted-foreground">Upcoming</p>
              <p className="text-2xl font-bold">3</p>
            </div>
          </div>
        </div>
        <div className="p-4 bg-background rounded-lg border">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-8 h-8 text-red-500" />
            <div>
              <p className="text-sm text-muted-foreground">This Week</p>
              <p className="text-2xl font-bold">0</p>
            </div>
          </div>
        </div>
        <div className="p-4 bg-background rounded-lg border">
          <div className="flex items-center gap-3">
            <CheckCircle className="w-8 h-8 text-green-500" />
            <div>
              <p className="text-sm text-muted-foreground">Completed</p>
              <p className="text-2xl font-bold">12</p>
            </div>
          </div>
        </div>
      </div>

      {/* Deadlines List */}
      <div className="bg-background rounded-lg border">
        <div className="p-4 border-b">
          <h2 className="font-semibold">All Deadlines</h2>
        </div>

        {deadlines.length === 0 ? (
          <div className="p-8 text-center text-muted-foreground">
            <Calendar className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>No deadlines tracked</p>
            <p className="text-sm">Upload documents to track deadlines</p>
          </div>
        ) : (
          <div className="divide-y">
            {deadlines.map((deadline) => (
              <div key={deadline.id} className="p-4 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                    deadline.days_left <= 7 ? 'bg-red-100' : 'bg-blue-100'
                  }`}>
                    <Calendar className={`w-6 h-6 ${
                      deadline.days_left <= 7 ? 'text-red-600' : 'text-blue-600'
                    }`} />
                  </div>
                  <div>
                    <p className="font-medium">{deadline.event}</p>
                    <p className="text-sm text-muted-foreground">{deadline.document_name}</p>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p className="text-sm text-muted-foreground">{deadline.category}</p>
                    <p className="font-medium">{formatDate(deadline.deadline_date)}</p>
                  </div>
                  <span className={`px-3 py-1 text-sm font-medium rounded ${statusColors[deadline.status]}`}>
                    {deadline.days_left} days
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
