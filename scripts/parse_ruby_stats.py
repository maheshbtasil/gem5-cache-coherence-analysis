#!/usr/bin/env python3
import os
import re

GEM5_DIR = os.path.expanduser("~/gem5")

# Expected Ruby result directories:
# You already have / will have these as you run MESI and MOESI:
ruby_runs = [
    "ruby_mesi_w2_pingpong_4core",
    "ruby_mesi_w3_mixed_4core",
    "ruby_moesi_w2_pingpong_4core",
    "ruby_moesi_w3_mixed_4core",
]

def parse_stats(path):
    if not os.path.exists(path):
        return None

    data = {
        "ipcs": {},

        # Ruby network stats (we’ll try a few common names)
        "ruby_total_messages": None,
        "ruby_total_incoming": None,
        "ruby_total_outgoing": None,
    }

    with open(path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            name = parts[0]
            value_str = parts[1]

            # Per-core IPC: system.cpu0.ipc, system.cpu1.ipc, ...
            if "system.cpu" in name and name.endswith(".ipc"):
                try:
                    val = float(value_str)
                except ValueError:
                    continue
                m = re.match(r"system\.cpu(\d+)\.ipc", name)
                if m:
                    core = int(m.group(1))
                    data["ipcs"][core] = val

            # Ruby network message counters (try several common stat names)
            elif name == "system.ruby.network.total_messages":
                try:
                    data["ruby_total_messages"] = float(value_str)
                except ValueError:
                    pass

            elif name == "system.ruby.network.total_incoming_messages":
                try:
                    data["ruby_total_incoming"] = float(value_str)
                except ValueError:
                    pass

            elif name == "system.ruby.network.total_outgoing_messages":
                try:
                    data["ruby_total_outgoing"] = float(value_str)
                except ValueError:
                    pass

    return data

def main():
    print("workload,protocol,avg_ipc,cpu0_ipc,cpu1_ipc,cpu2_ipc,cpu3_ipc,"
          "ruby_total_messages,ruby_total_incoming,ruby_total_outgoing")

    for run in ruby_runs:
        stats_path = os.path.join(GEM5_DIR, run, "stats.txt")
        if not os.path.exists(stats_path):
            # Directory or stats.txt not present yet
            # Try to decode workload + protocol from the name anyway
            parts = run.split("_")
            proto = parts[1] if len(parts) > 1 else "unknown"
            workload = parts[2] if len(parts) > 2 else "unknown"
            print(f"{workload},{proto},MISSING,,,,,MISSING,MISSING,MISSING")
            continue

        stats = parse_stats(stats_path)
        if stats is None:
            parts = run.split("_")
            proto = parts[1] if len(parts) > 1 else "unknown"
            workload = parts[2] if len(parts) > 2 else "unknown"
            print(f"{workload},{proto},MISSING,,,,,MISSING,MISSING,MISSING")
            continue

        # Decode workload + protocol from directory name
        parts = run.split("_")
        proto = parts[1] if len(parts) > 1 else "unknown"
        workload = parts[2] if len(parts) > 2 else "unknown"

        ipcs = stats["ipcs"]
        ipc_values = [ipcs.get(i, 0.0) for i in range(4)]
        avg_ipc = sum(ipc_values) / 4.0

        ruby_total_messages = stats["ruby_total_messages"]
        ruby_total_incoming = stats["ruby_total_incoming"]
        ruby_total_outgoing = stats["ruby_total_outgoing"]

        def fmt(x):
            if x is None:
                return "NA"
            # integer-like stats can be big; print without decimals
            if abs(x - int(x)) < 1e-9:
                return str(int(x))
            return f"{x:.6f}"

        row = [
            workload,
            proto,
            f"{avg_ipc:.6f}",
            f"{ipc_values[0]:.6f}",
            f"{ipc_values[1]:.6f}",
            f"{ipc_values[2]:.6f}",
            f"{ipc_values[3]:.6f}",
            fmt(ruby_total_messages),
            fmt(ruby_total_incoming),
            fmt(ruby_total_outgoing),
        ]

        print(",".join(row))

if __name__ == "__main__":
    main()
