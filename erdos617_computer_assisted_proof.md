# Erdős Problem #617: a computer-assisted proof for five colors

**Date:** 2026-07-21  
**Status:** complete proof bundle; new result, not peer reviewed

## Theorem

Every five-edge-coloring of `K_26` has six vertices whose induced `K_6`
misses a color.  Thus Erdős Problem #617 is true for five colors.

The proof is a one-color induction.  Its only finite ingredients are two
11-vertex cases and ten 16-vertex cases.  Every finite UNSAT claim has a
DIMACS instance, a CaDiCaL DRAT trace, independent `drat-trim` verification,
and an independently written semantic auditor.

## 1. One-color reduction

Suppose a balanced five-coloring of `K_26` exists.  For each color `c`, let
`G_c` be its color graph.  Then:

1. `alpha(G_c)<=5`, because an independent six-set misses `c`.
2. Every six-set spans at most 11 edges of `G_c`, because the other four
   colors occupy four distinct edges of that 15-edge `K_6`.

We prove that every 26-vertex graph with these two properties has at least 66
edges.  The five color classes would then require `5*66=330` edges, but
`K_26` has only 325.

## 2. Local-floor induction

For `r=2,3,4,5`, let `L_r` be the minimum number of edges in a graph on
`5r+1` vertices satisfying

```text
alpha(G)<=r,  and  e(G[S])<=11 for every six-set S.
```

We prove

```text
L_2>=36,  L_3>=46,  L_4>=56,  L_5>=66.
```

Assume the bound for `L_(r-1)`.  Choose a minimum-degree vertex `v` of degree
`d<=4`, let `A=N(v)`, and let `R` be its other non-neighbors, so
`|R|=5r-d`.  Every `(5r-4)`-subset of `R` satisfies the rank-`r-1`
conditions: an independent `r`-set there could be enlarged by `v`, and the
local upper bound is hereditary.  Double-counting gives

```text
e(R) >= ceil(L_(r-1)|R|(|R|-1)/((5r-4)(5r-5))).
```

Every vertex of `A` has at least `d-1` further incident edges, so the non-root
edges meeting `A` number at least `ceil(d(d-1)/2)`.  Including the root edges
gives:

| Rank | `d=0` | `d=1` | `d=2` | `d=3` | `d=4` |
|---|---:|---:|---:|---:|---:|
| `r=3`, using `L_2>=36` | 69 | 61 | 55 | 50 | 46 |
| `r=4`, using `L_3>=46` | 73 | 67 | 62 | 59 | 56 |
| `r=5`, using `L_4>=56` | 80 | 75 | 71 | 68 | 66 |

Thus only minimum degree five is exceptional at ranks three and four.
Minimum degree at least six gives 48, 63, and 78 edges respectively.

## 3. Certified base: `L_2>=36`

Let `G` have 11 vertices and `alpha(G)<=2`.  If a minimum-degree vertex has
degree at most four, its six non-neighbors induce a clique: a nonedge among
them, with the root, would be an independent triple.  This forbidden `K_6`
contradicts the local upper bound.  Minimum degree at least seven gives at
least 39 edges.

The remaining degree-five and degree-six branches with at most 35 edges are
CNF-certified UNSAT.  A minimum-degree root and its neighborhood are fixed
canonically.  Orbit CEGAR retains only genuine necessary six-set clauses.

| Branch | CNF SHA-256 | DRAT SHA-256 |
|---|---|---|
| `delta=5` | `fdbc3b6794cf1b060c10bfb95522824020756c441427f4f88b19dd2079e394f5` | `fc64b4bf8500b1c511187c6c5e3d3472fa11ce2b14272176055d836e9fcfeb98` |
| `delta=6` | `8be7878e1f52027902356525046eca0a4a6077aae43a65ccdd0d04e69875e154` | `e79c636cd550d6856dfd1e943909c512d4967ca8ec153e6c4e85bfc7a8d5f279` |

`audit_l2_cegar_cnf.py` independently rebuilds the mandatory prefix and
checks every retained clause as a valid twelve-edge forbidden set inside one
six-set.  It finds 14,105 local clauses for `delta=5` and 161,525 for
`delta=6`.

## 4. Sparse six-critical graphs

Every graph of chromatic number at least six contains a six-critical
subgraph.  Such a graph has minimum degree five.  The Kostochka--Yancey bound
for a six-critical graph on `h` vertices is

```text
e(H)>=ceil((14h-9)/5).
```

Gallai's exact formula gives

```text
f_6(8)=23, f_6(9)=26, f_6(10)=28, f_6(11)=29,
```

For order 12, only the lower bound `f_6(12)>=33` is needed.  Here is the
precise deduction from Kostochka--Yancey's Brooks-type theorem.  Every
six-Ore graph has order congruent to 1 modulo 5, so a 12-vertex six-critical
graph is not six-Ore.  The theorem's non-Ore bound, with `k=6` and `y_6=8`,
is

```text
e(G) >= (28*12-8)/10 = 32.8,
```

and integrality gives `e(G)>=33`.  No upper bound or exact evaluation of
`f_6(12)` is used.  Equality in the basic Kostochka--Yancey bound is
characterized by six-Ore graphs.

References:

- A. Kostochka and M. Yancey, [Ore's conjecture on color-critical graphs is
  almost true](https://kostochk.web.illinois.edu/docs/2016/jctb14-y.pdf),
  *J. Combin. Theory B* 109 (2014), 73--101.
- A. Kostochka and M. Yancey, [A Brooks-type result for sparse critical
  graphs](https://kostochk.web.illinois.edu/docs/submit/cca18y.pdf).

A six-Ore graph on 11 vertices is an Ore composition of two `K_6`s, so its
edge-side induces `K_6-e`.  A six-Ore graph on 16 vertices is a composition
of three `K_6`s.  If its top edge-side is `K_6`, it again contains `K_6-e`;
if that side has 11 vertices, deleting the top composition edge removes at
most one edge from its earlier `K_6-e`.  Hence every such 11- or 16-vertex
equality graph has a six-set with at least 13 edges, contradicting the upper
bound 11.

Choose a vertex set `U` whose induced graph `J=G[U]` contains a spanning
six-critical graph.  Put `h=|U|`, `X=V(G)-U`, `t=|X|`, let `y=e(G[X])`, and
let `x` count `U`--`X` edges.  When `delta(G)>=5`,

```text
2y+x>=5t,
x+y>=g(t):=max(ceil(5t/2),5t-binomial(t,2)).
```

For `t=5,4,3,2,1`, `g(t)=15,14,12,9,5`.  Using the induced graph `J`, not
just its critical spanning subgraph, makes every independence argument below
an argument in `G` itself.

## 5. Human rank-four gate: `L_4>=56`

Assume a 21-vertex graph has `alpha<=4`, the local bound, and at most 55
edges.  The induction and handshake bounds force minimum degree five and
53, 54, or 55 edges.  Also `chi(G)>=ceil(21/4)=6`.

- At 53 edges, the critical count leaves only a `K_6`, forbidden locally.
- At 54 edges, critical orders 8, 9, and 10 require respectively `23+33`,
  `26+30`, and `28+28` edges.  Order 11 forces `e(J)=29`, the forbidden
  six-Ore equality case.
- At 55 edges, only orders 11, 12, and 13 remain.  At order 11, 29 edges is
  the Ore case.  With 30 edges, the ten outside vertices use all 25 remaining
  edges, so `x=0,y=25`.  Their graph has an independent pair.  An independent
  triple in `J` would combine with it to give an independent five-set;
  therefore `alpha(J)<=2`, and `L_2>=36` contradicts `e(J)=30`.  At order 12,
  `f_6(12)+g(9)=33+23=56`.  At order 13, equality gives `e(J)=35,x=0,y=20`.
  An outside independent pair again forces `alpha(J)<=2`; the complement of
  `J` is triangle-free, so Turan gives
  `e(J)>=binomial(13,2)-floor(13^2/4)=36`.

Therefore `L_4>=56`.

## 6. Rank-three gate: `L_3>=46`

Take an edge-minimal counterexample.  Every edge is alpha-critical.  The
induction and handshake bounds force minimum degree five, so it has 40--45
edges, and `chi(G)>=ceil(16/3)=6`.

At 40 edges it is 5-regular.  The local bound excludes `K_6`, so Brooks'
theorem 5-colors every component, a contradiction.  At 41 and 42 edges, the
critical-core count leaves only `K_6`.

For 43--45 edges use the induced critical-core setup above.

- Order 8 is impossible because `e(J)>=23` and the average over its 28
  six-subsets is `23*15/28>12`.
- At order 9 only `e(J)=26` or 27 fits.  The outside seven-set has a nonedge.
  The degree and edge budgets allow at most three cross edges in the first
  case and one in the second.  The complement of `J` has respectively 10 or
  9 edges and maximum degree at most three.  The cross-neighborhood of that
  outside nonedge cannot cover every complement edge, so a nonedge of `J`
  avoids it.  Together they form an independent four-set.
- At order 10, `e(J)>=28`; the degree count forces at least 13 edges inside
  the outside six-set.
- At order 11, `e(J)=29` is the Ore case.  The only other possibility is
  `e(J)=30` in a 45-edge graph.  The outside five-set is a `K_5` with five
  cross edges.  The local bound gives each vertex of `J` at most one outside
  neighbor.  Since `30<36`, the base result gives an independent triple in
  `J`; it misses at least one outside vertex and forms an independent four-set.
- Orders 12 through 15 require at least 47, 47, 47, and 46 edges.
- A spanning 43-edge critical graph is a forbidden 16-vertex six-Ore graph.

Thus a 44-edge candidate is itself six-critical.  A 45-edge candidate
contains a spanning six-critical graph with 44 or 45 edges.

### 6.1 The 44-edge branch

Choose a degree-five root `v`.  Since the graph is six-critical, `G-v` is
5-colorable.  Its 15 vertices split into five independent triples.  Every
triple meets `N(v)`, or it extends with `v` to an independent four-set, so
every triple contains exactly one root-neighbor.  Relabeling yields

```text
{1,6,7}, {2,8,9}, {3,10,11}, {4,12,13}, {5,14,15}.
```

The full CNF for this necessary configuration is UNSAT.

### 6.2 The exhaustive 45-edge split

If the spanning critical graph has 44 edges, its extra edge cannot meet the
root (otherwise the root has critical degree four).  If the whole graph is
critical, choose any non-root edge.  Hence there is a non-root edge `e` such
that `(G-v)-e` is 5-colorable.

Under permutations of the five root-neighbors (`A`) and ten non-neighbors
(`B`), `e` has type `AA`, `AB`, or `BB`.  If its endpoints receive different
colors, the five classes are independent triples in `G`, giving the same
root-factor CNF at 45 edges.

If the endpoints share color zero, only that class can fail to be independent
in `G`.  The class sizes are

```text
(3,3,3,3,3) or (4,2,3,3,3).
```

Every ordinary triple meets `A`.  In the second pattern, the special
four-set induces only `e`, so each of its two independent triples also meets
`A`.  Counting the five `A` vertices, modulo permutations, gives exactly:

| Case | Orbit | `A`-counts by class |
|---|---|---|
| `T_AB` | `AB` | `1;1,1,1,1` |
| `T_BB1` | `BB` | `1;1,1,1,1` |
| `T_BB0` | `BB` | `0;2,1,1,1` |
| `Q_AA` | `AA` | `2,0;1,1,1` |
| `Q_AB` | `AB` | `2,0;1,1,1` |
| `Q_BB2` | `BB` | `2,0;1,1,1` |
| `Q_BB1S` | `BB` | `1,1;1,1,1` |
| `Q_BB1T` | `BB` | `1,0;2,1,1` |

There is no `T_AA`: its special triple uses two root-neighbors, leaving only
three for four ordinary triples.  `audit_m45_case_split.py` independently
enumerates the count possibilities and confirms exactly eight branches.

Each fixed formula encodes `alpha<=3`, minimum degree five, the fixed root,
exactly 45 edges, alpha-criticality of every edge, all 8,008 local six-set
constraints, and the stated partition.  `audit_localfloor_fixed_cnf.py`
independently reproduces every 3,764,318-clause formula byte-for-byte;
`audit_localfloor_rootfactor_cnf.py` does the same for both 3,761,530-clause
root-factor formulas.

| Formula | CNF SHA-256 | DRAT SHA-256 |
|---|---|---|
| `m44_rootfactor` | `601ac13460c4e2617a7a747f88974f0353a844ec55304cfb9fc7f09c8a29c94b` | `69ae093187e92c83fd1604bc948dd5b60a33b7f1433bfcdda203d750fc326c59` |
| `m45_rootfactor` | `f449802d1730ea3b764daea48e39fe4bded590a8307532e1ef71ebfa25bc3d9c` | `f2716bf2ff2b5d2e6922c1b821004b6a2b5e4ff0665b0c39d6d39f0543baa1f7` |
| `T_AB` | `07c4c59b01f14774d3ef9f660d2ab2fc740173d781e6871246d7a1e5ec310b91` | `e426edb2774e85711bb7df1b6447d7aee1bb336910d5f058acc1f4a248e8ca69` |
| `T_BB1` | `493c0ad7d39a2bb5350f58cc5357f1721b5a28e850a0372a377dc62e1769f9f4` | `887aea7a1350d8642e8f9438313a96c80212f374b4848a5e9ae5a68821e9acd7` |
| `T_BB0` | `e965dc7886931f6c44d3491630a9d9bf240c85038510935e44291afb4e4fd61d` | `b4c50c6cc27727f16f3344d35adde1458e8f4aefbe53d131466f5ac76c9e6af8` |
| `Q_AA` | `fc186e61ec47bb1aeef9362d5cda7db5994aa5108a7875c2feaef7946a25d258` | `9c0be3fc585b23929a844ee369ff37e4725a8daa6909fb920289cdc0b14871da` |
| `Q_AB` | `7e335195d1e1f6932aef92eff57254a48147877f147aa570ec6d5f63a79d1e75` | `ae76969bf48e1029ee0b7ac7bbcf76e595b476b65ac0b3dea0f9f5046e80d13c` |
| `Q_BB2` | `7f7ff601fe771ef45d14d676eae0ad0bb940b613306133a6b942c642fd42cdde` | `771137ca0043076925835aa17b44589a81f8bbb6e28cb4c5e325920f22fd62ce` |
| `Q_BB1S` | `d6125c02bc29dbc6e59da23dcdbe98d69943fbb67214a0a5f1c353ac6eceaccf` | `49997a534c07f6027aad21084f4d06a8db9edcf5a225bb50a55e776a35bcce68` |
| `Q_BB1T` | `3648021437ad6fbb6e49790a2bd6eac4aab15323cbcbc2213809c0b3af7ec9be` | `c5de707ca9adc6e3e34de90b0f131c37ec5c314c25d1957d178e68c481a422f7` |

Every row returned `s VERIFIED` under `drat-trim`, with `0 RAT lemmas`.
This proves `L_3>=46`.

## 7. Final rank: `L_5>=66`

The induction handles minimum degree at most four; minimum degree at least six
gives 78 edges.  A 26-vertex counterexample of minimum degree five with at
most 65 edges would be 5-regular.  Since `alpha<=5`, its chromatic number is
at least six.  The local bound excludes `K_6`; Brooks' theorem therefore
5-colors every component (the odd-cycle exception is irrelevant to a
5-regular graph), a contradiction.

## 8. Conclusion and status

Each of the five color graphs would have at least 66 edges, requiring
`330>325`.  Therefore no balanced five-coloring of `K_26` exists.

This is a new computer-assisted proof bundle, not a claim of publication or
peer acceptance.  Independent reproduction and specialist review should
precede any public announcement.

`audit_proof_arithmetic.py` independently checks every numerical induction
table and critical-core lower-bound total used above.
