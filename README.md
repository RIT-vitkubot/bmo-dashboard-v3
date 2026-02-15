# BMO Status Monitor (Dashboard v3)

## Project Overview
BMO Status Monitor is a minimalist command center designed to provide real-time visualization of BMO's internal computational state and current activities. This application is specifically tailored to monitor BMO's work, providing the human operator with transparency into what BMO is doing right now.

## Core Objectives
- **Activity Monitoring:** Real-time visibility into BMO's current, pending, and completed tasks.
- **BMO Core Health:** Live telemetry of BMO's computational environment (CPU, RAM, Disk).
- **Status Communication:** A dedicated channel for BMO to broadcast contextual messages and internal thoughts.

## Technical Stack
- **Backend:** Flask (Python) with `psutil` for system telemetry.
- **Frontend:** Vue.js 3 + Tailwind CSS (Vite).
- **Design:** Minimalist Glassmorphism, True Dark Mode, focusing on high-density information without clutter.

## Data Model (Minimalist)
To maintain focus and speed, the data model has been simplified to its core components:
- **Activity Name:** What is being worked on.
- **Status:** The lifecycle state (Pending, Active, Completed).

*Priorities and project categories have been deprecated in favor of a lean "activity stream" model.*

## Features
- **Process Columns:** Three-column layout separating pending thoughts, active processes, and completed logs.
- **Telemetry Gauges:** Real-time monitoring of host resources.
- **Contextual Broadcast:** A header widget displaying BMO's current mood or specific status updates.

## Current State
- **v3.1 Refactor:** Simplified datamodel, removed priority/project overhead, updated UI for BMO-centric monitoring. [CURRENT]
