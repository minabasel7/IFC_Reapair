"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, CheckCircle2, ShieldCheck, Zap, Database, Download } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="px-6 h-16 flex items-center justify-between border-b border-border/40 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded bg-primary text-primary-foreground flex items-center justify-center font-bold">
            IR
          </div>
          <span className="font-semibold text-lg tracking-tight">IFC Repair</span>
        </div>
        <nav className="hidden md:flex gap-6 text-sm font-medium text-muted-foreground">
          <Link href="#features" className="hover:text-foreground transition-colors">Features</Link>
          <Link href="#how-it-works" className="hover:text-foreground transition-colors">How it works</Link>
          <Link href="#pricing" className="hover:text-foreground transition-colors">Pricing</Link>
        </nav>
        <div className="flex items-center gap-4">
          <Link href="/dashboard" className="text-sm font-medium hover:text-foreground transition-colors">
            Login
          </Link>
          <Link href="/dashboard" className="text-sm font-medium bg-foreground text-background px-4 py-2 rounded-full hover:bg-foreground/90 transition-colors">
            Upload IFC
          </Link>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 px-6 overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-neutral-900 via-background to-background -z-10" />
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white to-neutral-500">
                Repair IFC Files in Minutes, <br className="hidden md:block" /> Not Days
              </h1>
              <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed">
                Automatically validate, repair and optimize OpenBIM IFC models using an intelligent workflow powered by IfcOpenShell.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link href="/dashboard" className="w-full sm:w-auto flex items-center justify-center gap-2 bg-foreground text-background px-8 py-4 rounded-full font-medium text-lg hover:bg-foreground/90 transition-colors">
                  Upload IFC <ArrowRight className="w-5 h-5" />
                </Link>
                <Link href="#learn-more" className="w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-4 rounded-full font-medium text-lg border border-border hover:bg-muted/50 transition-colors">
                  Learn More
                </Link>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 px-6 bg-neutral-950">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold tracking-tight mb-4">Enterprise-Grade IFC Repair</h2>
              <p className="text-muted-foreground max-w-2xl mx-auto text-lg">
                Our engine is built to handle massive models, fixing semantic errors while strictly preserving geometry and valid data.
              </p>
            </div>
            <div className="grid md:grid-cols-3 gap-8">
              <FeatureCard 
                icon={<ShieldCheck className="w-6 h-6" />}
                title="Strict Validation"
                description="Detect duplicate GUIDs, missing relationships, and schema violations with pinpoint accuracy."
              />
              <FeatureCard 
                icon={<Zap className="w-6 h-6" />}
                title="Semantic Auto-Repair"
                description="Automatically reconnect broken spatial hierarchies and repair invalid references without data loss."
              />
              <FeatureCard 
                icon={<Database className="w-6 h-6" />}
                title="Bonsai Compatible"
                description="Repaired files remain fully compatible with BlenderBIM, Bonsai, Solibri, and all major OpenBIM software."
              />
            </div>
          </div>
        </section>

        {/* How it works */}
        <section id="how-it-works" className="py-24 px-6 border-t border-border/50">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold tracking-tight text-center mb-16">How it works</h2>
            <div className="space-y-12">
              <Step number="1" title="Upload your model">
                Drag and drop your .ifc file securely. We never store your files permanently.
              </Step>
              <Step number="2" title="Automatic Validation">
                Our IfcOpenShell backend parses the file, checking for thousands of potential semantic and structural issues.
              </Step>
              <Step number="3" title="Intelligent Repair">
                The repair engine safely patches GUIDs, properties, and relationships while keeping geometry completely intact.
              </Step>
              <Step number="4" title="Download Reports & File">
                Get your fixed IFC file immediately alongside detailed HTML, PDF, or JSON compliance reports.
              </Step>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/40 py-12 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-primary text-primary-foreground flex items-center justify-center font-bold text-xs">
              IR
            </div>
            <span className="font-semibold text-sm">IFC Repair</span>
          </div>
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} IFC Repair SaaS. All rights reserved.
          </p>
          <div className="flex gap-4 text-sm text-muted-foreground">
            <Link href="#" className="hover:text-foreground transition-colors">Privacy</Link>
            <Link href="#" className="hover:text-foreground transition-colors">Terms</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <div className="p-6 rounded-2xl bg-background border border-border hover:border-neutral-700 transition-colors">
      <div className="w-12 h-12 rounded-xl bg-neutral-900 border border-neutral-800 flex items-center justify-center text-neutral-300 mb-6">
        {icon}
      </div>
      <h3 className="text-xl font-semibold mb-3">{title}</h3>
      <p className="text-muted-foreground leading-relaxed">
        {description}
      </p>
    </div>
  );
}

function Step({ number, title, children }: { number: string, title: string, children: React.ReactNode }) {
  return (
    <div className="flex gap-6 items-start">
      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-neutral-900 border border-neutral-800 flex items-center justify-center font-bold text-lg">
        {number}
      </div>
      <div>
        <h3 className="text-xl font-semibold mb-2">{title}</h3>
        <p className="text-muted-foreground text-lg">{children}</p>
      </div>
    </div>
  );
}
