const API_BASE_URL = "http://localhost:8000"; // Backend URLconst API_BASE_URL = "http://localhost:5000/api"; // should be changed to backend URL



let state = {let state = {

    currentTransactionType: 'vehicle', // Default: vehicle, bank, ecommerce, ethereum    currentModel: 'lightgbm', // Default model

    currentSignal: null,                // 'fraud' or 'legit' (non-fraud)    currentSignal: null,      // 'fraud' or 'legit'

    lastResult: null                    // Stores the response from the last analysis    lastResult: null          // Stores the response from the last analysis

};};





// Handle Transaction Type Card Clicks// Handle Model Card Clicks

function selectModel(card, transactionType) {function selectModel(card, modelId) {

    document.querySelectorAll('.model-card').forEach(c => c.classList.remove('active'));    document.querySelectorAll('.model-card').forEach(c => c.classList.remove('active'));

    card.classList.add('active');    card.classList.add('active');

        

    state.currentTransactionType = transactionType;    state.currentModel = modelId;

    console.log(`[State] Transaction type set to: ${transactionType}`);    console.log(`[State] Model set to: ${modelId}`);

}}



function selectSignal(card, signalType) {function selectSignal(card, signalType) {

    document.querySelectorAll('.signal-card').forEach(c => c.classList.remove('active'));    document.querySelectorAll('.signal-card').forEach(c => c.classList.remove('active'));

    card.classList.add('active');    card.classList.add('active');

        

    state.currentSignal = signalType;    state.currentSignal = signalType;

    console.log(`[State] Signal set to: ${signalType}`);    console.log(`[State] Signal set to: ${signalType}`);

}}



async function runAnalysis() {async function runAnalysis() {

    const analyzeBtn = document.getElementById('analyzeBtn');    const analyzeBtn = document.getElementById('analyzeBtn');

    const resultCard = document.getElementById('resultCard');    const resultCard = document.getElementById('resultCard');

    const placeholder = document.getElementById('placeholder');    const placeholder = document.getElementById('placeholder');



    if (!state.currentSignal) {    if (!state.currentSignal) {

        alert("⚠️ Please select a signal type (Fraud or Legit).");        alert("⚠️ Please select a signal type (Fraud or Legit).");

        return;        return;

    }    }



    const payload = {    const payload = {

        transaction_type: state.currentTransactionType,        model_used: state.currentModel,

        fraud_label: state.currentSignal === 'fraud' ? 'fraud' : 'non-fraud'        forced_signal: state.currentSignal,

    };        timestamp: new Date().toISOString()

    };

    analyzeBtn.innerText = "Running Detection...";

    analyzeBtn.disabled = true;    analyzeBtn.innerText = "Broadcasting to Backend...";

    analyzeBtn.style.opacity = "0.7";    analyzeBtn.disabled = true;

        analyzeBtn.style.opacity = "0.7";

    resultCard.classList.add('hidden');    

    placeholder.classList.remove('hidden');    resultCard.classList.add('hidden');

    placeholder.innerHTML = `    placeholder.classList.remove('hidden');

        <div style="display:flex; flex-direction:column; align-items:center; gap:10px;">    placeholder.innerHTML = `

            <div class="spinner"></div>        <div style="display:flex; flex-direction:column; align-items:center; gap:10px;">

            Testing <strong>${state.currentSignal.toUpperCase()}</strong> samples from ${state.currentTransactionType} dataset...            <div class="spinner"></div>

        </div>            Sending <strong>${state.currentSignal.toUpperCase()}</strong> signal via ${state.currentModel}...

    `;        </div>

    `;

    try {

        // Call backend /test/run-test endpoint    try {

        const response = await fetch(`${API_BASE_URL}/test/run-test`, {        // Network request

            method: 'POST',        const response = await fetch(`${API_BASE_URL}/analyze`, {

            headers: {            method: 'POST',

                'Content-Type': 'application/json',            headers: {

                'Accept': 'application/json'                'Content-Type': 'application/json',

            },                'Accept': 'application/json'

            body: JSON.stringify(payload)            },

        });            body: JSON.stringify(payload)

        });

        if (!response.ok) {

            const errorData = await response.json();        if (!response.ok) {

            throw new Error(errorData.detail || `Server Error: ${response.statusText}`);            throw new Error(`Server Error: ${response.statusText}`);

        }        }



        const data = await response.json();        const data = await response.json();

                

        state.lastResult = data;         state.lastResult = data; 



        renderResults(data); // Renders result        renderResults(data); // Renders result



    } catch (error) {    } catch (error) {

        console.error("Analysis Failed:", error);        console.error("Analysis Failed:", error);

        alert(`Analysis Failed: ${error.message}. \nCheck console for details.`);        alert(`Analysis Failed: ${error.message}. \nCheck console for details.`);

                

        placeholder.innerHTML = `<div style="color: var(--accent-red)">Error: ${error.message}</div>`;        placeholder.innerHTML = "Error connecting to backend.";

    } finally {    } finally {

        analyzeBtn.innerText = "Run Fraud Detection Test";        analyzeBtn.innerText = "Broadcast Signal";

        analyzeBtn.disabled = false;        analyzeBtn.disabled = false;

        analyzeBtn.style.opacity = "1";        analyzeBtn.style.opacity = "1";

    }    }

}}



function renderResults(data) {function renderResults(data) {

    const placeholder = document.getElementById('placeholder');    const placeholder = document.getElementById('placeholder');

    const resultCard = document.getElementById('resultCard');    const resultCard = document.getElementById('resultCard');

        

    const riskBadge = document.getElementById('riskBadge');    const riskBadge = document.getElementById('riskBadge');

    const scoreValue = document.getElementById('scoreValue');    const scoreValue = document.getElementById('scoreValue');

    const scoreText = document.getElementById('scoreText');    const scoreText = document.getElementById('scoreText');

    const proofHash = document.getElementById('proofHash');    const proofHash = document.getElementById('proofHash');

    const commitBtn = document.getElementById('commitBtn');    const commitBtn = document.getElementById('commitBtn');



    placeholder.classList.add('hidden');    placeholder.classList.add('hidden');

    resultCard.classList.remove('hidden');    resultCard.classList.remove('hidden');



    resultCard.classList.remove('high-risk', 'low-risk');    resultCard.classList.remove('high-risk', 'low-risk');

        

    // Calculate average fraud score from results    if (data.risk_level === 'HIGH' || state.currentSignal === 'fraud') {

    const avgScore = data.results.reduce((sum, r) => sum + r.fraud_score, 0) / data.results.length;        resultCard.classList.add('high-risk');

    const avgRiskLevel = data.results[0].risk_level; // Use first result's risk level        riskBadge.innerText = "FRAUD DETECTED";

            riskBadge.style.background = "#ef4444";

    if (avgScore >= 50 || state.currentSignal === 'fraud') {        scoreValue.style.color = "#fca5a5";

        resultCard.classList.add('high-risk');    } else {

        riskBadge.innerText = "FRAUD DETECTED";        resultCard.classList.add('low-risk');

        riskBadge.style.background = "#ef4444";        riskBadge.innerText = "LEGITIMATE";

        scoreValue.style.color = "#fca5a5";        riskBadge.style.background = "#22c55e";

    } else {        scoreValue.style.color = "#86efac";

        resultCard.classList.add('low-risk');    }

        riskBadge.innerText = "LEGITIMATE";

        riskBadge.style.background = "#22c55e";    // Inject Data from Backend

        scoreValue.style.color = "#86efac";    scoreValue.innerText = data.score; // Backend provided hash

    }    scoreText.innerText = data.message || "Analysis complete.";

    proofHash.innerText = data.proof_hash; // Backend provided hash

    // Display results

    scoreValue.innerText = Math.round(avgScore);    // Enable Commit Button

    scoreText.innerText = `Tested ${data.total_samples} ${data.transaction_type} transactions (${data.fraud_label})`;    commitBtn.disabled = false;

        commitBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> Commit Proof to Chain`;

    // Show database IDs    commitBtn.style.background = "#334155";

    const dbIds = data.results.map(r => r.database_id).join(', ');}

    proofHash.innerText = `Database IDs: ${dbIds}`;

async function commitToLedger() {

    // Enable Commit Button (though in test mode, commitment is automatic)    const commitBtn = document.getElementById('commitBtn');

    commitBtn.disabled = true;    

    commitBtn.innerHTML = `✅ Results Saved to Database`;    if (!state.lastResult) {

    commitBtn.style.background = "#22c55e";        alert("No analysis data found to commit.");

}        return;

    }

async function commitToLedger() {

    // This function is not used in the new flow since blockchain logging    commitBtn.innerText = "Signing & Committing...";

    // happens automatically in the backend for high-risk transactions    commitBtn.style.background = "#4f46e5";

    alert("Blockchain logging is handled automatically by the backend for high-risk transactions.");    commitBtn.disabled = true;

}

    try {

document.addEventListener('DOMContentLoaded', () => {        // Network request

    const style = document.createElement('style');        const response = await fetch(`${API_BASE_URL}/commit`, {

    style.innerHTML = `            method: 'POST',

        .spinner {            headers: {

            width: 24px; height: 24px;                'Content-Type': 'application/json'

            border: 3px solid rgba(59, 130, 246, 0.3);            },

            border-radius: 50%;            body: JSON.stringify({

            border-top-color: #3b82f6;                proof_hash: state.lastResult.proof_hash,

            animation: spin 1s ease-in-out infinite;                transaction_id: state.lastResult.transaction_id

        }            })

        @keyframes spin { to { transform: rotate(360deg); } }        });

    `;

    document.head.appendChild(style);        if (!response.ok) throw new Error("Commit failed on server.");

    

    console.log("Scanner Initialized. Connecting to:", API_BASE_URL);        const data = await response.json();

});

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