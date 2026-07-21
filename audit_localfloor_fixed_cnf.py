#!/usr/bin/env python3
"""Independently regenerate and hash any fixed m=45 local-floor CNF."""
import hashlib,itertools,pathlib,sys
N,ALPHA,DEG,CAP,FLOOR=16,3,5,45,45
NV,NC=26450,3764318
PARTS={
'T_AB':[[1,6,7],[2,8,9],[3,10,11],[4,12,13],[5,14,15]],
'T_BB1':[[6,7,1],[2,8,9],[3,10,11],[4,12,13],[5,14,15]],
'T_BB0':[[6,7,8],[1,2,9],[3,10,11],[4,12,13],[5,14,15]],
'Q_AA':[[1,2,6,7],[8,9],[3,10,11],[4,12,13],[5,14,15]],
'Q_AB':[[1,6,2,7],[8,9],[3,10,11],[4,12,13],[5,14,15]],
'Q_BB2':[[6,7,1,2],[8,9],[3,10,11],[4,12,13],[5,14,15]],
'Q_BB1S':[[6,7,1,8],[2,9],[3,10,11],[4,12,13],[5,14,15]],
'Q_BB1T':[[6,7,1,8],[9,10],[2,3,11],[4,12,13],[5,14,15]]}

class Gen:
 def __init__(self,case):
  self.case=case;self.variables=0;self.clauses=0;self.edge=[[0]*N for _ in range(N)];self.edges=[]
  for u in range(N):
   for v in range(u+1,N):
    z=self.nv();self.edge[u][v]=self.edge[v][u]=z;self.edges.append(z)
 def nv(self):self.variables+=1;return self.variables
 def emit(self,c):self.clauses+=1;yield (' '.join(map(str,c))+' 0\n').encode()
 def atmost(self,lits,k):
  if k>=len(lits):return
  if k==0:
   for x in lits:yield from self.emit([-x])
   return
  c=[[self.nv() for _ in range(k)] for _ in range(len(lits)-1)]
  for i in range(len(lits)-1):yield from self.emit([-lits[i],c[i][0]])
  for i in range(1,len(lits)-1):yield from self.emit([-c[i-1][0],c[i][0]])
  for i in range(1,len(lits)-1):
   for j in range(1,k):
    yield from self.emit([-lits[i],-c[i-1][j-1],c[i][j]])
    yield from self.emit([-c[i-1][j],c[i][j]])
  for i in range(1,len(lits)):yield from self.emit([-lits[i],-c[i-1][k-1]])
 def body(self):
  V=list(range(N))
  for S in itertools.combinations(V,ALPHA+1):yield from self.emit([self.edge[u][v] for u,v in itertools.combinations(S,2)])
  for v in V:
   q=[self.edge[v][w] for w in V if w!=v]
   for sub in itertools.combinations(q,len(q)-DEG+1):yield from self.emit(sub)
  for v in range(1,N):yield from self.emit([self.edge[0][v] if v<=DEG else -self.edge[0][v]])
  tag=self.case.split('_',1)[1];orbit='AA' if tag.startswith('AA') else 'AB' if tag.startswith('AB') else 'BB'
  du,dv={'AA':(1,2),'AB':(1,6),'BB':(6,7)}[orbit];removed=self.edge[du][dv]
  yield from self.emit([removed]);color=[[self.nv() for _ in range(5)] for _ in range(N)]
  yield from self.emit([color[du][0]]);yield from self.emit([color[dv][0]])
  for v in range(1,N):
   yield from self.emit(color[v])
   for a in range(5):
    for b in range(a+1,5):yield from self.emit([-color[v][a],-color[v][b]])
  for u in range(1,N):
   for v in range(u+1,N):
    if self.edge[u][v]==removed:continue
    for c in range(5):yield from self.emit([-self.edge[u][v],-color[u][c],-color[v][c]])
  sizes=[3]*5 if self.case.startswith('T_') else [4,2,3,3,3]
  for c in range(5):
   q=[color[v][c] for v in range(1,N)]
   yield from self.atmost(q,sizes[c]);yield from self.atmost([-x for x in q],len(q)-sizes[c])
  for c,P in enumerate(PARTS[self.case]):
   for v in P:yield from self.emit([color[v][c]])
  for u in range(N):
   for v in range(u+1,N):
    W=[]
    for I in itertools.combinations([z for z in V if z not in (u,v)],ALPHA-1):
     w=self.nv();W.append(w);yield from self.emit([-w,self.edge[u][v]]);T=[u,v,*I]
     for a,b in itertools.combinations(T,2):
      if (a,b)!=(u,v):yield from self.emit([-w,-self.edge[a][b]])
    yield from self.emit([-self.edge[u][v],*W])
  yield from self.atmost(self.edges,CAP);yield from self.atmost([-x for x in self.edges],len(self.edges)-FLOOR)
  for S in itertools.combinations(V,6):
   q=[self.edge[u][v] for u,v in itertools.combinations(S,2)]
   for twelve in itertools.combinations(q,12):yield from self.emit([-x for x in twelve])

def fhash(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()
def main():
 case=sys.argv[1];assert case in PARTS;g=Gen(case);h=hashlib.sha256();h.update(f'p cnf {NV} {NC}\n'.encode())
 for line in g.body():h.update(line)
 assert (g.variables,g.clauses)==(NV,NC),(g.variables,g.clauses)
 path=f'erdos617_localfloor_n16_a3_d5_m45_fixed_{case}_full.cnf';a,e=fhash(path),h.hexdigest();assert a==e,(a,e)
 print(f'PASS {case}: {a}')
if __name__=='__main__':main()
