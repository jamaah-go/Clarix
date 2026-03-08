import { FileText, Clock, AlertTriangle, CheckCircle } from 'lucide-react'

export default function DashboardPage() {
  const stats = [
    {
      name: 'Total Documents',
      value: '127',
      change: '+12%',
      icon: FileText,
    },
    {
      name: 'Pending Review',
      value: '8',
      change: '-3',
      icon: Clock,
    },
    {
      name: 'Risk Items',
      value: '15',
      change: '+5',
      icon: AlertTriangle,
    },
    {
      name: 'Completed',
      value: '104',
      change: '+8',
      icon: CheckCircle,
    },
  ]

  const recentActivity = [
    { id: 1, action: 'Document uploaded', document: 'MSA-Vendor-2024.pdf', time: '5 min ago' },
    { id: 2, action: 'Clause extracted', document: 'NDA-Partner.docx', time: '12 min ago' },
    { id: 3, action: 'Redline accepted', document: 'SOW-Contractor.docx', time: '1 hour ago' },
    { id: 4, action: 'Deadline approaching', document: 'License-Agreement.pdf', time: '2 hours ago' },
  ]

  const upcomingDeadlines = [
    { id: 1, event: 'License Renewal', date: 'Mar 15, 2026', daysLeft: 10 },
    { id: 2, event: 'Notice Period', date: 'Mar 20, 2026', daysLeft: 15 },
    { id: 3, event: 'Compliance Review', date: 'Apr 1, 2026', daysLeft: 27 },
  ]

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Overview of your contract intelligence</p>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-8">
        {stats.map((stat) => (
          <div key={stat.name} className="p-6 bg-background rounded-lg border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">{stat.name}</p>
                <p className="text-2xl font-bold">{stat.value}</p>
                <p className="text-xs text-muted-foreground">{stat.change}</p>
              </div>
              <stat.icon className="w-8 h-8 text-muted-foreground" />
            </div>
          </div>
        ))}
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        {/* Recent Activity */}
        <div className="bg-background rounded-lg border">
          <div className="p-4 border-b">
            <h2 className="font-semibold">Recent Activity</h2>
          </div>
          <div className="divide-y">
            {recentActivity.map((item) => (
              <div key={item.id} className="p-4 flex items-center justify-between">
                <div>
                  <p className="font-medium">{item.action}</p>
                  <p className="text-sm text-muted-foreground">{item.document}</p>
                </div>
                <p className="text-sm text-muted-foreground">{item.time}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Upcoming Deadlines */}
        <div className="bg-background rounded-lg border">
          <div className="p-4 border-b">
            <h2 className="font-semibold">Upcoming Deadlines</h2>
          </div>
          <div className="divide-y">
            {upcomingDeadlines.map((item) => (
              <div key={item.id} className="p-4 flex items-center justify-between">
                <div>
                  <p className="font-medium">{item.event}</p>
                  <p className="text-sm text-muted-foreground">{item.date}</p>
                </div>
                <span className={`px-2 py-1 text-xs font-medium rounded ${
                  item.daysLeft <= 7 ? 'bg-red-100 text-red-800' :
                  item.daysLeft <= 14 ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {item.daysLeft} days
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
