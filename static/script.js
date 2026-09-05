// ===============================
// ResolveAI Premium Dashboard JS
// ===============================

// Live Date & Time
function updateClock() {
    const now = new Date();

    const dateEl = document.getElementById("liveDate");
    const timeEl = document.getElementById("liveTime");

    if (dateEl)
        dateEl.innerHTML = now.toDateString();

    if (timeEl)
        timeEl.innerHTML = now.toLocaleTimeString();
}

setInterval(updateClock, 1000);
updateClock();


// ===============================
// Dark Mode
// ===============================

const themeBtn = document.getElementById("themeBtn");

if (localStorage.getItem("theme") === "light") {
    document.body.classList.add("light-mode");
}

if (themeBtn) {
    themeBtn.addEventListener("click", () => {

        document.body.classList.toggle("light-mode");

        if (document.body.classList.contains("light-mode")) {
            localStorage.setItem("theme", "light");
            themeBtn.innerHTML = "☀️";
        } else {
            localStorage.setItem("theme", "dark");
            themeBtn.innerHTML = "🌙";
        }

    });
}


// ===============================
// Animated Counters
// ===============================

document.querySelectorAll(".counter").forEach(counter => {

    const target = Number(counter.innerText);

    let count = 0;

    const speed = target / 50;

    const updateCount = () => {

        if (count < target) {

            count += speed;

            counter.innerText = Math.ceil(count);

            requestAnimationFrame(updateCount);

        } else {

            counter.innerText = target;

        }

    };

    updateCount();

});


// ===============================
// Toast Notification
// ===============================

function showToast(message) {

    let toast = document.getElementById("toast");

    if (!toast) {
        toast = document.createElement("div");
        toast.id = "toast";

        toast.style.position = "fixed";
        toast.style.bottom = "20px";
        toast.style.right = "20px";
        toast.style.padding = "15px 20px";
        toast.style.background = "#4ea3ff";
        toast.style.color = "white";
        toast.style.borderRadius = "12px";
        toast.style.zIndex = "9999";

        document.body.appendChild(toast);
    }

    toast.innerHTML = message;

    toast.style.display = "block";

    setTimeout(() => {
        toast.style.display = "none";
    }, 3000);
}


// ===============================
// Welcome Toast
// ===============================

window.addEventListener("load", () => {
    showToast("🤖 ResolveAI Dashboard Loaded");
});


// ===============================
// Confidence Meter Animation
// ===============================

const confidenceFill =
    document.querySelector(".confidence-fill");

if (confidenceFill) {

    let width = 0;

    const target = 94;

    const interval = setInterval(() => {

        if (width >= target) {

            clearInterval(interval);

        } else {

            width++;

            confidenceFill.style.width = width + "%";

        }

    }, 20);

}


// ===============================
// Export CSV
// ===============================

function exportCSV() {

    let csv =
        "Ticket ID,Customer,Issue,Status\n" +
        "1001,Arun,Internet Down,Escalated\n" +
        "1002,Priya,Password Reset,Resolved\n" +
        "1003,Rahul,Billing Query,In Progress";

    const blob = new Blob([csv], {
        type: "text/csv"
    });

    const url =
        window.URL.createObjectURL(blob);

    const a =
        document.createElement("a");

    a.href = url;

    a.download = "resolveai-report.csv";

    a.click();

    showToast("📤 Report Exported");
}


// ===============================
// Search Filter
// ===============================

const searchInput =
    document.querySelector(".search-box input");

if (searchInput) {

    searchInput.addEventListener("keyup", () => {

        const filter =
            searchInput.value.toLowerCase();

        document
            .querySelectorAll(".menu li")
            .forEach(item => {

                item.style.display =
                    item.innerText
                    .toLowerCase()
                    .includes(filter)
                    ? "block"
                    : "none";

            });

    });

}


// ===============================
// Activity Feed Auto Update
// ===============================

const activities = [

    "🎫 New Ticket Created",
    "🤖 AI Suggested Resolution",
    "👤 Customer Registered",
    "📚 Knowledge Base Updated",
    "⚠️ Ticket Escalated",
    "✅ Ticket Resolved"

];

setInterval(() => {

    const lists =
        document.querySelectorAll(".panel ul");

    if (lists.length > 0) {

        const li =
            document.createElement("li");

        li.innerHTML =
            activities[
                Math.floor(
                    Math.random() *
                    activities.length
                )
            ];

        lists[0].prepend(li);

        if (lists[0].children.length > 8) {
            lists[0].removeChild(
                lists[0].lastChild
            );
        }

    }

}, 10000);


// ===============================
// Ticket Analytics Chart
// ===============================

const ticketChart =
    document.getElementById("ticketChart");

if (ticketChart) {

    new Chart(ticketChart, {

        type: "line",

        data: {

            labels: [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ],

            datasets: [{

                label: "Tickets",

                data: [
                    12,
                    20,
                    15,
                    30,
                    25,
                    40,
                    32
                ],

                borderColor: "#4ea3ff",

                backgroundColor:
                    "rgba(78,163,255,.2)",

                fill: true,

                tension: .4

            }]

        }

    });

}


// ===============================
// Doughnut Chart
// ===============================

const pieChart =
    document.getElementById("pieChart");

if (pieChart) {

    new Chart(pieChart, {

        type: "doughnut",

        data: {

            labels: [
                "Resolved",
                "Escalated",
                "Open"
            ],

            datasets: [{

                data: [
                    60,
                    25,
                    15
                ],

                backgroundColor: [
                    "#2ecc71",
                    "#ff5e7a",
                    "#4ea3ff"
                ]

            }]

        }

    });

}


// ===============================
// Notification Bell
// ===============================

const bell =
    document.getElementById("notificationBtn");

if (bell) {

    bell.addEventListener("click", () => {

        showToast(
            "🔔 3 New Notifications"
        );

    });

}
window.addEventListener("load", () => {

    const loader =
        document.getElementById("loader");

    if(loader){

        loader.style.display = "block";

        setTimeout(() => {

            loader.style.display = "none";

        }, 1500);

    }

});


// ===============================
// Resolve Ticket Demo
// ===============================

function checkTicket() {

    const ticket =
        document.getElementById("ticketInput");

    const result =
        document.getElementById("result");

    if (!ticket || !result) return;

    if (ticket.value === "") {

        result.innerHTML =
            "❌ Enter Ticket ID";

        return;
    }

    result.innerHTML =
        "✅ AI Resolution Generated for Ticket #" +
        ticket.value;

    showToast(
        "🤖 Ticket Processed"
    );

}