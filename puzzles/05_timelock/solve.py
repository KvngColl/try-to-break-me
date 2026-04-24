"""
Puzzle 5 — Your solve script.
Factor N using Fermat factorization, then unlock the time-lock instantly.
"""

import json
import math

with open("ciphertext.json") as f:
    data = json.load(f)

N = data["N"]
T = data["T"]
C = data["C"]

# ----- YOUR ATTACK HERE -----
# Fermat factorization: N = a^2 - b^2 = (a+b)(a-b)
# Start at a = ceil(sqrt(N)) and increment until a^2 - N is a perfect square.

def isqrt(n):
    import math
    return math.isqrt(n)

p, q = None, None
a = isqrt(N)
if a * a < N:
    a += 1

for _ in range(100000):
    b2 = a * a - N
    b = isqrt(b2)
    if b * b == b2:
        p = a + b
        q = a - b
        break
    a += 1

if p and q and p * q == N:
    print(f"Factored! p = {p}")
    print(f"          q = {q}")
    phi = (p - 1) * (q - 1)
    e = pow(2, T, phi)
    mask = pow(2, e, N)
    flag_int = (C - mask) % N
    flag = flag_int.to_bytes((flag_int.bit_length() + 7) // 8, 'big')
    print(f"Flag: {flag.decode()}")
else:
    print("Fermat factorization failed — try a wider search range.")
