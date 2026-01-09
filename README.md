# 🚀 Execution Intelligence Core

> **Deterministic execution intelligence engine for process monitoring, risk assessment, and operational insights.**

Execution Intelligence Core is a backend system that transforms raw execution events into **actionable intelligence**.  
It explains *what happened*, *why it happened*, *who is responsible*, *whether it is recurring*, *how long it has been happening*, and *what is likely to happen next* — **without using LLMs or black-box ML**.

---

## ✨ Key Capabilities

✔ Event ingestion  
✔ Persistent execution memory  
✔ Policy violation detection  
✔ Responsibility attribution  
✔ Temporal reasoning  
✔ Deterministic risk scoring  
✔ Queryable insight APIs  
✔ Fully documented OpenAPI contracts  

---

## 🧠 What Problem Does This Solve?

Modern systems generate **events**, but humans need **answers**.

Execution Intelligence Core answers questions like:

- Why is this process blocked?
- Which step is causing delays?
- Who is responsible?
- Is this a recurring issue?
- How long has this been happening?
- Is this process at risk of failure?

This system sits **between raw logs and dashboards**, providing **explainable decision support**.

---

## 🏗️ Architecture Overview

```
┌────────────┐
│  Client /  │
│  Producer  │
└─────┬──────┘
      │
      ▼
┌───────────────────────┐
│  FastAPI Ingestion    │
│  POST /event          │
└─────┬─────────────────┘
      │
      ▼
┌──────────────────────────────┐
│ Execution Intelligence Core  │
│                              │
│  - Policy reasoning          │
│  - History analysis          │
│  - Temporal reasoning        │
│  - Responsibility mapping    │
│  - Risk scoring              │
└─────┬────────────────────────┘
      │
      ▼
┌──────────────────────────────┐
│ Persistent Memory (JSON)     │
│ Execution history & state    │
└──────────────────────────────┘
      │
      ▼
┌──────────────────────────────┐
│ Query & Insight APIs         │
│                              │
│  GET /process/{id}/summary   │
│  GET /process/{id}/risk      │
│  GET /stats/high-risk-procs  │
└──────────────────────────────┘
```

---

## 📦 Technology Stack

- **Python 3.10+**
- **FastAPI**
- **Pydantic**
- **Uvicorn**
- **JSON-based persistence**

---

## ▶️ Running the Project

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## 🏁 Project Status

✅ Core complete  
✅ Stable  
✅ Documented  
✅ Portfolio-ready  

---

> *Execution Intelligence is not about predicting the future — it’s about understanding the present deeply enough to act correctly.*
