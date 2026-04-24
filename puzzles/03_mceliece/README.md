# Puzzle 3 — Broken Goppa (McEliece)

## The Math

**McEliece (1978)** is the oldest post-quantum proposal still standing after 45+ years of cryptanalysis.

It uses **error-correcting codes** as the trap. The public key is a disguised generator matrix `G_pub` of a **Goppa code**. Encryption adds a random error vector `e` of weight `t`:

```
c = m * G_pub + e
```

Decryption uses the secret structure of the code (the Goppa polynomial) to efficiently correct the `t` errors and recover `m`.

**Security:** Recovering `m` from `c` without knowing the code structure is an instance of the **Syndrome Decoding Problem**, which is NP-complete. No quantum speedup changes this — Grover's algorithm only gives a square-root improvement, which is absorbed by doubling parameters.

NIST selected **HQC** (a code-based scheme) as its fourth post-quantum standard in March 2025.

**Reference:** McEliece, R.J. (1978). "A Public-Key Cryptosystem Based On Algebraic Coding Theory." JPL DSN Progress Report.

---

## The Challenge

A McEliece-inspired scheme was used to encrypt the flag. The public generator matrix and ciphertext are in `ciphertext.json`.

The implementation has a structural flaw that makes the code trivially identifiable.

**Recover the flag.**

---

## Hints

<details>
<summary>Hint 1 (mild)</summary>
Real McEliece scrambles the generator matrix with a random invertible matrix S and a permutation matrix P to hide the code's structure. What if those weren't applied?
</details>

<details>
<summary>Hint 2 (moderate)</summary>
Look at the structure of the public generator matrix. A systematic code has identity as its first k columns. If the scrambling was skipped, `G_pub = G` directly — and decoding becomes trivial.
</details>

<details>
<summary>Hint 3 (strong)</summary>
The matrix is in systematic form `[I | P]`. The ciphertext is `c = m * G + e`. Since `e` is small, round `c * G^T * (G * G^T)^{-1}` to recover `m` — or just read off the first `k` bits after error correction via majority-vote on the redundant positions.
</details>

---

## Format

Flag: `FLAG{...}`  
Submit your solution in `solve.py`.
