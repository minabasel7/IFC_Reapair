import Link from "next/link";
import { LayoutDashboard, FileUp, History, Settings, LogOut } from "lucide-react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border/40 hidden md:flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-border/40">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded bg-primary text-primary-foreground flex items-center justify-center font-bold">
              IR
            </div>
            <span className="font-semibold text-lg tracking-tight">IFC Repair</span>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2 rounded-md bg-neutral-900 text-foreground font-medium">
            <LayoutDashboard className="w-4 h-4" /> Dashboard
          </Link>
          <Link href="#" className="flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:bg-neutral-900/50 hover:text-foreground font-medium transition-colors">
            <FileUp className="w-4 h-4" /> Upload
          </Link>
          <Link href="#" className="flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:bg-neutral-900/50 hover:text-foreground font-medium transition-colors">
            <History className="w-4 h-4" /> History
          </Link>
          <Link href="#" className="flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:bg-neutral-900/50 hover:text-foreground font-medium transition-colors">
            <Settings className="w-4 h-4" /> Settings
          </Link>
        </nav>
        <div className="p-4 border-t border-border/40">
          <div className="flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:text-foreground font-medium transition-colors cursor-pointer">
            <LogOut className="w-4 h-4" /> Sign Out
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col">
        <header className="h-16 flex items-center px-8 border-b border-border/40 justify-between md:justify-end">
          <div className="md:hidden flex items-center gap-2">
            <div className="w-8 h-8 rounded bg-primary text-primary-foreground flex items-center justify-center font-bold">
              IR
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-sm font-medium px-3 py-1 rounded-full bg-neutral-900 border border-neutral-800">
              Pro Plan
            </div>
            <div className="w-8 h-8 rounded-full bg-neutral-800" />
          </div>
        </header>
        <div className="flex-1 p-8 overflow-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
