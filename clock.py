import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from pytz import timezone

# Must be the first Streamlit command
st.set_page_config(page_title="Analog Clock", layout="centered")

# Auto-refresh every 1 second
st_autorefresh(interval=1000, key="clockrefresh")

def draw_clock():
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    # Clock face
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=4)
    ax.add_artist(circle)

    # Tick marks and numbers
    for i in range(12):
        angle = math.radians(i * 30)
        x_outer = math.sin(angle)
        y_outer = math.cos(angle)
        x_inner = 0.9 * math.sin(angle)
        y_inner = 0.9 * math.cos(angle)
        ax.plot([x_inner, x_outer], [y_inner, y_outer], 'k', lw=2)

        # Numbers
        num_x = 0.75 * math.sin(angle)
        num_y = 0.75 * math.cos(angle)
        ax.text(num_x, num_y, str(i if i != 0 else 12), fontsize=14, ha='center', va='center')

    # Get local time
    local_tz = timezone("Asia/Kolkata")  # Change this to your local timezone if needed
    now = datetime.now(local_tz)
    second = now.second
    minute = now.minute
    hour = now.hour % 12

    # Angles
    sec_angle = math.radians(second * 6)
    min_angle = math.radians(minute * 6 + second * 0.1)
    hour_angle = math.radians(hour * 30 + minute * 0.5)

    # Reverse angle for clockwise rotation
    def hand_coords(length, angle):
        x = length * math.sin(angle)
        y = length * math.cos(angle)
        return [0, x], [0, y]

    # Draw hands
    ax.plot(*hand_coords(0.5, hour_angle), color='black', lw=6)
    ax.plot(*hand_coords(0.7, min_angle), color='blue', lw=4)
    ax.plot(*hand_coords(0.9, sec_angle), color='red', lw=2)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    return fig, now

st.title("Parithi Clock")
fig, current_time = draw_clock()
st.pyplot(fig)

# Digital time display
st.markdown(f"## 🕒 {current_time.strftime('%H:%M:%S')}")
