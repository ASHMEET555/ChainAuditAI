const API_BASE_URL = "http://localhost:5000/api"; // should be changed to backend URL

let state = {
    currentModel: 'lightgbm', // Default model
    currentSignal: null,      // 'fraud' or 'legit'
    lastResult: null          // Stores the response from the last analysis
};


// Handle Model Card Clicks
function selectModel(card, modelId) {
    document.querySelectorAll('.model-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');
    
    state.currentModel = modelId;
    console.log(`[State] Model set to: ${modelId}`);
}

function selectSignal(card, signalType) {
    document.querySelectorAll('.signal-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');
    
    state.currentSignal = signalType;
    console.log(`[State] Signal set to: ${signalType}`);
}

async function runAnalysis() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultCard = document.getElementById('resultCard');
    const placeholder = document.getElementById('placeholder');

    if (!state.currentSignal) {
        alert("⚠️ Please select a signal type (Fraud or Legit).");
        return;
    }

    const payload = {
        model_used: state.currentModel,
        forced_signal: state.currentSignal,
        timestamp: new Date().toISOString()
    };

    analyzeBtn.innerText = "Broadcasting to Backend...";
    analyzeBtn.disabled = true;
    analyzeBtn.style.opacity = "0.7";
    
    resultCard.classList.add('hidden');
    placeholder.classList.remove('hidden');
    placeholder.innerHTML = `
        <div style="display:flex; flex-direction:column; align-items:center; gap:10px;">
            <div class="spinner"></div>
            Sending <strong>${state.currentSignal.toUpperCase()}</strong> signal via ${state.currentModel}...
        </div>
    `;

    try {
        // Network request
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.statusText}`);
        }

        const data = await response.json();
        
        state.lastResult = data; 

        renderResults(data); // Renders result

    } catch (error) {
        console.error("Analysis Failed:", error);
        alert(`Analysis Failed: ${error.message}. \nCheck console for details.`);
        
        placeholder.innerHTML = "Error connecting to backend.";
    } finally {
        analyzeBtn.innerText = "Broadcast Signal";
        analyzeBtn.disabled = false;
        analyzeBtn.style.opacity = "1";
    }
}

function renderResults(data) {
    const placeholder = document.getElementById('placeholder');
    const resultCard = document.getElementById('resultCard');
    
    const riskBadge = document.getElementById('riskBadge');
    const scoreValue = document.getElementById('scoreValue');
    const scoreText = document.getElementById('scoreText');
    const proofHash = document.getElementById('proofHash');
    const commitBtn = document.getElementById('commitBtn');

    placeholder.classList.add('hidden');
    resultCard.classList.remove('hidden');

    resultCard.classList.remove('high-risk', 'low-risk');
    
    if (data.risk_level === 'HIGH' || state.currentSignal === 'fraud') {
        resultCard.classList.add('high-risk');
        riskBadge.innerText = "FRAUD DETECTED";
        riskBadge.style.background = "#ef4444";
        scoreValue.style.color = "#fca5a5";
    } else {
        resultCard.classList.add('low-risk');
        riskBadge.innerText = "LEGITIMATE";
        riskBadge.style.background = "#22c55e";
        scoreValue.style.color = "#86efac";
    }

    // Inject Data from Backend
    scoreValue.innerText = data.score; // Backend provided hash
    scoreText.innerText = data.message || "Analysis complete.";
    proofHash.innerText = data.proof_hash; // Backend provided hash

    // Enable Commit Button
    commitBtn.disabled = false;
    commitBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> Commit Proof to Chain`;
    commitBtn.style.background = "#334155";
}

async function commitToLedger() {
    const commitBtn = document.getElementById('commitBtn');
    
    if (!state.lastResult) {
        alert("No analysis data found to commit.");
        return;
    }

    commitBtn.innerText = "Signing & Committing...";
    commitBtn.style.background = "#4f46e5";
    commitBtn.disabled = true;

    try {
        // Network request
        const response = await fetch(`${API_BASE_URL}/commit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                proof_hash: state.lastResult.proof_hash,
                transaction_id: state.lastResult.transaction_id
            })
        });

        if (!response.ok) throw new Error("Commit failed on server.");

        const data = await response.json();

        commitBtn.innerText = "Proof On-Chain!";
        commitBtn.style.background = "#22c55e";
        
        alert(`SUCCESS: Block #${data.block_number} mined.\nTransaction Hash: ${data.tx_hash}`);

    } catch (error) {
        console.error("Commit Error:", error);
        alert("Failed to commit proof to ledger.");
        
        // Reset button
        commitBtn.innerText = "Retry Commit";
        commitBtn.disabled = false;
        commitBtn.style.background = "#ef4444";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const style = document.createElement('style');
    style.innerHTML = `
        .spinner {
            width: 24px; height: 24px;
            border: 3px solid rgba(59, 130, 246, 0.3);
            border-radius: 50%;
            border-top-color: #3b82f6;
            animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
    `;
    document.head.appendChild(style);
    
    console.log("Scanner Initialized. Connecting to:", API_BASE_URL);
});