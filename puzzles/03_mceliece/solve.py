"""
Puzzle 3 — Your solve script.
"""

import json
import hashlib

with open("ciphertext.json") as f:
    data = json.load(f)

k = data["k"]
n = data["n"]
t = data["t"]
G_pub = data["G_pub"]
c = data["ciphertext_bits"]
flag_ct = bytes.fromhex(data["flag_ciphertext"])

# ----- YOUR ATTACK HERE -----
# G_pub is in systematic form [I_k | P].
# The ciphertext c = m * G + e where e has weight t=4.
# Since the first k columns of G_pub form I_k, the first k bits of c are:
#   c[:k] = m + e[:k]
# With only t=4 errors spread over n=64 bits, try all C(64,4) = 635,376
# error patterns to find one that gives a valid codeword.

# Simple approach: the first k bits of c are m XOR (error bits in first k positions).
# With t=4 errors and k=32, most likely 0-2 errors land in the first 32 positions.
# Try all C(32,0)+C(32,1)+C(32,2) = 529 candidates for the message.

from itertools import combinations

G_pub = [list(row) for row in G_pub]
c = list(c)

def matvec_gf2(G, v):
    n = len(G[0])
    result = [0] * n
    for i, bit in enumerate(v):
        if bit:
            result = [(result[j] + G[i][j]) % 2 for j in range(n)]
    return result

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

message_bits = None
for num_errors_in_k in range(t + 1):
    for err_positions in combinations(range(k), num_errors_in_k):
        candidate = c[:k][:]
        for pos in err_positions:
            candidate[pos] ^= 1
        # Check: does candidate * G_pub match c with ≤ t errors total?
        encoded = matvec_gf2(G_pub, candidate)
        if hamming(encoded, c) <= t:
            message_bits = candidate
            break
    if message_bits:
        break

if message_bits:
    # Reconstruct G from message_bits to get the key
    # Key is derived from G (not G_pub — but G_pub IS G here since no scrambling)
    G = G_pub
    key = hashlib.sha256(bytes(
        sum(G[i][j] << (j % 8) for j in range(len(G[0]))) % 256
        for i in range(len(G))
    )).digest()[:16]
    ks = (key * (len(flag_ct) // 16 + 1))[:len(flag_ct)]
    flag = bytes(a ^ b for a, b in zip(flag_ct, ks))
    print(flag)
else:
    print("Attack failed — check your error enumeration.")
