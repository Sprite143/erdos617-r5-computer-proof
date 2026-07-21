#!/usr/bin/env node
// Proof-producing CEGAR for the exceptional branches in the L_r induction.
import fs from 'node:fs';import {spawnSync} from 'node:child_process';
const N=Number(process.argv[2]),ALPHA=Number(process.argv[3]),CAP=Number(process.argv[4]);
const stem=process.argv[5]??`local_floor_n${N}_a${ALPHA}_d5`;
const DEG=Number(process.argv[6]??5);
const critical=process.argv.includes('--critical');
const chromaticCritical=process.argv.includes('--chromatic-critical');
const rootTripleFactor=process.argv.includes('--root-triple-factor');
const nearColorArg=process.argv.find(x=>x.startsWith('--root-near-fivecolor='));
const rootNearFiveColor=nearColorArg?nearColorArg.split('=')[1]:null;
const nearPatternArg=process.argv.find(x=>x.startsWith('--near-pattern='));
const nearPattern=nearPatternArg?nearPatternArg.split('=')[1]:null;
const fixedNearArg=process.argv.find(x=>x.startsWith('--fixed-near-partition='));
const fixedNearPartition=fixedNearArg?fixedNearArg.split('=')[1]:null;
const floorArg=process.argv.find(x=>x.startsWith('--floor='));
const FLOOR=floorArg?Number(floorArg.slice(8)):0;
const solver=process.env.CADICAL??'./cadical-src/build/cadical';
if(!N||!ALPHA||!CAP)throw new Error('usage: N ALPHA EDGE_CAP STEM');
function* choose(a,k,s=0,p=[]){if(p.length===k){yield [...p];return;}for(let i=s;i<=a.length-(k-p.length);i++){p.push(a[i]);yield*choose(a,k,i+1,p);p.pop();}}
let variables=0;const nv=()=>++variables,edge=Array.from({length:N},()=>new Int32Array(N)),edges=[];
for(let u=0;u<N;u++)for(let v=u+1;v<N;v++)edges.push(edge[u][v]=edge[v][u]=nv());
const clauses=[];
function atMost(lits,k){if(k>=lits.length)return;if(k===0){for(const x of lits)clauses.push([-x]);return;}const c=Array.from({length:lits.length-1},()=>Array.from({length:k},nv));for(let i=0;i<lits.length-1;i++)clauses.push([-lits[i],c[i][0]]);for(let i=1;i<lits.length-1;i++)clauses.push([-c[i-1][0],c[i][0]]);for(let i=1;i<lits.length-1;i++)for(let j=1;j<k;j++){clauses.push([-lits[i],-c[i-1][j-1],c[i][j]]);clauses.push([-c[i-1][j],c[i][j]]);}for(let i=1;i<lits.length;i++)clauses.push([-lits[i],-c[i-1][k-1]]);}
const V=[...Array(N).keys()];
// alpha <= ALPHA.
for(const S of choose(V,ALPHA+1))clauses.push([...choose(S,2)].map(([u,v])=>edge[u][v]));
// degree at least DEG at every vertex, direct monotone CNF.
for(let v=0;v<N;v++){const q=V.filter(w=>w!==v).map(w=>edge[v][w]);for(const sub of choose(q,q.length-DEG+1))clauses.push(sub);}
// Canonical minimum-degree vertex and sorted neighborhood.
for(let v=1;v<N;v++)clauses.push([v<=DEG?edge[0][v]:-edge[0][v]]);
if(rootTripleFactor){
  if(N!==16||DEG!==5)throw new Error('--root-triple-factor requires N=16, DEG=5');
  for(let i=0;i<5;i++){
    const T=[1+i,6+2*i,7+2*i];
    for(const [u,v] of choose(T,2))clauses.push([-edge[u][v]]);
  }
}
if(rootNearFiveColor){
  if(N!==16||DEG!==5||!['AA','AB','BB'].includes(rootNearFiveColor))
    throw new Error('--root-near-fivecolor requires N=16, DEG=5 and AA|AB|BB');
  const distinguished=rootNearFiveColor==='AA'?[1,2]:rootNearFiveColor==='AB'?[1,6]:[6,7];
  const removed=edge[distinguished[0]][distinguished[1]];clauses.push([removed]);
  const color=Array.from({length:N},()=>Array.from({length:5},nv));
  clauses.push([color[distinguished[0]][0]],[color[distinguished[1]][0]]);
  for(let v=1;v<N;v++){
    clauses.push([...color[v]]);
    for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)clauses.push([-color[v][a],-color[v][b]]);
  }
  for(let u=1;u<N;u++)for(let v=u+1;v<N;v++)if(edge[u][v]!==removed)
    for(let c=0;c<5;c++)clauses.push([-edge[u][v],-color[u][c],-color[v][c]]);
  if(nearPattern){
    if(!['T','Q'].includes(nearPattern))throw new Error('--near-pattern requires T|Q');
    const sizes=nearPattern==='T'?[3,3,3,3,3]:[4,2,3,3,3];
    for(let c=0;c<5;c++){
      const q=V.slice(1).map(v=>color[v][c]);
      atMost(q,sizes[c]);atMost(q.map(x=>-x),q.length-sizes[c]);
    }
  }
  if(fixedNearPartition){
    const parts={
      T_AB:[[1,6,7],[2,8,9],[3,10,11],[4,12,13],[5,14,15]],
      T_BB1:[[6,7,1],[2,8,9],[3,10,11],[4,12,13],[5,14,15]],
      T_BB0:[[6,7,8],[1,2,9],[3,10,11],[4,12,13],[5,14,15]],
      Q_AA:[[1,2,6,7],[8,9],[3,10,11],[4,12,13],[5,14,15]],
      Q_AB:[[1,6,2,7],[8,9],[3,10,11],[4,12,13],[5,14,15]],
      Q_BB2:[[6,7,1,2],[8,9],[3,10,11],[4,12,13],[5,14,15]],
      Q_BB1S:[[6,7,1,8],[2,9],[3,10,11],[4,12,13],[5,14,15]],
      Q_BB1T:[[6,7,1,8],[9,10],[2,3,11],[4,12,13],[5,14,15]]
    };
    const P=parts[fixedNearPartition];if(!P)throw new Error('unknown --fixed-near-partition');
    for(let c=0;c<5;c++)for(const v of P[c])clauses.push([color[v][c]]);
  }
}
// In an inclusion-minimal candidate every present edge is alpha-critical.
if(critical)for(let u=0;u<N;u++)for(let v=u+1;v<N;v++){
  const witnesses=[];
  for(const I of choose(V.filter(z=>z!==u&&z!==v),ALPHA-1)){
    const w=nv();witnesses.push(w);clauses.push([-w,edge[u][v]]);const T=[u,v,...I];
    for(const [a,b] of choose(T,2))if(a!==u||b!==v)clauses.push([-w,-edge[a][b]]);
  }
  clauses.push([-edge[u][v],...witnesses]);
}
if(chromaticCritical)for(let ei=0;ei<edges.length;ei++){
  const gate=edges[ei],color=Array.from({length:N},()=>Array.from({length:5},nv));
  for(let v=0;v<N;v++){
    clauses.push([-gate,...color[v]]);
    for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)clauses.push([-gate,-color[v][a],-color[v][b]]);
  }
  let fj=0;for(let u=0;u<N;u++)for(let v=u+1;v<N;v++,fj++)if(fj!==ei)
    for(let c=0;c<5;c++)clauses.push([-gate,-edges[fj],-color[u][c],-color[v][c]]);
}
atMost(edges,CAP);
if(FLOOR)atMost(edges.map(x=>-x),edges.length-FLOOR);
const sixes=[...choose(V,6)].map(S=>({S,q:[...choose(S,2)].map(([u,v])=>edge[u][v])}));
const sixIndex=new Map(sixes.map((z,i)=>[z.S.join(','),i]));
const A=V.slice(1,DEG+1),B=V.slice(DEG+1);
const constrained=new Set();
function writeCnf(){fs.writeFileSync(`${stem}.cnf`,[`p cnf ${variables} ${clauses.length}`,...clauses.map(c=>`${c.join(' ')} 0`)].join('\n')+'\n');}
if(process.argv.includes('--full')){
  for(let i=0;i<sixes.length;i++){
    for(const twelve of choose(sixes[i].q,12))clauses.push(twelve.map(x=>-x));
    constrained.add(i);
  }
  writeCnf();
  const run=spawnSync(solver,['--unsat',`${stem}.cnf`,`${stem}.drat`],{stdio:'inherit'});
  console.log(JSON.stringify({status:run.status===20?'UNSAT':run.status===10?'SAT':'UNKNOWN',N,ALPHA,CAP,variables,clauses:clauses.length,denseConstraints:constrained.size,cnf:`${stem}.cnf`,proof:run.status===20?`${stem}.drat`:null},null,2));
  process.exit(run.status??1);
}
for(let iteration=1;;iteration++){
  writeCnf();const run=spawnSync(solver,['--sat',`${stem}.cnf`],{encoding:'utf8',maxBuffer:64<<20});
  if(run.status===20){
    const proof=spawnSync(solver,['--unsat',`${stem}.cnf`,`${stem}.drat`],{stdio:'inherit'});
    if(proof.status!==20)throw new Error(`proof run exit ${proof.status}`);
    console.log(JSON.stringify({status:'UNSAT',N,ALPHA,CAP,iteration,variables,clauses:clauses.length,denseConstraints:constrained.size,cnf:`${stem}.cnf`,proof:`${stem}.drat`},null,2));process.exit(20);
  }
  if(run.status!==10)throw new Error(`scout exit ${run.status}: ${run.stderr}`);
  const truth=new Set();for(const line of run.stdout.split(/\n/))if(line.startsWith('v '))for(const z of line.slice(2).trim().split(/\s+/).map(Number))if(z>0)truth.add(z);
  const bad=[];for(let i=0;i<sixes.length;i++)if(!constrained.has(i)&&sixes[i].q.reduce((z,x)=>z+truth.has(x),0)>11)bad.push(i);
  console.error(JSON.stringify({iteration,bad:bad.length,constrained:constrained.size,variables,clauses:clauses.length}));
  if(!bad.length){console.log(JSON.stringify({status:'SAT',N,ALPHA,CAP,iteration,edges:edges.filter(x=>truth.has(x))},null,2));process.exit(10);}
  const add=new Set();
  for(const i of bad){const S=sixes[i].S,has0=S.includes(0),ac=S.filter(v=>A.includes(v)).length,bset=S.filter(v=>v>DEG).map(v=>v-(DEG+1));
    for(const aa of choose(A,ac))for(let shift=0;shift<B.length;shift++){
      const bb=bset.map(v=>DEG+1+(v+shift)%B.length),T=[...(has0?[0]:[]),...aa,...bb].sort((x,y)=>x-y);
      const j=sixIndex.get(T.join(','));if(j!==undefined&&!constrained.has(j))add.add(j);
    }}
  for(const i of add){for(const twelve of choose(sixes[i].q,12))clauses.push(twelve.map(x=>-x));constrained.add(i);}
}
