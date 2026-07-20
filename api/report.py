import json
from datetime import datetime

class ReportGenerator:
    def __init__(self, stats: dict, validation_results: dict, repairs_performed: int, val_time: float, rep_time: float):
        self.stats = stats
        self.validation_results = validation_results
        self.repairs_performed = repairs_performed
        self.val_time = val_time
        self.rep_time = rep_time

    def generate_json(self, download_url: str = None) -> dict:
        remaining_issues = [i for i in self.validation_results["issues"] if i["type"] not in ["duplicate_guid", "missing_spatial_hierarchy"]]
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "validation_score": self.validation_results["score"],
            "statistics": self.stats,
            "detected_issues": self.validation_results["total_issues"],
            "repairs_performed": self.repairs_performed,
            "remaining_warnings": len(remaining_issues),
            "validation_time_ms": self.val_time,
            "repair_time_ms": self.rep_time,
            "issues_list": remaining_issues,
            "download_url": download_url
        }

    def generate_html(self) -> str:
        html = f"""
        <html>
            <head><title>IFC Repair & Validation Report</title></head>
            <body>
                <h1>Validation Score: {self.validation_results['score']}</h1>
                <p>Repairs Performed: {self.repairs_performed}</p>
                <p>Entities Scanned: {self.stats['entities_count']}</p>
            </body>
        </html>
        """
        return html
