// ============================================================
//  main.js - Supply Chain Traceability App
//  Handles: AI Predictions, Preservation Advice, Chatbot UI
// ============================================================

// ---- Shelf-Life Prediction ----
function predictShelfLife(publicId) {
    const btn = document.getElementById('btn-predict');
    const box = document.getElementById('result-box');
    if (!btn || !box) return;

    btn.setAttribute('aria-busy', 'true');
    btn.textContent = 'Analysing...';
    box.classList.add('is-visible');
    box.innerHTML = '<span class="spinner"></span> Running shelf-life model...';

    fetch(`/ml/predict/${publicId}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                box.innerHTML = `<p style="color:#e05252;">Error: ${data.error}</p>`;
            } else {
                const riskClass = data.risk_label === 'Safe' ? 'risk-safe'
                                : data.risk_label === 'At Risk' ? 'risk-warn'
                                : 'risk-crit';
                box.innerHTML = `
                    <h4>Shelf-Life Prediction</h4>
                    <p>Estimated Remaining Days: <strong>${data.remaining_days}</strong></p>
                    <p>Risk Status: <span class="badge ${riskClass}">${data.risk_label}</span></p>
                `;
            }
        })
        .catch(err => {
            box.innerHTML = `<p style="color:#e05252;">Request failed: ${err}</p>`;
        })
        .finally(() => {
            btn.removeAttribute('aria-busy');
            btn.textContent = 'Predict Shelf-Life (AI)';
        });
}

// ---- Preservation Advice (RAG) ----
function getPreservationAdvice(publicId) {
    const btn = document.getElementById('btn-advise');
    const box = document.getElementById('result-box');
    if (!btn || !box) return;

    btn.setAttribute('aria-busy', 'true');
    btn.textContent = 'Searching knowledge base...';
    box.classList.add('is-visible');
    box.innerHTML = '<span class="spinner"></span> Retrieving best preservation advice...';

    fetch(`/preservation/advise/${publicId}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                box.innerHTML = `<p style="color:#e05252;">Error: ${data.error}</p>`;
            } else {
                const confPct = Math.round((data.confidence || 0) * 100);
                box.innerHTML = `
                    <h4>Preservation Recommendation</h4>
                    <p>${data.advice}</p>
                    <small style="color:var(--text-muted);">Knowledge base match confidence: ${confPct}%</small>
                `;
            }
        })
        .catch(err => {
            box.innerHTML = `<p style="color:#e05252;">Request failed: ${err}</p>`;
        })
        .finally(() => {
            btn.removeAttribute('aria-busy');
            btn.textContent = 'Get Preservation Advice (RAG)';
        });
}

// ---- AI Chatbot ----
function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const history = document.getElementById('chat-history');
    if (!input || !history) return;

    const question = input.value.trim();
    if (!question) return;

    // Append user message
    const userP = document.createElement('p');
    userP.className = 'user-msg';
    userP.textContent = 'You: ' + question;
    history.appendChild(userP);
    input.value = '';
    history.scrollTop = history.scrollHeight;

    // Show typing indicator
    const loadingP = document.createElement('p');
    loadingP.className = 'ai-msg';
    loadingP.innerHTML = '<span class="spinner"></span> Assistant is thinking...';
    history.appendChild(loadingP);

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
    })
        .then(res => res.json())
        .then(data => {
            loadingP.innerHTML = '';
            loadingP.textContent = 'Assistant: ' + (data.answer || 'No response.');
            history.scrollTop = history.scrollHeight;
        })
        .catch(err => {
            loadingP.textContent = 'Assistant: Sorry, an error occurred.';
        });
}

function submitQuickQuery(queryText) {
    const input = document.getElementById('chat-input');
    input.value = queryText;
    sendChatMessage();
}

// ---- Blockchain transaction modal ----
function showTxDetails(txHash) {
    const modal = document.getElementById('tx-modal');
    const contentDiv = document.getElementById('tx-details-content');
    if (!modal || !contentDiv) return;

    modal.setAttribute('open', 'true');
    contentDiv.innerHTML = 'Loading transaction data from Web3 node...';

    fetch(`/api/transaction/${txHash}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                contentDiv.innerHTML = `<div class="alert alert-error">${data.error}</div>`;
            } else {
                const statusStr = data.status === 1
                    ? '<span class="badge risk-safe">Success</span>'
                    : '<span class="badge risk-crit">Failed</span>';
                contentDiv.innerHTML = `
                    <div class="tx-detail-grid">
                        <strong>Tx Hash:</strong><div class="tx-hash">${data.hash}</div>
                        <strong>Block Number:</strong><div>${data.block_number}</div>
                        <strong>From:</strong><div class="tx-hash">${data.from}</div>
                        <strong>To Contract:</strong><div class="tx-hash">${data.to}</div>
                        <strong>Gas Used:</strong><div>${data.gas_used}</div>
                        <strong>Status:</strong><div>${statusStr}</div>
                    </div>
                `;
            }
        })
        .catch(() => {
            contentDiv.innerHTML = '<div class="alert alert-error">Error fetching transaction details.</div>';
        });
}

// Allow Enter key to submit chat
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keydown', e => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }
});
