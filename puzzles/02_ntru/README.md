# Puzzle 2 — Tiny Keys (NTRU)

## The Math

**NTRU** (Hoffstein, Pipher, Silverman, 1998) is one of the oldest post-quantum proposals — it has withstood 25+ years of cryptanalysis.

Keys and ciphertexts are polynomials in the ring `Z[x]/(x^N - 1)`, reduced mod `q`.

**Key generation:**
- Choose small polynomials `f`, `g` with coefficients in `{-1, 0, 1}`
- Public key: `h = p * g * f^{-1} (mod q)`
- Private key: `f` (and `f_p = f^{-1} mod p`)

**Encryption of message `m`:**
```
e = r*h + m  (mod q)
```
where `r` is a small random "blinding" polynomial.

**Decryption:**
```
a = f*e (mod q)  →  m = a * f_p (mod p)
```

Security depends on the difficulty of finding `f` and `g` given only `h`. This is believed to be as hard as the **NTRU problem**, which resists both classical and quantum attacks under correct parameters.

**Reference:** Hoffstein, J., Pipher, J., Silverman, J.H. (1998). "NTRU: A Ring-Based Public Key Cryptosystem." ANTS 1998.

---

## The Challenge

The flag was encrypted with NTRU. The public key `h` and ciphertext `e` are in `ciphertext.json`.

There is a subtle flaw in how the private key was generated. Find it and recover the flag.

---

## Hints

<details>
<summary>Hint 1 (mild)</summary>
NTRU security requires `f` to be chosen with a specific, bounded number of ±1 coefficients. What if the balance is off?
</details>

<details>
<summary>Hint 2 (moderate)</summary>
Look at the distribution of `f`'s coefficients. If almost all are 0, the polynomial is unusually sparse. Sparse polynomials are vulnerable to lattice attacks with a much smaller basis.
</details>

<details>
<summary>Hint 3 (strong)</summary>
`f` here has only 3 non-zero coefficients (instead of ~N/3). Build the standard NTRU lattice and run LLL reduction — the short vector will be `f` itself.
</details>

---

## Format

Flag: `FLAG{...}`  
Submit your solution in `solve.py`.
