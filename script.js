const API_BASE_URL = "https://sadia.pythonanywhere.com/api";
const API_REPORTS = `${API_BASE_URL}/reports`;
const AUTH_KEY = "crms-auth";

// --- LOGIN LOGIC ---
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const user = document.getElementById('loginUser').value.trim();
        const pass = document.getElementById('loginPass').value.trim();
        
        if (user === "command@crms" && pass === "ops@123") {
            localStorage.setItem(AUTH_KEY, "true");
            window.location.href = "home.html"; 
        } else {
            alert("Ghalat Credentials! Try again.");
        }
    });
}

// --- FORM SUBMISSION (Fix for Submit Issue) ---
const reportForm = document.getElementById('reportForm');
if (reportForm) {
    reportForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(reportForm);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch(API_REPORTS, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (response.ok) {
                alert("FIR Successfully Registered!");
                window.location.href = "home.html";
            }
        } catch (error) {
            alert("Error submitting report. Check connection.");
        }
    });
}

// --- LIVE STATS ---
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
        // Fallback agar API slow ho
        document.getElementById('statTotal').textContent = "0";
    }
}

// --- LOGOUT ---
document.addEventListener('click', (e) => {
    if (e.target.id === 'logoutBtn') {
        localStorage.removeItem(AUTH_KEY);
        window.location.href = "index.html";
    }
});

loadStats();
// --- SUSPECTS & EVIDENCE LOADING ---
async function loadSuspectData() {
    const suspectTable = document.getElementById('suspectsListData');
    if (!suspectTable) return;

    try {
        const response = await fetch(API_REPORTS);
        const data = await response.json();
        const reports = data.data || data || [];

        suspectTable.innerHTML = ""; // Clear loading text

        reports.forEach(report => {
            const row = `
                <tr>
                    <td><strong>${report.suspect_name || 'Unknown'}</strong></td>
                    <td>#${report.id || 'N/A'}</td>
                    <td>${report.crime_type || 'General'}</td>
                    <td><span class="status-badge">${report.status || 'Active'}</span></td>
                    <td><button class="view-btn">View Profile</button></td>
                </tr>`;
            suspectTable.innerHTML += row;
        });
    } catch (e) {
        suspectTable.innerHTML = "<tr><td colspan='5'>Error loading suspects.</td></tr>";
    }
}
loadSuspectData();