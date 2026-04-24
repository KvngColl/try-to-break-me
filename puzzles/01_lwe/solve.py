"""
Puzzle 1 — Your solve script.
Load ciphertext.json and recover the flag.
"""

import json
import numpy as np
import hashlib

with open("ciphertext.json") as f:
    data = json.load(f)

n = data["n"]
q = data["q"]
A = np.array(data["A"])
b = np.array(data["b"])
flag_ct = bytes.fromhex(data["flag_ciphertext"])

# ----- YOUR ATTACK HERE -----
# Hint: the secret s has entries in {0, 1}.
# For each coordinate j, consider: b_i - A[i,j]*s[j] ≈ <A[i, -j], s[-j]> + e_i
# With M samples you can distinguish s[j]=0 vs s[j]=1.

s_recovered = np.zeros(n, dtype=int)

# TODO: fill in s_recovered

# ----- DECRYPT FLAG -----
key = hashlib.sha256(s_recovered.astype(np.uint8).tobytes()).digest()[:16]
keystream = (key * (len(flag_ct) // 16 + 1))[:len(flag_ct)]
flag = bytes(f ^ k for f, k in zip(flag_ct, keystream))
print(flag)
