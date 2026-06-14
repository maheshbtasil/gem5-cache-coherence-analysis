# gem5 Cache and Coherence Analysis

## Overview

This project evaluates how **L1 cache latency** and **cache coherence protocols** affect multicore processor performance using the **gem5 simulator**.

The study compares workload behavior under different architectural configurations, including classic cache models and Ruby memory system protocols such as **MESI** and **MOESI**.

---

## Key Objectives

- Analyze the impact of L1 cache latency on IPC
- Compare MESI and MOESI cache coherence protocols
- Evaluate multicore performance using synthetic workloads
- Identify how software-level sharing patterns affect scalability

---

## Technologies Used

- gem5 Simulator
- Python
- Bash/Shell scripting
- Linux/Ubuntu
- Multicore simulation
- Cache coherence analysis

---

## Workloads

Three synthetic multicore workloads were used:

- **W1 – Read-Mostly Workload**  
  Threads repeatedly read from shared data.

- **W2 – Write-Sharing Ping-Pong Workload**  
  Threads update shared data using synchronization, creating cache-line contention.

- **W3 – Mixed Private + Shared Workload**  
  Threads perform private computation along with shared updates.

---

## Experiments

### Classic Cache Model

L1 cache latency was tested using:

- 2 cycles
- 4 cycles
- 6 cycles

### Ruby Memory System

Cache coherence protocols compared:

- MESI CMP Directory
- MOESI CMP Directory

---

## Key Findings

- Increasing L1 latency reduced IPC across workloads.
- Workload sharing behavior had a larger impact than hardware-level tuning.
- Write-sharing workloads showed poor multicore scalability.
- MESI and MOESI showed very similar IPC results for the tested synthetic workloads.
- Software-level contention was the main performance bottleneck.

---

## Repository Structure

```text
gem5-cache-coherence-analysis/
│
├── README.md
├── CPRE581_Project_Report.pdf
├── scripts/
│   ├── parse_classic_stats.py
│   ├── parse_ruby_stats.py
│   └── run_classic_sweep.sh
