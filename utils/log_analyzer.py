# log_analyzer.py
# Author(s): Wai Man Cheng, ChatGPT (OpenAI 4.0 AI Assistant)
# Description:
# -------------
# Scans log files generated during testing and searches for known error patterns
# defined in a YAML config. Summarizes findings per log file and outputs to CSV.

import os
import re
import yaml
import csv
from datetime import datetime

# Load log pattern definitions from YAML
def load_patterns(yaml_path="utils/log_patterns.yaml"):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

# Search a log file for patterns and return matched results
def analyze_log_file(filepath, patterns):
    summary = {
        "filename": os.path.basename(filepath),
        "matches": []
    }

    with open(filepath, 'r') as f:
        lines = f.readlines()

    for category, regex_list in patterns.items():
        for regex in regex_list:
            pattern = re.compile(regex, re.IGNORECASE)
            for line in lines:
                if pattern.search(line):
                    summary["matches"].append({
                        "category": category,
                        "pattern": regex,
                        "line": line.strip()
                    })
    return summary

# Write results to CSV
def write_summary_to_csv(summary_list, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ["filename", "category", "pattern", "line"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in summary_list:
            for match in entry["matches"]:
                row = {"filename": entry["filename"], **match}
                writer.writerow(row)

# Main analyzer function
def run_log_analysis(log_dir, pattern_yaml="utils/log_patterns.yaml"):
    print(f"🔍 Analyzing logs in {log_dir} using {pattern_yaml}...")
    patterns = load_patterns(pattern_yaml)
    summary = []

    for file in os.listdir(log_dir):
        if file.endswith(".log") or file.endswith(".txt"):
            full_path = os.path.join(log_dir, file)
            file_summary = analyze_log_file(full_path, patterns)
            summary.append(file_summary)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = os.path.join(log_dir, f"log_analysis_summary_{timestamp}.csv")
    write_summary_to_csv(summary, output_csv)
    print(f"✅ Summary written to {output_csv}")

# Run as script
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("log_dir", help="Directory containing logs to analyze")
    parser.add_argument("--patterns", default="utils/log_patterns.yaml", help="Path to YAML file with regex patterns")
    args = parser.parse_args()

    run_log_analysis(args.log_dir, args.patterns)
