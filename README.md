# Wireless AP Performance Automation Framework (MVP)

Author(s): Wai Man Cheng & ChatGPT (OpenAI GPT-4o)

---

## 📌 Project Overview
This project is a modular and scalable **PyATS-based wireless performance automation framework** designed for:

- Manual & future automated test execution
- SSH-based device interaction (AP, sniffer, switch, etc.)
- Stats/log collection, analysis, and AI-enhanced troubleshooting

This is an MVP implementation for **peak wireless performance test validation**, targeting Cisco APs but extendable to any vendor.

---

## ✅ Key Features

### 🧪 Test Execution Modes
- **Manual Mode (MVP)**: user manually connects wireless client and starts/stops traffic.
- **Future Automation Support**: architecture supports later automation for WLAN provisioning and traffic generation.

### 📊 Data Collection
- **Access Point Console Log Collector**
- **Access Point Stats Collector**:
  - Version info
  - Performance (MCS/NSS/Agg)
  - CPU usage (4 cores)
  - Memory usage
- **Switch Port Stats** (optional)
- **IxChariot or iPerf Performance Result Parsing**

### 🧠 AI-Ready Architecture
- Optional integration with future AI agent for:
  - Log pattern recognition
  - Suggesting root causes for test failures
  - Prompting user for missing stats or log commands

### 📂 Log Management
- Results saved under `run_logs/`
- Timestamped folders for each test run

---

## 🏗️ Project Structure

```
automation_mvp/
├── collectors/                  # Stats/log collector modules
│   ├── log_collector.py
│   ├── stats_collector.py
│   ├── stats_generator.py
│   ├── stats_runner.py
│   └── ...
├── configs/                    # Schema for stats collection
│   └── stats_schema.yaml
├── mock_samples/              # Sample log/stats for mock mode
├── tests/                     # Test runners for different scenarios
│   ├── performance_test_runner.py
│   └── generic_test_runner.py
├── utils/                     # Common utilities
├── run_logs/                  # Auto-generated output folders
├── testbed.yaml               # PyATS testbed file
├── manual_test_runner.py      # Entry point for manual testing
└── README.md                  # Project documentation
```

---

## 🧪 How to Run a Manual Test

### 🛠 Prerequisites
- Python 3.8+
- [pyATS installed](https://developer.cisco.com/docs/pyats/)

### 🧪 Test Execution
```bash
cd automation_mvp
python3 manual_test_runner.py --test_type performance --mock
```

- You'll be prompted to:
  - Enter AP log/stats collection commands
  - Hit Enter to start/stop the test
  - Stats and logs will be saved with timestamp

### 🗃 Output Folder
```
run_logs/
  ap_stats_20250411_171530/
    version/
    cpu/
    memory/
    performance/
    summary.csv
  logs_AP_20250411_171530/
    log_1_show_log.txt
    ...
```

---

## 🧪 Test Scripts
You can run these individually:
```bash
python3 test_stats_collector.py
python3 test_stats_runner.py
```
These help validate isolated modules without full test flow.

---

## 🧠 Future Enhancements
- AI chatbot/agent for troubleshooting
- Graphical interface for drag/drop test configuration
- Enhanced IxChariot / iPerf parsing logic
- Wireless client automation
- Support for multi-client, roaming, security, and stress tests

---

## 🤝 Contributions
This project is built by Wai Man Cheng in collaboration with ChatGPT-4o as a showcase of:

- Network automation design
- Python scripting best practices
- AI-assisted architecture thinking

---

## 📬 Contact
Wai Man Cheng  
[LinkedIn](https://linkedin.com/in/waimancheng)  
ymancheng@gmail.com

---
