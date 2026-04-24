# Puzzle 1 — Small Secrets (LWE)

## The Math

**Learning With Errors (LWE)** was introduced by Oded Regev in 2005.  
Given `m` samples of the form `(a_i, b_i)` where:

```
b_i = <a_i, s> + e_i  (mod q)
```

- `a_i` is a random vector in Z_q^n
- `s` is a secret vector in Z_q^n
- `e_i` is a small "error" drawn from a Gaussian distribution

...recovering `s` from the samples is believed to be as hard as solving the **Shortest Vector Problem (SVP)** in worst-case lattices — an NP-hard problem.

This hardness is the foundation of **ML-KEM (CRYSTALS-Kyber)**, NIST's post-quantum KEM standard.

**Reference:** Regev, O. (2005). "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography." STOC 2005. [https://cims.nyu.edu/~regev/papers/qcrypto.pdf](https://cims.nyu.edu/~regev/papers/qcrypto.pdf)

---

## The Challenge

Someone implemented an LWE-based encryption scheme to hide a flag.  
They chose parameters they thought were secure — but made one critical mistake.

The ciphertext is in `ciphertext.json`. The flawed encryption is in `challenge.py`.

**Recover the flag.**

---

## Hints

<details>
<summary>Hint 1 (mild)</summary>
LWE security depends on the secret `s` being indistinguishable from random. What if it isn't?
</details>

<details>
<summary>Hint 2 (moderate)</summary>
Check the range of values the secret key entries can take. Compare to the modulus `q`.
</details>

<details>
<summary>Hint 3 (strong)</summary>
The secret vector entries are drawn from `{0, 1}` instead of `Z_q`. This is a "binary LWE" instance with very small secrets. With enough samples, you can recover each coordinate by taking a majority vote on the rounded inner products.
</details>

---

## Format

Flag: `FLAG{...}`  
Submit your solution in `solve.py`.
