"""
Puzzle 4 — Lazy Hashing (SPHINCS+ / WOTS+)

A simplified WOTS+ one-time signature scheme.
The same key pair is used to sign two different messages.

Flaw: deliberately introduced. Find it.
"""

import hashlib
import json
import os

FLAG = b"FLAG{0ne_t1me_means_ONE_t1me}"

# Winternitz parameter: each signature element covers log2(w) bits of message
W = 16       # Winternitz parameter (chain length)
N = 32       # hash output length in bytes
LOG_W = 4    # bits per message chunk (log2(16))
# For a 256-bit message hash, we need 64 message chunks + checksum chunks
CHUNKS = 64  # ceil(256 / log2(w)) = ceil(256/4)
CS_CHUNKS = 3  # checksum chunks (covers up to 64 * 15 = 960, needs 10 bits → 3 chunks)


def hash_n(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()[:N]


def chain(x: bytes, start: int, steps: int) -> bytes:
    """Apply hash `steps` times starting from position `start`."""
    val = x
    for i in range(start, start + steps):
        val = hash_n(val + i.to_bytes(1, 'big'))
    return val


def msg_to_digits(msg_hash: bytes) -> list:
    """Convert a 32-byte hash to base-W digits + checksum digits."""
    digits = []
    for byte in msg_hash:
        digits.append((byte >> 4) & 0xF)
        digits.append(byte & 0xF)
    # Checksum
    checksum = sum(W - 1 - d for d in digits)
    cs_digits = []
    for _ in range(CS_CHUNKS):
        cs_digits.append(checksum % W)
        checksum //= W
    return digits + cs_digits[::-1]


def keygen(seed: bytes):
    sk = [hash_n(seed + i.to_bytes(2, 'big')) for i in range(CHUNKS + CS_CHUNKS)]
    pk = [chain(sk[i], 0, W - 1) for i in range(len(sk))]
    return sk, pk


def sign(sk: list, message: bytes) -> list:
    msg_hash = hash_n(message)
    digits = msg_to_digits(msg_hash)
    sig = [chain(sk[i], 0, digits[i]) for i in range(len(sk))]
    return sig


def verify(pk: list, message: bytes, sig: list) -> bool:
    msg_hash = hash_n(message)
    digits = msg_to_digits(msg_hash)
    for i in range(len(pk)):
        candidate = chain(sig[i], digits[i], W - 1 - digits[i])
        if candidate != pk[i]:
            return False
    return True


def encrypt_flag(sk, flag):
    key = hashlib.sha256(b"".join(sk)).digest()[:16]
    ks = (key * (len(flag) // 16 + 1))[:len(flag)]
    return bytes(a ^ b for a, b in zip(flag, ks)).hex()


if __name__ == "__main__":
    seed = os.urandom(N)
    sk, pk = keygen(seed)

    # BUG: sign two different messages with the same one-time key pair
    msg1 = b"the weather today is quite nice"
    msg2 = b"please send 1000 dollars to alice"

    sig1 = sign(sk, msg1)
    sig2 = sign(sk, msg2)

    assert verify(pk, msg1, sig1)
    assert verify(pk, msg2, sig2)

    flag_ct = encrypt_flag(sk, FLAG)

    # Target: forge a signature for msg3 using sig1 and sig2
    msg_target = b"transfer all funds to attacker"

    out = {
        "W": W, "N": N, "CHUNKS": CHUNKS, "CS_CHUNKS": CS_CHUNKS,
        "pk": [x.hex() for x in pk],
        "msg1": msg1.hex(),
        "sig1": [x.hex() for x in sig1],
        "msg2": msg2.hex(),
        "sig2": [x.hex() for x in sig2],
        "msg_target": msg_target.hex(),
        "flag_ciphertext": flag_ct,
        "note": "Forge a valid signature for msg_target using sig1 and sig2."
    }
    with open("ciphertext.json", "w") as fout:
        json.dump(out, fout, indent=2)

    print("Ciphertext written to ciphertext.json")
    print(f"flag_ciphertext: {flag_ct}")
