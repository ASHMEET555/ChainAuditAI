// ===============================
// CONFIG
// ===============================
const API_BASE_URL = "http://localhost:8000/test"; // Pointing to /test router

// ===============================
// GLOBAL STATE
// ===============================
let state = {
    currentTransactionType: "vehicle",
    currentModel: "lightgbm",
    currentSignal: null,
    lastResult: null
};

// ... (Select Model/Signal functions remain the same) ...
function selectModel(card, modelId) {
    document.querySelectorAll(".model-card").forEach(c => c.classList.remove("active"));
    card.classList.add("active");
    state.currentModel = modelId;
}

function selectSignal(card, signalType) {
    document.querySelectorAll(".signal-card").forEach(c => c.classList.remove("active"));
    card.classList.add("active");
    state.currentSignal = signalType;
}

// ===============================
// RUN ANALYSIS
// ===============================
async function runAnalysis() {
    const analyzeBtn = document.getElementById("analyzeBtn");
    const resultCard = document.getElementById("resultCard");
    const placeholder = document.getElementById("placeholder");

    if (!state.currentSignal) {
        alert("Please select Fraud or Legit signal.");
        return;
    }

    // Correct Payload for TestRequest
    const payload = {
        transaction_type: state.currentTransactionType,
        fraud_label: state.currentSignal === "fraud" ? "fraud" : "non-fraud",
        num_samples: 1 // Explicitly ask for 1 sample
    };

    // UI Loading State
    analyzeBtn.innerText = "Broadcasting...";
    analyzeBtn.disabled = true;
    analyzeBtn.style.opacity = "0.7";

    resultCard.classList.add("hidden");
    placeholder.classList.remove("hidden");
    placeholder.innerHTML = `
        <div style="display:flex; flex-direction:column; align-items:center; gap:10px;">
            <div class="spinner"></div>
            Processing <strong>${state.currentSignal.toUpperCase()}</strong> Transaction...
        </div>
    `;

    try {
        const response = await fetch(`${API_BASE_URL}/run-test`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.statusText}`);
        }

        const data = await response.json();
        
        // FIX: Extract the first result from the list
        if (data.results && data.results.length > 0) {
            const firstResult = data.results[0];
            state.lastResult = firstResult;
            renderResults(firstResult); // Pass the specific result item
        } else {
            throw new Error("No results returned from backend");
        }

    } catch (error) {
        console.error("Analysis Error:", error);
        placeholder.innerHTML = `<span style="color:red">Connection Failed: ${error.message}</span>`;
    } finally {
        analyzeBtn.innerText = "Broadcast Signal";
        analyzeBtn.disabled = false;
        analyzeBtn.style.opacity = "1";
    }
}


// ===============================
// RENDER RESULTS
// ===============================
function renderResults(result) {
    const placeholder = document.getElementById("placeholder");
    const resultCard = document.getElementById("resultCard");
    const riskBadge = document.getElementById("riskBadge");
    const scoreValue = document.getElementById("scoreValue");
    const scoreText = document.getElementById("scoreText");
    const proofHash = document.getElementById("proofHash");
    const commitBtn = document.getElementById("commitBtn");

    placeholder.classList.add("hidden");
    resultCard.classList.remove("hidden");
    resultCard.classList.remove("high-risk", "low-risk");

    // Check Score (0-100)
    const isHighRisk = result.fraud_score > 50;

    if (isHighRisk) {
        resultCard.classList.add("high-risk");
        riskBadge.innerText = "FRAUD DETECTED";
        riskBadge.style.background = "#ef4444";
        scoreValue.style.color = "#fca5a5";
    } else {
        resultCard.classList.add("low-risk");
        riskBadge.innerText = "LEGITIMATE";
        riskBadge.style.background = "#22c55e";
        scoreValue.style.color = "#86efac";
    }

    // Display Backend Data
    scoreValue.innerText = result.fraud_score;
    scoreText.innerText = isHighRisk ? "High probability of fraud." : "Transaction appears safe.";
    
    // Display Blockchain Hash
    if (result.blockchain_tx) {
        proofHash.innerText = result.blockchain_tx;
        proofHash.style.color = "#4ade80"; // Green for success
    } else {
        proofHash.innerText = "Failed to write to chain (Check Backend Logs)";
        proofHash.style.color = "#f87171"; // Red for failure
    }

    // Disable manual commit since we do it automatically now
    commitBtn.disabled = true;
    commitBtn.innerText = "Auto-Logged to Chain";
    commitBtn.style.background = "#334155";
}

// ... (Spinner Styles) ...
document.addEventListener("DOMContentLoaded", () => {
    const style = document.createElement("style");
    style.innerHTML = `
        .hidden { display: none; }
        .spinner {
            width: 24px; height: 24px;
            border: 3px solid rgba(59, 130, 246, 0.3);
            border-radius: 50%;
            border-top-color: #3b82f6;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
    `;
    document.head.appendChild(style);
});