# Puzzle 4 — Lazy Hashing (SPHINCS+)

## The Math

**SPHINCS+** (now NIST FIPS 205 as **SLH-DSA**) is a stateless hash-based signature scheme. Its security rests on just two assumptions:

1. **Second-preimage resistance** of the underlying hash function
2. **Pseudorandomness** of the PRF used to generate one-time keys

It combines:
- **WOTS+** (Winternitz One-Time Signatures) — signs one message per key pair
- **XMSS trees** — Merkle trees of WOTS+ public keys
- **HT (Hypertree)** — a tree-of-trees structure for the full key hierarchy

The entire structure only needs the hash function to be secure — no number theory, no lattices.

**Reference:** Bernstein et al. (2019). "SPHINCS+: Submission to the NIST Post-Quantum Project." [https://sphincs.org/data/sphincs+-r3.1-specification.pdf](https://sphincs.org/data/sphincs+-r3.1-specification.pdf)

---

## The Challenge

A simplified WOTS+ (Winternitz One-Time Signature) is used to sign and authenticate the flag. The verification data is in `ciphertext.json`.

The implementation reuses the same one-time key pair to sign two different messages. This is catastrophic for WOTS+.

**Forge a valid signature for the target message and recover the flag.**

---

## Hints

<details>
<summary>Hint 1 (mild)</summary>
WOTS+ signs a message by applying a hash chain to each key segment. The direction depends on the message digit. What happens if you see two signatures for two different messages?
</details>

<details>
<summary>Hint 2 (moderate)</summary>
In WOTS+, signing `m` produces `sig` where `sig[i] = hash^(w-1-m[i])(sk[i])`. If you have `sig1` for `m1` and `sig2` for `m2`, and `m1[i] < m2[i]`, you can advance `sig1[i]` forward in the chain to get the correct value for a message with digit `m2[i]`.
</details>

<details>
<summary>Hint 3 (strong)</summary>
Given two (message, signature) pairs signed with the same WOTS+ key, you can construct a valid signature for any message `m_target` where `m_target[i] >= min(m1[i], m2[i])` for all `i`. Apply hash chains forward from whichever signature gives a lower chain position.
</details>

---

## Format

Flag: `FLAG{...}`  
Submit your solution in `solve.py`.
