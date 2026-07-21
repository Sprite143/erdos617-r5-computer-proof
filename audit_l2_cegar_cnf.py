#!/usr/bin/env python3
"""Independent semantic audit of the two L2 orbit-CEGAR formulas."""
import hashlib,itertools,pathlib,sys
N,ALPHA,CAP=11,2,35

def prefix(deg):
    variables=0
    def nv():
        nonlocal variables;variables+=1;return variables
    edge=[[0]*N for _ in range(N)];edges=[]
    for u in range(N):
        for v in range(u+1,N):
            z=nv();edge[u][v]=edge[v][u]=z;edges.append(z)
    C=[];V=list(range(N))
    for S in itertools.combinations(V,3):C.append(tuple(edge[u][v] for u,v in itertools.combinations(S,2)))
    for v in V:
        q=[edge[v][w] for w in V if w!=v]
        C.extend(itertools.combinations(q,len(q)-deg+1))
    for v in range(1,N):C.append((edge[0][v] if v<=deg else -edge[0][v],))
    k=CAP;c=[[nv() for _ in range(k)] for _ in range(len(edges)-1)]
    for i in range(len(edges)-1):C.append((-edges[i],c[i][0]))
    for i in range(1,len(edges)-1):C.append((-c[i-1][0],c[i][0]))
    for i in range(1,len(edges)-1):
        for j in range(1,k):
            C.append((-edges[i],-c[i-1][j-1],c[i][j]));C.append((-c[i-1][j],c[i][j]))
    for i in range(1,len(edges)):C.append((-edges[i],-c[i-1][k-1]))
    assert variables==1945
    inv={edge[u][v]:(u,v) for u in range(N) for v in range(u+1,N)}
    return C,inv

def parse(s):
    q=tuple(map(int,s.split()));assert q[-1]==0;return q[:-1]
def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return h.hexdigest()
def main():
    deg=int(sys.argv[1]);assert deg in (5,6)
    path=pathlib.Path(f'erdos617_localfloor_n11_a2_d{deg}_orbit.cnf')
    pre,inv=prefix(deg)
    with path.open() as f:
        hdr=f.readline().split();assert hdr[:2]==['p','cnf'];nv,nc=map(int,hdr[2:]);assert nv==1945
        count=0
        for e in pre:
            count+=1;assert parse(f.readline())==e
        local=0
        for line in f:
            count+=1;local+=1;q=parse(line)
            assert len(q)==len(set(q))==12 and all(x<0 and -x in inv for x in q)
            vs=set()
            for x in q:vs.update(inv[-x])
            assert len(vs)==6
        assert count==nc
    print(f'PASS d={deg}: prefix={len(pre)} local={local} clauses={nc} sha256={digest(path)}')
if __name__=='__main__':main()
