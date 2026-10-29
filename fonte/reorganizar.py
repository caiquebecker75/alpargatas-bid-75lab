# Reorganiza o deck do BID em capítulos com capa, num roteiro comercial (pedido do Caique de 29/10/2026).
# Lê o index.html atual, reaproveita as telas que ficam e escreve as novas. Rodar uma vez:
#   python3 fonte/reorganizar.py
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
html = (RAIZ / 'index.html').read_text(encoding='utf-8')

ini = html.index('<div id="wrap"><div id="stage"')
ini = html.index('\n', ini) + 1
fim = html.index('  <header id="topo">')
corpo = html[ini:fim]

# cada tela atual, pela classe s-*
telas = {}
for m in re.finditer(r'(?:  <!-- =+[^\n]*-->\n)?  <section\b[^>]*class="tela (s-[a-z]+)[^"]*"[^>]*>.*?\n  </section>\n', corpo, re.S):
    telas[m.group(1)] = m.group(0)

def tela(cls):
    return telas[cls]

def troca_cap(sec, cap):
    return re.sub(r'data-cap="[^"]*"', f'data-cap="{cap}"', sec, count=1)

CTA = lambda txt: f'<span class="cta so-tela"><svg class="ic"><use href="#i-clique"/></svg>{txt}</span>'

# ------------------------------------------------------------------ capítulos
CAPS = [
    ('desafio', '01', 'O desafio', 'Lemos o escopo como operação contínua, não como lista de peças.',
     ['35 campanhas em 2027', 'O desafio é simultaneidade', 'O investimento é do franqueado', 'A tese']),
    ('quem-somos', '02', 'Quem é a 75 LAB', 'Por que existimos, o que nos diferencia e quem responde pela conta.',
     ['Propósito', 'Diferencial', 'A estrutura', 'Quem responde pela conta', 'Nossos números', 'Clientes']),
    ('provas', '03', 'O que já entregamos', 'Criação, engenharia e execução, com prova.',
     ['Cases', 'Engenharia e aproveitamento de chapa', 'Depoimento e vídeos']),
    ('operacao', '04', 'Como vamos operar', 'Processo, fluxo, sistema e time desenhados para o calendário de vocês.',
     ['O processo da pauta à loja', 'Fluxo e controles', 'Simulador do Ariuno', 'O time dedicado', 'Como dimensionamos']),
    ('tecnologia', '05', 'Tecnologia antes de produzir', 'A loja modelada e a IA no lugar certo do processo.',
     ['As lojas que já modelamos', 'Onde a IA entra']),
    ('rastreio', '06', 'Rastreio peça a peça', 'O que acontece depois do caminhão vira dado.',
     ['Como funciona', 'O painel', 'O que vocês ganham', 'Fechamento de ciclo', 'O compromisso']),
    ('demo', '07', 'Na prática: São João 2027', 'Uma campanha inteira montada para vocês verem.', []),
    ('comeco', '08', 'Como começamos', 'Riscos endereçados e um início antes do contrato.',
     ['Riscos e continuidade', 'Começar antes do contrato', 'Fale com a gente']),
]
TRILHA = ''.join(f'<span data-c="{n}">{n}<b>{t}</b></span>' for _, n, t, _, _ in CAPS)

def capitulo(i, tema='escuro'):
    cid, n, t, frase, itens = CAPS[i]
    lis = ''.join(f'<li><i>{k+1:02d}</i>{x}</li>' for k, x in enumerate(itens))
    return f'''  <!-- ===================================================== capítulo {n} -->
  <section id="cap-{cid}" class="tela s-cap" data-tema="{tema}" data-titulo="Capítulo {n} · {t}" data-cap="({n}) {t}" data-capitulo="{n}">
    <span class="num-cap sangra">{n}</span>
    <div class="texto">
      <span class="eyebrow anima"><b>Capítulo {n}</b> de 08</span>
      <h2 class="anima d1">{t}</h2>
      <p class="lead anima d2">{frase}</p>
    </div>
    <ol class="dentro anima d3">{lis}</ol>
    <div class="trilha-cap anima d4" data-atual="{n}">{TRILHA}</div>
  </section>

'''

def cap(sec, n):
    c = CAPS[int(n) - 1]
    return troca_cap(sec, f'({n}) {c[2]}')

# ------------------------------------------------------------------ telas novas
RESUMO = '''  <!-- ===================================================== resumo executivo -->
  <section id="resumo" class="tela s-res" data-tema="claro" data-titulo="Resumo executivo" data-cap="Resumo executivo">
    <span class="destaque-cap anima">Resumo executivo · a proposta em uma página</span>
    <h2 class="anima d1">Duas operações dedicadas, DTC e B2B, <span class="onda t-teal">medidas loja a loja.</span></h2>
    <div class="quatro">
      <div class="bl anima d2"><span class="n">01</span><b>O desafio</b><strong>35</strong><em>campanhas em 2027</em><p>23 no DTC e 12 no B2B, até 8 em produção no mesmo dia, em 728 lojas onde o investimento na produção é do franqueado.</p></div>
      <div class="bl anima d2"><span class="n">02</span><b>Nossa resposta</b><strong>14</strong><em>pessoas · 12,6 FTE</em><p>Dois núcleos dedicados, sem fila compartilhada, dimensionados pelas horas reais medidas no nosso sistema de gestão.</p></div>
      <div class="bl anima d3"><span class="n">03</span><b>Como entregamos</b><strong>5</strong><em>etapas com critério de saída</em><p>Briefing e aprovação peça a peça no Ariuno, lojas modeladas em 3D antes de produzir e engenharia com aproveitamento de chapa.</p></div>
      <div class="bl anima d3"><span class="n">04</span><b>Como medimos</b><strong>D+15</strong><em>ciclo fechado em cada campanha</em><p>Cada peça com código único: recebimento em D+2, instalação com foto em D+7 e a próxima tiragem calibrada pelo que foi instalado.</p></div>
    </div>
    <div class="faixa-res anima d4">
      <div><svg class="ic"><use href="#i-check"/></svg><span><b>Já somos fornecedor cadastrado</b> da Alpargatas, a 2,5 km da sede.</span></div>
      <div><svg class="ic"><use href="#i-moeda"/></svg><span><b>Open cost completo</b> e três modelos comparados, no documento comercial.</span></div>
      <div><svg class="ic"><use href="#i-calendario"/></svg><span><b>Recomendação:</b> setup e handover antes do contrato, para a primeira campanha não ser de aprendizado.</span></div>
    </div>
  </section>

'''

FRANQUEADO = '''  <!-- ===================================================== o investimento é do franqueado -->
  <section class="tela s-fra2" data-tema="claro" data-titulo="O investimento é do franqueado" data-cap="(01) O desafio">
    <h2 class="anima">Quem paga a produção é o franqueado. <span class="onda t-teal">Ele paga pelo que é produzido, não pelo que é instalado.</span></h2>
    <p class="lead anima d1">O briefing coloca a otimização do investimento do franqueado ao lado da unicidade de marca e da excelência de execução. Entre a gráfica e a loja existem duas perdas que hoje ninguém mede.</p>
    <div class="funil anima d2">
      <div class="et e1"><span class="rot">Produzido</span><div class="bar"><i></i></div><b>100%</b><small>é o que o franqueado paga</small></div>
      <div class="perda p1"><span>Perda 1</span><b>Não chega</b><p>A loja pagou e ficou sem o material. A reclamação chega na marca, não na agência.</p></div>
      <div class="et e2"><span class="rot">Entregue</span><div class="bar"><i></i></div><b>?</b><small>hoje ninguém sabe</small></div>
      <div class="perda p2"><span>Perda 2</span><b>Chega e não é instalado</b><p>O custo saiu inteiro e o retorno é zero.</p></div>
      <div class="et e3"><span class="rot">Instalado</span><div class="bar"><i></i></div><b>?</b><small>é o que gera resultado</small></div>
    </div>
    <div class="resposta anima d3">
      <span class="eyebrow">O que a 75 LAB faz com isso</span>
      <p>Medimos as duas perdas peça a peça e usamos o número para calibrar a tiragem seguinte. O franqueado passa a pagar pelo que de fato vai para a loja.</p>
      <button class="botao mini seta so-tela" data-ir="cap-rastreio" data-cursor="Ir">Ver como medimos</button>
    </div>
  </section>

'''

PROPOSITO = '''  <!-- ===================================================== propósito -->
  <section id="proposito" class="tela s-prop" data-tema="lime" data-titulo="Propósito" data-cap="(02) Quem é a 75 LAB">
    <span class="eyebrow anima">Nosso propósito</span>
    <h2 class="anima d1">Transformar intenção em realidade <span class="apagada">no ponto de venda.</span></h2>
    <p class="lead anima d2">A 75 LAB nasceu da soma de dois lados que quase nunca se sentam à mesma mesa: o varejo e a indústria. Por mais de 15 anos vivemos a distância entre a intenção comercial de uma marca e o que de fato acontece na loja. Existimos para fechar essa distância.</p>
    <div class="balcao anima d3">
      <div class="lado-b"><span>Indústria</span><b>Lançamento, categoria, P&amp;L</b><small>o lado de quem vende para o varejo</small></div>
      <div class="meio-b"><img src="assets/75lab-black.png" alt="75 LAB"><i>← valor →</i></div>
      <div class="lado-b"><span>Varejo</span><b>Layout, execução, aprovação</b><small>o lado de quem opera a loja</small></div>
    </div>
    <blockquote class="anima d4">“Criamos o que gostaríamos de ter tido como clientes.”<cite>Daniel Coimbra, cofundador e CEO da 75 LAB</cite></blockquote>
    <span class="assin-prop anima d4">Ideia boa é a que acontece.</span>
  </section>

'''

DIFERENCIAL = '''  <!-- ===================================================== diferencial -->
  <section id="diferencial" class="tela s-dif" data-tema="escuro" data-titulo="Diferencial" data-cap="(02) Quem é a 75 LAB">
    <h2 class="anima">Não somos uma agência tradicional. <span class="t-lime">Somos uma aceleradora de trade.</span></h2>
    <div class="modelos anima d1">
      <div class="mod trad"><span class="eyebrow">Modelo tradicional</span><div class="seq"><span>Briefing</span><span>Retrabalho</span><span>Atraso</span><span class="x">Verba evapora</span></div></div>
      <div class="mod lab"><span class="eyebrow">Modelo 75 LAB</span><div class="seq"><span>Intenção</span><span>Imersão</span><span>Solução</span><span>Execução</span><span class="ok">Resultado</span></div></div>
    </div>
    <div class="pilares anima d2">
      <div><i>01</i><b>Vivemos o trade, não só aprendemos</b><p>Os sócios vêm do varejo e da indústria: os dois lados do balcão estão na mesma mesa.</p></div>
      <div><i>02</i><b>Solução certa, nunca de prateleira</b><p>Montamos a estrutura pela demanda de cada cliente, não um pacote pronto.</p></div>
      <div><i>03</i><b>Para cada desafio, a equipe certa</b><p>Hub de especialistas e fornecedores, com governança ponta a ponta e sem markup oculto.</p></div>
      <div><i>04</i><b>Prova acima de promessa</b><p>Medimos o que entregamos: peça a peça, loja a loja.</p></div>
    </div>
    <div class="provas anima d3">
      <div><b class="num"><span data-conta="95">0</span>%</b><span>projetos aprovados</span></div>
      <div><b class="num">−<span data-conta="25">0</span>%</b><span>de custo de produção com o fornecedor certo</span></div>
      <div><b class="num"><span data-conta="15000">0</span>+</b><span>PDVs positivados</span></div>
      <div><b class="num">+<span data-conta="15">0</span></b><span>anos no trade, dos dois lados do balcão</span></div>
    </div>
    <p class="fonte">Fonte: 75lab.com.br, números da 75 LAB.</p>
  </section>

'''

RESP = '''  <!-- ===================================================== quem responde -->
  <section id="quem-responde" class="tela s-resp2" data-tema="claro" data-titulo="Quem responde pela conta" data-cap="(02) Quem é a 75 LAB">
    <h2 class="anima">Quem responde pela conta <span class="onda t-teal">é quem opera.</span></h2>
    <p class="lead anima d1">É o mesmo time que opera a conta, não uma equipe montada para a concorrência.</p>
    <div class="pessoas anima d2">
      <div class="pessoa"><b class="num"><span data-conta="20">0</span><small>anos</small></b><div><h3>Daniel Coimbra</h3><p>de trade marketing, do lado de quem vende para o varejo</p></div></div>
      <div class="pessoa"><b class="num"><span data-conta="15">0</span><small>anos</small></b><div><h3>Caique Becker</h3><p>de varejo, do lado de quem operou a loja</p></div></div>
    </div>
    <div class="cad anima d3">
      <span class="eyebrow"><b>(✓)</b> Já somos fornecedor cadastrado da Alpargatas</span>
      <div class="checks"><span>Alvará</span><span>AVCB</span><span>ABVTEX</span><span>Certidões</span><span>DCTFWeb</span><span>Termo de adesão</span></div>
    </div>
    <a class="rota2 anima d4" href="https://www.google.com/maps/dir/?api=1&origin=Av.+das+Na%C3%A7%C3%B5es+Unidas%2C+12901+-+Brooklin%2C+S%C3%A3o+Paulo+-+SP&destination=Av.+das+Na%C3%A7%C3%B5es+Unidas%2C+14261+-+Vila+Gertrudes%2C+S%C3%A3o+Paulo+-+SP&travelmode=driving" target="_blank" rel="noopener" data-cursor="Abrir">
      <img src="assets/img/rota-75lab-alpargatas.webp" alt="Trajeto entre a 75 LAB e a sede da Alpargatas">
      <span class="info"><span class="eyebrow">Na mesma avenida da sede</span><b><span class="num">2,5</span> km · <span class="num">11</span> min</b><small class="so-tela">Clique para abrir a rota no Google Maps</small></span>
    </a>
    <div class="palco-duo anima zoom d1">
      <img class="marca" src="assets/logos/75lab-logo-lime.svg" alt="75 LAB">
      <img class="duo" src="assets/img/caique-daniel.webp" alt="Daniel Coimbra e Caique Becker, da 75 LAB">
      <span class="quem"><b>Daniel Coimbra</b><b>Caique Becker</b>cofundadores da 75 LAB</span>
    </div>
    <p class="fonte">Rota e tempo: Google Maps, 28/10/2026 · 75 LAB, Av. das Nações Unidas, 12.901 · Alpargatas, Av. das Nações Unidas, 14.261.</p>
  </section>

'''

CLIENTES = '''  <!-- ===================================================== clientes -->
  <section class="tela s-cli2" data-tema="claro2" data-titulo="Clientes" data-cap="(02) Quem é a 75 LAB">
    <h2 class="anima">Já trabalhamos os dois canais <span class="onda t-teal">que vocês têm.</span></h2>
    <p class="lead anima d1">Gôndola de supermercado e loja de categoria: são as duas lógicas de ponto de venda do escopo de vocês, e as marcas que atendemos vivem nelas.</p>
    <div class="grupo anima d2"><div class="cab-g"><svg class="ic"><use href="#i-caixa"/></svg><b>Canal alimentar</b><span>supermercado, atacado e conveniência</span></div>
      <div class="logos">LOGOS_A</div></div>
    <div class="grupo anima d3"><div class="cab-g"><svg class="ic"><use href="#i-loja"/></svg><b>Varejo especializado</b><span>loja de categoria e rede franqueada</span></div>
      <div class="logos">LOGOS_E</div></div>
  </section>

'''
LOGOS_A = ['whiskas:Whiskas', 'pedigree:Pedigree', 'seara:Seara', 'lactalis:Lactalis', 'parmalat:Parmalat', 'unilever:Unilever', '3coracoes:3 Corações', 'madalena:Madalena']
LOGOS_E = ['boticario:O Boticário', 'petz:Petz', 'brastemp:Brastemp', 'consul:Consul', 'drogaria-sao-paulo:Drogaria São Paulo', 'dpsp:Grupo DPSP', 'loungerie:Loungerie', 'evino:Evino',
           'grand-cru:Grand Cru', 'eudora:Eudora', 'quem-disse-berenice:Quem disse, Berenice?', 'premierpet:PremieRpet', 'kelcat:Kelcat', 'keldog:Keldog', 'pipicat:Pipicat']
logo = lambda s: ''.join(f'<div><img src="assets/clientes/{a}.png" alt="{b}"></div>' for a, b in (x.split(':') for x in s))
CLIENTES = CLIENTES.replace('LOGOS_A', logo(LOGOS_A)).replace('LOGOS_E', logo(LOGOS_E))

ENGENHARIA = '''  <!-- ===================================================== engenharia e aproveitamento -->
  <section id="engenharia" class="tela s-eng" data-tema="claro" data-titulo="Engenharia e aproveitamento de chapa" data-cap="(03) O que já entregamos">
    <h2 class="anima">A peça é desenhada para a fábrica, <span class="onda t-teal">não só para o render.</span></h2>
    <p class="lead anima d1">Todo executivo sai com vistas, cortes, planificado com faca 1:1, lista de materiais e o estudo de aproveitamento de chapa. Quando a geometria desperdiça material, a gente muda a peça.</p>
    <div class="estudo anima d2">
      <span class="eyebrow">Estudo de chapa · display Président (Lactalis) · chapa de 2000 × 1000 mm</span>
      <div class="barras-e">
        <div class="be"><span>Laterais duplas</span><div class="b"><i style="--w:50%"></i></div><b>84 <small>embalagens de 150 g por chapa · 3 displays</small></b></div>
        <div class="be"><span>Laterais simples</span><div class="b"><i style="--w:83.3%"></i></div><b>140 <small>5 displays</small></b></div>
        <div class="be ok"><span>Versão adotada</span><div class="b"><i style="--w:100%"></i></div><b>168 <small>6 displays · 59% da chapa</small></b></div>
      </div>
      <div class="ganho"><b class="num">2×</b><span>o produto exposto por chapa comprada, mudando a peça e não o fornecedor</span></div>
      <img class="chapa amplia" src="assets/eng/pre-chapa-2000.webp" data-amplia="assets/eng/pre-aprov-folha.webp" data-legenda="Président · aproveitamento de chapa" alt="Chapa com 6 displays encaixados" data-cursor="Ampliar">
    </div>
    <div class="folhas anima d3">
      <span class="eyebrow">Executivos que entregamos<span class="so-tela"> · clique para ampliar a folha</span></span>
      <button class="fl amplia" data-amplia="assets/eng/pre-faca-folha.webp" data-legenda="Président · planificado com faca e cotas" data-cursor="Ampliar"><img src="assets/eng/pre-faca.webp" alt=""><b>Président</b><span>planificado com faca 1:1</span></button>
      <button class="fl amplia" data-amplia="assets/eng/sca-aprov-folha.webp" data-legenda="Scala Flow · aproveitamento de chapa por kit e por lote" data-cursor="Ampliar"><img src="assets/eng/sca-chapas.webp" alt=""><b>Scala</b><span>até 71% da chapa por lote</span></button>
      <button class="fl amplia" data-amplia="assets/eng/sni-vistas-folha.webp" data-legenda="Snickers · separador de compras, vistas e perspectiva" data-cursor="Ampliar"><img src="assets/eng/sni-chapa.webp" alt=""><b>Snickers</b><span>5 displays por chapa, 72%</span></button>
      <button class="fl amplia" data-amplia="assets/eng/pok-corte-folha.webp" data-legenda="Pokémon · brandwall, corte A-A e detalhes construtivos" data-cursor="Ampliar"><img src="assets/eng/pok-corte.webp" alt=""><b>Pokémon</b><span>cenografia: corte e detalhes</span></button>
    </div>
    <p class="fonte">Fonte: projetos executivos da 75 LAB (outubro de 2026), em DXF e PDF A2. Aproveitamento com 6 mm entre peças e 10 mm de margem.</p>
  </section>

'''

PROCESSO = '''  <!-- ===================================================== processo -->
  <section id="metodo" class="tela s-proc" data-tema="escuro" data-titulo="O processo da pauta à loja" data-cap="(04) Como vamos operar">
    <h2 class="anima">Da pauta à loja em cinco etapas, <span class="t-lime">e nenhuma começa antes de a anterior fechar.</span></h2>
    <p class="lead anima d1">Exemplo real do calendário de vocês: São João, na loja em 17 de maio de 2027, contado para trás nos 100 dias úteis do briefing.</p>
    <div class="etapas anima d2">
      ETAPAS
    </div>
    <div class="regua-p anima d3">
      <div class="seg" style="--w:10%"><span>18/12</span></div><div class="seg" style="--w:20%"><span>05/01</span></div><div class="seg" style="--w:20%"><span>02/02</span></div><div class="seg prod" style="--w:35%"><span>04/03</span></div><div class="seg" style="--w:15%"><span>26/04</span></div><b class="fimr">17/05 · na loja</b>
    </div>
    <p class="nota-p anima d3"><b>A produção leva 35 dos 100 dias.</b> É a etapa que não comprime, por isso a concorrência de três fornecedores abre em 04/03, e não em abril.</p>
  </section>

'''
ETAPAS = [
    ('1', 'Pauta', '10 d.u.', '18/12 a 05/01', 'Briefing do cliente', 'Pauta validada', 'Escopo, prazo e formatos acordados por escrito'),
    ('2', 'Direção', '20 d.u.', '05/01 a 02/02', 'Pauta validada', 'KV ou rota criativa', 'Aprovação formalizada e registrada'),
    ('3', 'Engenharia', '20 d.u.', '02/02 a 04/03', 'KV aprovado', 'Arte-final e planta técnica', 'Checagem técnica e legal assinada'),
    ('4', 'Produção', '35 d.u.', '04/03 a 26/04', 'Arte-final', 'Material produzido', 'Três orçamentos, protótipo testado e QA de lote'),
    ('5', 'Loja', '15 d.u.', '26/04 a 17/05', 'Material produzido', 'Material posicionado', 'Comprovação de entrega e de execução'),
]
PROCESSO = PROCESSO.replace('ETAPAS', ''.join(
    f'<div class="et{" prod" if n == "4" else ""}"><span class="bola">{n}</span><b>{t}</b><em>{d} · {dt}</em>'
    f'<dl><dt>Entra</dt><dd>{e}</dd><dt>Sai</dt><dd>{s}</dd><dt>Só avança quando</dt><dd>{q}</dd></dl></div>'
    for n, t, d, dt, e, s, q in ETAPAS))

FLUXO = '''  <!-- ===================================================== fluxo -->
  <section id="fluxo" class="tela s-flu2" data-tema="claro" data-titulo="Fluxo e controles" data-cap="(04) Como vamos operar">
    <h2 class="anima">A arte rápida de 2 dias não entra <span class="onda t-teal">na mesma fila do ciclo de 100.</span></h2>
    <div class="raias anima d1">
      <div class="raia rapida"><div class="nome"><b>Via rápida</b><span>Arte rápida · 1 a 2 dias úteis</span></div>
        <div class="estacoes"><i class="token"></i><span class="est"><i></i><span>Pedido</span></span><span class="est"><i></i><span>Triagem e SLA</span></span><span class="est"><i></i><span>Criação</span></span><span class="est"><i></i><span>Aprovação</span></span><span class="est"><i></i><span>Entrega</span></span></div></div>
      <div class="raia ciclo"><div class="nome"><b>Ciclo de campanha</b><span>100 dias úteis</span></div>
        <div class="estacoes"><i class="token"></i><span class="est"><i></i><span>Pauta</span></span><span class="est"><i></i><span>Direção</span></span><span class="est"><i></i><span>Engenharia</span></span><span class="est"><i></i><span>Produção</span></span><span class="est"><i></i><span>Loja</span></span></div></div>
    </div>
    <span class="eyebrow tit-ctl anima d2">Os seis controles que valem para as duas filas</span>
    <div class="controles2 anima d2">
      <div><svg class="ic"><use href="#i-chat"/></svg><b>Tráfego</b><p>Todo pedido entra no Ariuno por formulário e vira card com responsável, prazo e etapa. Nada corre por e-mail solto.</p></div>
      <div><svg class="ic"><use href="#i-relogio"/></svg><b>SLA por tipo</b><p>Prazo visível para vocês. O tempo esperando aprovação aparece separado do atraso da agência.</p></div>
      <div><svg class="ic"><use href="#i-versao"/></svg><b>Versão e aprovação</b><p>Cada versão fica no card, com data e autor. Qual arte foi para a gráfica está no sistema.</p></div>
      <div><svg class="ic"><use href="#i-pasta"/></svg><b>SharePoint e acervo</b><p>Base de lojas, layouts, artes finais e cronograma integrado, no lugar que vocês já usam.</p></div>
      <div><svg class="ic"><use href="#i-fabrica"/></svg><b>Fornecedor</b><p>Três orçamentos, protótipo testado em loja e QA de lote antes de liberar a tiragem.</p></div>
      <div><svg class="ic"><use href="#i-escudo"/></svg><b>Conformidade</b><p>Checagem técnica e legal assinada, faturamento conferido antes do pagamento e SEFAZ sob nossa gestão.</p></div>
    </div>
  </section>

'''

SIMULADOR = '''  <!-- ===================================================== simulador do Ariuno -->
  <section id="cliente-fee" class="tela s-simu" data-tema="claro2" data-titulo="Simulador do Ariuno" data-cap="(04) Como vamos operar">
    <span class="eyebrow anima"><b>Ariuno personalizado</b> · criado para atender a Alpargatas</span>
    <h2 class="anima d1">Entrada, saída e avaliação de cada material, <span class="t-teal">passo a passo.</span></h2>
    <div class="fases anima d2"><span class="f-ent">Entrada</span><span class="f-sai">Saída</span><span class="f-ava">Avaliação</span></div>
    <ol class="passos-s anima d2" id="simPassos">
      <li class="on" data-fase="ent" data-img="0"><button data-cursor="Ver"><i>1</i><b>O trade pede pelo link</b></button><p>Sem login: o trade de vocês abre o link da campanha e marca as peças. As peças do escopo já vêm mapeadas por canal e tipo de campanha.</p></li>
      <li data-fase="ent" data-img="1"><button data-cursor="Ver"><i>2</i><b>Uma peça por formato de loja</b></button><p>A peça que vale para vários formatos vira uma por formato: Premium, Standard, Light, Compacta, Quiosque. Na demonstração, 10 pedidas viram 15.</p></li>
      <li data-fase="sai" data-img="1"><button data-cursor="Ver"><i>3</i><b>A arte entra em cada peça</b></button><p>O time entrega a arte dentro da própria peça e ela passa a aparecer como esperando vocês. Cada versão fica guardada com data e autor.</p></li>
      <li data-fase="ava" data-img="2"><button data-cursor="Ver"><i>4</i><b>Aprovar ou pedir ajuste na arte</b></button><p>Vocês aprovam ou marcam o ajuste em cima da peça: ponto numerado, seta, área destacada, anexo e print colado.</p></li>
      <li data-fase="ava" data-img="3"><button data-cursor="Ver"><i>5</i><b>A situação de cada material</b></button><p>Aprovadas, esperando vocês, em ajuste, em criação e sem arte. As aprovadas entram no quadro de produção num card por campanha.</p></li>
    </ol>
    <div class="tela-s anima dir d2">
      <div class="barra-j"><i></i><i></i><i></i><span id="simUrl">ariuno.com.br/?briefingFee=…</span></div>
      <div class="vista" id="simVista">
        <img class="on" src="assets/ariuno/fee-briefing.webp" alt="Briefing pelo link" data-url="ariuno.com.br/?briefingFee=…">
        <img src="assets/ariuno/fee-aprovacao.webp" alt="Peças por formato de loja" data-url="ariuno.com.br/?aprovacaoFee=…" loading="lazy">
        <img src="assets/ariuno/fee-ajuste.webp" alt="Ajuste marcado na arte" data-url="ariuno.com.br/?aprovacaoFee=…" loading="lazy">
        <img src="assets/ariuno/fee-aba.webp" alt="Situação de cada peça" data-url="ariuno.com.br · Gestão Cliente Fee" loading="lazy">
      </div>
      <div class="ctl-s so-tela"><button id="simAnt" data-cursor="Voltar">← Passo anterior</button><span id="simN">Passo 1 de 5</span><button id="simProx" class="prox" data-cursor="Seguir">Próximo passo →</button></div>
    </div>
    <div class="story" aria-hidden="true">
      <figure><img src="assets/ariuno/fee-briefing.webp" alt=""><figcaption><i>1</i>Entrada · o trade pede pelo link</figcaption></figure>
      <figure><img src="assets/ariuno/fee-aprovacao.webp" alt=""><figcaption><i>2 e 3</i>Uma peça por formato, com a arte dentro</figcaption></figure>
      <figure><img src="assets/ariuno/fee-ajuste.webp" alt=""><figcaption><i>4</i>Avaliação · ajuste marcado na arte</figcaption></figure>
      <figure><img src="assets/ariuno/fee-aba.webp" alt=""><figcaption><i>5</i>A situação de cada material</figcaption></figure>
    </div>
    <p class="fonte">Fonte: Ariuno, sistema de gestão da 75 LAB, em modo demonstração · campanha de exemplo Dia das Mães + Aura.</p>
  </section>

'''

def papel(nome, desc, sen, pct, h):
    return (f'<div class="pp"><div class="q"><strong>{nome}</strong><em>{desc}</em></div><span class="sen">{sen}</span>'
            f'<span class="ded{" parcial" if pct < 100 else ""}">{pct}%</span><span class="h"><b>{h}</b> h/mês</span></div>')

TIME = '''  <!-- ===================================================== o time -->
  <section id="time" class="tela s-time2" data-tema="claro" data-titulo="O time dedicado" data-cap="(04) Como vamos operar">
    <h2 class="anima">Um time só de vocês: <span class="t-teal">6 pessoas no DTC, 5 no B2B.</span></h2>
    <div class="legenda-t anima d1">
      <span><i class="d"></i><b>Dedicada</b> trabalha só na conta de vocês (100% = 176 h por mês)</span>
      <span><i class="c"></i><b>Compartilhada</b> parte do tempo em cada canal, com a porcentagem declarada</span>
      <span><b>FTE</b> = quantas pessoas em tempo integral isso soma</span>
    </div>
    <div class="nucleo2 anima d2"><div class="cab2"><b>Núcleo DTC</b><span><strong>6,8</strong> FTE · <strong>1.197</strong> h/mês</span></div>
      DTC_PAPEIS
    </div>
    <div class="nucleo2 b2b anima d3"><div class="cab2"><b>Núcleo B2B</b><span><strong>5,8</strong> FTE · <strong>1.021</strong> h/mês</span></div>
      B2B_PAPEIS
    </div>
    <div class="comp2 anima d4"><span class="eyebrow">Compartilhados entre os dois núcleos</span>
      <div class="cp"><strong>Diretor(a) de criação</strong><span class="pill a">30% DTC · 53 h</span><span class="pill b">30% B2B · 53 h</span><small>uma só direção nos dois canais: unicidade de marca</small></div>
      <div class="cp"><strong>Arquiteto(a) e 3D</strong><span class="pill a">25% DTC · 44 h</span><span class="pill b">50% B2B · 88 h</span><small>projetos especiais, lojas modeladas e GC</small></div>
      <div class="cp"><strong>Analista fiscal</strong><span class="pill a">25% DTC · 44 h</span><span class="pill b">25% B2B · 44 h</span><small>faturamento, SEFAZ e pagamentos</small></div>
    </div>
    <div class="total-t anima d4"><b class="num" data-conta="14">0</b><span>pessoas<br><strong>12,6 FTE</strong> no total</span></div>
  </section>

'''
TIME = TIME.replace('DTC_PAPEIS', ''.join(papel(*p) for p in [
    ('Gestor(a) de conta DTC', 'pauta, cronograma integrado e SharePoint', 'Sênior', 100, 176),
    ('Designer 3D e engenharia de PDV', 'engenharia por formato, executivo e loja em 3D', 'Pleno', 100, 176),
    ('Designer gráfico e arte-final', 'desdobramento do KV nos formatos', 'Pleno', 100, 176),
    ('Produtor(a) de fornecedores', 'três orçamentos, fornecedor e QA de lote', 'Sênior', 100, 176),
    ('Produtor(a) de campo e SAC', 'protótipo em loja e atendimento à rede', 'Pleno', 100, 176),
    ('Analista de logística', 'envio loja a loja e ocorrências', 'Pleno', 100, 176),
])).replace('B2B_PAPEIS', ''.join(papel(*p) for p in [
    ('Gestor(a) de conta B2B', 'alimentar e especializado, pauta e status', 'Sênior', 100, 176),
    ('Designer gráfico sênior', 'KV, desdobramento e as 16 peças da campanha', 'Sênior', 100, 176),
    ('Designer de artes rápidas', 'as 8 artes da semana e vídeos curtos', 'Pleno', 100, 176),
    ('Produtor(a) de fornecedores', 'orçamento, negociação e amostras', 'Pleno', 100, 176),
    ('Analista de logística e implementação', 'operador logístico, GC e ativações', 'Pleno', 75, 132),
]))

LOJAS = '''  <!-- ===================================================== lojas modeladas -->
  <section id="bim" class="tela s-lojas" data-tema="escuro" data-titulo="As lojas que já modelamos" data-cap="(05) Tecnologia antes de produzir">
    <h2 class="anima">Já modelamos as lojas de vocês. <span class="t-lime">A peça é aprovada dentro da loja antes de existir.</span></h2>
    <p class="lead anima d1">Cinco ambientes em 3D, com o enxoval de São João aplicado. Com a planta e as fotos de cada loja, modelamos as 728: cada franqueado vê, no próprio espaço, como a campanha vai ficar antes de a faca ser cortada.</p>
    <div class="galeria-l anima d2">
      <button class="lj grande amplia" data-amplia="assets/lojas/folha-shopping.webp" data-legenda="Loja de shopping · 20 renders" data-cursor="Ampliar"><img src="assets/lojas/shopping.webp" alt=""><b>Loja de shopping</b><span>20 renders</span></button>
      <button class="lj amplia" data-amplia="assets/lojas/folha-rua.webp" data-legenda="Loja de rua · 12 renders" data-cursor="Ampliar"><img src="assets/lojas/rua.webp" alt=""><b>Loja de rua</b><span>12 renders</span></button>
      <button class="lj amplia" data-amplia="assets/lojas/folha-quiosque.webp" data-legenda="Quiosque · 14 renders" data-cursor="Ampliar"><img src="assets/lojas/quiosque.webp" alt=""><b>Quiosque</b><span>14 renders</span></button>
      <button class="lj amplia" data-amplia="assets/lojas/folha-store-in-store.webp" data-legenda="Store in store · 13 renders" data-cursor="Ampliar"><img src="assets/lojas/store-in-store.webp" alt=""><b>Store in store</b><span>13 renders</span></button>
      <button class="lj amplia" data-amplia="assets/lojas/folha-corredor.webp" data-legenda="Corredor do varejo · 8 renders" data-cursor="Ampliar"><img src="assets/lojas/corredor.webp" alt=""><b>Corredor do varejo</b><span>8 renders</span></button>
    </div>
    CTA_LOJAS
    <div class="ganhos2 anima d3">
      <div><b>Compra mais certa</b><p>A dimensão errada aparece no modelo, não no protótipo: corrigir é um arquivo, não 728 reimpressões.</p></div>
      <div><b>Criação mais impactante</b><p>A visibilidade é decidida vendo a peça no big hello, na vitrine e na mesa de cada formato.</p></div>
      <div><b>Teste mais barato</b><p>Rodar uma alternativa custa uma tarde, não um lote.</p></div>
    </div>
    <p class="fonte">* Modelos feitos pela 75 LAB apenas com base em visitas às lojas e em referências visuais, sem planta nem manual de marca de vocês.</p>
  </section>

'''.replace('CTA_LOJAS', CTA('Clique numa loja para ver todos os renders'))

IA = '''  <!-- ===================================================== IA -->
  <section class="tela s-ia2" data-tema="claro" data-titulo="Onde a IA entra" data-cap="(05) Tecnologia antes de produzir">
    <h2 class="anima">A IA acelera o repetível. <span class="onda t-teal">Quem decide é o time.</span></h2>
    <div class="proc-ia anima d1">
      <div class="cab-ia"><span></span>PASSOS</div>
      <div class="linha-ia sem"><span class="rot">Sem IA</span>SEM</div>
      <div class="linha-ia com"><span class="rot">Com IA</span>COM</div>
    </div>
    <div class="vant anima d2">
      <span class="eyebrow">O que vocês ganham</span>
      <div><b>Mais alternativas</b><p>Vários caminhos de conceito antes de escolher, no tempo em que antes saía um.</p></div>
      <div><b>Formatos em paralelo</b><p>As 5 versões de loja são adaptadas juntas, não uma depois da outra.</p></div>
      <div><b>Menos erro de texto</b><p>Decupagem e conferência automática contra o briefing antes da revisão humana.</p></div>
      <div><b>Tempo onde importa</b><p>O time sai do repetitivo e gasta horas em direção, engenharia e execução.</p></div>
    </div>
    <div class="regras-ia anima d3">
      <div class="nao"><span class="eyebrow">Onde a IA não entra</span><p>Direção de arte · texto legal e regulatório · aprovação final · assinatura técnica de planta</p></div>
      <div class="prot"><span class="eyebrow">Como protegemos</span><p>Contas corporativas, com material de cliente fora de treinamento · revisor humano nomeado em toda peça · histórico de versão com quem aprovou e quando · ferramentas: ChatGPT e Claude</p></div>
    </div>
  </section>

'''
PASSOS_IA = [('Briefing', 'leitura e decupagem', 'decupagem automática do briefing', True),
             ('Conceito', 'um caminho por vez', 'vários caminhos visuais para escolher', True),
             ('Desdobramento', 'formato a formato', 'os 5 formatos adaptados juntos', True),
             ('Engenharia', 'medida e planta técnica', 'medida e planta técnica', False),
             ('Arte-final', 'conferência manual', 'conferência de texto automática', True),
             ('Aprovação', 'time e cliente', 'time e cliente', False)]
IA = (IA.replace('PASSOS', ''.join(f'<b>{p}</b>' for p, _, _, _ in PASSOS_IA))
        .replace('SEM', ''.join(f'<span class="cel">{s}</span>' for _, s, _, _ in PASSOS_IA))
        .replace('COM', ''.join(f'<span class="cel{" ia" if ia else " hum"}">{"<i>IA</i>" if ia else "<i>Time</i>"}{c}</span>' for _, _, c, ia in PASSOS_IA)))

COMO_FUNCIONA = '''  <!-- ===================================================== rastreio: como funciona -->
  <section id="serie" class="tela s-rc" data-tema="claro" data-titulo="Rastreio: como funciona" data-cap="(06) Rastreio peça a peça">
    <h2 class="anima">Cada peça tem um código único <span class="onda t-teal">e conta a própria história.</span></h2>
    <div class="etq anima d1"><svg class="ic"><use href="#i-qr"/></svg><div><b>ALP-SJ27-TST-0412</b><span>testeira · São João 2027 · loja 0412</span></div></div>
    <div class="trilha2 anima d2">
      <div class="pt"><span class="bola"><svg class="ic"><use href="#i-tag"/></svg></span><b>1 · Código na peça</b><p>Cada peça sai da gráfica com etiqueta própria, não um QR de campanha.</p></div>
      <div class="pt"><span class="bola"><svg class="ic"><use href="#i-fabrica"/></svg></span><b>2 · Expedição</b><p>O scan na saída do fornecedor registra o que foi enviado para cada loja.</p></div>
      <div class="pt"><span class="bola"><svg class="ic"><use href="#i-loja"/></svg></span><b>3 · Recebimento</b><p>A loja escaneia ao receber: relatório em D+2.</p></div>
      <div class="pt"><span class="bola"><svg class="ic"><use href="#i-camera"/></svg></span><b>4 · Instalação com foto</b><p>Montada, fotografada, com GPS: relatório em D+7.</p></div>
      <div class="pt"><span class="bola"><svg class="ic"><use href="#i-lupa"/></svg></span><b>5 · Auditoria</b><p>Continua lá? Amostra por loja e ocorrência automática de quem não leu.</p></div>
      <div class="pt fim"><span class="bola"><svg class="ic"><use href="#i-grafico"/></svg></span><b>6 · Painel</b><p>Tudo ao vivo, por loja, rede, formato e estado, desde o primeiro envio.</p></div>
    </div>
    <div class="dois-t anima d3">
      <div class="tp"><svg class="ic"><use href="#i-qr"/></svg><div><b>QR em etiqueta</b><span>para material de campanha, descartável e em massa</span><small>testeira, tag de gancheira, display de caixa, bandeirola, adesivo de chão</small></div></div>
      <div class="tp"><svg class="ic"><use href="#i-sinal"/></svg><div><b>GPS ou BLE</b><span>para ativo caro que volta</span><small>corner, ilha, ambientação de GC, cenografia de flagship, mesa big hello</small></div></div>
      <div class="tp vivo"><svg class="ic"><use href="#i-check"/></svg><div><b>Já está no ar</b><span>o scan abre a página da peça, com montagem, vídeo e AR, e registra loja, GPS e foto</span><small>em uso nas peças que produzimos, não é protótipo de apresentação</small></div></div>
    </div>
  </section>

'''

DEMO = '''  <!-- ===================================================== campanha demo -->
  <section id="campanha-demo" class="tela s-demo" data-tema="foto" data-titulo="Na prática: campanha demo São João 2027" data-cap="(07) Na prática: São João 2027">
    <video class="kv sangra" src="assets/video/kv-sj-animado.mp4" poster="assets/img/kv-sj-1.webp" muted loop playsinline preload="none"></video>
    <div class="veu sangra"></div>
    <div class="cartao-d anima esq">
      <span class="eyebrow"><b>Capítulo 07</b> · Na prática</span>
      <h2>Montamos uma campanha inteira de São João <span class="t-lime">para vocês verem.</span></h2>
      <p>Conceito, três KVs e as 51 peças da lista do BID em 3D, do DTC ao B2B. Está numa apresentação própria, feita para navegar.</p>
      <div class="nums-d"><span><b>1</b>conceito</span><span><b>3</b>key visuals</span><span><b>51</b>peças em 3D</span><span><b>4</b>canais</span></div>
      <a class="botao cheio grande-b so-tela" href="https://projetos.75lab.com.br/havaianas-sao-joao-2027/" target="_blank" rel="noopener" data-cursor="Abrir">Clique e abra a campanha completa <span class="ext">↗</span></a>
      <p class="aviso-d">Campanha demonstrativa, criada sem briefing nem manual de marca de vocês.</p>
    </div>
    <a class="qr-d anima zoom d2" href="https://projetos.75lab.com.br/havaianas-sao-joao-2027/" target="_blank" rel="noopener" data-cursor="Abrir">
      <img src="assets/qr/campanha-sj.svg" alt="QR da campanha demo">
      <b>Aponte a câmera do celular</b>
      <span>projetos.75lab.com.br/havaianas-sao-joao-2027</span>
    </a>
    <div class="pecas-d anima d3">
      <img src="assets/img/sj-p030.webp" alt=""><img src="assets/img/sj-p004.webp" alt=""><img src="assets/img/sj-p040.webp" alt=""><img src="assets/img/sj-p059.webp" alt=""><img src="assets/img/sj-p012.webp" alt="">
    </div>
  </section>

'''

INICIO = '''  <!-- ===================================================== começar antes do contrato -->
  <section id="inicio" class="tela s-ini" data-tema="escuro" data-titulo="Começar antes do contrato" data-cap="(08) Como começamos">
    <span class="eyebrow anima"><b>Nossa recomendação</b></span>
    <h2 class="anima d1">Começar antes do previsto: <span class="t-lime">setup, onboarding e handover antes de o contrato valer.</span></h2>
    <p class="lead anima d2">Na conta regressiva do calendário de 2027, entre a entrega desta proposta e o primeiro ciclo que ainda cabe completo há cinco dias úteis. Se a estrutura só começar a montar quando o contrato estiver vigente, a primeira campanha de vocês vira a nossa campanha de aprendizado.</p>
    <div class="leg anima d2"><span><i style="background:repeating-linear-gradient(135deg,rgba(242,241,233,.35) 0 6px,rgba(242,241,233,.1) 6px 12px)"></i>Herdada em andamento: handover</span><span><i style="background:var(--lime)"></i>Ciclo completo conosco</span></div>
    <div class="mapa anima d3" id="mapaTra"></div>
    <div class="tres-i anima d4">
      <div><i>1</i><b>Setup</b><p>Acessos, SharePoint, base de lojas, layouts e fornecedores homologados prontos. Estrutura operando em até 30 dias.</p></div>
      <div><i>2</i><b>Onboarding</b><p>Assessment de 15 dias com trade, marketing, operações, rede e franquias, suprimentos e fiscal: é dele que sai o cronograma real do ano.</p></div>
      <div><i>3</i><b>Handover</b><p>As campanhas já em andamento passam para nós em paralelo com a estrutura atual, sem corte seco, até D+90.</p></div>
    </div>
  </section>

'''

# ------------------------------------------------------------------ ajustes nas telas que ficam
vol = tela('s-vol')
vol = vol.replace('<h2 class="anima">35 campanhas em 2027.', '<span class="destaque-cap anima">O que entendemos do desafio</span>\n    <h2 class="anima">35 campanhas em 2027.')
vol = vol.replace('<div class="topo-col"><b class="num" data-conta="23">0</b><span>DTC<br>campanhas</span></div>', '<div class="topo-col"><b class="canal-n">DTC</b><span>lojas próprias,<br>franquias e quiosques</span></div>')
vol = vol.replace('<div class="topo-col"><b class="num" data-conta="12">0</b><span>B2B<br>campanhas</span></div>', '<div class="topo-col"><b class="canal-n">B2B</b><span>varejo alimentar<br>e especializado</span></div>')
vol = cap(vol, '01')

sim = cap(tela('s-sim'), '01').replace('<span class="so-tela">Arraste a linha verde e confira.</span>', '')
sim = sim.replace('<div class="gantt anima d2" id="gantt"></div>', '<div class="gantt anima d2" id="gantt"></div>\n    ' + CTA('Arraste a linha verde ou use os botões para ver o pico'))
tese = cap(tela('s-tese'), '01')

fre = cap(tela('s-fre'), '02').replace(' <span class="so-tela">Clique em cada uma.</span>', '')
fre = fre.replace('<div class="detalhe anima d3">', CTA('Clique em cada frente') + '\n    <div class="detalhe anima d3">')
fre = fre.replace('    <template id="freDados">', '    <div class="todas-f" aria-hidden="true"></div>\n    <template id="freDados">')

num = cap(tela('s-num'), '02')
num = num.replace('<span class="subtitulo anima">Nossos números</span>\n    <h2 class="anima">A operação é dimensionada <span class="onda t-teal">por ano, não por campanha.</span></h2>',
                  '<span class="destaque-cap anima">Números da 75 LAB · 12 meses medidos no nosso sistema</span>\n    <h2 class="anima">A 75 LAB em números: <span class="onda t-teal">a operação que já rodamos hoje.</span></h2>')
num = num.replace('<p class="fonte">Fonte: Ariuno, sistema de gestão da 75 LAB', '<p class="fonte">Dados da própria 75 LAB, não de cliente. Fonte: Ariuno, sistema de gestão da 75 LAB')

cases = cap(tela('s-cases'), '03')
cases = cases.replace('<div class="grade">', CTA('Gire as peças com o mouse, veja a foto ou abra em AR no celular') + '\n    <div class="grade">')

dep = cap(tela('s-dep'), '03')
for r in ('reel3', 'reel1'):
    dep = re.sub(r'\s*<button class="vid" data-src="assets/video/' + r + r'\.mp4".*?</button>', '', dep, flags=re.S)
novos = ''.join(
    f'\n        <button class="vid" data-src="assets/video/{a}.mp4" data-poster="assets/video/{a}.webp" data-dur="{d}" data-cursor="Assistir"><span class="capa"><img src="assets/video/{a}.webp" alt="" loading="lazy"><i></i><em>{d}</em></span><b>{t}</b></button>'
    for a, d, t in [('alltak-hausdecor', '1min17', 'Alltak · HausDecor'), ('boticario', '53s', 'O Boticário · display flex'), ('evino', '1min25', 'Evino · corta-gotas')])
dep = dep.replace('<b>Depoimento · stand Alltak Decor</b></button>', '<b>Depoimento · stand Alltak Decor</b></button>' + novos, 1)
dep = dep.replace('<span class="eyebrow">Os vídeos da 75 LAB<span class="so-tela"> · clique para assistir no celular ao lado</span></span>',
                  '<span class="eyebrow">Projetos da 75 LAB em vídeo</span>\n      ' + CTA('Clique num vídeo para assistir no celular ao lado'))
dep = dep.replace('<p class="fonte">Vídeos: Instagram @setecincolab, publicados no site 75lab.com.br, e case do stand Alltak Decor.</p>',
                  '<p class="fonte">Vídeos de projetos da 75 LAB: Instagram @setecincolab, site 75lab.com.br e acervo de cases.</p>')

dim = cap(tela('s-dim'), '04')
dim = dim.replace('<h2 class="anima">O tamanho do time <span class="t-lime">saiu do nosso sistema,</span> não de estimativa.</h2>',
                  '<span class="destaque-cap anima">A performance real da 75 LAB</span>\n    <h2 class="anima">O tamanho do time saiu <span class="t-lime">da nossa performance medida,</span> não de estimativa.</h2>')
dim = dim.replace('<div class="etapa-n"><i>1</i>Medimos: horas por entrega no Ariuno</div>', '<div class="etapa-n"><i>1</i>Nossa performance: horas por entrega, medidas na 75 LAB</div>')

qr = cap(tela('s-qr'), '06')
qr = qr.replace('<div class="janela anima d2">', CTA('Clique nas abas para trocar a vista do painel') + '\n    <div class="janela anima d2">')
dad = cap(tela('s-dad'), '06').replace('data-titulo="Relato vira dado auditável"', 'data-titulo="O que vocês ganham"')
fec = cap(tela('s-fec'), '06')
com = cap(tela('s-com'), '06')
ris = cap(tela('s-ris'), '08').replace('<div class="lista anima d1">', CTA('Clique em cada risco para ver a resposta') + '\n    <div class="lista anima d1">')
fimt = cap(tela('s-fim'), '08')
capa = tela('s-capa').replace('data-ir="essencial"', 'data-ir="resumo"').replace('<button class="botao seta" data-ir="time" data-cursor="Ver">Ver o time</button>', '<button class="botao seta" data-ir="campanha-demo" data-cursor="Ver">Ver a campanha demo</button>')

novo = ''.join([
    capa, RESUMO,
    capitulo(0), vol, sim, FRANQUEADO, tese,
    capitulo(1), PROPOSITO, DIFERENCIAL, fre, RESP, num, CLIENTES,
    capitulo(2), cases, ENGENHARIA, dep,
    capitulo(3), PROCESSO, FLUXO, SIMULADOR, TIME, dim,
    capitulo(4), LOJAS, IA,
    capitulo(5), COMO_FUNCIONA, qr, dad, fec, com,
    DEMO,
    capitulo(7), ris, INICIO, fimt,
])
saida = html[:ini] + '\n' + novo + html[fim:]
saida = saida.replace('<symbol id="i-funil"', '<symbol id="i-clique" viewBox="0 0 48 48"><path d="M19 26V9a4 4 0 0 1 8 0v13l9 2c3 .7 5 3.6 4.4 6.6L39 39c-.5 3-3 5-6 5H24c-2 0-3.8-1-5-2.6L11 31c-1.4-2 0-4.8 2.4-4.8 1 0 2 .4 2.7 1.2L19 30"/><path d="M8 12l4 2M10 4l3 4M18 1v4"/></symbol>\n  <symbol id="i-funil"', 1)
(RAIZ / 'index.html').write_text(saida, encoding='utf-8')
n = len(re.findall(r'<section\b[^>]*class="tela', saida))
print('telas', n)
