/* Local-only visual editor for index.html.
 Loaded by the page only when it is served from localhost, and never
 requested on a deployed host. Saves through serve.py. */
(function(){
"use strict";
var A=window.__kb;
if(!A){ console.warn("editor.js: page hook missing"); return; }

var nodes=A.nodes, nodeById=A.nodeById, LAYOUT=A.LAYOUT, CONTENT=A.CONTENT,
  layout=A.layout, stage=A.stage, wires=A.wires, arcsEl=A.arcsEl,
  paintWires=A.paintWires, redrawArcs=A.redrawArcs, dlg=A.dlg, openDetail=A.openDetail,
  hubH1=A.hub.h1, hubRole=A.hub.role, hubBio=A.hub.bio;
var editing=false;

/* the toolbar is built here, so it is absent from a deployed index.html */
var bar=document.createElement("div");
bar.className="editbar"; bar.id="editbar";
bar.innerHTML='<button id="modeBtn" type="button">Edit</button>'+
'<button id="saveBtn" class="primary" type="button" hidden>Save</button>'+
'<button id="resetBtn" type="button" hidden>Reset layout</button>'+
'<span class="st" id="editSt"></span>';
document.body.appendChild(bar);

/* ================= local editor =================
 Only wired up when the page is served from localhost. Drag to move,
 the right handle resizes, the top handle rotates, and every bit of
 text becomes editable. Save posts to serve.py, which writes
 layout.json and content.json next to this file. */

document.body.classList.add("has-editor");
var modeBtn=document.getElementById("modeBtn"),
    saveBtn=document.getElementById("saveBtn"),
    resetBtn=document.getElementById("resetBtn"),
    editSt=document.getElementById("editSt");

var EDITABLE=[[hubH1,"name"],[hubRole,"role"],[hubBio,"bio"]];

function setEditing(on){
  editing=on; A.setEditing(on);
  document.body.classList.toggle("editing",on);
  modeBtn.textContent=on?"Preview":"Edit";
if(!on&&dlg.open){ dlg.close ? dlg.close() : dlg.removeAttribute("open"); }
  saveBtn.hidden=!on; resetBtn.hidden=!on;
  editSt.textContent=on?"drag / resize / retype":"";
  EDITABLE.forEach(function(p){ p[0].contentEditable=on?"true":"false"; });
  nodes.forEach(function(n){
    ["nm","rl","wh"].forEach(function(cls){
      var el=n.el.querySelector("."+cls);
      if(el) el.contentEditable=on?"true":"false";
    });
  });
}
modeBtn.addEventListener("click",function(){ setEditing(!editing); });

document.getElementById("cards").addEventListener("click",function(ev){
  var pen=ev.target.closest(".editbtn");
  if(!pen||!editing) return;
  ev.stopPropagation();
  var card=pen.closest(".card");
  openDetail(card.dataset.id, card, true);
});

/* --- drag, resize, rotate --- */
var drag=null;
document.getElementById("cards").addEventListener("mousedown",function(ev){
  if(!editing) return;
  var card=ev.target.closest(".card"); if(!card) return;
  if(ev.target.isContentEditable) return;
  if(ev.target.closest(".editbtn")) return;
  var n=nodeById(card.dataset.id); if(!n) return;
  var h=ev.target.closest(".handle");
  drag={n:n,mode:h?h.dataset.h:"move",sx:ev.clientX,sy:ev.clientY,
        ox:n.x,oy:n.y,ow:n.w,orot:n.rot};
  ev.preventDefault();
});
window.addEventListener("mousemove",function(ev){
  if(!drag) return;
  var n=drag.n, dx=ev.clientX-drag.sx, dy=ev.clientY-drag.sy;
  if(drag.mode==="move"){ n.x=drag.ox+dx; n.y=drag.oy+dy; }
  else if(drag.mode==="w"){
    n.el.style.width=Math.max(150,Math.min(460,drag.ow+dx))+"px";
    n.w=n.el.offsetWidth; n.h=n.el.offsetHeight;
  } else {
    var r=n.el.getBoundingClientRect();
    var a=Math.atan2(ev.clientY-(r.top+r.height/2), ev.clientX-(r.left+r.width/2));
    n.rot=Math.max(-45,Math.min(45,a*180/Math.PI+90));
  }
  n.pinned=true;
  place(n); redrawWires();
});
window.addEventListener("mouseup",function(){ if(drag){ drag=null; drawArcsNow(); } });

function place(n){
  n.el.style.left=Math.round(n.x-n.w/2)+"px";
  n.el.style.top=Math.round(n.y-n.h/2)+"px";
  n.el.style.transform="rotate("+n.rot.toFixed(2)+"deg)";
}
function redrawWires(){
  var W=stage.clientWidth,H=stage.clientHeight,cx=W/2,cy=H/2;
  var hubEl=document.querySelector(".hub");
  var hw=hubEl.offsetWidth/2, hh=hubEl.offsetHeight/2, out="";
  nodes.forEach(function(n){
    var dx=n.x-cx, dy=n.y-cy, len=Math.hypot(dx,dy)||1;
    function edge(hw,hh,inset){
      var ax=Math.abs(dx),ay=Math.abs(dy);
      return Math.min(ax>0.001?hw/ax:1e9, ay>0.001?hh/ay:1e9)+inset/len;
    }
    var t1=edge(hw,hh,7), t2=edge(n.w/2,n.h/2,7);
    var x1=cx+dx*t1,y1=cy+dy*t1,x2=n.x-dx*t2,y2=n.y-dy*t2;
    if((x2-x1)*dx+(y2-y1)*dy>0)
      out+='<line data-cat="'+n.e.cat+'" x1="'+x1.toFixed(1)+'" y1="'+y1.toFixed(1)+
           '" x2="'+x2.toFixed(1)+'" y2="'+y2.toFixed(1)+'"></line>';
  });
  wires.innerHTML=out; paintWires();
}
function drawArcsNow(){ redrawArcs(); }

/* --- drag the section labels; hold shift to rotate --- */
var adrag=null;
arcsEl.addEventListener("mousedown",function(ev){
  if(!editing) return;
  var el=ev.target.closest(".arc"); if(!el) return;
  var W=stage.clientWidth,H=stage.clientHeight;
  var r=el.getBoundingClientRect(), sr=stage.getBoundingClientRect();
  var cur=(LAYOUT.arcs||{})[el.dataset.cat]||{};
  var rotating=!!ev.target.closest(".arc-h");
  adrag={el:el,cat:el.dataset.cat,sx:ev.clientX,sy:ev.clientY,rot:rotating,
         ox:(r.left-sr.left)+r.width/2, oy:(r.top-sr.top)+r.height/2,
         orot:(typeof cur.rot==="number")?cur.rot:currentRot(el), W:W, H:H};
  ev.preventDefault();
});
function currentRot(el){
  var m=/rotate\(([-0-9.]+)deg\)/.exec(el.style.transform||"");
  return m?parseFloat(m[1]):0;
}
window.addEventListener("mousemove",function(ev){
  if(!adrag) return;
  LAYOUT.arcs=LAYOUT.arcs||{};
  var o=LAYOUT.arcs[adrag.cat]=LAYOUT.arcs[adrag.cat]||{};
  if(adrag.rot||ev.shiftKey){
    o.rot=+(adrag.orot+(ev.clientX-adrag.sx)*0.5).toFixed(1);
    o.fx=+(adrag.ox/adrag.W).toFixed(4); o.fy=+(adrag.oy/adrag.H).toFixed(4);
  }else{
    o.fx=+(((adrag.ox+ev.clientX-adrag.sx))/adrag.W).toFixed(4);
    o.fy=+(((adrag.oy+ev.clientY-adrag.sy))/adrag.H).toFixed(4);
    o.rot=+adrag.orot.toFixed(1);
  }
  drawArcsNow();
});
window.addEventListener("mouseup",function(){ adrag=null; });

/* --- save / reset --- */
function collect(){
  var W=stage.clientWidth,H=stage.clientHeight;
  var cards={};
  nodes.forEach(function(n){
    if(!n.pinned) return;
    cards[n.e.id]={fx:+(n.x/W).toFixed(4),fy:+(n.y/H).toFixed(4),
                   w:Math.round(n.el.offsetWidth/A.cardScale()),
                   rot:+n.rot.toFixed(2)};
  });
  var ctext={};
  nodes.forEach(function(n){
    /* start from anything the modal editor already set, then take the
       card-face text straight from the DOM */
    var o=Object.assign({},(CONTENT.cards||{})[n.e.id]||{});
    [["nm","name"],["rl","role"],["wh","when"]].forEach(function(p){
      var el=n.el.querySelector("."+p[0]);
      if(el) o[p[1]]=el.innerHTML.trim();
    });
    ctext[n.e.id]=o;
  });
  return {
    layout:{cards:cards,arcs:(LAYOUT.arcs||{})},
    content:{hub:{name:hubH1.innerHTML.trim(),role:hubRole.innerHTML.trim(),
                  bio:hubBio.innerHTML.trim()},cards:ctext}
  };
}
saveBtn.addEventListener("click",function(){
  editSt.textContent="saving...";
  fetch("/api/save",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify(collect())})
    .then(function(r){ return r.ok?r.json():Promise.reject(r.status); })
    .then(function(){ editSt.textContent="saved to json"; setTimeout(function(){
      if(editing) editSt.textContent="drag / resize / retype"; },1800); })
    .catch(function(err){ editSt.textContent="save failed ("+err+")"; });
});
resetBtn.addEventListener("click",function(){
  LAYOUT.cards={}; LAYOUT.arcs={};
  nodes.forEach(function(n){ n.pinned=false; n.el.style.width=""; });
  layout();
  editSt.textContent="layout reset (not yet saved)";
});
})();
