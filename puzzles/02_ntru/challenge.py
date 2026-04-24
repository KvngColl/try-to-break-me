"""
Puzzle 2 — Tiny Keys (NTRU)

NTRU-based encryption with a deliberately sparse private key.
Flaw: find it.
"""

import json
import hashlib
import random

FLAG = b"FLAG{sp4rs3_k3ys_sp34k_v0lum3s}"

# Parameters: N prime, q prime — ensures x^N - 1 factors and inversions exist
N = 53
P_MOD = 3
Q = 127


def polymul(a, b, n, mod):
    r = [0] * n
    for i in range(n):
        if a[i] == 0:
            continue
        for j in range(n):
            r[(i + j) % n] = (r[(i + j) % n] + a[i] * b[j]) % mod
    return r


def polyadd(a, b, n, mod):
    return [(a[i] + b[i]) % mod for i in range(n)]


def polyinv(f, n, mod):
    """Inverse of f mod (x^n - 1) over Z/mod via extended Euclidean on polynomials."""
    # Represent x^n - 1
    xn_minus_1 = [-1] + [0] * (n - 1) + [1]  # coefficients of x^n - 1 (low to high)

    def poly_mod(a, b):
        """Reduce polynomial a mod polynomial b over Z/mod (low-to-high indexing)."""
        a = list(a)
        db = len(b) - 1
        while len(a) - 1 >= db:
            if a[-1] % mod == 0:
                a.pop()
                continue
            try:
                coeff = a[-1] * pow(b[-1], -1, mod) % mod
            except ValueError:
                return None
            deg_diff = len(a) - 1 - db
            for i in range(len(b)):
                a[deg_diff + i] = (a[deg_diff + i] - coeff * b[i]) % mod
            while a and a[-1] % mod == 0:
                a.pop()
        return a or [0]

    def poly_xgcd(a, b):
        """Extended GCD of polynomials over Z/mod."""
        old_r, r = list(a), list(b)
        old_s, s = [1], [0]
        old_t, t = [0], [1]

        for _ in range(200):
            if not any(x % mod for x in r):
                break
            dr = len(r) - 1
            while dr > 0 and r[dr] % mod == 0:
                dr -= 1
            if dr == 0 and r[0] % mod == 0:
                break

            q_poly, _ = _poly_divmod(old_r, r, mod)
            old_r, r = r, poly_sub(old_r, polymul_dense(q_poly, r, mod), mod)
            old_s, s = s, poly_sub(old_s, polymul_dense(q_poly, s, mod), mod)
            old_t, t = t, poly_sub(old_t, polymul_dense(q_poly, t, mod), mod)

        return old_r, old_s, old_t

    # Simpler: circulant matrix inverse via Fermat (only works when mod is prime)
    # Build circulant and invert over Z/mod
    mat = [[f[(j - i) % n] % mod for j in range(n)] for i in range(n)]
    aug = [mat[i] + [1 if i == j else 0 for j in range(n)] for i in range(n)]

    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col] % mod != 0), None)
        if pivot is None:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        inv_p = pow(aug[col][col] % mod, mod - 2, mod)  # Fermat (mod prime)
        aug[col] = [x * inv_p % mod for x in aug[col]]
        for row in range(n):
            if row != col and aug[row][col] % mod != 0:
                fac = aug[row][col] % mod
                aug[row] = [(aug[row][k] - fac * aug[col][k]) % mod for k in range(2 * n)]

    return [aug[i][n + i] % mod for i in range(n)]


def keygen(n, p, q, seed=42):
    rng = random.Random(seed)

    # BUG: df=3 instead of df≈n//3=17. Extremely sparse private key.
    df = 3   # should be ~17 for N=53
    positions = rng.sample(range(n), df * 2)
    f = [0] * n
    for pos in positions[:df]:
        f[pos] = 1
    for pos in positions[df:]:
        f[pos] = -1
    f[0] = (f[0] + 1) % 3 if f[0] != 2 else 1  # standard +1 tweak

    fq = polyinv(f, n, q)
    if fq is None:
        return keygen(n, p, q, seed + 1)

    dg = n // 3
    g_pos = rng.sample(range(n), dg * 2)
    g = [0] * n
    for pos in g_pos[:dg]:
        g[pos] = 1
    for pos in g_pos[dg:]:
        g[pos] = -1

    pg = [p * x % q for x in g]
    h = polymul(pg, fq, n, q)
    return f, g, h


def encrypt_flag(f, flag):
    key = hashlib.sha256(bytes(x % 256 for x in f)).digest()[:16]
    ks = (key * (len(flag) // 16 + 1))[:len(flag)]
    return bytes(a ^ b for a, b in zip(flag, ks)).hex()


if __name__ == "__main__":
    f, g, h = keygen(N, P_MOD, Q)
    flag_ct = encrypt_flag(f, FLAG)

    out = {
        "N": N, "p": P_MOD, "q": Q,
        "h": h,
        "flag_ciphertext": flag_ct,
        "note": "Recover f using the NTRU lattice. f is unusually sparse."
    }
    with open("ciphertext.json", "w") as fout:
        json.dump(out, fout, indent=2)

    print("Ciphertext written to ciphertext.json")
    print(f"flag_ciphertext: {flag_ct}")
