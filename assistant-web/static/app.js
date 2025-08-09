const $ = (id) => document.getElementById(id);

const eyeL = () => document.getElementById('eyeL');
const eyeR = () => document.getElementById('eyeR');
const lidL = () => document.getElementById('lidL');
const lidR = () => document.getElementById('lidR');

let targetX = 0, targetY = 0;
let offX = 0, offY = 0;
let nextSaccade = Date.now() + 2000 + Math.random()*2000;

function lerp(a,b,t){ return a + (b-a)*t; }

function animateEyes(){
  const now = Date.now();
  if(now > nextSaccade){
    targetX = (Math.random()*6-3);
    targetY = (Math.random()*4-2);
    nextSaccade = now + 2000 + Math.random()*3000;
  }
  offX = lerp(offX, targetX, 0.08);
  offY = lerp(offY, targetY, 0.08);

  const lx = 210 + offX;
  const ly = 270 + offY;
  const rx = 390 + offX;
  const ry = 270 + offY;

  eyeL().setAttribute('cx', lx);
  eyeL().setAttribute('cy', ly);
  eyeR().setAttribute('cx', rx);
  eyeR().setAttribute('cy', ry);

  requestAnimationFrame(animateEyes);
}

function blink(){
  // animate lids down and up
  const duration = 140; // ms
  const start = performance.now();
  function frame(t){
    const p = Math.min(1, (t - start)/duration);
    const ease = p*p*(3-2*p);
    const h = 84 * ease; // same as eye diameter
    lidL().setAttribute('height', h);
    lidR().setAttribute('height', h);
    if(p < 1) requestAnimationFrame(frame);
    else setTimeout(()=>{ // open
      const s2 = performance.now();
      function up(t2){
        const p2 = Math.min(1, (t2 - s2)/duration);
        const ease2 = 1 - (p2*p2*(3-2*p2));
        const h2 = 84 * ease2;
        lidL().setAttribute('height', h2);
        lidR().setAttribute('height', h2);
        if(p2 < 1) requestAnimationFrame(up);
      }
      requestAnimationFrame(up);
    }, 60);
  }
  requestAnimationFrame(frame);
}

setInterval(()=>{
  if(Math.random() < 0.2) blink();
}, 1500);

async function refresh(){
  try{
    const r = await fetch('/api/data');
    const d = await r.json();

    document.getElementById('time').textContent = d.time || '--:--';

    const co2El = document.getElementById('co2');
    co2El.textContent = `${d.co2} ppm`;
    if(d.co2 >= 1000) co2El.classList.add('warn'); else co2El.classList.remove('warn');

    document.getElementById('temp').textContent = `${d.temp.toFixed(0)} °C`;
    document.getElementById('bus').textContent = `${d.bus_in} min`;
    document.getElementById('meeting').textContent = d.meeting || '—';
  }catch(e){
    console.error(e);
  }
}

setInterval(refresh, 1200);
refresh();
animateEyes();
