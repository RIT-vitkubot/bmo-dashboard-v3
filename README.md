# BMO Dashboard v3

## Project Overview
BMO Dashboard v3 is an intelligent command center designed to provide real-time visualization of BMO's internal state, active tasks, and system health. The primary objective of this application is to provide the human operator (Vít Parma) with transparency into BMO's current activities, planned work, and completed objectives.

## Core Objectives
- **Operational Transparency:** Real-time visibility into BMO's task queue.
- **System Monitoring:** Live telemetry of the host Ubuntu server (CPU, RAM, Disk).
- **Proactive Communication:** Direct interface for BMO's contextual suggestions and status updates.

## Technical Stack
- **Backend:** Flask (Python) with `psutil` for system telemetry.
- **Frontend:** Vue.js 3 + Tailwind CSS for a modern, reactive UI.
- **Design Language:** Glassmorphism with True Dark Mode, focusing on high legibility and Apple-style minimalism.
- **State Management:** Real-time updates via WebSockets (planned) and periodic API polling.

## Features
- **Task Visualization:** A three-column Trello-style layout showing BMO's status (ToDo, In Progress, Done).
- **System Health Gauges:** Real-time monitoring of host resources.
- **"BMO Says" Widget:** Context-aware status messages and alerts.

## Implementation Status
- **Phase 1 (The Face):** Core UI skeleton, layout, and basic API integration. [COMPLETED]
- **Phase 2 (The Heart):** Persistence layer and enhanced system telemetry. [IN PROGRESS]
