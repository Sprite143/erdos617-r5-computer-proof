# Erdős–Gyárfás Problem #617: the `r=5` case

This repository contains a new computer-assisted proof claiming that the
`r=5` case of Erdős Problem #617 is true:

> Every five-edge-coloring of `K_26` contains six vertices whose induced
> `K_6` omits at least one color.

This settles only the `r=5` instance, not the full conjecture for every
`r >= 3`.

## Status

**New and not yet peer-reviewed.** The formulas and certificates have passed
the documented independent checks, but specialist review and external
replication should precede any claim that the result is formally settled.

## Main idea

For each color `c`, let `G_c` contain the edges of that color. In a hypothetical
counterexample, `alpha(G_c) <= 5`, and every six vertices span at most 11 edges
of `G_c` because the other four colors must each occur.

The proof establishes the one-color lower bounds

```text
L_2 >= 36,  L_3 >= 46,  L_4 >= 56,  L_5 >= 66,
```

using degree deletion, critical-graph extremal results, and twelve finite UNSAT
calculations. Thus every color class would contain at least 66 edges, requiring
at least `5 * 66 = 330` edges, while `K_26` has only 325.

## Start here

- [`erdos617_computer_assisted_proof.md`](erdos617_computer_assisted_proof.md)
  — human-readable proof.
- [`erdos617_reproduce.md`](erdos617_reproduce.md) — exact reproduction and
  certificate-checking instructions.
- [`SHA256SUMS.txt`](SHA256SUMS.txt) — hashes of the uploaded files.

## Verification files

- `cegar_local_floor_mindeg5.mjs` generates all twelve formulas.
- `audit_proof_arithmetic.py` checks the numerical induction.
- `audit_m45_case_split.py` checks the exhaustive eight-way case split.
- `audit_l2_cegar_cnf.py` semantically audits the two rank-two formulas.
- `audit_localfloor_fixed_cnf.py` and
  `audit_localfloor_rootfactor_cnf.py` independently reproduce the full
  16-vertex formulas.
- The two included `.cnf`/`.drat` pairs are the rank-two base cases. The ten
  much larger 16-vertex formulas and traces are reproducibly generated using
  the commands in `erdos617_reproduce.md`; their expected hashes are recorded
  in the proof.

## AI disclosure

AI systems were used extensively in discovering, writing, testing, and auditing
this proof. These included OpenAI Codex (GPT-5) and Anthropic Claude (exact
model/version to be supplied by the submitter). A human submitter should read,
understand, and accept responsibility for the argument before presenting it as
a proof claim.

## Author and contact

Replace this section before publishing with the responsible human author's
full name and preferred contact information.

## License

No license has yet been selected. Add an appropriate license before others are
invited to reuse or modify the code.
