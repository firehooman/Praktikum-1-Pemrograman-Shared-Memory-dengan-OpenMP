# Praktikum 1 - Pemrograman Shared Memory dengan OpenMP

Kode asesmen A05. Berisi paralelisasi perkalian matriks (`matmul.c`) dan
penghitungan bilangan prima dengan eksperimen scheduling (`prima.c`).

## Struktur folder

```
p1-openmp/
├── README.md
├── src/
│   ├── matmul.c      # perkalian matriks, serial vs paralel
│   ├── prima.c       # hitung prima 2..10^7, reduction + schedule(runtime)
│   └── grafik.py     # olah hasil mentah jadi tabel dan grafik
└── hasil/
    ├── matmul.txt    # keluaran mentah 4 jumlah thread x 3 ulangan
    ├── prima.txt     # keluaran mentah 3 kebijakan x 4 thread x 3 ulangan
    ├── grafik_speedup_matmul.png
    └── grafik_scheduling_8thread.png
```

## Kebutuhan

- GCC dengan dukungan OpenMP (`gcc -fopenmp`)
- Python 3 dengan matplotlib (hanya untuk `grafik.py`)
- Diuji di Ubuntu 24.04 (WSL), GCC 13.3.0, Intel Core i5-6200U (2 core fisik, 4 core logis)

## Kompilasi

```bash
gcc -O2 -fopenmp src/matmul.c -o matmul -lm
gcc -O2 -fopenmp src/prima.c -o prima
```

## Menjalankan

Perkalian matriks (argumen = ukuran matriks n, bawaan 1024):

```bash
OMP_NUM_THREADS=4 ./matmul 1024
```

Keluaran: `n=... thread=... serial=... paralel=... benar=ya`.
`benar=ya` berarti hasil paralel sama dengan hasil serial.

Bilangan prima (kebijakan scheduling diatur lewat `OMP_SCHEDULE`):

```bash
OMP_SCHEDULE="static" OMP_NUM_THREADS=4 ./prima
OMP_SCHEDULE="dynamic,1000" OMP_NUM_THREADS=4 ./prima
OMP_SCHEDULE="guided" OMP_NUM_THREADS=4 ./prima
```

Hasil yang benar selalu `prima=664579`.

## Mengulang eksperimen

```bash
for t in 1 2 4 8; do
  for r in 1 2 3; do
    OMP_NUM_THREADS=$t ./matmul 1024 >> hasil/matmul.txt
  done
done

for s in "static" "dynamic,1000" "guided"; do
  for t in 1 2 4 8; do
    for r in 1 2 3; do
      echo -n "$s;$t;$r;" >> hasil/prima.txt
      OMP_SCHEDULE="$s" OMP_NUM_THREADS=$t ./prima >> hasil/prima.txt
    done
  done
done
```

## Membuat tabel dan grafik

```bash
python3 src/grafik.py
```

Mencetak Tabel 2 dan Tabel 3 (median) dan menyimpan dua grafik PNG ke `hasil/`.

## Catatan

- Variabel `jumlah` di `prima.c` memakai `reduction(+:jumlah)`. Tanpa klausa ini
  hasilnya salah karena race condition.
- Waktu diukur dengan `omp_get_wtime()`; tabel memakai median dari 3 pengulangan.
