# Insere o capítulo "Rede e gestão" (05) depois de "Como vamos operar" e renumera os capítulos seguintes.
#   python3 fonte/capitulo_rede.py   (rodar uma vez)
import re
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
p = RAIZ / 'index.html'
s = p.read_text(encoding='utf-8')
assert 'id="cap-rede"' not in s, 'já foi inserido'

CAPS = [('01', 'O desafio'), ('02', 'Quem é a 75 LAB'), ('03', 'O que já entregamos'), ('04', 'Como vamos operar'),
        ('05', 'Rede e gestão'), ('06', 'Tecnologia antes de produzir'), ('07', 'Rastreio peça a peça'),
        ('08', 'Na prática: São João 2027'), ('09', 'Como começamos')]
TRILHA = ''.join(f'<span data-c="{n}">{n}<b>{t}</b></span>' for n, t in CAPS)

# 1) renumera os capítulos de 05 em diante (de trás para frente)
for velho, novo in [('08', '09'), ('07', '08'), ('06', '07'), ('05', '06')]:
    s = s.replace(f'data-cap="({velho})', f'data-cap="({novo})')
    s = s.replace(f'data-titulo="Capítulo {velho} ·', f'data-titulo="Capítulo {novo} ·')
    s = s.replace(f'data-capitulo="{velho}"', f'data-capitulo="{novo}"')
    s = s.replace(f'<span class="num-cap sangra">{velho}</span>', f'<span class="num-cap sangra">{novo}</span>')
    s = s.replace(f'<b>Capítulo {velho}</b> de 08', f'<b>Capítulo {novo}</b> de 08')
    s = s.replace(f'<!-- ===================================================== capítulo {velho} -->', f'<!-- ===================================================== capítulo {novo} -->')
s = s.replace('<b>Capítulo 07</b> · Na prática', '<b>Capítulo 08</b> · Na prática')
s = s.replace(' de 08</span>', ' de 09</span>')
s = re.sub(r'<div class="trilha-cap anima d4" data-atual="(\d+)">.*?</div>', lambda m: f'<div class="trilha-cap anima d4" data-atual="{m.group(1)}">{TRILHA}</div>', s)

CTA = lambda txt: f'<span class="cta so-tela"><svg class="ic"><use href="#i-clique"/></svg>{txt}</span>'
MODS = [('atendimento', 'Atendimento à rede', 'E-mail e WhatsApp numa caixa só: cada conversa vira ticket ligado à loja, com prazo.'),
        ('lojas', 'Base de lojas e layouts', 'As 728 lojas com formato, planta, fotos e pontos de visibilidade.'),
        ('cronograma', 'Cronograma integrado', 'DTC e B2B no mesmo calendário, cada campanha nas cinco etapas.'),
        ('sharepoint', 'SharePoint integrado', 'O acervo fica no SharePoint de vocês, organizado por campanha, formato e loja.'),
        ('status', 'Status e report', 'Onde cada campanha está agora e o relatório que chega sem ninguém pedir.')]
ON = ' class="on"'
LAZY = ' loading="lazy"'
botoes = ''.join(f'<li{ON if i == 0 else ""}><button data-v="{v}" data-cursor="Ver"><i>{i+1:02d}</i><b>{t}</b></button><p>{d}</p></li>' for i, (v, t, d) in enumerate(MODS))
imgs = ''.join(f'<img{ON if i == 0 else ""} src="assets/rede/{v}.webp" alt="{t}" data-v="{v}"{"" if i == 0 else LAZY}>' for i, (v, t, _) in enumerate(MODS))
story = ''.join(f'<figure><img src="assets/rede/{v}.webp" alt=""><figcaption><i>{i+1:02d}</i>{t}</figcaption></figure>' for i, (v, t, _) in enumerate(MODS))

NOVO = f'''  <!-- ===================================================== capítulo 05 -->
  <section id="cap-rede" class="tela s-cap" data-tema="escuro" data-titulo="Capítulo 05 · Rede e gestão" data-cap="(05) Rede e gestão" data-capitulo="05">
    <span class="num-cap sangra">05</span>
    <div class="texto">
      <span class="eyebrow anima"><b>Capítulo 05</b> de 09</span>
      <h2 class="anima d1">Rede e gestão</h2>
      <p class="lead anima d2">Atendimento à rede, base de lojas, cronograma, SharePoint e report numa central só.</p>
    </div>
    <ol class="dentro anima d3"><li><i>01</i>A central da rede</li><li><i>02</i>Atendimento por WhatsApp e e-mail</li><li><i>03</i>Cronograma, SharePoint, status e report</li></ol>
    <div class="trilha-cap anima d4" data-atual="05">{TRILHA}</div>
  </section>

  <!-- ===================================================== a central da rede -->
  <section id="central" class="tela s-central" data-tema="claro2" data-titulo="A central da rede" data-cap="(05) Rede e gestão">
    <span class="eyebrow anima"><b>Simulação</b> · a central que montamos para a conta</span>
    <h2 class="anima d1">Uma central só para a rede, <span class="t-teal">a agência e vocês.</span></h2>
    <ol class="mods anima d2" id="modsCentral">{botoes}</ol>
    {CTA('Clique em cada módulo')}
    <div class="janela-c anima dir d2">
      <div class="barra-j"><i></i><i></i><i></i><span>central.75lab.com.br · conta Havaianas</span></div>
      <div class="vista" id="vistaCentral">{imgs}</div>
    </div>
    <a class="botao cheio seta abrir-c so-tela" href="assets/rede/central.html" target="_blank" rel="noopener" data-cursor="Abrir" id="abrirCentral">Abrir a simulação e navegar</a>
    <div class="story-c" aria-hidden="true">{story}</div>
    <p class="fonte">Simulação da central de rede e gestão da 75 LAB com dados de exemplo · nenhum dado de cliente. Lojas, franqueados e números fictícios.</p>
  </section>

  <!-- ===================================================== atendimento à rede -->
  <section id="atendimento" class="tela s-sac" data-tema="escuro" data-titulo="Atendimento à rede por WhatsApp e e-mail" data-cap="(05) Rede e gestão">
    <h2 class="anima">A rede fala com a gente por WhatsApp e e-mail. <span class="t-lime">Cada conversa vira ticket ligado à loja.</span></h2>
    <div class="passos-sac anima d1">
      <div><i>1</i><b>O franqueado escreve</b><p>No WhatsApp ou no e-mail da conta. O número cadastrado já identifica a loja.</p></div>
      <div><i>2</i><b>Vira ticket com prazo</b><p>Tema marcado (layout, montagem, não chegou, tiragem) e resposta em até 1 dia útil.</p></div>
      <div><i>3</i><b>A base de lojas responde</b><p>Formato, planta, pontos de visibilidade e as peças enviadas para aquela loja, na mesma tela.</p></div>
      <div><i>4</i><b>Resolve e registra</b><p>Reenvio, guia de montagem da loja ou foto da instalação. Tudo fica no histórico.</p></div>
      <div><i>5</i><b>Vira dado</b><p>Cada ocorrência entra no fechamento de ciclo e calibra a tiragem da próxima campanha.</p></div>
    </div>
    <img class="print-sac anima zoom d2 amplia" src="assets/rede/atendimento.webp" data-amplia="assets/rede/atendimento.webp" data-legenda="Atendimento à rede · simulação" alt="Atendimento à rede na central" data-cursor="Ampliar">
    <div class="base anima d3">
      <span class="eyebrow">O que a base de lojas guarda, loja a loja</span>
      <ul><li>Formato e metragem</li><li>Planta e pontos de visibilidade</li><li>Fotos da fachada e da execução</li><li>Peças de cada campanha</li><li>Contato do franqueado</li><li>Histórico de tickets</li></ul>
      <p>A planta muda, a base muda no mesmo dia, e o SharePoint recebe a versão nova.</p>
    </div>
    <p class="fonte">Simulação com dados de exemplo · nenhum dado de cliente.</p>
  </section>

  <!-- ===================================================== gestão: cronograma, sharepoint, status e report -->
  <section id="gestao" class="tela s-gest" data-tema="claro" data-titulo="Cronograma, SharePoint, status e report" data-cap="(05) Rede e gestão">
    <h2 class="anima">Vocês sabem onde cada coisa está <span class="onda t-teal">sem precisar perguntar.</span></h2>
    <div class="tres-g anima d1">
      <div><svg class="ic"><use href="#i-calendario"/></svg><b>Cronograma integrado</b><p>DTC e B2B no mesmo calendário, cada campanha nas cinco etapas, com a data de loja e o pico de simultaneidade à vista.</p></div>
      <div><svg class="ic"><use href="#i-pasta"/></svg><b>SharePoint integrado</b><p>O acervo fica no SharePoint de vocês, por campanha, formato e loja, com a versão aprovada e quem aprovou.</p></div>
      <div><svg class="ic"><use href="#i-grafico"/></svg><b>Status e report</b><p>Status quinzenal etapa a etapa e report semanal automático: o que aconteceu e o que precisa de vocês.</p></div>
    </div>
    <div class="prints-g anima d2">
      <img class="amplia" src="assets/rede/cronograma.webp" data-amplia="assets/rede/cronograma.webp" data-legenda="Cronograma integrado · simulação" alt="Cronograma integrado" data-cursor="Ampliar">
      <img class="amplia" src="assets/rede/sharepoint.webp" data-amplia="assets/rede/sharepoint.webp" data-legenda="SharePoint integrado · simulação" alt="SharePoint integrado" data-cursor="Ampliar">
      <img class="amplia" src="assets/rede/status.webp" data-amplia="assets/rede/status.webp" data-legenda="Status e report · simulação" alt="Status e report" data-cursor="Ampliar">
    </div>
    <div class="cad-g anima d3">
      <span class="eyebrow">A cadência da gestão</span>
      <div><b>Toda hora</b><span>painel ao vivo e atendimento à rede</span></div>
      <div><b>Semanal</b><span>pauta com o trade e report por e-mail</span></div>
      <div><b>Quinzenal</b><span>status de cada campanha</span></div>
      <div><b>Mensal</b><span>fechamento de ciclo e indicadores</span></div>
      <div><b>Trimestral</b><span>estratégia e calendário seguinte</span></div>
    </div>
    <p class="fonte">Simulação com dados de exemplo · nenhum dado de cliente.</p>
  </section>

'''
i = s.index('<section id="dimensionamento"')
k = s.index('</section>', i) + len('</section>\n')
s = s[:k] + '\n' + NOVO + s[k:]
p.write_text(s, encoding='utf-8')
print('telas', len(re.findall(r'<section\b[^>]*class="tela', s)))
