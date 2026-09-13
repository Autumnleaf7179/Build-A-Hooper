"""Runtime edits for the captured game bundle.

The imported JavaScript is a single minified Next.js chunk rather than source
code. Keeping these small, checked replacements separate makes the offline
behavior editable without rewriting the downloaded bundle.
"""


CHUNK_NAME = "11mz9sgpnk78r.js"


def patch_game_chunk(document):
    replacements = [
        (
            'function a5(e){if(!e)return e_();for(let a=0;a<20;a+=1){let a=e_();if(a.id!==e)return a}let a=eh().filter(a=>a.id!==e);if(0===a.length)return e_();let r=Math.floor(Math.random()*a.length);return a[r]}',
            '''let offlineTeamRollHistory=[],offlinePendingAttributes=null,offlineNavigatePosition=null;function a5(e,a){let r=eh().filter(a=>a.id!==e);if(0===r.length)return e_();let s=new Map;for(let e of offlineTeamRollHistory){let a=e.franchiseId??e.id;s.set(a,(s.get(a)??0)+1)}let t=r.map(e=>{let a=s.get(e.franchiseId??e.id)??0;return{item:e,weight:1/(1+a)}}),i=Math.random()*t.reduce((e,a)=>e+a.weight,0),o=t[t.length-1].item;for(let e of t)if((i-=e.weight)<=0){o=e.item;break}return a&&offlineTeamRollHistory.push(o),o}''',
        ),
        (
            'I(a5(a));let r=a5(a),s=window.setInterval(()=>{I(a5(a))},140)',
            'I(a5(a));let r=a5(a,!0),s=window.setInterval(()=>{I(a5(a))},140)',
        ),
        (
            'function rb(){v(null),w(null),H(null),J([]),Y([]),q(null),Q(null),ea(null),ei(!1),en(null),ed(null),ep(0),eP(null),eD(0),eb(!1),eA(!1),ef(!1),eC(null),eM(null),ej([]),eU(null),_("idle"),h("PG"),I(null),F("idle"),g(0),T(null),x("idle")}',
            'function rb(){offlineTeamRollHistory=[],offlinePendingAttributes=null,v(null),w(null),H(null),J([]),Y([]),q(null),Q(null),ea(null),ei(!1),en(null),ed(null),ep(0),eP(null),eD(0),eb(!1),eA(!1),ef(!1),eC(null),eM(null),ej([]),eU(null),_("idle"),h("PG"),I(null),F("idle"),g(0),T(null),x("idle")}',
        ),
        (
            'onClick:function(){if(r){if(rb(),g(a8(r)),"classic"===r){u(null),a("positionSelect");return}if("blind"===r){u(null),_("idle"),a("positionRoll");return}u(null),a("build")}}',
            'onClick:function(){if(r){rb(),g(a8(r)),u(null),_("idle"),a("build")}}',
        ),
        (
            'function rf(){r&&("chaos"===r||null!==p)&&(rb(),g(a8(r)),a("build"))}',
            '''function offlineFinalizeBuild(e,a){let r=o[a]??o.PG,s=0,t=0;for(let[a,i]of Object.entries(r))s+=l(e.find(e=>e.attribute===a))*i,t+=i;let i=0===t?25:n(Math.round(s/t)),c="PG"===a||"SG"===a?"All-Around Guard":"SF"===a?"All-Around Wing":"PF"===a?"All-Around Forward":"Interior Anchor";return{position:a,overall:i,archetype:{name:c,description:"A balanced offline build shaped by your drafted attributes."},ratings:Object.fromEntries(e.map(e=>[e.attribute,Math.round(e.ratingValue??i)]))}}function rf(){if(r&&p){if(offlinePendingAttributes){q(offlineFinalizeBuild(offlinePendingAttributes,p));offlinePendingAttributes=null}g(a8(r)),a("teamReveal")}}''',
        ),
        (
            'a.length>=i.length){let e,s,t;',
            'a.length>=i.length){offlinePendingAttributes=a,offlineNavigatePosition("positionSelect");return}if(a.length>=i.length){let e,s,t;',
        ),
        (
            '[ai,ao]=(0,t.useState)(null),an=(0,t.useMemo)',
            '[ai,ao]=(0,t.useState)(null),offlineNavigatePosition=a,an=(0,t.useMemo)',
        ),
        (
            'children:"Classic Mode"',
            'children:"Position Selection"',
        ),
        (
            'Classic gives you full control before the build room opens. Choose your position, then start spinning.',
            'Choose your position after drafting all 13 attributes, then start your career team spin.',
        ),
    ]

    for old, new in replacements:
        if old not in document:
            raise RuntimeError(f"Expected game bundle text was not found: {old[:80]}")
        document = document.replace(old, new, 1)
    return document