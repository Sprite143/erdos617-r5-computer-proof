# Erdős–Gyárfás Problem #617: the r=5 case

This repository contains a new computer-assisted proof claiming that the
r=5 case of Erdős Problem #617 is true.

## Status

New and not yet peer-reviewed. Independent specialist review is requested
before the result is considered settled.

## Main result

Every 5-edge-coloring of K_26 contains six vertices whose induced K_6
omits at least one color.

The proof establishes that each color class in a hypothetical
counterexample would require at least 66 edges. The five classes would
therefore require at least 330 edges, while K_26 has only 325.

## Contents

- `erdos617_computer_assisted_proof.md` — human-readable proof
- `erdos617_reproduce.md` — reproduction instructions
- `cegar_local_floor_mindeg5.mjs` — formula generator
- `audit_*.py` — independent encoding and arithmetic auditors
- `*.cnf` and `*.drat` — base-case formulas and checked certificates

The larger formulas and certificates are reproducibly generated using
the instructions in `erdos617_reproduce.md`.

## AI disclosure

AI systems were used extensively in discovering, writing, testing, and
auditing this proof. These included OpenAI Codex (GPT-5.6) and Anthropic
Claude Fable 5. A human submitter should read and
understand the argument before presenting it as a proof claim.

## Verification

The finite component consists of twelve UNSAT instances. The formulas
were independently reconstructed, all instances were re-solved, and the
saved DRAT certificates were checked using `drat-trim`.



