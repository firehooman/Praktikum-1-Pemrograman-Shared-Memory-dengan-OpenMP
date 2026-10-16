/* matmul.c - kerangka Praktikum 1 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

static void isi_acak(double *m, int n, unsigned seed) {
    srand(seed);
    for (long i = 0; i < (long)n * n; i++) m[i] = (double)rand() / RAND_MAX;
}

/* Versi serial: acuan kebenaran dan waktu. Jangan diubah. */
static void matmul_serial(const double *A, const double *B, double *C, int n) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            double s = 0.0;
            for (int k = 0; k < n; k++) s += A[(long)i * n + k] * B[(long)k * n + j];
            C[(long)i * n + j] = s;
        }
}

static void matmul_paralel(const double *A, const double *B, double *C, int n) {
    #pragma omp parallel for
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            double s = 0.0;
            for (int k = 0; k < n; k++) s += A[(long)i * n + k] * B[(long)k * n + j];
            C[(long)i * n + j] = s;
        }
}

static int sama(const double *X, const double *Y, long len, double tol) {
    for (long i = 0; i < len; i++) {
        double skala = fabs(Y[i]) > 1.0 ? fabs(Y[i]) : 1.0;
        if (fabs(X[i] - Y[i]) > tol * skala) return 0;
    }
    return 1;
}

int main(int argc, char **argv) {
    int n = (argc > 1) ? atoi(argv[1]) : 1024;
    long len = (long)n * n;
    double *A = malloc(len * sizeof(double)), *B = malloc(len * sizeof(double));
    double *Cs = malloc(len * sizeof(double)), *Cp = malloc(len * sizeof(double));
    isi_acak(A, n, 1);
    isi_acak(B, n, 2);
    double t0 = omp_get_wtime();
    matmul_serial(A, B, Cs, n);
    double t1 = omp_get_wtime();
    matmul_paralel(A, B, Cp, n);
    double t2 = omp_get_wtime();
    printf("n=%d thread=%d serial=%.3f paralel=%.3f benar=%s\n",
           n, omp_get_max_threads(), t1 - t0, t2 - t1,
           sama(Cp, Cs, len, 1e-9) ? "ya" : "TIDAK");
    free(A); free(B); free(Cs); free(Cp);
    return 0;
}
