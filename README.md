# FocusFlow: Personal Productivity Analytics System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

[![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)](https://streamlit.io/)

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Project Overview

**FocusFlow** is a "Quantified Self" application designed to track, store, and analyze personal concentration habits. Unlike traditional Pomodoro timers, this system focuses on **Data Persistence** and **Visual Analytics**.

By collecting granular data on focus sessions (duration, time of day, day of week), the system employs **Time Series Analysis** and **Heatmaps** to help users identify their "Peak Performance Hours" and visualize their productivity growth over time.

> **Key Concept**: Transforming subjective "feelings of productivity" into objective, actionable data insights.

## Key Features

### 1. Gamified Data Collection (Timer)
- **Pomodoro Logic**: Standard focus timer with visual progress tracking.
- **Reward System**: Users "grow" different virtual plants (e.g., Sunflower, Cactus) upon completing sessions to encourage consistency.
- **Data Persistence**: All records are automatically saved to a local CSV database (`focus_history.csv`) for long-term storage.

### 2. Mock Data Generator (Simulation)
- Includes a built-in simulation engine using `NumPy` to generate realistic historical data.
- **Scenario Simulation**: Simulates a "Learning Curve" scenario where user productivity improves by **~30%** over a 30-day period (ideal for demonstrating analytics capabilities).

### 3. Analytics Dashboard
- **Time Series Analysis**: Line charts tracking daily focus duration trends.
- **Habit Heatmap**: A scatter/bubble chart visualizing the correlation between "Day of Week" and "Hour of Day" to pinpoint optimal work windows.
- **Distribution Analysis**: Pie charts showing the diversity of "harvested" plants (gamification stats).
- **KPI Metrics**: Real-time calculation of Total Hours, Session Counts, and Best Time Slots.

## Tech Stack
- **Frontend**: Streamlit (Web App Interface)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express (Interactive Charts)
- **Storage**: Local CSV (Lightweight Database)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/jolyne525/pomodoro.git
cd pomodoro
