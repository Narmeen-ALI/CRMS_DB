const API_BASE_URL = "https://sadia.pythonanywhere.com/api";
const API_REPORTS = `${API_BASE_URL}/reports`;
const AUTH_KEY = "crms-auth";

// --- 1. LOGIN LOGIC ---
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const user = document.getElementById('loginUser').value.trim();
        const pass = document.getElementById('loginPass').value.trim();
        
        if (user === "command@crms" && pass === "ops@123") {
            localStorage.setItem(AUTH_KEY, "true");
            window.location.href = "home.html"; // Seedha Home par bhejo
        } else {
            alert("Invalid Credentials!");
        }
    });
}

// --- 2. SECURITY CHECK (Redirect Loop Fixer) ---
const currentPage = window.location.pathname;

// Agar user Home/Map par hai aur login nahi kiya, toh Login page par bhejo
if ((currentPage.includes("home.html") || currentPage.includes("map.html")) && !localStorage.getItem(AUTH_KEY)) {
    window.location.href = "index.html";
}

// Agar user Login page par hai aur pehle se login hai, toh seedha Home par bhejo
if (currentPage.includes("index.html") && localStorage.getItem(AUTH_KEY)) {
    window.location.href = "home.html";
}

// --- 3. LIVE STATS LOGIC ---
async function loadStats() {
    const statTotal = document.getElementById('statTotal');
    if (!statTotal) return; 

    try {
        const response = await fetch(API_REPORTS);
        const data = await response.json();
        const reports = data.data || data || [];
        
        document.getElementById('statTotal').textContent = reports.length;
        document.getElementById('statClosed').textContent = reports.filter(r => r.status?.toLowerCase() === 'closed').length;
        document.getElementById('statInvest').textContent = reports.length - reports.filter(r => r.status?.toLowerCase() === 'closed').length;
    } catch (error) {
        console.error("Stats Error:", error);
    }
}

// --- 4. LOGOUT LOGIC ---
document.addEventListener('click', (e) => {
    if (e.target.id === 'logoutBtn') {
        localStorage.removeItem(AUTH_KEY);
        window.location.href = "index.html";
    }
});

loadStats();