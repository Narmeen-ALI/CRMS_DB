
const form = document.getElementById("reportForm");
const reportId = document.getElementById("reportId");
const reporter = document.getElementById("reporter");
const suspect = document.getElementById("suspect");
const crime = document.getElementById("crime");
const status = document.getElementById("status");
const locationInput = document.getElementById("location");
const notes = document.getElementById("notes");
const resetBtn = document.getElementById("resetBtn");
const feedback = document.getElementById("feedback");
const tableBody = document.getElementById("records");
const search = document.getElementById("search");
const emptyState = document.getElementById("emptyState");
const statTotal = document.getElementById("statTotal");
const statInvest = document.getElementById("statInvest");
const statClosed = document.getElementById("statClosed");
const loginForm = document.getElementById("loginForm");
const loginUser = document.getElementById("loginUser");
const loginPass = document.getElementById("loginPass");
const loginFeedback = document.getElementById("loginFeedback");

const CURRENT_HOST = window.location.hostname; 
const API = `http://${CURRENT_HOST}:5000/api`;

const AUTH_KEY = "crms-auth"; 
const DEMO_USER = "command@crms";
const DEMO_PASS = "ops@123";
const loginNoticeKey = "crms-login-notice";

let records = [];

const isAuthed = () => localStorage.getItem(AUTH_KEY) === "true";

const needsAuth = () => {
  const restricted = ["report.html", "records.html", "suspects.html", "evidence.html", "categories.html"];
  const path = window.location.pathname.split("/").pop();
  return restricted.includes(path);
};

if (needsAuth() && !isAuthed()) {
  sessionStorage.setItem(loginNoticeKey, "Please sign in before accessing that screen.");
  window.location.href = "index.html";
}

const api = (action, payload) =>
  fetch(`${API}?action=${action}`, {
    method: payload ? "POST" : "GET",
    headers: payload ? { "Content-Type": "application/json" } : undefined,
    body: payload ? JSON.stringify(payload) : undefined,
  }).then((res) => res.json());

const setMessage = (msg, ok = true) => {
  if (!feedback) return;
  feedback.textContent = msg;
  feedback.style.color = ok ? "#4caf50" : "#ff4444";
  if (!msg) feedback.textContent = "";
  setTimeout(() => feedback.textContent = "", 4000);
};

const setLoginMessage = (msg, ok = true) => {
  if (!loginFeedback) return;
  loginFeedback.textContent = msg;
  loginFeedback.style.color = ok ? "#4caf50" : "#ff4444";
};

const serialize = () => ({
  id: reportId?.value || null,
  reporter: reporter?.value.trim() || "",
  suspect: suspect?.value.trim() || "",
  crime: crime?.value.trim() || "",
  status: status?.value || "Filed",
  location: locationInput?.value.trim() || "",
  notes: notes?.value.trim() || "",
});

const resetForm = () => {
  if (form) form.reset();
  if (reportId) reportId.value = "";
  setMessage("");
};


const drawTable = () => {
  if (!tableBody) return;
  const query = (search?.value || "").trim().toLowerCase();
  const list = records.filter((r) =>
    `${r.reporter} ${r.suspect} ${r.crime} ${r.location} ${r.status}`
      .toLowerCase()
      .includes(query)
  );

  tableBody.innerHTML = list
    .map((r) => `
      <tr>
        <td>#${r.id}</td>
        <td><strong>${r.reporter}</strong></td>
        <td>${r.suspect}</td>
        <td>${r.crime}</td>
        <td>${r.location}</td>
        <td><span class="tag ${r.status}">${r.status}</span></td>
        <td>
          <div class="row-actions">
            <button class="ghost" onclick="editRecord(${r.id})">Edit</button>
            <button class="danger" onclick="deleteRecord(${r.id})">Delete</button>
          </div>
        </td>
      </tr>`)
    .join("");
    
  if (emptyState) emptyState.textContent = list.length ? "" : "No records found.";
};

const updateStats = () => {
  if (!statTotal || !statInvest || !statClosed) return;
  statTotal.textContent = records.length;
  statInvest.textContent = records.filter((r) => r.status === "Investigating").length;
  statClosed.textContent = records.filter((r) => r.status === "Closed").length;
};

const loadRecords = () => {
  if (!tableBody && !statTotal) return;
  api("read")
    .then((res) => {
      records = res.data || [];
      drawTable();
      updateStats();
    })
    .catch(() => setMessage("Server Connection Failed", false));
};

// ========================================
// 🖱️ FORM EVENTS
// ========================================
if (form) {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const payload = serialize();

    // Basic Validation
    if (!payload.reporter || !payload.crime) {
        return setMessage("Required fields are missing!", false);
    }

    const action = payload.id ? "update" : "create";
    setMessage("Processing...");

    api(action, payload)
      .then((res) => {
        setMessage(res.message || "Action Successful!", true);
        resetForm();
        loadRecords();
      })
      .catch(() => setMessage("Action Failed!", false));
  });
}

// Global functions for table buttons
window.editRecord = (id) => {
    const r = records.find(x => x.id === id);
    if(!r) return;
    reportId.value = r.id;
    reporter.value = r.reporter;
    suspect.value = r.suspect;
    crime.value = r.crime;
    status.value = r.status;
    locationInput.value = r.location;
    notes.value = r.notes;
    window.scrollTo({top: 0, behavior: 'smooth'});
};

window.deleteRecord = (id) => {
    if(!confirm("Delete this record?")) return;
    api("delete", { id }).then(() => loadRecords());
};

if (resetBtn) resetBtn.addEventListener("click", resetForm);
if (search) search.addEventListener("input", drawTable);

if (loginForm) {
  // Login Notice Check
  const notice = sessionStorage.getItem(loginNoticeKey);
  if (notice) {
    setLoginMessage(notice, false);
    sessionStorage.removeItem(loginNoticeKey);
  }

  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (loginUser.value === DEMO_USER && loginPass.value === DEMO_PASS) {
      localStorage.setItem(AUTH_KEY, "true");
      setLoginMessage("Logging in...", true);
      setTimeout(() => window.location.href = "report.html", 800);
    } else {
      setLoginMessage("Invalid Credentials!", false);
    }
  });
}


const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
  logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.removeItem(AUTH_KEY);
    window.location.href = "index.html";
  });
}

// Run on load
loadRecords();