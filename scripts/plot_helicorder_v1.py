#!/usr/bin/env python
from obspy import read
import numpy as np
import matplotlib.pyplot as plt
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

os.makedirs("/home/유저명/helicorder/plots", exist_ok=True)

for tr in st:
    station = tr.stats.station
    channel = tr.stats.channel[-1]
    outfile = f"/home/유저명/helicorder/plots/helicorder_{station}_{datestr}0000_{channel}.png"
    print(f"Saving {outfile}")
    tr.plot(
        type='dayplot',
        linewidth=0.5,
        show_y_UTC_label=False,
        x_labels_size=10,
        y_labels_size=9,
        vertical_scaling_range=10000,
        color=['k', 'r', 'b', 'g'],
        title=f'{tr.id}   {str(tr.stats.starttime)[:10]}',
        outfile=outfile
    )

print("All dayplots saved successfully!")