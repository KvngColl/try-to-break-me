"""
Puzzle 5 — Slow Locker (Time-Lock Puzzle)

RSA-based time-lock puzzle.
Without the factorization, solving requires T sequential squarings.
With it — instant.

Flaw: deliberately introduced. Find it.
"""

import json
import math
import hashlib
import random

FLAG = b"FLAG{f3rm4t_f4ct0rs_f4st_pr1m3s}"

# BUG: p and q are chosen to be very close together (differ by < 1000).
# Real RSA requires p and q to be randomly chosen, far apart.
# When |p - q| is small, Fermat factorization trivially recovers them.

def next_prime(n):
    """Find the next prime >= n (Miller-Rabin)."""
    if n < 2:
        return 2
    candidate = n if n % 2 != 0 else n + 1
    while not is_prime(candidate):
        candidate += 2
    return candidate


def is_prime(n, k=20):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    rng = random.Random(n)  # deterministic for reproducibility
    for _ in range(k):
        a = rng.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_close_primes(bits=256, seed=1337):
    """Generate two primes p, q close together (within 1000)."""
    rng = random.Random(seed)
    base = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
    p = next_prime(base)
    q = next_prime(p + rng.randint(2, 999))  # BUG: q ≈ p
    return p, q


if __name__ == "__main__":
    p, q = gen_close_primes(bits=256)
    N = p * q
    phi = (p - 1) * (q - 1)

    # Time parameter: T squarings would take ~years on modern hardware
    T = 10**9

    # Secret = flag interpreted as integer
    flag_int = int.from_bytes(FLAG, 'big')

    # Compute the time-lock mask: 2^(2^T) mod N
    # (We use phi shortcut since we know p, q)
    e = pow(2, T, phi)
    mask = pow(2, e, N)

    # Puzzle ciphertext
    C = (flag_int + mask) % N

    out = {
        "N": N,
        "T": T,
        "C": C,
        "note": "C = flag_int + 2^(2^T) mod N. Factor N to solve instantly."
    }
    with open("ciphertext.json", "w") as fout:
        json.dump(out, fout, indent=2)

    print("Ciphertext written to ciphertext.json")
    print(f"N  = {N}")
    print(f"C  = {C}")
    print(f"T  = {T}")
