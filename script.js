// --- 1. LIVE SERVER CONFIGURATION ---
// Ye link aapke PythonAnywhere wale backend se connect karega
const API_BASE_URL = "https://sadia.pythonanywhere.com/api";
const API_REPORTS = `${API_BASE_URL}/reports`;
const AUTH_KEY = "crms-auth";

// --- 2. LOGIN LOGIC ---
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const user = document.getElementById('loginUser').value.trim();
        const pass = document.getElementById('loginPass').value.trim();
        const feedback = document.getElementById('loginFeedback');

        // Demo Credentials Check
        if (user === "command@crms" && pass === "ops@123") {
            feedback.textContent = "Access Granted. Redirecting...";
            feedback.style.color = "#4caf50";
            localStorage.setItem(AUTH_KEY, "true");
            setTimeout(() => { window.location.href = "home.html"; }, 1000);
        } else {
            feedback.textContent = "Invalid Credentials!";
            feedback.style.color = "#ff4444";
        }
    });
}

// --- 3. LIVE STATS LOGIC (FETCH FROM SERVER) ---
async function loadStats() {
    const statTotal = document.getElementById('statTotal');
    if (!statTotal) return; // Sirf login page par chalay ga

    try {
        const response = await fetch(API_REPORTS);
        const data = await response.json();
        const reports = data.data || data || [];
        
        // Calculations
        const total = reports.length;
        const closed = reports.filter(r => r.status && r.status.toLowerCase() === 'closed').length;
        const pending = total - closed;

        // Update UI
        document.getElementById('statTotal').textContent = total;
        document.getElementById('statClosed').textContent = closed;
        document.getElementById('statInvest').textContent = pending;
    } catch (error) {
        console.error("Stats Error:", error);
    }
}

// --- 4. LOGOUT LOGIC ---
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem(AUTH_KEY);
        window.location.href = "index.html";
    });
}

// Page load hote hi stats update karein
loadStats();