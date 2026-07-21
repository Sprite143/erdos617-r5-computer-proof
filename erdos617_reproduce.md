# Reproducing the Erdős #617 certificate bundle

Required tools:

- Node.js 18+
- Python 3.10+
- CaDiCaL commit `c60730422e758ef1cebe7aeddf2dda31c996bf04`
- `drat-trim` commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`

Set `CADICAL` to the CaDiCaL executable.  Generate the two root-factor
formulas:

```bash
CADICAL=/path/to/cadical node cegar_local_floor_mindeg5.mjs 16 3 44 erdos617_localfloor_n16_a3_d5_m44_rootfactor_full 5 --critical --root-triple-factor --floor=44 --full
CADICAL=/path/to/cadical node cegar_local_floor_mindeg5.mjs 16 3 45 erdos617_localfloor_n16_a3_d5_m45_rootfactor_full 5 --critical --root-triple-factor --floor=45 --full
```

For each row below, substitute `NAME`, `ORBIT`, and `PATTERN`:

```text
T_AB    AB T
T_BB1   BB T
T_BB0   BB T
Q_AA    AA Q
Q_AB    AB Q
Q_BB2   BB Q
Q_BB1S  BB Q
Q_BB1T  BB Q
```

```bash
CADICAL=/path/to/cadical node cegar_local_floor_mindeg5.mjs 16 3 45 erdos617_localfloor_n16_a3_d5_m45_fixed_NAME_full 5 --critical --root-near-fivecolor=ORBIT --near-pattern=PATTERN --fixed-near-partition=NAME --floor=45 --full
```

Check each proof with:

```bash
/path/to/drat-trim FORMULA.cnf FORMULA.drat
```

Every check must end with `s VERIFIED`.  Run the semantic audits with:

```bash
python3 audit_m45_case_split.py
python3 audit_proof_arithmetic.py
python3 audit_l2_cegar_cnf.py 5
python3 audit_l2_cegar_cnf.py 6
python3 audit_localfloor_rootfactor_cnf.py 44
python3 audit_localfloor_rootfactor_cnf.py 45
for c in T_AB T_BB1 T_BB0 Q_AA Q_AB Q_BB2 Q_BB1S Q_BB1T; do
  python3 audit_localfloor_fixed_cnf.py "$c"
done
```

The full expected hashes are in `erdos617_computer_assisted_proof.md`.
