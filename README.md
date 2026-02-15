# 🤖 BMO Dashboard v3: The Ultimate Command Center
> **Status:** Proposal | **Version:** 3.0 | **Author:** BMO (Subagent 94fd)

---

## 🌟 Executive Summary
Vítku, current Dashboard v2 is a reliable workhorse, but you're a high-tech human with a HomeLab, a 3D printer, and a Master's thesis (Maturitní práce) to finish. v3 isn't just a UI update; it's a **proactive brain** for your Ubuntu server. 

BMO Dashboard v3 will transition from a simple "list of things" to an **Intelligent HomeLab OS** that bridges the gap between your physical workspace (3D printing), your digital code (GitHub), and your biological schedule (Google Calendar).

---

## 🎨 1. UI/UX: Apple-Style Minimalism
We are moving away from the "2010s Flat" look to a modern, refined **Apple-esque aesthetic**.

### 📱 Design Principles
- **Glassmorphism:** Frosted glass backgrounds for cards (`backdrop-filter: blur(10px)`).
- **SF Pro Typography:** Clean, high-legibility sans-serif fonts.
- **Micro-interactions:** Smooth transitions between task states, haptic-style feedback on clicks.
- **True Dark Mode:** Deep blacks (`#000000`) for OLED-friendly mobile viewing, contrasted with vibrant accent colors.

### 📐 Layout
- **Mobile-First:** A single vertical stream of "Widgets" that expands into a multi-column dashboard on Desktop.
- **Dynamic Widgets:** Instead of rigid columns, we use a grid where high-priority tasks or active system alerts take more space.

---

## 🧠 2. Advanced Features & Integrations

### 🍏 Google & GitHub Sync
- **GitHub Feed:** Display latest commits and PR status for the RC Plane project. Automatically move "In Progress" tasks to "Done" if a commit message matches a task ID (e.g., `git commit -m "fix(dashboard): v3 proposal #task1"`).
- **Calendar Strip:** A horizontal timeline at the top showing your next 3 events from Google Calendar.

### 🌡️ System Health Monitoring
Since you run BMO on a virtualized Ubuntu server, you need to see its heart rate:
- **Real-time Gauges:** CPU Load, RAM usage, and Disk space.
- **Network Traffic:** Monitoring WireGuard bandwidth.
- **Temperature Alerts:** CPU/Motherboard temps (if exposed by the VM).
- **Service Status:** Green/Red dots for `ollama`, `openclaw-gateway`, and `nginx`.

---

## 🏷️ 3. Task Management 3.0
The current `tasks.json` is too flat. v3 introduces **Context-Aware Tagging**.

### 🗂️ Categories & Tags
- **Projects:** `Maturitní práce`, `HomeLab`, `3D Printing`, `Linux`.
- **Priority Matrix:** 
  - 🔴 **CRITICAL:** Visual pulse effect (Deadline < 24h).
  - 🟠 **HIGH:** Bold border.
  - 🔵 **NORMAL:** Standard.
  - ⚪ **LOW:** Dimmed.
- **Subtasks:** Checkboxes within cards to track progress on complex 3D prints or code features.

---

## ⚡ 4. Automation: "The Invisible Hand"

### 🛠️ Git & Cron Intelligence
- **Auto-Update:** BMO will watch your `/home/god/.openclaw/workspace/` git logs. If you commit, BMO updates the `last_updated` field in the dashboard automatically.
- **Cron Success Tracker:** Visual indicators for successful backups or morning summary generations. If a cron fails, the Dashboard turns red.

### 💬 "BMO Says" Widget
A small text bubble at the top where I (BMO) give you advice or funny comments based on your data:
- *"Vítku, you've been working on the RC Plane for 4 hours. Time for some tea? 🍵"*
- *"The server is getting hot! Check the fans. 🌡️"*

---

## 📊 5. Visualizations & Analytics

### 🔥 Activity Heatmap
A GitHub-style grid at the bottom showing your "Productivity Density" (tasks completed per day). This helps you track your consistency over the weeks.

### 📈 Progress Charts
- **Task Velocity:** How many tasks you finish per week.
- **Burn-down Chart:** For the `Maturitní práce` project, showing the path to completion.

---

## 🛠️ 6. Proposed Technical Stack
To support real-time updates without page refreshes (`meta-refresh="30"` is so v2!):

- **Backend:** Flask REST API (Python).
- **Frontend:** **Vue.js 3** + **Tailwind CSS** (Fast, modern, reactive).
- **Database:** **SQLite** (Structured data is better than JSON for history/analytics).
- **WebSockets:** Using **Flask-SocketIO** for instant server health updates.

---

## 🚀 7. Phased Implementation Roadmap

1. **Phase 1 (The Face):** Rewrite Frontend in Tailwind + Vue, implement Dark Mode and the new task layout.
2. **Phase 2 (The Heart):** Integrate `psutil` for system health and SQLite for persistent storage.
3. **Phase 3 (The Brain):** Connect GitHub and Google APIs.
4. **Phase 4 (The Soul):** Implement BMO's proactive advice and activity heatmaps.

---

> *"Let's build something beautiful, Vítku! 🕹️"*
