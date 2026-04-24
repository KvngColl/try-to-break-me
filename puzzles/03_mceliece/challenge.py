"""
Puzzle 3 — Broken Goppa (McEliece)

A code-based encryption scheme.
The generator matrix is not properly scrambled.

Flaw: deliberately introduced. Find it.
"""

import numpy as np
import json
import hashlib
import random

FLAG = b"FLAG{unscr4mbled_c0des_c4n7_h1d3}"

# Parameters: [n, k, t] linear code
# Real McEliece uses Goppa codes with n=1024, k=524, t=50
# We use a small binary linear code for the puzzle
K = 32   # message length (bits)
N = 64   # codeword length (bits)
T = 4    # error-correction capacity (errors added during encryption)


def random_binary_matrix(rows, cols, rng):
    return [[rng.randint(0, 1) for _ in range(cols)] for _ in range(rows)]


def matmul_gf2(A, B):
    """Matrix multiply over GF(2)."""
    rows_a, cols_a = len(A), len(A[0])
    rows_b, cols_b = len(B), len(B[0])
    assert cols_a == rows_b
    C = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(cols_a)) % 2
    return C


def matvec_gf2(G, v):
    """Multiply matrix G (k x n) by row vector v (length k) over GF(2)."""
    n = len(G[0])
    result = [0] * n
    for i, bit in enumerate(v):
        if bit:
            result = [(result[j] + G[i][j]) % 2 for j in range(n)]
    return result


def keygen(k, n, seed=42):
    rng = random.Random(seed)

    # Build systematic generator matrix G = [I_k | P] over GF(2)
    # This is a valid generator matrix for a [n, k] linear code
    identity = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
    P = random_binary_matrix(k, n - k, rng)
    G = [identity[i] + P[i] for i in range(k)]

    # BUG: real McEliece applies G_pub = S * G * Perm where S is a random
    # invertible k×k matrix and Perm is a random n×n permutation matrix.
    # Here we skip that step entirely — G_pub = G is unscrambled.
    G_pub = G  # should be S * G * Perm

    return G, G_pub


def encrypt(G_pub, message_bits, n, t, seed=99):
    rng = random.Random(seed)
    c = matvec_gf2(G_pub, message_bits)
    # Add t random errors
    error_positions = rng.sample(range(n), t)
    for pos in error_positions:
        c[pos] ^= 1
    return c


def flag_to_bits(flag):
    bits = []
    for byte in flag:
        for bit_idx in range(7, -1, -1):
            bits.append((byte >> bit_idx) & 1)
    return bits


def encrypt_flag(G, flag):
    key = hashlib.sha256(bytes(
        sum(G[i][j] << (j % 8) for j in range(len(G[0]))) % 256
        for i in range(len(G))
    )).digest()[:16]
    ks = (key * (len(flag) // 16 + 1))[:len(flag)]
    return bytes(a ^ b for a, b in zip(flag, ks)).hex()


if __name__ == "__main__":
    G, G_pub = keygen(K, N)

    # Encrypt first K bits of flag as the "message"
    flag_bits = flag_to_bits(FLAG)[:K]
    c = encrypt(G_pub, flag_bits, N, T)

    flag_ct = encrypt_flag(G, FLAG)

    out = {
        "k": K, "n": N, "t": T,
        "G_pub": G_pub,
        "ciphertext_bits": c,
        "flag_ciphertext": flag_ct,
        "note": "G_pub is the unscrambled generator matrix. Exploit its systematic form."
    }
    with open("ciphertext.json", "w") as fout:
        json.dump(out, fout, indent=2)

    print("Ciphertext written to ciphertext.json")
    print(f"flag_ciphertext: {flag_ct}")
