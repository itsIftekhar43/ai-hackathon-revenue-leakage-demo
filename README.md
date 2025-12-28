![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![OpenAI](https://img.shields.io/badge/AI-OpenAI-purple)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Status](https://img.shields.io/badge/Status-Hackathon%20Ready-success)


# ai-hackathon-revenue-leakage-demo
AI-powered audit engine using Python, OpenAI, and FastAPI

ai-audit-engine-demo/
│
├── app.py                     # FastAPI entry point
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not committed)
├── .gitignore
│
├── ai/
│   └── openai_client.py       # OpenAI integration
│
├── rules/
│   └── rules_engine.py        # Mandatory audit validations
│
├── anomaly/
│   └── anomaly_detector.py    # Anomaly detection logic
│
├── reports/                   # (Future) CSV / Excel reports
├── data/                      # Sample data
│
└── README.md


🚀 Tech Stack

Python 3.10+

FastAPI

OpenAI API

Pydantic

GitHub Codespaces / VS Code

Ready for Azure / AWS deployment


🧪 Features Implemented
✅ Rules Engine

Fare must be > 0

Tax cannot be negative

Commission cannot exceed fare

✅ AI Audit Engine

Uses OpenAI to generate human-like audit explanations

Explains rule violations clearly for auditors

✅ Anomaly Detection

Flags suspicious refunds (e.g., refund > 80% of fare)

✅ API Contract Validation

Strong request validation using Pydantic