#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from obspy import read
from datetime import datetime, timedelta, UTC
import glob
import os

yesterday = datetime.now(UTC) - timedelta(days=1)
year = yesterday.strftime("%Y")
datestr = yesterday.strftime("%Y%m%d")
julday = yesterday.strftime("%j")

pattern = f"/home/유저명/path_to_mseed_data/station.network.location.channel.{year}.{julday}"

files = glob.glob(pattern)
print(f"Found {len(files)} files for {year}.{julday}")
if not files:
    raise FileNotFoundError(f"No file matching pattern: {pattern}")

st = read(files[0])
for f in files[1:]:
    st += read(f)

st.detrend('demean')
st.detrend()
st.taper(0.0005, 'cosine')
st.filter('bandpass', freqmin=1, freqmax=20)

outdir = "/home/유저명/helicorder/plots"
os.makedirs(outdir, exist_ok=True)

for tr in st:
    data = tr.data
    npts = tr.stats.npts
    delta = tr.stats.delta
    times = np.arange(0, npts * delta, delta)
    starttime = tr.stats.starttime.datetime

    interval = 15 * 60
    segments = [int(i * interval / delta) for i in range(int(times[-1] // interval) + 1)]

    fig, ax = plt.subplots(figsize=(10, 8))
    scale = 10000
    threshold_raw = 50000

    for i in range(len(segments) - 1):
        seg_data = data[segments[i]:segments[i + 1]]
        seg_time = np.linspace(0, interval, len(seg_data))
        color = 'red' if np.any(np.abs(seg_data) > threshold_raw) else 'black'
        ax.plot(seg_time, seg_data / scale + i, color=color, linewidth=0.5)

    ax.set_ylim(len(segments) - 1, -0.5)
    ax.set_xlim(0, interval)
    ax.set_xticks(np.linspace(0, interval, 16))
    ax.set_xticklabels([str(int(x / 60)) for x in np.linspace(0, 15 * 60, 16)])
    ax.set_yticks(np.arange(0, len(segments) - 1, 4))
    yt_labels = [(starttime + timedelta(minutes=15 * i)).strftime('%H')
                 for i in range(0, len(segments) - 1, 4)]
    ax.set_yticklabels(yt_labels)
    ax.set_xlabel('Time in Minutes')
    ax.set_title(f'{tr.id}   {str(starttime)[:10]}')
    ax.set_facecolor('white')
    plt.tight_layout()

    station = tr.stats.station
    channel = tr.stats.channel[-1]
    outfile = f"{outdir}/helicorder_{station}_{datestr}0000_{channel}.png"
    print(f"Saving {outfile}")
    plt.savefig(outfile, dpi=150)
    plt.close(fig)

print("All custom dayplots saved successfully!")
