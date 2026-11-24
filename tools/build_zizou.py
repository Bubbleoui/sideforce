import re,shutil,os,sys
SRC='/home/claude/sideforce/index.html';OUT='/home/claude/sideforce/zizou'
s=open(SRC,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:90]);s=s.replace(a,b)
def line(prefix,new):
    global s
    m=re.search(r'^'+re.escape(prefix)+r'.*$',s,re.M);assert m,prefix;s=s[:m.start()]+new+s[m.end():]

# ---- chemins / isolation des données ----
rep('<script src="vendor/supabase.js"></script>','<script src="../vendor/supabase.js"></script>')
rep('function col(name){\n  return{','function col(name0){var name="zz_"+name0;\n  return{')
rep('path=nid()+"."+ext','path="zz/"+nid()+"."+ext')
s=s.replace('"sf_','"zz_').replace("'sf_","'zz_").replace('"sf-board-"','"zz-board-"')

# ---- textes ----
rep('<title>SideForce Pipeline</title>','<title>Zizou Project</title>')
s=s.replace('aria-label="SideForce"','aria-label="Zizou Project"')
s=s.replace('SideForce Pipeline','Zizou Project').replace('" · SideForce"','" · Zizou Project"')
s=s.replace('onglet SideForce de Maya','onglet Zizou de Maya')
s=s.replace('Storyline — SIDE FORCE V2','Storyline — ZIZOU PROJECT').replace('Récap SIDE FORCE','Récap ZIZOU PROJECT').replace('"SIDE FORCE",0,0','"ZIZOU",0,0')
s=s.replace('storyline-sideforce.md','storyline-zizou.md').replace('preprod-sideforce.csv','preprod-zizou.csv')
s=s.replace('V2 · Pipeline','Pipeline de préprod')

# ---- palette : thèmes ----
m=re.search(r':root\{\n  --bg:#1f1f1f.*?color-scheme:dark;\n\}',s,re.S);assert m
s=s[:m.start()]+''':root{
  --bg:#0a1230; --panel:#101b44; --panel2:#16245a; --line:#2a3b7e;
  --ink:#ffffff; --mute:#9fb0e4; --lime:#ff4a3d; --on-lime:#ffffff; --black:#050a1f; --late:#ffb020;
  --font:'Roboto Condensed','Arial Narrow',Arial,sans-serif;
  --s0:#24367a; --tint:rgba(150,180,255,.05);
  --lg:linear-gradient(135deg,#ffffff 0%,#ffffff 38%,#ff8479 68%,#ff4a3d 100%);--lgglow:rgba(70,120,255,.5);
  color-scheme:dark;
}'''+s[m.end():]
line('html[data-theme="clair"]{--bg','html[data-theme="clair"]{--bg:#dde2f0;--panel:#eceff8;--panel2:#e2e7f4;--line:#bcc5df;--ink:#0f1a3d;--mute:#56628c;--lime:#d8281c;--on-lime:#ffffff;--black:#cdd4ea;--late:#b36b00;--s0:#b4bedb;--tint:rgba(15,26,61,.04);--lg:linear-gradient(135deg,#0f2a8a 0%,#0f2a8a 45%,#d8281c 100%);--lgglow:rgba(30,60,160,.18);color-scheme:light}')
line('@property --hue','@property --lime{syntax:"<color>";inherits:true;initial-value:#ff4a3d}\n@property --on-lime{syntax:"<color>";inherits:true;initial-value:#ffffff}')
line('html[data-theme="crazy"]{--bg','html[data-theme="crazy"]{--bg:#040a3a;--panel:#0a1470;--panel2:#101f8f;--line:#2f49d0;--ink:#ffffff;--mute:#b6c4ff;--black:#020624;--late:#ffcc33;--s0:#1b2fa8;--tint:rgba(255,255,255,.06);--lg:linear-gradient(100deg,#2f6bff,#ffffff,#ef4135,#ffffff,#2f6bff);--lgglow:rgba(239,65,53,.55);color-scheme:dark;animation:crzhue 7s linear infinite}')
line('@keyframes crzhue','@keyframes crzhue{0%,100%{--lime:#ff4a3d;--on-lime:#ffffff}33%{--lime:#ffffff;--on-lime:#0a1230}66%{--lime:#5b8dff;--on-lime:#ffffff}}')
rep('conic-gradient(from var(--ang),#ff2d95,#ffe14d,#38ff9c,#2dd4ff,#a45bff,#ff2d95)','conic-gradient(from var(--ang),#2f6bff,#ffffff,#ef4135,#ffffff,#2f6bff)')
for a,b in [('#ff2d95','#ef4135'),('#2dd4ff','#2f6bff'),('#a45bff','#ffffff'),('#ffe14d','#ffffff'),('#38ff9c','#2f6bff'),('rgba(255,45,149','rgba(239,65,53'),('rgba(45,212,255','rgba(47,107,255'),('rgba(164,91,255','rgba(255,255,255'),('rgba(56,255,156','rgba(47,107,255'),('rgba(255,80,220','rgba(239,65,53'),('rgba(255,120,255','rgba(255,255,255'),('#12002b','#040a3a'),('#ff3d81','#ffcc33'),('#fff6ff','#ffffff'),('#b9a3e6','#b6c4ff')]:
    s=s.replace(a,b)
# lime -> rouge coq
s=s.replace('rgba(198,244,50','rgba(255,74,61').replace('#c6f432','#ff4a3d').replace('#C6F432','#ff4a3d')
# palettes JS
line('var PCOLORS=','var PCOLORS=["#ff4a3d","#ffffff","#4d8dff","#ffd34d","#8fd8ff","#ff8a7d"];')
line('var MMCAT=','var MMCAT={"Personnage":"#8fd8ff","Lieu":"#ffd34d","Idée":"#ff4a3d","Thème":"#4d8dff","Autre":"#9db0e6"},MMAC=["#ff4a3d","#4d8dff","#ffffff","#ffd34d","#8fd8ff","#ff8a7d"];')
line('var FCOL=','var FCOL=[["","Sans couleur"],["#ff4a3d","Rouge"],["#4d8dff","Bleu"],["#ffffff","Blanc"],["#ffd34d","Or"],["#8fd8ff","Ciel"],["#ff8a7d","Corail"]];')
line('var DCOL=','var DCOL=["#ff4a3d","#4d8dff","#ffffff","#ffd34d","#8fd8ff","#ff8a7d","#c9d3f5","#8a8a8a"],DHL=["#fff176","#ff9a90","#ffd34d","#8fd8ff","#c9d3f5","#ffb3d9"];')
line('var PAL=','var PAL=["#ff4a3d","#ffffff","#4d8dff","#ffd34d","#8fd8ff","#ff8a7d","#c9d3f5","#8a8a8a","#000000"];')
line('var PLC=','var PLC=["#ff4a3d","#4d8dff","#ffd34d","#ffffff","#8a8a8a"],PEC=["#ff4a3d","#4d8dff","#ffd34d","#ffffff","#8fd8ff","#8a8a8a"];')
rep('["","#ffb84d","#ff4a3d"][i]','["","#ffd34d","#4d8dff"][i]')
line('var THEMES=','var THEMES=[["sombre","Nuit bleue","#0a1230","#ff4a3d"],["clair","Clair","#dde2f0","#d8281c"],["crazy","Crazy","#040a3a","#ef4135"]];')
# particules tricolores
rep('function fxColor(crazy){if(crazy)return "hsl("+Math.floor(Math.random()*360)+" 100% 62%)";','var FXPAL=["#ef4135","#ffffff","#2f6bff","#ff7a6e","#8fb0ff"];\nfunction fxColor(crazy){if(crazy)return FXPAL[Math.floor(Math.random()*FXPAL.length)];')
rep('fxBX.fillStyle="hsl("+Math.floor(p.h)+" 100% 62%)"','fxBX.fillStyle=FXPAL[Math.floor(p.h/72)%5]')
rep('a=[cs.getPropertyValue("--lime").trim()||"#ff4a3d",cs.getPropertyValue("--ink").trim()||"#fff"]','a=[cs.getPropertyValue("--lime").trim()||"#ff4a3d",cs.getPropertyValue("--ink").trim()||"#fff","#2f6bff"]')
rep('return a[Math.random()<.7?0:1]','return a[Math.floor(Math.random()*3)]')

# logo
rep('aspect-ratio:800/341','aspect-ratio:800/311')
# signature DA : titres blancs + liseré tricolore
SIG='''
/* ===== DA Zizou : tricolore ===== */
.top h1{color:var(--ink)}
.top h1::after{content:"";display:block;height:7px;width:132px;margin-top:12px;background:linear-gradient(90deg,#1d4fd8 0 33.3%,#ffffff 33.3% 66.6%,#ef4135 66.6%);box-shadow:0 0 14px -2px rgba(47,107,255,.7)}
html[data-theme="clair"] .top h1::after{background:linear-gradient(90deg,#1d4fd8 0 33.3%,#c9d2ee 33.3% 66.6%,#d8281c 66.6%);box-shadow:none}
.side::before{content:"";display:block;height:5px;margin:-1px 0 14px;background:linear-gradient(90deg,#1d4fd8 0 33.3%,#ffffff 33.3% 66.6%,#ef4135 66.6%)}
html[data-theme="clair"] .side::before{background:linear-gradient(90deg,#1d4fd8 0 33.3%,#c9d2ee 33.3% 66.6%,#d8281c 66.6%)}
.big{color:var(--ink)}.big small{color:var(--lime)}
'''
rep('html.noanim *,html.noanim *::before',SIG+'html.noanim *,html.noanim *::before')

rep('<meta name="theme-color" content="#1F1F1F">','<meta name="theme-color" content="#0a1230">')
# manifest / sw / icônes
os.makedirs(OUT+'/icons',exist_ok=True)
open(OUT+'/index.html','w',encoding='utf-8').write(s)
open(OUT+'/sw.js','w').write(open('/home/claude/sideforce/sw.js').read().replace('"sf-v1"','"zz-v1"'))
open(OUT+'/manifest.webmanifest','w').write('''{
  "name": "Zizou Project",
  "short_name": "Zizou",
  "description": "Pipeline de préproduction Zizou Project",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#0a1230",
  "theme_color": "#0a1230",
  "lang": "fr",
  "icons": [
    {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
    {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
    {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
''')
shutil.copy('/home/claude/zz-build/logo.png',OUT+'/icons/logo.png')
print('built',len(s))
