/* prima.c - kerangka Praktikum 1 */
#include <stdio.h>
#include <omp.h>

static int is_prima(long x) {
    if (x < 2) return 0;
    for (long d = 2; d * d <= x; d++)
        if (x % d == 0) return 0;
    return 1;
}

int main(void) {
    const long N = 10000000; /* 10^7 */
    long jumlah = 0;
    double t0 = omp_get_wtime();

    #pragma omp parallel for reduction(+:jumlah) schedule(runtime)
    for (long x = 2; x <= N; x++)
        jumlah += is_prima(x);

    double t1 = omp_get_wtime();
    printf("N=%ld prima=%ld waktu=%.3f\n", N, jumlah, t1 - t0);
    return 0;
}
