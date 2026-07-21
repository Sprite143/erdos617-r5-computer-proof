#!/usr/bin/env python3
"""Independent byte-level audit of the m=44/45 root-factor CNFs."""
import hashlib,itertools,pathlib,sys
N,ALPHA,DEG,NV,NC=16,3,5,25320,3761530
class Gen:
 def __init__(self,m):
  self.m=m;self.variables=0;self.clauses=0;self.edge=[[0]*N for _ in range(N)];self.edges=[]
  for u in range(N):
   for v in range(u+1,N):
    z=self.nv();self.edge[u][v]=self.edge[v][u]=z;self.edges.append(z)
 def nv(self):self.variables+=1;return self.variables
 def emit(self,c):self.clauses+=1;yield (' '.join(map(str,c))+' 0\n').encode()
 def atmost(self,lits,k):
  if k>=len(lits):return
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
  for S in itertools.combinations(V,4):yield from self.emit([self.edge[u][v] for u,v in itertools.combinations(S,2)])
  for v in V:
   q=[self.edge[v][w] for w in V if w!=v]
   for sub in itertools.combinations(q,len(q)-DEG+1):yield from self.emit(sub)
  for v in range(1,N):yield from self.emit([self.edge[0][v] if v<=DEG else -self.edge[0][v]])
  for i in range(5):
   T=[1+i,6+2*i,7+2*i]
   for u,v in itertools.combinations(T,2):yield from self.emit([-self.edge[u][v]])
  for u in range(N):
   for v in range(u+1,N):
    W=[]
    for I in itertools.combinations([z for z in V if z not in (u,v)],2):
     w=self.nv();W.append(w);yield from self.emit([-w,self.edge[u][v]]);T=[u,v,*I]
     for a,b in itertools.combinations(T,2):
      if (a,b)!=(u,v):yield from self.emit([-w,-self.edge[a][b]])
    yield from self.emit([-self.edge[u][v],*W])
  yield from self.atmost(self.edges,self.m);yield from self.atmost([-x for x in self.edges],len(self.edges)-self.m)
  for S in itertools.combinations(V,6):
   q=[self.edge[u][v] for u,v in itertools.combinations(S,2)]
   for twelve in itertools.combinations(q,12):yield from self.emit([-x for x in twelve])
def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()
def main():
 m=int(sys.argv[1]);assert m in (44,45);g=Gen(m);h=hashlib.sha256();h.update(f'p cnf {NV} {NC}\n'.encode())
 for line in g.body():h.update(line)
 assert (g.variables,g.clauses)==(NV,NC)
 path=f'erdos617_localfloor_n16_a3_d5_m{m}_rootfactor_full.cnf';a,e=digest(path),h.hexdigest();assert a==e,(a,e)
 print(f'PASS m={m}: {a}')
if __name__=='__main__':main()
