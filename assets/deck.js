(function(){
  'use strict';
  const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const stage=$('#stage'), telas=$$('.tela'), wipe=$('#wipe'), prog=$('#prog i'), cont=$('#cont'), capTxt=$('#capTxt');
  const SVGNS='http://www.w3.org/2000/svg';
  // ?pdf=1: cada tela já no estado final, sem transição nem temporizador (usado para gerar o PDF)
  const modoPdf=new URLSearchParams(location.search).has('pdf');
  if(modoPdf)document.documentElement.classList.add('pdf');
  const reduz=matchMedia('(prefers-reduced-motion: reduce)').matches||modoPdf;
  let atual=0, escalaAtual=1, emTransicao=false, pendente=null;
  const total=telas.length, dd=n=>String(n).padStart(2,'0');
  const autos={};let autoAtivos=[]; // temporizador dos botões (ver mais abaixo)

  /* ---------------------------------------------------------- miolo: o conteúdo de cada tela encolhe por igual, centralizado,
     e o fundo continua ocupando a tela inteira (o que tem a classe sangra fica fora do miolo) */
  telas.forEach(t=>{
    const m=document.createElement('div');m.className='miolo';
    [...t.childNodes].forEach(n=>{if(!(n.nodeType===1&&n.classList.contains('sangra')))m.appendChild(n);});
    t.appendChild(m);
  });

  /* ---------------------------------------------------------- palco */
  function escala(){
    escalaAtual=Math.min(innerWidth/1600,innerHeight/900);
    stage.style.transform='scale('+escalaAtual+')';
  }
  addEventListener('resize',escala);escala();

  /* ---------------------------------------------------------- contadores */
  function contar(el){
    const alvo=parseFloat(el.dataset.conta),casas=+el.dataset.casas||0,t0=performance.now(),dur=1300;
    const fmt=new Intl.NumberFormat('pt-BR',{minimumFractionDigits:casas,maximumFractionDigits:casas});
    if(reduz){el.textContent=fmt.format(alvo);return;}
    (function passo(t){const p=Math.min(1,(t-t0)/dur),v=alvo*(1-Math.pow(1-p,3));el.textContent=fmt.format(v);if(p<1)requestAnimationFrame(passo);})(t0);
  }

  /* ---------------------------------------------------------- navegação */
  const aoEntrar={};
  function aplicar(n){
    telas[atual].querySelectorAll('video').forEach(v=>v.pause());
    pararAutos();
    telas[atual].classList.remove('ativa');
    atual=n;const t=telas[n];
    t.classList.add('ativa');
    stage.className='t-'+({claro:'claro',claro2:'claro',escuro:'escuro',lime:'lime',foto:'foto'}[t.dataset.tema]||'escuro')+(n===0?' capa':'');
    capTxt.textContent=t.dataset.cap||'';
    prog.style.width=((n+1)/total*100)+'%';
    cont.textContent=dd(n+1)+' / '+dd(total);
    $('#ant').disabled=n===0;$('#prox').disabled=n===total-1;
    t.querySelectorAll('[data-conta]').forEach(contar);
    $$('#sumLista button').forEach((b,i)=>b.classList.toggle('atual',i===n));
    history.replaceState(null,'','#'+(n+1));
    const fn=aoEntrar[t.classList[1]];if(fn)fn(t);
    iniciarAutos(t);
  }
  function ir(n){
    n=Math.max(0,Math.min(total-1,n));
    if(emTransicao){pendente=n;return;}
    if(n===atual)return;
    if(reduz||!wipe.animate){aplicar(n);return;}
    const dir=n>atual?1:-1, paraLime=telas[n].dataset.tema==='lime';
    wipe.classList.toggle('ink',paraLime);
    wipe.querySelector('img').src=paraLime?'assets/75lab-lime.png':'assets/75lab-black.png';
    const de=dir>0?'inset(0 0 0 100%)':'inset(0 100% 0 0)', meio='inset(0 0 0 0)', para=dir>0?'inset(0 100% 0 0)':'inset(0 0 0 100%)';
    emTransicao=true;
    const ease='cubic-bezier(.7,0,.3,1)';
    wipe.animate([{clipPath:de},{clipPath:meio}],{duration:360,easing:ease,fill:'forwards'}).onfinish=()=>{
      aplicar(n);
      wipe.animate([{clipPath:meio},{clipPath:para}],{duration:420,easing:ease,fill:'forwards'}).onfinish=()=>{emTransicao=false;if(pendente!==null){const p=pendente;pendente=null;ir(p);}};
    };
  }
  addEventListener('hashchange',()=>{const n=parseInt(location.hash.slice(1),10);if(!isNaN(n))ir(n-1);});
  $('#ant').addEventListener('click',e=>{e.stopPropagation();ir(atual-1);});
  $('#prox').addEventListener('click',e=>{e.stopPropagation();ir(atual+1);});
  // data-ir aponta para o id da tela (ou o número dela, contado de 1)
  const indice=v=>/^\d+$/.test(v)?+v-1:telas.findIndex(t=>t.id===v);
  $$('[data-ir]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();ir(indice(b.dataset.ir));}));

  /* sumário */
  const sum=$('#sumario'), lista=$('#sumLista');
  telas.forEach((t,i)=>{
    const li=document.createElement('li'), b=document.createElement('button');
    b.innerHTML='<b>'+dd(i+1)+'</b>'+t.dataset.titulo;b.dataset.cursor='Ir';
    b.addEventListener('click',e=>{e.stopPropagation();fecharSum();setTimeout(()=>ir(i),60);});
    li.appendChild(b);lista.appendChild(li);
  });
  function abrirSum(){sum.classList.add('aberto');}
  function fecharSum(){sum.classList.remove('aberto');}
  $$('[data-sumario]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();abrirSum();}));
  $('.fechar',sum).addEventListener('click',e=>{e.stopPropagation();fecharSum();});

  /* teclado, clique e toque */
  addEventListener('keydown',e=>{
    if(caixa.classList.contains('aberta')){if(e.key==='Escape')fecharCaixa();return;}
    if(sum.classList.contains('aberto')){if(e.key==='Escape')fecharSum();return;}
    if(['ArrowRight','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();ir(atual+1);}
    else if(['ArrowLeft','PageUp','Backspace'].includes(e.key)){e.preventDefault();ir(atual-1);}
    else if(e.key==='Home')ir(0);else if(e.key==='End')ir(total-1);
    else if(e.key==='m'||e.key==='M')sum.classList.contains('aberto')?fecharSum():abrirSum();
  });
  const INTERATIVO='a,button,input,.amplia,[data-cursor],#gantt,#compBim,#grade728,#tabEtq,.carta,#sumario,.ct,model-viewer,.celular,.janela';
  $('#wrap').addEventListener('click',e=>{
    if(e.target.closest(INTERATIVO))return;
    if(sum.classList.contains('aberto'))return;
    ir(e.clientX>innerWidth/2?atual+1:atual-1);
  });
  let x0=null,y0=null;
  addEventListener('touchstart',e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY;},{passive:true});
  addEventListener('touchend',e=>{
    if(x0===null)return;const dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;
    if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)&&!e.target.closest('#gantt,#compBim,model-viewer'))ir(dx<0?atual+1:atual-1);x0=null;
  });

  /* lightbox */
  const caixa=$('#caixa');
  function fecharCaixa(){caixa.classList.remove('aberta');}
  $$('[data-amplia]').forEach(el=>el.addEventListener('click',e=>{
    e.stopPropagation();$('#cxImg').src=el.dataset.amplia;$('#cxTxt').textContent=el.dataset.legenda||'';caixa.classList.add('aberta');
  }));
  caixa.addEventListener('click',e=>{if(e.target===caixa||e.target.closest('.fechar'))fecharCaixa();});

  /* ---------------------------------------------------------- cursor e luz */
  const cur=$('#cursor'),anel=$('#anel'),anelTxt=$('#anelTxt');
  let mx=innerWidth/2,my=innerHeight/2,ax=mx,ay=my;
  addEventListener('mousemove',e=>{
    document.body.classList.add('tem-mouse');mx=e.clientX;my=e.clientY;
    cur.style.transform='translate('+mx+'px,'+my+'px)';
    const alvo=e.target.closest('[data-cursor],a,button,.amplia');
    anel.classList.toggle('sobre',!!alvo);
    anelTxt.textContent=alvo?(alvo.dataset.cursor||'Ir'):'';
    const r=stage.getBoundingClientRect();
    stage.style.setProperty('--mx',((mx-r.left)/escalaAtual)+'px');stage.style.setProperty('--my',((my-r.top)/escalaAtual)+'px');
  },{passive:true});
  (function segue(){ax+=(mx-ax)*.2;ay+=(my-ay)*.2;anel.style.transform='translate('+ax+'px,'+ay+'px)';requestAnimationFrame(segue);})();
  addEventListener('mousedown',()=>document.body.classList.add('clicou'));
  addEventListener('mouseup',()=>document.body.classList.remove('clicou'));
  addEventListener('touchstart',()=>document.body.classList.remove('tem-mouse'),{passive:true});
  $('#verAssim').addEventListener('click',()=>document.body.classList.add('forcar'));

  /* ---------------------------------------------------------- 02 essencial */
  (function(){
    const dados=$$('#essDados')[0].content.querySelectorAll('i');
    $$('.s-ess .tile').forEach(b=>b.addEventListener('click',e=>{
      e.stopPropagation();const d=dados[+b.dataset.alvo];
      $$('.s-ess .tile').forEach(x=>x.classList.toggle('on',x===b));
      $('#essTit').textContent=d.dataset.t;const p=$('#essTxt');p.textContent=d.textContent;
      p.classList.remove('troca');void p.offsetWidth;p.classList.add('troca');
      $('#essIr').dataset.ir=d.dataset.ir;
    }));
    // o botão do painel lê o destino na hora do clique
    const bt=$('#essIr');const novo=bt.cloneNode(true);bt.replaceWith(novo);
    novo.addEventListener('click',e=>{e.stopPropagation();ir(indice(novo.dataset.ir));});
  })();

  /* ---------------------------------------------------------- 04 simultaneidade (Gantt) */
  (function(){
    const FER=['2026-09-07','2026-10-12','2026-11-02','2026-11-15','2026-11-20','2026-12-25','2027-01-01','2027-02-08','2027-02-09','2027-03-26','2027-04-21','2027-05-01','2027-05-27','2027-09-07','2027-10-12','2027-11-02','2027-11-15','2027-11-20','2027-12-25'];
    const fer=new Set(FER), D=s=>new Date(s+'T12:00:00'), iso=d=>d.toISOString().slice(0,10);
    const br=d=>dd(d.getDate())+'/'+dd(d.getMonth()+1)+'/'+d.getFullYear();
    function recua(d,n){d=new Date(d);while(n>0){d.setDate(d.getDate()-1);const w=d.getDay();if(w&&w<6&&!fer.has(iso(d)))n--;}return d;}
    const C=[['Masterbrand Verão 26.27','2','2027-01-04'],['Carnaval','2','2027-02-01'],['Point on Top','E','2027-03-09'],['Dia das Mães + Aura','E','2027-04-06'],['Dia das Mães','A','2027-04-12'],['Dia dos Namorados','E','2027-05-11'],['Slides · Copa Feminina','2','2027-05-13'],['São João · Parintins','2','2027-05-17'],['Masculino + Dia dos Pais','2','2027-07-12'],['Nova Coleção','E','2027-08-24'],['Puffed','E','2027-09-01'],['Tradi 65 anos','2','2027-09-09'],['Dia das Crianças','2','2027-09-13'],['Masterbrand Verão 27.28','2','2027-10-19'],['Black Friday','A','2027-11-16']]
      .map(([n,c,d])=>({n,c,fim:D(d),ini:recua(D(d),100)}));
    const T0=D('2026-08-01'),T1=D('2027-12-31'),INICIO=D('2026-11-09');
    const W=1456,H=400,LX=212,TOP=40,RH=18.8,HIST=TOP+C.length*RH+14;
    const x=d=>LX+(d-T0)/(T1-T0)*(W-LX);
    const conta=d=>C.filter(c=>c.ini<=d&&d<c.fim).length;
    const box=$('#gantt'),svg=document.createElementNS(SVGNS,'svg');
    svg.setAttribute('viewBox','0 0 '+W+' '+H);svg.setAttribute('role','img');
    svg.setAttribute('aria-label','Calendário B2B 2027 com a janela de 100 dias úteis de cada campanha');
    const el=(tag,at,pai=svg)=>{const e=document.createElementNS(SVGNS,tag);for(const k in at)e.setAttribute(k,at[k]);pai.appendChild(e);return e;};
    const txt=(s,at,pai)=>{const e=el('text',at,pai);e.textContent=s;return e;};
    const MES=['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ'];
    for(let m=new Date(T0);m<=T1;m.setMonth(m.getMonth()+1)){
      const xm=x(m);el('line',{x1:xm,y1:TOP-8,x2:xm,y2:HIST+44,stroke:'#F2F1E9','stroke-opacity':m.getMonth()===0?.45:.12});
      txt(MES[m.getMonth()]+(m.getMonth()===0?' '+String(m.getFullYear()).slice(2):''),{x:xm+4,y:TOP-10,'font-family':'Space Mono','font-size':10,fill:'#F2F1E9','fill-opacity':.6,'letter-spacing':1});
    }
    const xi=x(INICIO);
    el('line',{x1:xi,y1:TOP-30,x2:xi,y2:HIST-6,stroke:'#C0EE4E','stroke-dasharray':'4 4','stroke-width':1.5});
    txt('09/11/26 · início',{x:xi-6,y:TOP-30,'text-anchor':'end','font-family':'Space Mono','font-size':10,fill:'#C0EE4E'});
    const COR={'2':'#C0EE4E',E:'#06C6AE',A:'#F2F1E9'},NOME={'2':'os dois canais',E:'especializado',A:'alimentar'};
    C.forEach((c,i)=>{
      const y=TOP+i*RH;
      c.lab=txt(c.n,{x:LX-26,y:y+12,'text-anchor':'end','font-family':'Space Grotesk','font-size':12,fill:'#F2F1E9','fill-opacity':.7});
      el('rect',{x:LX-18,y:y+4,width:8,height:8,fill:COR[c.c]}).appendChild(document.createElementNS(SVGNS,'title')).textContent=NOME[c.c];
      if(c.ini<INICIO)el('rect',{x:x(c.ini),y:y+3,width:x(Math.min(INICIO,c.fim))-x(c.ini),height:11,fill:'none',stroke:'#F2F1E9','stroke-opacity':.25,'stroke-dasharray':'3 3'});
      const a=c.ini<INICIO?INICIO:c.ini;
      c.bar=el('rect',{x:x(a),y:y+3,width:Math.max(0,x(c.fim)-x(a)),height:11,fill:'#F2F1E9','fill-opacity':.2});
      const xf=x(c.fim);el('path',{d:'M'+xf+' '+(y+2)+'l5 6.5-5 6.5-5-6.5z',fill:'#F2F1E9','fill-opacity':.7});
      txt(dd(c.fim.getDate())+'/'+dd(c.fim.getMonth()+1),{x:xf+9,y:y+12,'font-family':'Space Mono','font-size':9.5,fill:'#F2F1E9','fill-opacity':.6});
    });
    // histograma semanal da sobreposição
    txt('em produção, semana a semana',{x:LX-26,y:HIST+24,'text-anchor':'end','font-family':'Space Mono','font-size':9.5,fill:'#F2F1E9','fill-opacity':.55});
    let pico={n:0,d:null};
    for(let d=new Date(T0);d<=T1;d.setDate(d.getDate()+7)){
      const n=conta(d);if(n>pico.n)pico={n,d:new Date(d)};
      el('rect',{x:x(d)+1,y:HIST+40-n*4.5,width:Math.max(2,(W-LX)/74-2),height:n*4.5,fill:n>=6?'#C0EE4E':'#F2F1E9','fill-opacity':n>=6?.85:.25});
    }
    // dia exato do pico
    for(let d=new Date(T0);d<=T1;d.setDate(d.getDate()+1)){const n=conta(d);if(n>pico.n||(n===pico.n&&!pico.exato)){pico={n,d:new Date(d),exato:true};}}
    // linha arrastável
    const g=el('g',{class:'arraste'});
    const lin=el('line',{y1:TOP-6,y2:HIST+44,stroke:'#C0EE4E','stroke-width':2.5},g);
    const alca=el('rect',{y:TOP-30,width:86,height:20,fill:'#C0EE4E'},g);
    const rot=txt('',{y:TOP-16,'text-anchor':'middle','font-family':'Space Mono','font-size':10.5,'font-weight':700,fill:'#050505'},g);
    el('rect',{x:LX,y:TOP-34,width:W-LX,height:HIST+80-TOP,fill:'transparent'},svg).style.cursor='ew-resize';
    svg.appendChild(g);
    const N=$('#simN'),Dt=$('#simD');
    function marca(d){
      const xx=x(d);lin.setAttribute('x1',xx);lin.setAttribute('x2',xx);
      alca.setAttribute('x',xx-43);rot.setAttribute('x',xx);rot.textContent=br(d).slice(0,6)+String(d.getFullYear()).slice(2);
      let n=0;C.forEach(c=>{const on=c.ini<=d&&d<c.fim;if(on)n++;c.bar.setAttribute('fill',on?'#C0EE4E':'#F2F1E9');c.bar.setAttribute('fill-opacity',on?.95:.2);c.lab.setAttribute('fill',on?'#C0EE4E':'#F2F1E9');c.lab.setAttribute('fill-opacity',on?1:.6);});
      N.textContent=n;N.style.color=n>=6?'var(--lime)':'var(--paper)';Dt.textContent=br(d);
    }
    function deX(cx){const r=svg.getBoundingClientRect();const px=(cx-r.left)/r.width*W;const t=T0.getTime()+(Math.min(W,Math.max(LX,px))-LX)/(W-LX)*(T1-T0);const d=new Date(t);d.setHours(12,0,0,0);return d;}
    let arrastando=false;
    svg.addEventListener('pointerdown',e=>{arrastando=true;svg.setPointerCapture(e.pointerId);marca(deX(e.clientX));e.stopPropagation();});
    svg.addEventListener('pointermove',e=>{if(arrastando)marca(deX(e.clientX));});
    svg.addEventListener('pointerup',()=>{arrastando=false;});
    svg.addEventListener('click',e=>e.stopPropagation());
    box.appendChild(svg);
    const SJ=D('2027-05-15');
    $('#simPico').addEventListener('click',e=>{e.stopPropagation();marca(pico.d);});
    $('#simSJ').addEventListener('click',e=>{e.stopPropagation();marca(SJ);});
    // na entrada a linha corre do início até 15/05/2027
    aoEntrar['s-sim']=()=>{
      if(reduz){marca(SJ);return;}
      const a=INICIO.getTime(),b=SJ.getTime(),t0=performance.now();
      (function passo(t){const p=Math.min(1,(t-t0-500)/1600);if(p<0){marca(new Date(a));requestAnimationFrame(passo);return;}
        const e=1-Math.pow(1-p,3);marca(new Date(a+(b-a)*e));if(p<1)requestAnimationFrame(passo);})(t0);
    };
    marca(SJ);
  })();

  /* ---------------------------------------------------------- 07 quatro frentes */
  (function(){
    const dados=$('#freDados').content.querySelectorAll('i');
    $$('.s-fre .frente').forEach(b=>b.addEventListener('click',e=>{
      e.stopPropagation();const i=+b.dataset.f,d=dados[i];
      $$('.s-fre .frente').forEach(x=>x.classList.toggle('on',x===b));
      $('#freN').textContent='Frente 0'+(i+1);
      const box=$('#freBox');box.innerHTML='<h3></h3><p></p>';box.querySelector('h3').textContent=d.dataset.t;box.querySelector('p').textContent=d.textContent;
      box.classList.remove('troca');void box.offsetWidth;box.classList.add('troca');
    }));
  })();

  /* ---------------------------------------------------------- 12 método */
  (function(){
    const M=[['Briefing do cliente','Pauta validada','Escopo, prazo e formatos acordados por escrito'],
      ['Pauta validada','KV ou rota criativa','Aprovação formalizada e registrada'],
      ['KV aprovado','Arte-final e planta técnica','Checagem técnica e legal assinada'],
      ['Arte-final','Material produzido','3 orçamentos, protótipo testado e QA de lote'],
      ['Material produzido','Material posicionado','Comprovação de entrega e de execução']];
    const passos=$$('.s-met .passo'),barra=$('.s-met .progresso');
    function mostra(i){
      passos.forEach((p,j)=>{p.classList.toggle('on',j===i);p.classList.toggle('feito',j<i);});
      barra.style.width=(i*291.2)+'px';
      [['#metE',0],['#metS',1],['#metQ',2]].forEach(([s,k])=>{const p=$(s);p.textContent=M[i][k];p.classList.remove('troca');void p.offsetWidth;p.classList.add('troca');});
    }
    passos.forEach(p=>p.addEventListener('click',e=>{e.stopPropagation();mostra(+p.dataset.p);}));
    aoEntrar['s-met']=()=>mostra(0);
    roteiro('s-met',{itens:()=>passos,texto:k=>M[k].join(' ')});
  })();

  /* ---------------------------------------------------------- 15 fluxo */
  (function(){
    const dados=$('#fluDados').content.querySelectorAll('i');
    $$('.s-flu .ctl').forEach(b=>b.addEventListener('click',e=>{
      e.stopPropagation();const d=dados[+b.dataset.c];
      $$('.s-flu .ctl').forEach(x=>x.classList.toggle('on',x===b));
      $('#fluT').textContent=d.dataset.t;const p=$('#fluP');p.textContent=d.textContent;p.classList.remove('troca');void p.offsetWidth;p.classList.add('troca');
    }));
  })();

  /* ---------------------------------------------------------- 16 comparador BIM */
  (function(){
    const comp=$('#compBim');let arr=false;
    const poe=v=>comp.style.setProperty('--corte',Math.max(4,Math.min(96,v))+'%');
    const deX=cx=>{const r=comp.getBoundingClientRect();return (cx-r.left)/r.width*100;};
    comp.addEventListener('pointerdown',e=>{arr=true;comp.setPointerCapture(e.pointerId);poe(deX(e.clientX));e.stopPropagation();});
    comp.addEventListener('pointermove',e=>{if(arr)poe(deX(e.clientX));});
    comp.addEventListener('pointerup',()=>{arr=false;});
    comp.addEventListener('click',e=>e.stopPropagation());
    aoEntrar['s-bim']=()=>{
      if(reduz){poe(50);return;}
      const t0=performance.now();
      (function passo(t){const p=Math.min(1,Math.max(0,(t-t0-700)/1800));const v=96-Math.sin(p*Math.PI*.75)*72;poe(v);if(p<1)requestAnimationFrame(passo);})(t0);
    };
  })();

  /* ---------------------------------------------------------- 17 cartas */
  (function(){
    const cartas=$$('.s-ser .carta');
    cartas.forEach(c=>c.addEventListener('click',e=>{e.stopPropagation();c.classList.toggle('virada');}));
    $('#virarTodos').addEventListener('click',e=>{
      e.stopPropagation();const todas=cartas.every(c=>c.classList.contains('virada'));
      cartas.forEach((c,i)=>setTimeout(()=>c.classList.toggle('virada',!todas),i*110));
      e.currentTarget.firstChild.textContent=todas?'Virar todas':'Desvirar';
    });
    aoEntrar['s-ser']=()=>{cartas.forEach(c=>c.classList.remove('virada'));$('#virarTodos').firstChild.textContent='Virar todas';if(modoPdf)cartas[0].classList.add('virada');};
    roteiro('s-ser',{itens:()=>cartas,inicio:()=>-1,primeiro:1600,ms:()=>2800,laco:false});
  })();

  /* ---------------------------------------------------------- 18 etiqueta x rastreador */
  (function(){
    const tab=$('#tabEtq');
    $$('#tabEtq .h').forEach(h=>h.addEventListener('click',e=>{
      e.stopPropagation();const f='foco-'+h.dataset.foco,ja=tab.classList.contains(f);
      tab.classList.remove('foco-qr','foco-gps');if(!ja)tab.classList.add(f);
    }));
  })();

  /* ---------------------------------------------------------- 22 riscos */
  (function(){
    $$('.s-ris .risco button').forEach(b=>b.addEventListener('click',e=>{
      e.stopPropagation();const r=b.parentElement,ab=r.classList.contains('aberto');
      $$('.s-ris .risco').forEach(x=>x.classList.remove('aberto'));if(!ab)r.classList.add('aberto');
    }));
  })();

  /* ---------------------------------------------------------- 26 painel das 728 lojas */
  (function(){
    const grade=$('#grade728'),tip=$('#tip728'),lojas=$('.s-pai .lojas');
    let s=75;const rnd=()=>(s=(s*16807)%2147483647)/2147483647;
    const tipo=Array(728).fill(1);let n2=98,n3=41;
    while(n2){const i=Math.floor(rnd()*728);if(tipo[i]===1){tipo[i]=2;n2--;}}
    while(n3){const i=Math.floor(rnd()*728);if(tipo[i]===1){tipo[i]=3;n3--;}}
    const FMT=[['Premium',.18],['Standard',.32],['Light',.16],['Compacta 3',.14],['Layout antigo',.12],['Quiosque',.08]];
    const fmt=()=>{let r=rnd(),a=0;for(const [n,p] of FMT){a+=p;if(r<a)return n;}return 'Standard';};
    const frag=document.createDocumentFragment();
    tipo.forEach((k,i)=>{
      const c=document.createElement('i');c.className='k'+k;
      const dia=10+Math.floor(rnd()*7),f=fmt();
      c.dataset.t='Loja '+String(i+1).padStart(4,'0')+' · '+f+'\n'+(k===1?'instalada em '+dd(dia+1)+'/05, com foto':k===2?'recebida em '+dd(dia)+'/05 · aguardando instalação':'sem leitura de recebimento · ocorrência aberta');
      frag.appendChild(c);
    });
    grade.appendChild(frag);
    const cel=[...grade.children];
    grade.addEventListener('mouseover',e=>{
      const c=e.target.closest('i');if(!c)return;
      tip.textContent=c.dataset.t;tip.style.display='block';
      tip.style.left=(lojas.offsetLeft+c.offsetLeft+18)+'px';tip.style.top=(lojas.offsetTop+c.offsetTop-46)+'px';
    });
    grade.addEventListener('mouseleave',()=>{tip.style.display='none';});
    grade.addEventListener('click',e=>e.stopPropagation());
    $$('#filtros728 button').forEach(b=>b.addEventListener('click',e=>{
      e.stopPropagation();$$('#filtros728 button').forEach(x=>x.classList.toggle('on',x===b));
      grade.classList.remove('f1','f2','f3');if(b.dataset.f)grade.classList.add(b.dataset.f);
    }));
    aoEntrar['s-pai']=()=>{
      cel.forEach(c=>c.classList.remove('v'));
      if(reduz){cel.forEach(c=>c.classList.add('v'));return;}
      // varredura em diagonal, como leituras chegando
      cel.forEach((c,i)=>{const col=i%52,lin=Math.floor(i/52);setTimeout(()=>c.classList.add('v'),400+(col+lin*2)*14);});
    };
  })();

  /* ---------------------------------------------------------- 27 transição */
  (function(){
    const mapa=$('#mapaTra'),D=s=>new Date(s+'T12:00:00');
    const T0=D('2026-11-01'),T1=D('2027-04-30'),pc=d=>((d-T0)/(T1-T0)*100).toFixed(2)+'%';
    const mes=document.createElement('div');mes.className='meses';
    ['NOV','DEZ','JAN 27','FEV','MAR','ABR'].forEach(m=>{const s=document.createElement('span');s.textContent=m;mes.appendChild(s);});
    mapa.appendChild(mes);
    const camp=[['Masterbrand Verão 26.27 · 04/01','her','2026-11-01','2027-01-04'],['Carnaval · 01/02','her','2026-11-01','2027-02-01'],['Point on Top · 09/03','her','2026-11-01','2027-03-09'],['Dia das Mães + Aura · 06/04 · ciclo completo','nova','2026-11-09','2027-04-06']];
    camp.forEach(([n,k,a,b],i)=>{
      const d=document.createElement('div');d.className='camp '+k;
      d.style.cssText='top:'+(34+i*38)+'px;left:'+pc(D(a))+';width:calc('+pc(D(b))+' - '+pc(D(a))+')';
      d.innerHTML='<i style="transition-delay:'+(.3+i*.15)+'s"></i><span></span>';d.querySelector('span').textContent=n;mapa.appendChild(d);
    });
    [['2026-11-01','30/10 · entrega da proposta','prop'],['2026-11-09','09/11 · início do 1º ciclo completo','']].forEach(([d,t,k])=>{
      const l=document.createElement('div');l.className='linha-m '+k;l.style.left=pc(D(d));l.style.bottom='122px';
      const s=document.createElement('span');s.textContent=t;l.appendChild(s);if(k==='prop'){s.style.left='4px';}else{s.style.left='10px';s.style.bottom='-22px';}
      mapa.appendChild(l);
    });
    const mc=document.createElement('div');mc.className='marcos';
    [['2026-11-09','D+0','acervo e acessos'],['2026-11-24','D+15','base de 658 lojas e layouts'],['2026-12-09','D+30','fornecedores homologados'],['2027-01-08','D+60','1ª campanha em paralelo'],['2027-02-07','D+90','corte da estrutura antiga']].forEach(([d,b,t])=>{
      const m=document.createElement('div');m.className='marco';m.style.left=pc(D(d));m.innerHTML='<i></i><b></b><span></span>';m.querySelector('b').textContent=b;m.querySelector('span').textContent=t;mc.appendChild(m);
    });
    mapa.appendChild(mc);
  })();

  /* ---------------------------------------------------------- depoimento Alltak */
  (function(){
    const v=$('#vidDep'),cel=v.closest('.celular'),pr=$('#progDep');
    const alterna=e=>{e.stopPropagation();if(v.paused){v.play();}else{v.pause();}};
    $('#playDep').addEventListener('click',alterna);
    v.addEventListener('click',alterna);
    v.addEventListener('play',()=>cel.classList.add('tocando'));
    v.addEventListener('pause',()=>cel.classList.remove('tocando'));
    v.addEventListener('ended',()=>{cel.classList.remove('tocando');v.load();});
    v.addEventListener('timeupdate',()=>{pr.style.width=(v.duration?v.currentTime/v.duration*100:0)+'%';});
  })();

  /* ---------------------------------------------------------- Gestão Cliente Fee */
  (function(){
    const passos=$$('#feePassos .passo'),imgs=$$('#feeVista img'),url=$('#feeUrl');
    function mostra(k){
      passos.forEach((p,j)=>p.classList.toggle('on',j===k));imgs.forEach((m,j)=>m.classList.toggle('on',j===k));
      url.textContent=imgs[k].dataset.url;
    }
    passos.forEach((p,k)=>p.addEventListener('click',e=>{e.stopPropagation();mostra(k);}));
    aoEntrar['s-fee']=()=>mostra(0);
    // a tela do sistema também precisa de tempo de leitura: soma 1,5 s ao texto do passo
    roteiro('s-fee',{itens:()=>passos,texto:k=>passos[k].textContent,extra:1500});
  })();

  /* ---------------------------------------------------------- AR ao vivo */
  (function(){
    let carregou=false;
    function liga(mv,src,ios){mv.classList.add('carregando');mv.setAttribute('src',src);if(ios)mv.setAttribute('ios-src',ios);}
    $$('.s-ar model-viewer').forEach(mv=>mv.addEventListener('load',()=>mv.classList.remove('carregando')));
    aoEntrar['s-ar']=()=>{
      if(!carregou){carregou=true;const sc=document.createElement('script');sc.type='module';sc.src='assets/vendor/model-viewer.min.js';document.head.appendChild(sc);}
      $$('.s-ar model-viewer').forEach(mv=>{if(modoPdf)mv.removeAttribute('auto-rotate');if(!mv.getAttribute('src'))liga(mv,mv.dataset.src,mv.dataset.ios);});
    };
    $$('.s-ar .cartao').forEach(c=>{
      const mv=$('model-viewer',c),bts=$$('.chips button',c);
      bts.forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();bts.forEach(x=>x.classList.toggle('on',x===b));liga(mv,b.dataset.src,b.dataset.ios);}));
    });
  })();

  /* ---------------------------------------------------------- painel do QR */
  (function(){
    const abas=$$('#qrAbas button'),vistas=$$('#qrVista>div');
    abas.forEach((b,k)=>b.addEventListener('click',e=>{e.stopPropagation();abas.forEach(x=>x.classList.toggle('on',x===b));vistas.forEach((v,j)=>v.classList.toggle('on',j===k));}));
    // cada vista desce devagar pela tela do painel quando ela é mais alta que a janela
    vistas.forEach(v=>v.classList.add('pan'));
  })();

  /* ---------------------------------------------------------- temporizador
     Os botões de cada tela abrem sozinhos, um de cada vez, com tempo para ler.
     O primeiro clique da pessoa dentro da tela para o temporizador até ela sair e voltar. */
  function roteiro(cls,cfg){(autos[cls]=autos[cls]||[]).push(cfg);}
  // tempo de leitura: 3 s mais 45 ms por letra, entre 4,5 e 12 s
  const leitura=txt=>Math.max(4500,Math.min(12000,3000+String(txt||'').replace(/\s+/g,' ').trim().length*45));
  function pararAutos(){autoAtivos.forEach(clearTimeout);autoAtivos=[];$$('.relogio-auto').forEach(r=>r.remove());}
  function iniciarAutos(t){
    if(modoPdf)return;
    (autos[t.classList[1]]||[]).forEach(cfg=>{
      const itens=cfg.itens(),n=itens.length;if(!n)return;
      const ms=k=>cfg.ms?cfg.ms(k):leitura(cfg.texto?cfg.texto(k):itens[k].textContent)+(cfg.extra||0);
      let i=cfg.inicio?cfg.inicio():Math.max(0,itens.findIndex(x=>x.matches('.on,.aberto')||x.parentElement.classList.contains('aberto')));
      function relogio(k,dur){
        const alvo=itens[k];
        $$('.relogio-auto',t).forEach(r=>{if(r.parentElement&&itens.includes(r.parentElement))r.remove();});
        if(getComputedStyle(alvo).position==='static')alvo.style.position='relative';
        const r=document.createElement('i');r.className='relogio-auto';alvo.appendChild(r);
        r.style.transitionDuration=dur+'ms';void r.offsetWidth;r.classList.add('corre');
      }
      function passo(){
        if(i+1>=n&&cfg.laco===false){$$('.relogio-auto',t).forEach(r=>r.remove());return;}
        i=(i+1)%n;itens[i].click();
        if(i+1>=n&&cfg.laco===false)return;
        const d=ms(i);relogio(i,d);autoAtivos.push(setTimeout(passo,d));
      }
      if(i<0){autoAtivos.push(setTimeout(passo,cfg.primeiro||2500));return;}
      const d=ms(i);relogio(i,d);autoAtivos.push(setTimeout(passo,d));
    });
  }
  // clique de verdade da pessoa (não o do temporizador) dentro da tela para tudo
  stage.addEventListener('pointerdown',e=>{if(e.isTrusted&&e.target.closest('.tela.ativa'))pararAutos();},true);

  const textoDe=id=>k=>$(id).content.querySelectorAll('i')[k].textContent;
  roteiro('s-ess',{itens:()=>$$('.s-ess .tile'),texto:textoDe('#essDados')});
  roteiro('s-fre',{itens:()=>$$('.s-fre .frente'),texto:textoDe('#freDados')});
  roteiro('s-flu',{itens:()=>$$('.s-flu .ctl'),texto:textoDe('#fluDados')});
  roteiro('s-sim',{itens:()=>[$('#simPico'),$('#simSJ')],inicio:()=>-1,primeiro:6000,ms:()=>6500});
  roteiro('s-ar',{itens:()=>$$('.s-ar [data-ar=semp] .chips button'),ms:()=>8000});
  roteiro('s-ar',{itens:()=>$$('.s-ar [data-ar=panasonic] .chips button'),ms:()=>11000});
  roteiro('s-etq',{itens:()=>$$('#tabEtq .h'),inicio:()=>-1,primeiro:3500,ms:()=>6500});
  roteiro('s-qr',{itens:()=>$$('#qrAbas button'),ms:()=>8000});
  roteiro('s-ris',{itens:()=>$$('.s-ris .risco button'),texto:k=>$$('.s-ris .risco')[k].textContent});
  roteiro('s-pai',{itens:()=>$$('#filtros728 button'),ms:()=>5000});

  /* ---------------------------------------------------------- início */
  const h=parseInt(location.hash.slice(1),10);
  const n0=isNaN(h)?0:Math.max(0,Math.min(total-1,h-1));
  telas.forEach(t=>t.classList.remove('ativa'));atual=n0;telas[n0].classList.add('ativa');
  atual=n0===0?1:0;aplicar(n0); // força a primeira aplicação
  telas.forEach((t,i)=>{if(i!==n0)t.classList.remove('ativa');});
})();
