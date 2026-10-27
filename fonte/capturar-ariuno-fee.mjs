// Captura as telas da Gestão Cliente Fee na demo pública do Ariuno, em 2x.
// A demo não tem arte nas peças: o código publicado é trocado só nesta captura
// para apontar cada peça para uma imagem do briefing da Havaianas (local).
import { chromium } from '/Volumes/hd caique becker/Mac Caique/Projetos/ariuno-videos/node_modules/playwright/index.mjs';
import { readFileSync } from 'node:fs';

const OUT = process.argv[2] || new URL('./out/', import.meta.url).pathname;
const IMG = process.env.HOME + '/alpargatas-bid-75lab/assets/img/';
const arteDe = (nome) => {
  const n = nome.toLowerCase();
  if (n.includes('mesa')) return 'vis-mesa.webp';
  if (n.includes('cubo') || n.includes('palete')) return 'vis-bighello.webp';
  if (n.includes('big hello')) return 'vis-bighello.webp';
  if (n.includes('vitrine')) return 'vitrine.webp';
  if (n.includes('painel') || n.includes('prateleira') || n.includes('parede')) return 'vis-painel.webp';
  if (n.includes('quiosque')) return 'fmt-quiosque.webp';
  return 'esp-4.webp';
};

const navegador = await chromium.launch({ channel: 'chrome' });
const ctx = await navegador.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, locale: 'pt-BR' });
await ctx.route(/\/assets\/index-[^/]+\.js$/, async (route) => {
  const r = await route.fetch();
  let js = await r.text();
  const antes = js.length;
  js = js.replace('url:"",nome:"arte-v1.jpg"', 'url:"/__arte/"+encodeURIComponent(v.nome+"|"+v.formato)+".webp",nome:"arte-v1.jpg"');
  if (js.length === antes) console.log('AVISO: amostra não encontrada no código');
  await route.fulfill({ response: r, body: js });
});
await ctx.route(/\/__arte\//, (route) => {
  const nome = decodeURIComponent(route.request().url().split('/__arte/')[1]).split('|')[0];
  route.fulfill({ contentType: 'image/webp', body: readFileSync(IMG + arteDe(nome)) });
});
const pg = await ctx.newPage();
const espera = (ms) => pg.waitForTimeout(ms);
const tira = async (nome, opts = {}) => { await pg.screenshot({ path: OUT + nome, ...opts }); console.log('ok', nome); };
const esconderDemo = () => pg.evaluate(() => {
  for (const el of document.querySelectorAll('div')) if ((el.textContent || '').trim() === 'Demonstração: nada aqui é gravado.') el.style.display = 'none';
  for (const el of document.querySelectorAll('body *')) {
    if (/^Modo demonstração$/.test(el.textContent?.trim() || '')) {
      let p = el; while (p && getComputedStyle(p).position !== 'fixed') p = p.parentElement;
      if (p) p.style.display = 'none';
    }
  }
});

// ---- 1. aba interna
await pg.goto('https://ariuno.com.br/?demo=1');
await pg.evaluate(() => localStorage.setItem('ariuno_teste_cliente_fee', '1'));
await pg.goto('https://ariuno.com.br/?demo=1');
await espera(5000);
await pg.keyboard.press('Escape');
await espera(800);
await pg.getByText('Gestão Cliente Fee', { exact: true }).first().click();
await espera(2500);
await esconderDemo();
await espera(500);
await tira('fee-aba.png');

// ---- 2. janela da peça com ajuste marcado na arte
await pg.getByText('Light (cubos)', { exact: true }).first().click();
await espera(1500);
await esconderDemo();
await tira('fee-peca.png');
await pg.keyboard.press('Escape');

// ---- 3. briefing público
await pg.goto('https://ariuno.com.br/?briefingFee=demo');
await espera(3500);
const campos = pg.locator('input:not([type=date]):not([type=file]):not([type=checkbox])');
await campos.nth(0).fill('Mariana (Trade DTC)');
await campos.nth(1).fill('trade.dtc@alpargatas.com.br');
await pg.getByPlaceholder('Ex.: Dia das Mães + Aura').fill('Dia das Mães + Aura');
await campos.nth(3).fill('600').catch(() => {});
const datas = pg.locator('input[type=date]');
await datas.nth(0).fill('2027-01-25').catch(() => {});
await datas.nth(1).fill('2027-04-12').catch(() => {});
await pg.locator('textarea').first().fill('Dia das Mães com a linha Aura em destaque. Big Hello e vitrine com o KV, mesa com a coleção.').catch(() => {});
await espera(500);
await tira('fee-briefing.png');
await pg.mouse.wheel(0, 900);
await espera(800);
await tira('fee-briefing-pecas.png');

// ---- 4. aprovação pública
await pg.goto('https://ariuno.com.br/?aprovacaoFee=demo');
await espera(3500);
await pg.getByPlaceholder('Vai junto com as aprovações').fill('Mariana (Trade DTC)');
await espera(600);
await tira('fee-aprovacao.png');
await pg.getByRole('button', { name: 'Pedir ajuste' }).first().click();
await espera(1500);
const arte = pg.locator('img[alt]').filter({ hasNot: pg.locator('xx') }).last();
const box = await arte.boundingBox();
const em = (fx, fy) => [box.x + box.width * fx, box.y + box.height * fy];
await pg.mouse.click(...em(0.52, 0.30));
await espera(500);
const notas = pg.locator('textarea, input[type=text]');
const n = await notas.count();
for (let i = 0; i < n; i++) { const v = await notas.nth(i).inputValue().catch(() => 'x'); const ph = await notas.nth(i).getAttribute('placeholder'); if (!v && ph && !/Algo que vale/.test(ph)) { await notas.nth(i).fill('Trocar o KV pelo da linha Aura'); break; } }
await pg.getByRole('button', { name: 'Destacar área' }).click();
await pg.mouse.move(...em(0.08, 0.62)); await pg.mouse.down(); await pg.mouse.move(...em(0.50, 0.95), { steps: 8 }); await pg.mouse.up();
await pg.getByRole('button', { name: 'Seta' }).click();
await pg.mouse.move(...em(0.88, 0.12)); await pg.mouse.down(); await pg.mouse.move(...em(0.66, 0.36), { steps: 8 }); await pg.mouse.up();
await espera(600);
await tira('fee-ajuste-aberto.png');
console.log('fim');
await navegador.close();
