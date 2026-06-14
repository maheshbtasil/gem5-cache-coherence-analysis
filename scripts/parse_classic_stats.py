#!/usr/bin/env python3
import os
import re

GEM5_DIR = os.path.expanduser("~/gem5")

workloads = ["w1_read_mostly", "w2_pingpong", "w3_mixed"]
latencies = [2, 4, 6]

def parse_stats_file(path):
    data = {
        "sim_ticks": None,
        "sim_insts": None,
        "ipcs": {}
    }
    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        for line in f:
            # Total simulated ticks
            if line.startswith("sim_ticks"):
                parts = line.split()
                if len(parts) >= 2:
                    data["sim_ticks"] = float(parts[1])

            # Total simulated instructions
            elif line.startswith("sim_insts"):
                parts = line.split()
                if len(parts) >= 2:
                    data["sim_insts"] = float(parts[1])

            # Per-core IPC: system.cpu0.ipc, system.cpu1.ipc, ...
            elif "system.cpu" in line and ".ipc" in line:
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0]
                    value = float(parts[1])
                    m = re.match(r"system\.cpu(\d+)\.ipc", name)
                    if m:
                        core = int(m.group(1))
                        data["ipcs"][core] = value

    return data


def main():
    print("workload,latency,sim_ticks,sim_insts,avg_ipc,cpu0_ipc,cpu1_ipc,cpu2_ipc,cpu3_ipc")

    for w in workloads:
        for lat in latencies:
            outdir = f"mc_{w}_lat{lat}_4core"
            stats_path = os.path.join(GEM5_DIR, outdir, "stats.txt")

            stats = parse_stats_file(stats_path)
            if stats is None:
                print(f"{w},{lat},MISSING,MISSING,MISSING,,,,")
                continue

            sim_ticks = stats["sim_ticks"]
            sim_insts = stats["sim_insts"]
            ipcs = stats["ipcs"]

            ipc_values = [ipcs.get(i, 0.0) for i in range(4)]
            avg_ipc = sum(ipc_values) / 4.0

            row = [
                w,
                str(lat),
                str(sim_ticks) if sim_ticks is not None else "NA",
                str(sim_insts) if sim_insts is not None else "NA",
                f"{avg_ipc:.6f}",
                f"{ipc_values[0]:.6f}",
                f"{ipc_values[1]:.6f}",
                f"{ipc_values[2]:.6f}",
                f"{ipc_values[3]:.6f}",
            ]
            print(",".join(row))


if __name__ == "__main__":
    main()
