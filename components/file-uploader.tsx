"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { UploadCloud, File as FileIcon, X, CheckCircle2, AlertTriangle, Loader2, Download } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Client } from "@gradio/client";

export function FileUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "validating" | "repairing" | "success" | "error">("idle");
  const [progress, setProgress] = useState(0);
  const [report, setReport] = useState<any>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setStatus("idle");
      setReport(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/octet-stream": [".ifc"],
    },
    maxFiles: 1,
  });

  const handleProcess = async () => {
    if (!file) return;

    setStatus("uploading");
    setProgress(10);

    try {
      // Fake progress for UX
      const progressInterval = setInterval(() => {
        setProgress(p => {
          if (p < 40) return p + 5;
          if (p >= 40 && p < 80) {
            setStatus("validating");
            return p + 2;
          }
          if (p >= 80 && p < 95) {
            setStatus("repairing");
            return p + 1;
          }
          return p;
        });
      }, 500);

      // Hardcoded to point directly to Hugging Face
      const spaceName = "minabasely7/ifc-repair-api";
      
      const app = await Client.connect(spaceName);
      const result = await app.predict("/predict", [
        file,
      ]);

      clearInterval(progressInterval);

      const responseData = result.data as any[];

      if (!responseData || responseData.length < 2) {
        throw new Error("Invalid response from API");
      }

      const reportData = responseData[0] as any;
      const returnedFile = responseData[1] as any;

      if (returnedFile && returnedFile.url) {
        reportData.download_url = returnedFile.url;
      }

      setProgress(100);
      setStatus("success");
      setReport(reportData);

    } catch (error: any) {
      console.error(error);
      setStatus("error");
      if (error.message) {
        setReport({ detail: error.message });
      }
    }
  };

  const removeFile = () => {
    setFile(null);
    setStatus("idle");
    setProgress(0);
    setReport(null);
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div className="bg-neutral-900/30 border border-border rounded-xl p-6 md:p-8">
        
        {/* Strict Privacy Message */}
        <div className="flex items-start gap-3 mb-8 p-4 bg-neutral-950 rounded-lg border border-neutral-800">
          <ShieldIcon className="w-5 h-5 text-neutral-400 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-medium text-sm">Privacy Guarantee</h4>
            <p className="text-sm text-muted-foreground mt-1">
              Your IFC files are processed securely and are automatically deleted immediately after processing. We never store or use your models.
            </p>
          </div>
        </div>

        {!file && (
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors ${
              isDragActive ? "border-foreground bg-neutral-900/50" : "border-neutral-800 hover:border-neutral-700"
            }`}
          >
            <input {...getInputProps()} />
            <div className="w-16 h-16 rounded-full bg-neutral-900 mx-auto flex items-center justify-center mb-6">
              <UploadCloud className="w-8 h-8 text-neutral-400" />
            </div>
            <h3 className="text-xl font-medium mb-2">Drag & drop your IFC file here</h3>
            <p className="text-muted-foreground mb-6">or click to browse from your computer</p>
            <div className="text-xs text-neutral-500">
              Supported formats: .ifc • Max size: 200MB
            </div>
          </div>
        )}

        <AnimatePresence mode="wait">
          {file && status === "idle" && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-neutral-950 border border-neutral-800 rounded-xl p-6"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
                    <FileIcon className="w-6 h-6" />
                  </div>
                  <div>
                    <h4 className="font-medium truncate max-w-[200px] sm:max-w-xs">{file.name}</h4>
                    <p className="text-sm text-muted-foreground">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
                  </div>
                </div>
                <button onClick={removeFile} className="p-2 hover:bg-neutral-800 rounded-full transition-colors text-muted-foreground hover:text-foreground">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <button
                onClick={handleProcess}
                className="w-full bg-foreground text-background font-medium rounded-lg py-3 hover:bg-foreground/90 transition-colors"
              >
                Start Repair & Validation
              </button>
            </motion.div>
          )}

          {file && (status === "uploading" || status === "validating" || status === "repairing") && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-neutral-950 border border-neutral-800 rounded-xl p-6"
            >
              <div className="flex flex-col items-center justify-center py-8">
                <Loader2 className="w-10 h-10 animate-spin text-muted-foreground mb-6" />
                <h3 className="text-lg font-medium mb-2 capitalize">{status}...</h3>
                <p className="text-sm text-muted-foreground mb-8 text-center max-w-sm">
                  {status === "uploading" && "Uploading your model securely."}
                  {status === "validating" && "Running thousands of semantic and structural checks."}
                  {status === "repairing" && "Intelligently patching missing GUIDs and relationships."}
                </p>
                <div className="w-full max-w-md bg-neutral-900 rounded-full h-2 overflow-hidden">
                  <motion.div
                    className="bg-foreground h-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ ease: "linear" }}
                  />
                </div>
              </div>
            </motion.div>
          )}

          {file && status === "success" && report && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div className="bg-green-500/10 border border-green-500/20 rounded-xl p-6 text-center">
                <div className="w-16 h-16 rounded-full bg-green-500/20 text-green-500 flex items-center justify-center mx-auto mb-4">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-medium text-green-500 mb-2">Repair Successful</h3>
                <p className="text-green-500/80 mb-6">
                  {report.validation_score}/100 Score • {report.repairs_performed || 0} Issues Fixed
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  {report.download_url && (
                    <a href={report.download_url} download className="flex items-center justify-center gap-2 bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors">
                      <Download className="w-4 h-4" /> Download Repaired IFC
                    </a>
                  )}
                  <button onClick={removeFile} className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-medium border border-border hover:bg-neutral-800 transition-colors">
                    Process Another File
                  </button>
                </div>
              </div>

              {/* Report Summary */}
              <div className="bg-neutral-950 border border-neutral-800 rounded-xl p-6">
                <h4 className="font-medium mb-4">Validation Summary</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="p-4 bg-neutral-900 rounded-lg">
                    <div className="text-2xl font-semibold">{report.statistics?.entities_count || 0}</div>
                    <div className="text-sm text-muted-foreground">Total Entities</div>
                  </div>
                  <div className="p-4 bg-neutral-900 rounded-lg">
                    <div className="text-2xl font-semibold text-red-400">{report.detected_issues || 0}</div>
                    <div className="text-sm text-muted-foreground">Issues Found</div>
                  </div>
                  <div className="p-4 bg-neutral-900 rounded-lg">
                    <div className="text-2xl font-semibold text-green-400">{report.repairs_performed || 0}</div>
                    <div className="text-sm text-muted-foreground">Fixed</div>
                  </div>
                  <div className="p-4 bg-neutral-900 rounded-lg">
                    <div className="text-2xl font-semibold text-yellow-400">{report.remaining_warnings || 0}</div>
                    <div className="text-sm text-muted-foreground">Warnings</div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {file && status === "error" && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-center"
            >
              <div className="w-16 h-16 rounded-full bg-red-500/20 text-red-500 flex items-center justify-center mx-auto mb-4">
                <AlertTriangle className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-medium text-red-500 mb-2">Processing Failed</h3>
              <p className="text-red-500/80 mb-6">
                {report?.detail ? report.detail : "There was an error processing your IFC file. Please try again or contact support."}
              </p>
              <button onClick={removeFile} className="bg-red-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-red-600 transition-colors">
                Try Again
              </button>
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  );
}

function ShieldIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
      <path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>
    </svg>
  );
}
