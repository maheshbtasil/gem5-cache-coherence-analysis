#!/usr/bin/env bash
set -e

# Base paths
GEM5_DIR="$HOME/gem5"
GEM5_BIN="$GEM5_DIR/build/X86/gem5.opt"
CONFIG="$GEM5_DIR/configs/cpre581_proj/mc_classic.py"

NUM_CPUS=4

# Workloads and their options (number of threads)
WORKLOADS=("w1_read_mostly" "w2_pingpong" "w3_mixed")
OPTIONS=("4"             "4"           "4")

# L1 latency values to sweep (in cycles)
LATENCIES=(2 4 6)

echo "Running classic cache sweep (W1/W2/W3 × lat=2,4,6) ..."

for i in "${!WORKLOADS[@]}"; do
    W="${WORKLOADS[$i]}"
    OPTS="${OPTIONS[$i]}"

    for LAT in "${LATENCIES[@]}"; do
        OUTDIR="mc_${W}_lat${LAT}_4core"

        echo
        echo "=============================================="
        echo " Workload: $W  |  L1 latency: ${LAT} cycles"
        echo " Output dir: $OUTDIR"
        echo "=============================================="
        echo

        "$GEM5_BIN" \
          -d "$OUTDIR" \
          "$CONFIG" \
          --num-cpus="$NUM_CPUS" \
          --l1d-latency-cycles="$LAT" \
          --l1i-latency-cycles="$LAT" \
          --cmd="$GEM5_DIR/workloads/cpre581/$W" \
          --options="$OPTS"
    done
done

echo
echo "All classic runs finished. Check mc_* directories for stats.txt."
