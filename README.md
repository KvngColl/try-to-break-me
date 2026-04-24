# try-to-break-me

> Cryptographic puzzles based on the hardest encryption problems known to mathematics.  
> Each one is intentionally implemented with a subtle flaw. Find it. Break it.

---

## Background

These puzzles are grounded in the five families of encryption that have survived the most intense academic scrutiny — including NIST's post-quantum standardisation process. Breaking any of them (for real) would be a landmark result in cryptography.

Each puzzle here is **not** a secure implementation. There is a deliberate weakness hidden inside. Your job is to find it and recover the plaintext flag.

---

## The Puzzles

| # | Name | Family | Hardness Assumption | Difficulty |
|---|------|--------|---------------------|------------|
| 1 | [Small Secrets](puzzles/01_lwe/) | Lattice (LWE) | Learning With Errors | ⭐⭐ |
| 2 | [Tiny Keys](puzzles/02_ntru/) | Lattice (NTRU) | NTRU Problem | ⭐⭐⭐ |
| 3 | [Broken Goppa](puzzles/03_mceliece/) | Code-based | Syndrome Decoding | ⭐⭐⭐ |
| 4 | [Lazy Hashing](puzzles/04_sphincs/) | Hash-based | Second-preimage resistance | ⭐⭐ |
| 5 | [Slow Locker](puzzles/05_timelock/) | Time-lock | Sequential squaring (RSA) | ⭐⭐⭐⭐ |

---

## How to Play

1. Read the puzzle's `README.md` for background on the encryption scheme and the challenge description.
2. Read `challenge.py` — this is the flawed implementation that encrypted the flag.
3. Write your attack in `solve.py`.
4. Recover the flag in the format `FLAG{...}`.

```bash
pip install -r requirements.txt
cd puzzles/01_lwe
python challenge.py   # see the ciphertext
python solve.py       # write your attack here
```

---

## Research Foundations

These puzzles draw from:

- **LWE / Ring-LWE** — Regev (2005), Lyubashevsky et al. (2010). Worst-case hardness reduces to SVP in lattices (NP-hard).
- **NTRU** — Hoffstein, Pipher, Silverman (1998). 25+ years unbroken under correct parameters.
- **McEliece / Code-based** — McEliece (1978). The oldest post-quantum proposal still standing.
- **SPHINCS+ / SLH-DSA** — Bernstein et al. Security relies only on hash function properties. NIST FIPS 205.
- **Time-lock puzzles** — Rivest, Shamir, Wagner (1996). Inherently sequential computation.

NIST finalized ML-KEM, ML-DSA, and SLH-DSA as post-quantum standards in August 2024.

---

## Rules

- No bruteforce attacks on the flag format itself.
- The flaw is in the *implementation*, not the underlying math.
- Hints are in each puzzle's `README.md` (collapsed by default).
- Solutions live on the `solutions` branch — don't peek until you've tried.

---

## Contributing

Found a bug? Want to add a puzzle? Open a PR.  
New puzzles should follow the same format: real hardness assumption, one subtle implementation flaw, recoverable flag.
