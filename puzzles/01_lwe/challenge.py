"""
Puzzle 1 — Small Secrets (LWE)

A "secure" LWE encryption scheme.
The flag is encrypted below. Can you recover it?

Flaw: deliberately introduced. Find it.
"""

import numpy as np
import json
import hashlib

# Parameters
N = 64        # dimension
Q = 3329      # modulus (Kyber's q — looks legit)
M = 200       # number of LWE samples

FLAG = b"FLAG{t00_sm4ll_s3cr3ts_sink_sh1ps}"


def keygen(n, q):
    # BUG: secret is drawn from {0,1} not Z_q
    # Real LWE requires s uniform in Z_q (or Gaussian)
    s = np.random.randint(0, 2, size=n)
    return s


def encrypt_lwe(s, n, q, m):
    A = np.random.randint(0, q, size=(m, n))
    e = np.round(np.random.normal(0, 1.0, size=m)).astype(int) % q
    b = (A @ s + e) % q
    return A.tolist(), b.tolist()


def encrypt_flag(s, q, flag):
    key = hashlib.sha256(s.tobytes()).digest()[:16]
    # XOR with key stream (naive)
    keystream = (key * (len(flag) // 16 + 1))[:len(flag)]
    ct = bytes(f ^ k for f, k in zip(flag, keystream))
    return ct.hex()


if __name__ == "__main__":
    np.random.seed(42)
    s = keygen(N, Q)
    A, b = encrypt_lwe(s, N, Q, M)
    flag_ct = encrypt_flag(s, Q, FLAG)

    out = {
        "n": N,
        "q": Q,
        "m": M,
        "A": A,
        "b": b,
        "flag_ciphertext": flag_ct,
        "note": "Recover s, then decrypt the flag."
    }
    with open("ciphertext.json", "w") as f:
        json.dump(out, f, indent=2)

    print("Ciphertext written to ciphertext.json")
    print(f"flag_ciphertext: {flag_ct}")
