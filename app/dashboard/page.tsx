import { FileUploader } from "@/components/file-uploader";

export default function DashboardPage() {
  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-10">
        <h1 className="text-3xl font-bold tracking-tight mb-2">Upload IFC Model</h1>
        <p className="text-muted-foreground">
          Upload your OpenBIM IFC file for automatic validation and repair.
        </p>
      </div>
      
      <FileUploader />
      
      {/* Recent Activity / Stats placeholder */}
      <div className="mt-16 border-t border-border/50 pt-10">
        <h2 className="text-xl font-semibold mb-6">Recent Jobs</h2>
        <div className="bg-neutral-900/30 border border-neutral-800 rounded-xl overflow-hidden">
          <div className="text-center py-12 text-muted-foreground text-sm">
            No recent jobs found. Upload a file to get started.
          </div>
        </div>
      </div>
    </div>
  );
}
