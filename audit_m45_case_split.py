#!/usr/bin/env python3
"""Independent audit of the eight canonical n=16,m=45 branches."""
from itertools import product

def signatures(orbit,pattern):
    ae={'AA':2,'AB':1,'BB':0}[orbit]; out=set()
    if pattern=='T':
        for extra in (0,1):
            a0=ae+extra
            if 0<=a0<=3:
                for ordinary in product(range(1,4),repeat=4):
                    if a0+sum(ordinary)==5:
                        out.add((a0,tuple(sorted(ordinary,reverse=True))))
        return out
    for extra in range(3):
        a0=ae+extra
        if not 0<=a0<=4: continue
        # The special four-set induces only e.  Each of its two independent
        # triples must contain a root-neighbor.
        if ae==1 and extra<1: continue
        if ae==0 and extra<1: continue
        for a1 in range(3):
            for triples in product(range(1,4),repeat=3):
                if a0+a1+sum(triples)==5:
                    out.add((a0,a1,tuple(sorted(triples,reverse=True))))
    return out

actual={(o,p):signatures(o,p) for o in ('AA','AB','BB') for p in ('T','Q')}
expected={
 ('AA','T'):set(),
 ('AB','T'):{(1,(1,1,1,1))},
 ('BB','T'):{(1,(1,1,1,1)),(0,(2,1,1,1))},
 ('AA','Q'):{(2,0,(1,1,1))},
 ('AB','Q'):{(2,0,(1,1,1))},
 ('BB','Q'):{(2,0,(1,1,1)),(1,1,(1,1,1)),(1,0,(2,1,1))},
}
assert actual==expected
assert sum(map(len,actual.values()))==8
for k in sorted(actual): print(k,sorted(actual[k]))
print('PASS: exactly eight canonical branches')
