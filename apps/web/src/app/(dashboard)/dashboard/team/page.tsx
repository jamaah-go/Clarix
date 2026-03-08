'use client'

import { useState } from 'react'
import { Users, Plus, Mail, MoreVertical } from 'lucide-react'
import { formatDate } from '@/lib/utils'

interface TeamMember {
  id: string
  email: string
  full_name: string | null
  role: string
  created_at: string
}

export default function TeamPage() {
  const [members] = useState<TeamMember[]>([
    { id: '1', email: 'john@example.com', full_name: 'John Doe', role: 'admin', created_at: '2026-01-01' },
    { id: '2', email: 'jane@example.com', full_name: 'Jane Smith', role: 'member', created_at: '2026-01-15' },
  ])

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Team</h1>
          <p className="text-muted-foreground">Manage team members and permissions</p>
        </div>
        <button className="px-4 py-2 bg-primary text-white rounded-md flex items-center gap-2">
          <Plus className="w-4 h-4" /> Invite Member
        </button>
      </div>

      <div className="bg-background rounded-lg border">
        <div className="p-4 border-b">
          <h2 className="font-semibold">Team Members</h2>
        </div>

        <div className="divide-y">
          {members.map((member) => (
            <div key={member.id} className="p-4 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 bg-muted rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium">
                    {member.full_name?.charAt(0) || member.email.charAt(0)}
                  </span>
                </div>
                <div>
                  <p className="font-medium">{member.full_name || 'No name'}</p>
                  <p className="text-sm text-muted-foreground">{member.email}</p>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <span className={`px-2 py-1 text-xs font-medium rounded ${
                  member.role === 'admin' ? 'bg-primary text-primary-foreground' : 'bg-muted'
                }`}>
                  {member.role}
                </span>
                <p className="text-sm text-muted-foreground">
                  Joined {formatDate(member.created_at)}
                </p>
                <button className="p-2 hover:bg-muted rounded">
                  <MoreVertical className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Invite Modal would go here */}
    </div>
  )
}
