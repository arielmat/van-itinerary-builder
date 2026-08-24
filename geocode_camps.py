import json, urllib.request, urllib.parse, time, sys

SRC='/Users/ariel/Downloads/campgrounds_guatemala_mexico.json'
OUT='/Users/ariel/ca-van-router/camps_mx_gt.js'
PROG='/private/tmp/claude-501/-Users-ariel/063d445c-2e4a-47f3-9af2-492b60056023/scratchpad/geocode_progress.txt'

d=json.load(open(SRC))
places=d['places']
out=[]

def add(p, lat, lon, src):
    fac=p.get('facilities') or []
    desc=(p.get('description') or '').strip()
    if len(desc)>160: desc=desc[:157]+'...'
    out.append({
        "lat":round(float(lat),5),"lon":round(float(lon),5),
        "name":p['name'],"country":p['country'],
        "verified":p.get('verified',''),
        "facilities":fac[:8],"desc":desc,"src":src
    })

# keep already-geocoded
todo=[]
for p in places:
    loc=p.get('location')
    if loc and loc.get('lat') is not None:
        add(p, loc['lat'], loc['lon'], 'dataset')
    else:
        todo.append(p)

kept0=len(out)
hits=0; miss=0
for i,p in enumerate(todo):
    q=urllib.parse.quote(f"{p['name']} {p['country']}")
    cc='gt' if p['country']=='Guatemala' else 'mx'
    url=f"https://photon.komoot.io/api/?q={q}&limit=1&lat=19&lon=-99"
    try:
        req=urllib.request.Request(url, headers={'User-Agent':'overland-van-router/1.0'})
        r=json.load(urllib.request.urlopen(req, timeout=15))
        feats=r.get('features',[])
        if feats and (feats[0]['properties'].get('countrycode','').lower()==cc):
            c=feats[0]['geometry']['coordinates']
            add(p, c[1], c[0], 'photon'); hits+=1
        else:
            miss+=1
    except Exception:
        miss+=1
    if i%25==0:
        open(PROG,'w').write(f"{i}/{len(todo)} geocoded, hits={hits} miss={miss}\n")
    time.sleep(0.5)

# write JS
with open(OUT,'w') as f:
    f.write("/* iOverlander established campgrounds, Guatemala + Mexico.\n")
    f.write(f"   {kept0} from dataset coords + {hits} recovered via Photon (GT/MX filtered). */\n")
    f.write("const MX_GT_CAMPS = ")
    json.dump(out, f, ensure_ascii=False)
    f.write(";\n")
open(PROG,'w').write(f"DONE {len(out)} camps ({kept0} dataset + {hits} photon), miss={miss}\n")
