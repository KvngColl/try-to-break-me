# Puzzle 5 — Slow Locker (Time-Lock Puzzle)

## The Math

**Time-lock puzzles** (Rivest, Shamir, Wagner, 1996) are designed so that the solution requires a minimum amount of *sequential* computation — no parallelism helps.

The construction uses RSA:

```
Generate N = p*q (RSA modulus)
Pick a secret s
Compute: C = s + 2^(2^T) mod N
```

The solver must compute `2^(2^T) mod N` by performing `T` sequential squarings modulo `N`. No shortcut exists *without knowing the factorization* of `N` — because `φ(N) = (p-1)(q-1)` is needed to reduce the exponent.

**If you know p and q**, you can compute `e = 2^T mod φ(N)` in O(T) time, then `2^e mod N` instantly.

**Reference:** Rivest, R., Shamir, A., Wagner, D. (1996). "Time-lock puzzles and timed-release crypto." MIT/LCS/TR-684.

---

## The Challenge

A time-lock puzzle was used to seal the flag. `T` was chosen to require an estimated 10^9 sequential squarings — years of work without the factorization.

But `N` was generated carelessly.

The puzzle data is in `ciphertext.json`.

**Factor N. Recover the flag.**

---

## Hints

<details>
<summary>Hint 1 (mild)</summary>
Check the size of N. A real RSA modulus should be 2048 bits or more. How many bits is this one?
</details>

<details>
<summary>Hint 2 (moderate)</summary>
Try Fermat factorization: if `p` and `q` are close together (both near √N), then `N = ((p+q)/2)^2 - ((p-q)/2)^2`. Start from `ceil(√N)` and search upward.
</details>

<details>
<summary>Hint 3 (strong)</summary>
`p` and `q` differ by less than 1000. Fermat factorization finds them in under 1000 iterations. Once you have `p` and `q`, compute `phi = (p-1)*(q-1)`, then `e = pow(2, T, phi)`, then `mask = pow(2, e, N)`, then `flag = C - mask mod N` (converted to bytes).
</details>

---

## Format

Flag: `FLAG{...}`  
Submit your solution in `solve.py`.
