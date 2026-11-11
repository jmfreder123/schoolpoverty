import {readFileSync,writeFileSync} from 'fs';
import {feature} from 'topojson-client';
import {geoPath} from 'd3-geo';
const us=JSON.parse(readFileSync('node_modules/us-atlas/states-albers-10m.json'));
const p=geoPath();
const out={};
for(const f of feature(us,us.objects.states).features){
  const d=p(f).replace(/(\d+\.\d)\d+/g,'$1');
  const c=p.centroid(f), a=p.area(f), bb=p.bounds(f);
  out[f.id]={d,c:[Math.round(c[0]),Math.round(c[1])],a:Math.round(a),b:[bb[0][0],bb[0][1],bb[1][0],bb[1][1]].map(Math.round)};
}
writeFileSync('paths.json',JSON.stringify(out));
console.log(Object.keys(out).length, JSON.stringify(out).length);
