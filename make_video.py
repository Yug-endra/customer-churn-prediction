import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import imageio

OUT = r"D:\Internship\bubble_sort.mp4"

arr = [5, 3, 8, 1, 9, 2, 7, 4, 6]
n = len(arr)
a = list(arr)

# events: (snapshot, i, j, action, sorted_tail)
events = []
events.append((list(a), -1, -1, "start", 0))
for passk in range(n):
    swapped = False
    for i in range(n - passk - 1):
        events.append((list(a), i, i+1, "compare", passk))
        if a[i] > a[i+1]:
            a[i], a[i+1] = a[i+1], a[i]
            events.append((list(a), i, i+1, "swap", passk))
            swapped = True
    events.append((list(a), -1, -1, "pass_done", passk+1))
    if not swapped:
        # mark rest sorted
        break
events.append((list(a), -1, -1, "done", n))

FPS = 24
HOLD = {"start": 20, "compare": 7, "swap": 11, "pass_done": 14, "done": 36}

fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
fig.patch.set_facecolor("#0f172a")

def draw_frame(snap, i, j, action, tail):
    ax.clear()
    ax.set_facecolor("#0f172a")
    vals = snap
    m = len(vals)
    xs = np.arange(m)
    colors = []
    for idx in range(m):
        if idx >= m - tail:
            colors.append("#22c55e")
        else:
            colors.append("#3b82f6")
    if 0 <= i < m and action in ("compare", "swap"):
        colors[i] = "#facc15" if action == "compare" else "#ef4444"
    if 0 <= j < m and action in ("compare", "swap"):
        colors[j] = "#facc15" if action == "compare" else "#ef4444"
        if action == "swap":
            colors[i] = "#ef4444"
            colors[j] = "#ef4444"
    bars = ax.bar(xs, vals, color=colors, edgecolor="#1e293b", linewidth=1.2, width=0.7)
    for idx, v in enumerate(vals):
        ax.text(idx, v + 0.25, str(v), ha="center", va="bottom", color="white",
                fontsize=14, fontweight="bold")
    ax.set_ylim(0, max(arr) + 2)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("Bubble Sort — How it works", color="white", fontsize=22, fontweight="bold", pad=12)

    if action == "start":
        status = "Start: compare adjacent pairs; swap if left > right."
    elif action == "compare":
        status = f"Compare positions {i} & {j}:  {vals[i]} vs {vals[j]}"
    elif action == "swap":
        status = f"Swap! {vals[j]} <-> {vals[i]}  (out of order)"
    elif action == "pass_done":
        status = f"Pass done. Largest remaining bubbled to position {m-tail}."
    elif action == "done":
        status = "Fully sorted!"
    else:
        status = ""
    ax.text(0.5, -0.08, status, transform=ax.transAxes, ha="center", va="top",
            color="#94a3b8", fontsize=15)

    legend = [Patch(facecolor="#3b82f6", label="unsorted"),
              Patch(facecolor="#facc15", label="comparing"),
              Patch(facecolor="#ef4444", label="swapping"),
              Patch(facecolor="#22c55e", label="sorted")]
    ax.legend(handles=legend, loc="upper right", frameon=False, labelcolor="white", fontsize=11)

    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    return buf[:, :, :3].copy()

frames = []
for (snap, i, j, action, tail) in events:
    img = draw_frame(snap, i, j, action, tail if action!="start" else 0)
    for _ in range(HOLD[action]):
        frames.append(img)

writer = imageio.get_writer(OUT, fps=FPS, codec="libx264", quality=8, macro_block_size=16)
for f in frames:
    writer.append_data(f)
writer.close()
print("Wrote", OUT, "frames:", len(frames))
plt.close(fig)
