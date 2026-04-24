"""
Puzzle 2 — Your solve script.
Load ciphertext.json and recover the flag.
"""

import json
import numpy as np
import hashlib

with open("ciphertext.json") as f:
    data = json.load(f)

N = data["N"]
p = data["p"]
q = data["q"]
h = np.array(data["h"])
e = np.array(data["e"])
flag_ct = bytes.fromhex(data["flag_ciphertext"])

# ----- YOUR ATTACK HERE -----
# The NTRU lattice has basis:
#   [ I  H ]
#   [ 0  qI ]
# where H is the circulant matrix of h.
# LLL reduction on this 2N x 2N lattice recovers (f, g) as a short vector.
# f has only 3 non-zero entries — the lattice reduction will be fast.

f_recovered = np.zeros(N, dtype=int)

# TODO: build the lattice, run LLL, extract f

# ----- DECRYPT FLAG -----
key = hashlib.sha256(f_recovered.astype(np.int64).tobytes()).digest()[:16]
keystream = (key * (len(flag_ct) // 16 + 1))[:len(flag_ct)]
flag = bytes(a ^ b for a, b in zip(flag_ct, keystream))
print(flag)
