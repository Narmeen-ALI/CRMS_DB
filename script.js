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

// ========================================
// 🔗 CONNECTION SETTINGS (FIXED FOR MOBILE)
// ========================================
const CURRENT_HOST = window.location.hostname; 
const API = `http://${CURRENT_HOST}:5000/api`;

const AUTH_KEY = "crms-auth";
const DEMO_USER = "command@crms";
const DEMO_PASS = "ops@123";
const loginNoticeKey = "crms-login-notice";

let records = [];

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
};

const setLoginMessage = (msg, ok = true) => {
  if (!loginFeedback) return;
  loginFeedback.textContent = msg;
  loginFeedback.classList.remove("error", "success");
  loginFeedback.classList.add(ok ? "success" : "error");
};

const isAuthed = () => sessionStorage.getItem(AUTH_KEY) === "true";
const needsAuth = () => {
  const restricted = ["report.html", "records.html"];
  const path = window.location.pathname.split("/").pop();
  return restricted.includes(path);
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
  if (!form) return;
  form.reset();
  if (reportId) reportId.value = "";
  setMessage("");
};

// ========================================
// 📄 TABLE DRAW
// ========================================
const drawTable = () => {
  if (!tableBody) return;
  const query = (search?.value || "").trim().toLowerCase();
  const list = records.filter((r) =>
    `${r.reporter} ${r.suspect} ${r.crime} ${r.location} ${r.status}`
      .toLowerCase()
      .includes(query)
  );

  tableBody.innerHTML = list
    .map(
      (r) => `
      <tr>
        <td data-label="FIR #">#${r.id}</td>
        <td data-label="Reporter">${r.reporter}</td>
        <td data-label="Suspect">${r.suspect}</td>
        <td data-label="Crime Type">${r.crime}</td>
        <td data-label="Location">${r.location}</td>
        <td data-label="Status"><span class="tag ${r.status}">${r.status}</span></td>
        <td data-label="Actions">
          <div class="row-actions">
            <button class="ghost" data-action="edit" data-id="${r.id}">Edit</button>
            <button class="ghost pdf-btn" data-action="pdf" data-id="${r.id}">📄 PDF</button>
            <button class="danger" data-action="delete" data-id="${r.id}">Delete</button>
          </div>
        </td>
      </tr>`
    )
    .join("");
    
  if (emptyState) {
    emptyState.textContent = list.length ? "" : "No records yet. Start by filing one.";
  }
};

const updateStats = () => {
  if (!statTotal || !statInvest || !statClosed) return;
  const total = records.length;
  const investigating = records.filter((r) => r.status === "Investigating").length;
  const closed = records.filter((r) => r.status === "Closed").length;
  statTotal.textContent = total;
  statInvest.textContent = investigating;
  statClosed.textContent = closed;
};

const requiresRecords = Boolean(tableBody || statTotal);

const loadRecords = () => {
  if (!requiresRecords) return Promise.resolve();
  return api("read")
    .then((res) => {
      records = res.data || [];
      drawTable();
      updateStats();
    })
    .catch(() => setMessage("Unable to reach server", false));
};

if (form) {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const payload = serialize();
    if (!payload.reporter || !payload.suspect || !payload.crime || !payload.location) {
      return setMessage("All fields except notes are required", false);
    }
    const action = payload.id ? "update" : "create";
    setMessage("Saving...");
    api(action, payload)
      .then((res) => {
        setMessage(res.message || "Saved");
        resetForm();
        loadRecords();
      })
      .catch(() => setMessage("Save failed", false));
  });
}

if (resetBtn) {
  resetBtn.addEventListener("click", resetForm);
}

if (search) {
  search.addEventListener("input", drawTable);
}

// ========================================
// 📄 TABLE ACTIONS (Edit, PDF, Delete)
// ========================================
if (tableBody) {
  tableBody.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    const { action, id } = btn.dataset;
    const record = records.find((r) => String(r.id) === id);
    
    if (action === "edit" && record) {
      sessionStorage.setItem("crms-edit-record", JSON.stringify(record));
      window.location.href = "report.html#reportForm";
    }
    
    if (action === "pdf" && id) {
      const pdfUrl = `http://${CURRENT_HOST}:5000/api/download-pdf/${id}`;
      window.open(pdfUrl, '_blank');
      if (feedback) {
        setMessage(`📄 Downloading PDF for report #${id}...`, true);
        setTimeout(() => setMessage(""), 3000);
      }
    }
    
    if (action === "delete" && record) {
      if (!confirm(`Delete report #${record.id}?`)) return;
      setMessage("Deleting...");
      api("delete", { id: record.id })
        .then((res) => {
          setMessage(res.message || "Deleted");
          loadRecords();
        })
        .catch(() => setMessage("Delete failed", false));
    }
  });
}

loadRecords();

if (form) {
  const cached = sessionStorage.getItem("crms-edit-record");
  if (cached) {
    try {
      const record = JSON.parse(cached);
      reportId.value = record.id;
      reporter.value = record.reporter;
      suspect.value = record.suspect;
      crime.value = record.crime;
      status.value = record.status;
      locationInput.value = record.location;
      notes.value = record.notes || "";
      setMessage(`Editing report #${record.id}`);
    } catch (_) {}
    sessionStorage.removeItem("crms-edit-record");
  }
}

if (loginForm) {
  const loginNotice = sessionStorage.getItem(loginNoticeKey);
  if (loginNotice) {
    setLoginMessage(loginNotice, false);
    sessionStorage.removeItem(loginNoticeKey);
  }

  if (isAuthed()) {
    setLoginMessage("Already signed in. Access reports anytime.", true);
    loginForm.querySelector("button").disabled = true;
  }

  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const user = loginUser.value.trim();
    const pass = loginPass.value.trim();

    if (!user || !pass) {
      return setLoginMessage("Enter username and password", false);
    }

    if (user === DEMO_USER && pass === DEMO_PASS) {
      sessionStorage.setItem(AUTH_KEY, "true");
      setLoginMessage("Access granted. Redirecting…", true);
      loginForm.querySelector("button").disabled = true;
      setTimeout(() => (window.location.href = "report.html"), 800);
    } else {
      setLoginMessage("Invalid credentials. Use the demo pair shown above.", false);
    }
  });
}

if (needsAuth() && !isAuthed()) {
  sessionStorage.setItem(loginNoticeKey, "Please sign in before accessing that screen.");
  window.location.href = "index.html#loginForm";
}

// ========================================
// 🚪 LOGOUT FUNCTIONALITY (NEW ADDITION)
// ========================================
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        // Auth clear karein
        sessionStorage.removeItem(AUTH_KEY);
        sessionStorage.clear();
        // Login page par wapas bhej dein
        alert("Logged out successfully.");
        window.location.href = "index.html";
    });
}