"""Runtime edits for the captured game bundle.

The imported JavaScript is a single minified Next.js chunk rather than source
code. These focused transformations keep the downloaded capture intact while
adding the local data layer and offline game behavior.
"""

import re


CHUNK_NAME = "11mz9sgpnk78r.js"


ATTRIBUTES = [
    ("3PT", "Three-Point Shooting", "Three-point shooting.", "shooting"),
    ("MID", "Midrange", "Midrange scoring.", "shooting"),
    ("FIN", "Finishing", "Finishing around the rim.", "finishing"),
    ("DNK", "Dunking", "Dunks, contact, and rim pressure.", "finishing"),
    ("HAN", "Ball Handle", "Dribbling and ball control.", "playmaking"),
    ("PAS", "Passing", "Passing and play creation.", "playmaking"),
    ("CVIS", "Court Vision", "Sees passing windows before they open.", "playmaking"),
    ("OBIQ", "Offensive On-Ball IQ", "Reads and decisions with the ball.", "mental"),
    ("OFIQ", "Offensive Off-Ball IQ", "Spacing, cutting, screening, and movement.", "mental"),
    ("PDEF", "Perimeter Defense", "Point-of-attack defense and pressure.", "defense"),
    ("PDIQ", "Perimeter Defensive IQ", "Screen navigation and perimeter positioning.", "mental"),
    ("IDEF", "Interior Defense", "Paint defense and post resistance.", "defense"),
    ("IDIQ", "Interior Defensive IQ", "Help, rotations, and interior positioning.", "mental"),
    ("DBIQ", "Defensive On-Ball IQ", "On-ball reads and defensive decisions.", "mental"),
    ("DFIQ", "Defensive Off-Ball IQ", "Rotations, help defense, and communication.", "mental"),
    ("BLK", "Blocks", "Rim protection and blocks.", "defense"),
    ("REB", "Rebounding", "Offensive and defensive rebounding.", "defense"),
    ("ATH", "Athleticism", "Speed, explosiveness, agility, and vertical.", "physical"),
    ("STR", "Strength / Physicality", "Strength, contact, and physical presence.", "physical"),
    ("HGT", "Height", "Size and positional length.", "physical"),
    ("WGT", "Weight", "Mass and physical presence.", "physical"),
    ("END", "Injury Risk / Endurance", "Availability, stamina, and fatigue resistance.", "physical"),
    ("WRK", "Work Rate", "Effort, activity, and consistency.", "mental"),
    ("CLU", "Clutch / IQ", "Decision-making and late-game consistency.", "mental"),
]


def _attribute_js():
    return ",".join(
        '{key:"%s",name:"%s",shortName:"%s",description:"%s",category:"%s"}'
        % (key, name, key, description, category)
        for key, name, description, category in ATTRIBUTES
    )


def _generated_ratings_js():
    keys = ",".join(
        '"%s":f("%s")' % (key, key) for key, *_ in ATTRIBUTES
    )
    return (
        'function u(e,a,r={}){let s=p[a]??p.PG,t=Math.round((e-78)*.55),'
        'f=k=>c(r[k]??s[k]??65+t,35,99);return{%s}}' % keys
    )


def _replace(document, pattern, replacement, description):
    updated, count = re.subn(pattern, replacement, document, count=1)
    if count != 1:
        raise RuntimeError(f"Expected game bundle section was not found: {description}")
    return updated


def patch_game_chunk(document):
    document = _replace(
        document,
        r'let i=\[.*?\];i\.map\(e=>e\.key\);',
        'let offlineDatabase=globalThis.__OFFLINE_DATABASE__??{},i=offlineDatabase.attributes?.length?offlineDatabase.attributes:[%s];i.map(e=>e.key);'
        % _attribute_js(),
        "attribute definitions",
    )
    document = _replace(
        document,
        r'function u\(e,a,r=\{\}\)\{.*?return\{.*?\}\}',
        _generated_ratings_js(),
        "player rating generator",
    )
    document = _replace(
        document,
        r'(let P=\[.*?\];)function h',
        r'\1P=P.map(e=>{let a=(offlineDatabase.players??[]).find(a=>a.id===e.playerId||a.id===e.id);return a?{...e,attributes:{...e.attributes,...(a.attributes??{})}}:e});function h',
        "classic player data hook",
    )
    document = document.replace(
        'let q=V([...E,{',
        'let q=V([...E,...(offlineDatabase.teams?.franchises??[]),{',
        1,
    )
    document = _replace(
        document,
        r'(,Z=V\(\[.*?)(\]\)),Q=V\(\[',
        r'\1,...(offlineDatabase.teams?.teamSeasons??[])\2,Q=V([',
        "team-season data hook",
    )
    document = _replace(
        document,
        r'function a5\(e\)\{if\(!e\)return e_\(\);for\(let a=0;a<20;a\+=1\)\{.*?return a\[r\]\}',
        'let offlineTeamRollHistory=[],offlinePendingAttributes=null,offlineNavigatePosition=null;function a5(e,a){let r=eh().filter(a=>a.id!==e);if(0===r.length)return e_();let s=new Map;for(let e of offlineTeamRollHistory){let a=e.franchiseId??e.id;s.set(a,(s.get(a)??0)+1)}let t=r.map(e=>{let a=s.get(e.franchiseId??e.id)??0;return{item:e,weight:1/(1+a)}}),i=Math.random()*t.reduce((e,a)=>e+a.weight,0),o=t[t.length-1].item;for(let e of t)if((i-=e.weight)<=0){o=e.item;break}return a&&offlineTeamRollHistory.push(o),o}',
        "weighted team roulette",
    )
    document = document.replace(
        'I(a5(a));let r=a5(a),s=window.setInterval(()=>{I(a5(a))},140)',
        'I(a5(a));let r=a5(a,!0),s=window.setInterval(()=>{I(a5(a))},140)',
        1,
    )
    document = document.replace(
        'function rb(){v(null),w(null),H(null),J([]),Y([]),q(null),Q(null),ea(null),ei(!1),en(null),ed(null),ep(0),eP(null),eD(0),eb(!1),eA(!1),ef(!1),eC(null),eM(null),ej([]),eU(null),_("idle"),h("PG"),I(null),F("idle"),g(0),T(null),x("idle")}',
        'function rb(){offlineTeamRollHistory=[],offlinePendingAttributes=null,v(null),w(null),H(null),J([]),Y([]),q(null),Q(null),ea(null),ei(!1),en(null),ed(null),ep(0),eP(null),eD(0),eb(!1),eA(!1),ef(!1),eC(null),eM(null),ej([]),eU(null),_("idle"),h("PG"),I(null),F("idle"),g(0),T(null),x("idle")}',
        1,
    )
    document = document.replace(
        'onClick:function(){if(r){if(rb(),g(a8(r)),"classic"===r){u(null),a("positionSelect");return}if("blind"===r){u(null),_("idle"),a("positionRoll");return}u(null),a("build")}}',
        'onClick:function(){if(r){rb(),g(a8(r)),u(null),_("idle"),a("build")}}',
        1,
    )
    document = document.replace(
        'function rf(){r&&("chaos"===r||null!==p)&&(rb(),g(a8(r)),a("build"))}',
        'function offlineFinalizeBuild(e,a){let r=o[a]??o.PG,s=0,t=0;for(let[a,i]of Object.entries(r))s+=l(e.find(e=>e.attribute===a))*i,t+=i;let i=0===t?25:n(Math.round(s/t)),c="PG"===a||"SG"===a?"All-Around Guard":"SF"===a?"All-Around Wing":"PF"===a?"All-Around Forward":"Interior Anchor";return{position:a,overall:i,archetype:{name:c,description:"A balanced offline build shaped by your drafted attributes."},ratings:Object.fromEntries(e.map(e=>[e.attribute,Math.round(e.ratingValue??i)]))}}function rf(){if(r&&p){if(offlinePendingAttributes){q(offlineFinalizeBuild(offlinePendingAttributes,p));offlinePendingAttributes=null}g(a8(r)),a("teamReveal")}}',
        1,
    )
    document = document.replace(
        'a.length>=i.length){let e,s,t;',
        'a.length>=i.length){offlinePendingAttributes=a,offlineNavigatePosition("positionSelect");return}if(a.length>=i.length){let e,s,t;',
        1,
    )
    document = document.replace(
        '[ai,ao]=(0,t.useState)(null),an=(0,t.useMemo)',
        '[ai,ao]=(0,t.useState)(null),offlineNavigatePosition=a,an=(0,t.useMemo)',
        1,
    )
    document = document.replace('children:"Classic Mode"', 'children:"Position Selection"', 1)
    document = document.replace(
        'Classic gives you full control before the build room opens. Choose your position, then start spinning.',
        'Draft all attributes first, then choose your position and start your career team spin.',
        1,
    )
    return document