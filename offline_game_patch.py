"""Runtime edits for the captured game bundle.

The imported JavaScript is a single minified Next.js chunk rather than source
code. These focused transformations keep the downloaded capture intact while
adding the local data layer and offline game behavior.
"""

import re


CHUNK_NAME = "11mz9sgpnk78r.js"


ATTRIBUTES = [
    ("SPD", "Speed", "Straight-line movement speed.", "Athleticism"),
    ("ACC", "Acceleration", "How quickly the player reaches top speed.", "Athleticism"),
    ("EXP", "Explosiveness", "Burst, force production, and first-step pop.", "Athleticism"),
    ("STR", "Strength", "Force, contact balance, and physical presence.", "Athleticism"),
    ("VRT", "Vertical", "Vertical lift and jumping ability.", "Athleticism"),
    ("AGI", "Agility", "Change of direction and body control.", "Athleticism"),
    ("STA", "Stamina", "Ability to maintain effort over time.", "Athleticism"),
    ("DUR", "Durability", "Availability and resistance to injury.", "Athleticism"),
    ("PAC", "Pass Accuracy", "Technical accuracy on passes.", "Playmaking"),
    ("PVIS", "Pass Vision", "Sees passing windows and open teammates.", "Playmaking"),
    ("PIQ", "Pass IQ", "Makes the correct passing decision.", "Playmaking"),
    ("SWB", "Speed with Ball", "Movement speed while dribbling.", "Playmaking"),
    ("CAWR", "Court Awareness", "Awareness of spacing, timing, and game context.", "Playmaking"),
    ("HDL", "Handles", "Dribble control under pressure.", "Playmaking"),
    ("SCR", "Screens", "Quality and timing as a screener.", "Playmaking"),
    ("BSEC", "Ball Security", "Protects the ball from pressure and traps.", "Playmaking"),
    ("PFIN", "Passing Finesse", "Touch, disguise, and precision on difficult passes.", "Playmaking"),
    ("OMAN", "Offensive Manipulation", "Manipulates defenders and creates advantages.", "Playmaking"),
    ("DMAN", "Defensive Manipulation", "Manipulates defensive positioning and matchups.", "Playmaking"),
    ("DRM", "Dribble Mechanics", "Efficiency and variety of dribble moves.", "Playmaking"),
    ("LOB", "Lobs", "Accuracy and timing on lob passes.", "Playmaking"),
    ("ALY", "Alley-oops", "Finishes and delivers alley-oop plays.", "Playmaking"),
    ("PST", "Post Control", "Creates and protects position in the post.", "Playmaking"),
    ("FBR", "Fast Break", "Decision-making and execution in transition.", "Playmaking"),
    ("HKS", "Hook shots", "Touch and accuracy on hook shots.", "Scoring"),
    ("DNK", "Dunks", "Power and variety finishing above the rim.", "Scoring"),
    ("LAY", "Lay ups", "Accuracy on layups and close finishes.", "Scoring"),
    ("FLO", "Floaters", "Touch on floaters and runners.", "Scoring"),
    ("CTS", "Contested Shots", "Shot-making through defensive pressure.", "Scoring"),
    ("FT", "Free Throws", "Accuracy at the free-throw line.", "Scoring"),
    ("3PCS", "Three-Point Catch-and-Shoot", "Three-point shooting off the catch.", "Scoring"),
    ("3POD", "Three-Point Off-The-Dribble", "Three-point shooting off the dribble.", "Scoring"),
    ("MROD", "Mid-Range Off-The-Dribble", "Midrange creation off the dribble.", "Scoring"),
    ("MRCS", "Mid-Range Catch-and-Shoot", "Midrange shooting off the catch.", "Scoring"),
    ("STD", "Standing Dunk", "Two-foot power finishes from a standstill.", "Scoring"),
    ("SCT", "Scoring Technique", "Footwork, touch, and scoring craft.", "Scoring"),
    ("DFIN", "Driving Finishing", "Finishing ability on drives.", "Scoring"),
    ("PFD", "Post Fade", "Fadeaway scoring from the post.", "Scoring"),
    ("POTS", "Post Shots", "General shot-making from the post.", "Scoring"),
    ("FOUL", "Draw Foul", "Ability to force defensive fouls.", "Scoring"),
    ("SQ", "Shot IQ", "Selects efficient shots for the situation.", "Scoring"),
    ("FNS", "Finese shot", "Touch and finesse on difficult shots.", "Scoring"),
    ("DIQ", "Defensive IQ", "Overall reads of the play and game.", "Mental"),
    ("DBOIQ", "Defensive On-Ball IQ", "Reads and decisions while defending the ball.", "Mental"),
    ("DFOIQ", "Defensive Off-Ball IQ", "Reads and decisions away from the ball.", "Mental"),
    ("IDIQ", "Defensive Interior IQ", "Defensive reads in the paint.", "Mental"),
    ("PDIQ", "Defensive Perimeter IQ", "Defensive reads on the perimeter.", "Mental"),
    ("HLPQ", "Help Defense IQ", "Timing and decisions as a help defender.", "Mental"),
    ("DCMP", "Defensive Composure", "Poise and discipline on defense.", "Mental"),
    ("OCMP", "Offensive Composure", "Poise and decision-making on offense.", "Mental"),
    ("OFOIQ", "Offensive Off-Ball IQ", "Reads, cuts, and decisions away from the ball.", "Mental"),
    ("OFBIQ", "Offensive On-Ball IQ", "Reads and decisions with the ball.", "Mental"),
    ("OIQ", "Offensive IQ", "Overall offensive reads and decisions.", "Mental"),
    ("CON", "Consistency", "Reliability from game to game.", "Mental"),
    ("CONF", "Confidence", "Belief and assertiveness in key moments.", "Mental"),
    ("TMW", "Teamwork", "Connects actions to team success.", "Mental"),
    ("COM", "Competitiveness", "Competes through pressure and adversity.", "Mental"),
    ("LED", "Leadership", "Raises teammates and organizes the group.", "Mental"),
    ("CLT", "Clutch Ability", "Execution in high-leverage moments.", "Mental"),
    ("OWRK", "Offensive Work rate", "Effort and activity on offense.", "Mental"),
    ("DWRK", "Defensive Work Rate", "Effort and activity on defense.", "Mental"),
    ("HUS", "Hustle", "Extra effort, loose balls, and second actions.", "Mental"),
    ("STL", "Steals", "Creates steals and deflections.", "Defending"),
    ("BLK", "Blocks", "Rim protection and blocks.", "Defending"),
    ("IDEF", "Interior Defense", "Paint defense and post resistance.", "Defending"),
    ("PDEF", "Perimeter Defense", "Point-of-attack defense and pressure.", "Defending"),
    ("DPOS", "Defensive Positioning", "Stays in the right defensive position.", "Defending"),
    ("PIN", "Pass Interception", "Anticipates and intercepts passes.", "Defending"),
    ("HELP", "Help Defense", "Provides timely support to teammates.", "Defending"),
    ("SNAV", "Screen Navigation", "Fights over, under, and around screens.", "Defending"),
    ("DTECH", "Defensive Technique", "Fundamental defensive execution.", "Defending"),
    ("ONBD", "On-Ball Defense", "Defends the player with the ball.", "Defending"),
    ("OFBD", "Off-Ball Defense", "Defends away from the ball.", "Defending"),
    ("OREB", "Offensive Rebounds", "Creates extra possessions on offense.", "Rebounding"),
    ("DREB", "Defensive Rebounds", "Ends possessions with defensive rebounds.", "Rebounding"),
    ("RIQ", "Rebounding IQ", "Reads the ball and finds rebounding position.", "Rebounding"),
    ("BOX", "Box Out", "Seals opponents away from the rebound.", "Rebounding"),
    ("REFF", "Rebounding Effort", "Pursuit and second-effort rebounding.", "Rebounding"),
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