# grafik.py - olah hasil Praktikum 1 OpenMP
# Lokasi: p1-openmp/src/grafik.py
import os
import re
import statistics

import matplotlib
matplotlib.use("Agg")  # tanpa jendela, langsung simpan ke file
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HASIL = os.path.join(BASE, "hasil")


def med(xs):
    return statistics.median(xs)


# ---------- Bagian A: perkalian matriks ----------
serial = {}   # thread -> list waktu serial
paralel = {}  # thread -> list waktu paralel
benar_a = {}  # thread -> semua benar?

pola_a = re.compile(r"thread=(\d+) serial=([\d.]+) paralel=([\d.]+) benar=(\w+)")
with open(os.path.join(HASIL, "matmul.txt")) as f:
    for baris in f:
        m = pola_a.search(baris)
        if not m:
            continue
        t = int(m.group(1))
        serial.setdefault(t, []).append(float(m.group(2)))
        paralel.setdefault(t, []).append(float(m.group(3)))
        benar_a[t] = benar_a.get(t, True) and (m.group(4) == "ya")

threads = sorted(serial)
speedup = []

print("=== TABEL 2: Perkalian matriks (median) ===")
print(f"{'Thread':>6} {'Serial':>9} {'Paralel':>9} {'Speedup':>8} {'Efisiensi':>10} {'Benar?':>7}")
for t in threads:
    s, p = med(serial[t]), med(paralel[t])
    sp = s / p
    speedup.append(sp)
    print(f"{t:>6} {s:>9.3f} {p:>9.3f} {sp:>8.3f} {sp / t:>10.3f} {'ya' if benar_a[t] else 'TIDAK':>7}")

# ---------- Bagian B: bilangan prima ----------
waktu = {}   # (kebijakan, thread) -> list waktu
benar_b = {}  # (kebijakan, thread) -> semua 664579?
urutan = []   # urutan kebijakan sesuai kemunculan

pola_b = re.compile(r"^([^;]+);(\d+);(\d+);.*prima=(\d+) waktu=([\d.]+)")
with open(os.path.join(HASIL, "prima.txt")) as f:
    for baris in f:
        m = pola_b.search(baris.strip())
        if not m:
            continue
        k, t = m.group(1), int(m.group(2))
        if k not in urutan:
            urutan.append(k)
        waktu.setdefault((k, t), []).append(float(m.group(5)))
        benar_b[(k, t)] = benar_b.get((k, t), True) and (int(m.group(4)) == 664579)

tb = sorted({t for (_, t) in waktu})
print("\n=== TABEL 3: Bilangan prima (median detik) ===")
print(f"{'Kebijakan':<14}" + "".join(f"{str(t) + ' thr':>10}" for t in tb) + f"{'Speedup 8':>11} {'664579?':>8}")
waktu8 = {}
for k in urutan:
    med_t = {t: med(waktu[(k, t)]) for t in tb}
    waktu8[k] = med_t[8]
    sp8 = med_t[1] / med_t[8]
    ok = all(benar_b[(k, t)] for t in tb)
    print(f"{k:<14}" + "".join(f"{med_t[t]:>10.3f}" for t in tb) + f"{sp8:>11.2f} {'ya' if ok else 'TIDAK':>8}")

# ---------- Grafik 1: speedup matmul + garis ideal ----------
plt.figure(figsize=(6, 4.5))
plt.plot(threads, speedup, "o-", label="Speedup terukur")
plt.plot(threads, threads, "--", color="gray", label="Ideal (speedup = jumlah thread)")
for t, sp in zip(threads, speedup):
    plt.annotate(f"{sp:.2f}", (t, sp), textcoords="offset points", xytext=(0, 8), ha="center")
plt.xlabel("Jumlah thread")
plt.ylabel("Speedup")
plt.title("Speedup perkalian matriks terhadap jumlah thread")
plt.xticks(threads)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(HASIL, "grafik_speedup_matmul.png"), dpi=200)
plt.close()

# ---------- Grafik 2: batang waktu 8 thread per kebijakan ----------
plt.figure(figsize=(6, 4.5))
batang = plt.bar(urutan, [waktu8[k] for k in urutan], color=["#4C78A8", "#F58518", "#54A24B"][:len(urutan)])
for b in batang:
    plt.text(b.get_x() + b.get_width() / 2, b.get_height(), f"{b.get_height():.2f}",
             ha="center", va="bottom")
plt.xlabel("Kebijakan scheduling")
plt.ylabel("Waktu (detik)")
plt.title("Waktu bilangan prima dengan 8 thread")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(HASIL, "grafik_scheduling_8thread.png"), dpi=200)
plt.close()

print("\nGrafik tersimpan di folder hasil/:")
print("  grafik_speedup_matmul.png")
print("  grafik_scheduling_8thread.png")
