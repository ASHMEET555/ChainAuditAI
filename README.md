# 🔗 ChainAuditAI

**AI‑Powered Fraud Detection with Immutable On‑Chain Audit Trails**

ChainAuditAI is a hackathon project that combines **machine learning–based fraud detection** with **Ethereum blockchain** to create an immutable, verifiable audit trail of fraud decisions. Fraud detection happens **off‑chain** using trained AI models, while **cryptographic proof** of each decision is permanently recorded **on‑chain**, ensuring transparency, trust, and auditability.

# 🔗 Live Demo: https://chainauditai.onrender.com/
---

## 🧠 Project Overview

Modern fraud detection systems suffer from three major issues:

* Decisions are stored in **centralized databases**
* AI models act as **black boxes**
* Fraud labels can be **modified, deleted, or disputed**

**ChainAuditAI** solves this by:

* Detecting fraud using ML models (banking, e‑commerce, vehicle insurance, and Ethereum transactions)
* Generating a cryptographic fingerprint (hash) of the fraud decision
* Storing this proof on **Ethereum**, creating a **tamper‑proof audit trail**

Once recorded, fraud decisions **cannot be altered**, enabling reliable audits and regulatory trust.

---

## 🎯 Problem Statement

Fraud detection today lacks:

* Verifiable proof of *when* a decision was made
* Guarantees that decisions haven’t been altered
* Transparency for regulators and end users

This causes challenges for:

* **Banks & FinTechs** → Compliance & audits
* **Regulators** → Verification & trust
* **Users** → False fraud claims & disputes

---

## 💡 Solution Architecture

### High‑Level Flow

1. Transaction data is processed off‑chain
2. Domain‑specific ML model predicts fraud
3. Fraud metadata is hashed (SHA‑256)
4. Hash + metadata are stored on Ethereum
5. Anyone can later verify integrity by recomputing the hash

```
Transaction → AI Model → Fraud Decision → Hash → Ethereum Smart Contract
```

---

## 🏗️ Project Structure

```
ChainAuditAI/
│
├── backend/                # FastAPI backend & ML inference
│   ├── core/               # App config & utilities
│   ├── models/             # ML model logic
│   ├── routers/            # API routes
│   ├── schema/             # Pydantic schemas
│   ├── services/           # Fraud detection & blockchain services
│   ├── load_models.py      # Loads trained ML models
│   ├── transforms.py       # Feature preprocessing
│   └── main.py             # Backend entry point
│
├── blockchain/             # Ethereum integration
│   ├── fraudproof_ledger.sol  # Smart contract
│   └── abi.json               # Contract ABI
│
├── data/                   # Datasets
│   ├── bank_fraud.csv
│   ├── ecommerce_fraud.csv
│   ├── ecommerce_fraud_lite.csv
│   ├── vehicle_insurance_fraud.csv
│   └── eth_fraud.txt
│
├── model_wts/              # Trained model weights & features
│   ├── bank_model_weights.pkl
│   ├── ecommerce_model_weights.pkl
│   ├── ethereum_model_weights.pkl
│   ├── vehicle_model_weights.pkl
│   └── *_features.pkl
│
├── frontend/               # Web UI
│   ├── dashboard.html
│   ├── scanner.html
│   ├── dashboard.js
│   ├── scanner.js
│   └── styles.css
│
├── notebooks/              # Training & experimentation
│   ├── bank-account-fraud.ipynb
│   ├── ecommerce-fraud.ipynb
│   ├── eth-fraud-nb.ipynb
│   └── vehicle-fraudmain.ipynb
│
├── ARCHITECTURE.md
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 📊 Datasets Used

We trained and evaluated our fraud detection models using well-known, publicly available datasets from Kaggle, covering multiple real-world fraud domains:

* **E-Commerce Fraud**
  Fraudulent online transactions dataset
  Source: [https://www.kaggle.com/datasets/shriyashjagtap/fraudulent-e-commerce-transactions](https://www.kaggle.com/datasets/shriyashjagtap/fraudulent-e-commerce-transactions)

* **Ethereum Transaction Fraud**
  On-chain Ethereum transaction fraud detection dataset (ETFD)
  Source: [https://www.kaggle.com/datasets/hunedmaterwala/ethereum-transaction-fraud-detection-etfd-data](https://www.kaggle.com/datasets/hunedmaterwala/ethereum-transaction-fraud-detection-etfd-data)

* **Vehicle Insurance Fraud**
  Insurance claim fraud detection dataset
  Source: [https://www.kaggle.com/datasets/shivamb/vehicle-claim-fraud-detection](https://www.kaggle.com/datasets/shivamb/vehicle-claim-fraud-detection)

* **Bank Account Fraud**
  Large-scale banking fraud dataset (NeurIPS 2022)
  Source: [https://www.kaggle.com/datasets/sgpjesus/bank-account-fraud-dataset-neurips-2022](https://www.kaggle.com/datasets/sgpjesus/bank-account-fraud-dataset-neurips-2022)

These datasets allow ChainAuditAI to demonstrate **cross-domain fraud detection** while maintaining a unified, auditable blockchain-backed decision system.

---

## 🤖 Fraud Detection Models

We use **separate domain‑specific ML models** for better accuracy:

| Domain                  | Description                  |
| ----------------------- | ---------------------------- |
| Bank Fraud              | Suspicious bank transactions |
| E‑Commerce Fraud        | Online transaction abuse     |
| Vehicle Insurance Fraud | False insurance claims       |
| Ethereum Fraud          | Malicious on‑chain behavior  |

Models are trained offline and loaded during inference using serialized weights.

---

## ⛓️ Blockchain Layer

### Smart Contract: `FraudProofLedger`

The Ethereum smart contract stores:

* Fraud decision hash
* Model identifier
* Timestamp
* Transaction reference ID

Only **cryptographic proofs** are stored — no raw or sensitive data.

### Why Blockchain?

* 🔒 Tamper‑proof storage
* 🕒 Provable timestamps
* 📜 Verifiable audit trails
* 🤝 Trust without central authority

---

## 🌐 Frontend

The frontend provides:

* Fraud scanning interface
* Dashboard for recorded fraud proofs
* On‑chain verification view

Built with **HTML, CSS, and JavaScript**.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.9+
* Node.js (optional, for tooling)
* Ethereum wallet (MetaMask)
* Testnet ETH (Sepolia / Goerli)

### Installation

```bash
git clone https://github.com/your-org/ChainAuditAI.git
cd ChainAuditAI
pip install -r requirements.txt
```

### Run Backend

```bash
cd backend
python main.py
```

### Smart Contract Deployment

* Compile `fraudproof_ledger.sol`
* Deploy using Remix / Hardhat
* Update contract address & ABI

---

## 🔍 Verification Workflow

1. Fetch fraud record from blockchain
2. Recompute hash from original decision
3. Compare hashes
4. Integrity confirmed ✔️

---

## 🧑‍🤝‍🧑 Team

This project was built by a **team of 3** for a hackathon.

* **Gaurav Upreti** – Backend and Blockchain
* **Ashmeet Singh Sandhu** – Ml Model Training and Transformation Pipeline
* **R.M** – Frontend 

---

## 🏆 Hackathon Relevance

* Strong **Ethereum integration**
* Real‑world compliance use case
* Privacy‑preserving on‑chain design
* Clear AI + Web3 synergy

---

## 📌 Future Improvements

* Zero‑Knowledge Proofs (ZK‑ML)
* DAO‑based fraud dispute resolution
* On‑chain model versioning
* Multi‑chain support

---

## 📜 License

MIT License

---

**ChainAuditAI — Trust, Transparency, and Truth in Fraud Detection.**
