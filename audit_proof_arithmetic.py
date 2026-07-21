#!/usr/bin/env python3
"""Audit the numerical inequalities used in the local-floor proof."""
import math

def induction(prev,r,d):
    R=5*r-d;s=5*r-4
    eR=math.ceil(prev*R*(R-1)/(s*(s-1)))
    return eR+d+math.ceil(d*(d-1)/2)

assert [induction(36,3,d) for d in range(5)]==[69,61,55,50,46]
assert [induction(46,4,d) for d in range(5)]==[73,67,62,59,56]
assert [induction(56,5,d) for d in range(5)]==[80,75,71,68,66]

def ky(h):return math.ceil((14*h-9)/5)
def g(t):return max(math.ceil(5*t/2),5*t-t*(t-1)//2)
exact={8:23,9:26,10:28,11:29,12:33}
f=lambda h:exact.get(h,ky(h))

# Proper critical cores that can survive at rank four under 56 edges.
rank4={h:f(h)+g(21-h) for h in range(8,14)}
assert rank4=={8:56,9:56,10:56,11:54,12:56,13:55}

# Rank-three proper-core lower totals used in the case split.
rank3={h:f(h)+g(16-h) for h in range(8,16)}
assert rank3=={8:43,9:44,10:43,11:44,12:47,13:47,14:47,15:46}
assert ky(16)==43
print('PASS: induction tables and critical-core arithmetic')
