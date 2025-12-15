#!/usr/bin/env python

from datetime import datetime, timedelta, UTC
from obspy import read
import argparse
import glob
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Argument parsing
parser = argparse.ArgumentParser(
    description="Plot helicorder for given date."
)
parser.add_argument(
    "--date",
    type=str,
    help="Target date in YYYYMMDD format (default: yesterday in UTC)",
)
args = parser.parse_args()

# Target date setup
if args.date:
    try:
        target_dt = datetime.strptime(args.date, "%Y%m%d").replace(tzinfo=UTC)
    except ValueError:
        sys.exit("Invalid date format. Use YYYYMMDD (e.g., 20250101).")
else:
    target_dt = datetime.now(UTC) - timedelta(days=1)

year = target_dt.strftime("%Y")
datestr = target_dt.strftime("%Y%m%d")
julday = target_dt.strftime("%j")
print(f"Processing date: {datestr} (Julian day {julday})")

# Station-specific scale configuration
station_scale = {
    # --- Network ---
    # Format: StationName : ScaleValue
    # Example: JN01: 2000, JN02: 30000
    # ScaleValue must be an integer
}
threshold_raw = 1.5

# Load files
pattern = f"/path_to_mseed_data/station.network.location.channel.{year}.{julday}"
files = sorted(glob.glob(pattern))
print(f"Found {len(files)} files for {year}.{julday}")

if not files:
    sys.exit(f"No file matching pattern: {pattern}")

try:
    st = read(files[0])
    for f in files[1:]:
        st += read(f)
    st.merge(fill_value="interpolate")
    st.detrend("demean")
    st.taper(0.0005, "cosine")
    st.filter("bandpass", freqmin=1, freqmax=20)
except Exception as e:
    sys.exit(f"Error reading waveform files: {e}")

# Output directory
outdir = "/path_to_output_directory"
os.makedirs(outdir, exist_ok=True)

# Main plotting loop
for tr in st:
    try:
        station = tr.stats.station
        channel = tr.stats.channel[-1]
        data = tr.data
        delta = tr.stats.delta
        npts = tr.stats.npts
        times = np.arange(0, npts * delta, delta)
        starttime = tr.stats.starttime.datetime

        interval = 60 * 15
        segments = [int(i * interval / delta) for i in range(math.ceil(times[-1] / interval)
+ 1)]

        fig, ax = plt.subplots(figsize=(10, 8))
        scale = station_scale.get(station, 5000)

        for i in range(len(segments) - 1):
            seg_data = data[segments[i]:segments[i + 1]]
            seg_time = np.linspace(0, interval, len(seg_data))
            color = "red" if np.any(np.abs(seg_data / scale) > threshold_raw) else "black"
            ax.plot(seg_time, seg_data / scale + i, color=color, linewidth=0.5)

        # Axis configuration
        ax.set_ylim(len(segments) - 1, -0.5)
        ax.set_xlim(0, interval)
        ax.set_xticks(np.linspace(0, interval, 16))
        ax.set_xticklabels([str(int(x / 60)) for x in np.linspace(0, 15 * 60, 16)])
        ax.set_yticks(np.arange(0, len(segments) - 1, 4))
        yt_labels = [(starttime + timedelta(minutes=15 * i)).strftime("%H")
                     for i in range(0, len(segments) - 1, 4)]
        ax.set_yticklabels(yt_labels)
        ax.set_xlabel("Time (minutes)")
        ax.set_title(f"{tr.id}   {str(starttime)[:10]}")
        ax.set_facecolor("white")
        plt.tight_layout()

        outfile = f"{outdir}/helicorder_{station}_{datestr}0000_{channel}.png"
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        print(f"Saving {outfile}")
        plt.savefig(outfile, dpi=150)
        plt.close(fig)

    except Exception as e:
        print(f"Error plotting {tr.id}: {e}")
        continue

print("All helicorders saved successfully!")