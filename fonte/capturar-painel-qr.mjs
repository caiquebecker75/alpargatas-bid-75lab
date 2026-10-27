// Painel de QR (projetos.75lab.com.br/produtos/painel) em DEMONSTRAÇÃO para o deck da Alpargatas.
// O Firebase é trocado por módulos falsos só nesta captura: nada lê nem grava o banco real.
// Dados fictícios: lojas Havaianas em shoppings e redes do B2B alimentar; fotos do briefing.
import { chromium } from '/Volumes/hd caique becker/Mac Caique/Projetos/ariuno-videos/node_modules/playwright/index.mjs';
import { readFileSync } from 'node:fs';

const OUT = process.argv[2] || new URL('./out/', import.meta.url).pathname;
const IMG = process.env.HOME + '/alpargatas-bid-75lab/assets/img/';
let seed = 7;
const rnd = () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;
const pega = (a) => a[Math.floor(rnd() * a.length)];

const catalogo = [
  { slug: 'havaianas-natal-dtc', cliente: 'Havaianas', nome: 'Natal · DTC', cor: '#E4002B', sigla: 'NT', criado: '2026-09-28',
    pecas: [{ id: 'big-hello', nome: 'Big Hello' }, { id: 'mesa', nome: 'Mesa Big Hello' }, { id: 'vitrine', nome: 'Vitrine' }, { id: 'testeira', nome: 'Testeira' }, { id: 'cubo', nome: 'Solução para cubo' }] },
  { slug: 'havaianas-verao-aura-dtc', cliente: 'Havaianas', nome: 'Verão Aura · DTC', cor: '#0B6BCB', sigla: 'VA', criado: '2026-09-28',
    pecas: [{ id: 'big-hello', nome: 'Big Hello' }, { id: 'vitrine', nome: 'Vitrine' }, { id: 'nicho', nome: 'Solução de nicho' }] },
  { slug: 'havaianas-verao-b2b', cliente: 'Havaianas', nome: 'Verão · B2B Alimentar', cor: '#F59F00', sigla: 'VB', criado: '2026-09-28',
    pecas: [{ id: 'display', nome: 'Display de chão' }, { id: 'faixa', nome: 'Faixa de gôndola' }, { id: 'wobbler', nome: 'Wobbler' }] },
];
const DTC = [
  ['Havaianas Shopping Ibirapuera', -23.6105, -46.6656, 'São Paulo', 'SP'], ['Havaianas Morumbi Shopping', -23.6226, -46.6994, 'São Paulo', 'SP'],
  ['Havaianas Shopping Eldorado', -23.5728, -46.696, 'São Paulo', 'SP'], ['Havaianas Center Norte', -23.515, -46.623, 'São Paulo', 'SP'],
  ['Havaianas Shopping Tatuapé', -23.542, -46.576, 'São Paulo', 'SP'], ['Havaianas Oscar Freire', -23.562, -46.67, 'São Paulo', 'SP'],
  ['Havaianas Grand Plaza', -23.648, -46.533, 'Santo André', 'SP'], ['Havaianas Iguatemi Campinas', -22.893, -47.027, 'Campinas', 'SP'],
  ['Havaianas Ribeirão Shopping', -21.214, -47.812, 'Ribeirão Preto', 'SP'], ['Havaianas Praiamar', -23.969, -46.329, 'Santos', 'SP'],
  ['Havaianas Internacional Guarulhos', -23.47, -46.527, 'Guarulhos', 'SP'], ['Havaianas BarraShopping', -22.999, -43.359, 'Rio de Janeiro', 'RJ'],
  ['Havaianas Rio Sul', -22.956, -43.177, 'Rio de Janeiro', 'RJ'], ['Havaianas Shopping Leblon', -22.983, -43.216, 'Rio de Janeiro', 'RJ'],
  ['Havaianas Ipanema', -22.984, -43.203, 'Rio de Janeiro', 'RJ'], ['Havaianas Plaza Niterói', -22.896, -43.124, 'Niterói', 'RJ'],
  ['Havaianas Nova América', -22.878, -43.273, 'Rio de Janeiro', 'RJ'], ['Havaianas Diamond Mall', -19.933, -43.948, 'Belo Horizonte', 'MG'],
  ['Havaianas BH Shopping', -19.977, -43.944, 'Belo Horizonte', 'MG'], ['Havaianas Pátio Savassi', -19.939, -43.934, 'Belo Horizonte', 'MG'],
  ['Havaianas Center Shopping', -18.959, -48.28, 'Uberlândia', 'MG'], ['Havaianas ParkShoppingBarigüi', -25.435, -49.317, 'Curitiba', 'PR'],
  ['Havaianas Pátio Batel', -25.443, -49.291, 'Curitiba', 'PR'], ['Havaianas Catuaí Londrina', -23.329, -51.17, 'Londrina', 'PR'],
  ['Havaianas Iguatemi Florianópolis', -27.588, -48.501, 'Florianópolis', 'SC'], ['Havaianas Beiramar', -27.59, -48.547, 'Florianópolis', 'SC'],
  ['Havaianas Atlântico Shopping', -26.99, -48.634, 'Balneário Camboriú', 'SC'], ['Havaianas Garten Joinville', -26.276, -48.846, 'Joinville', 'SC'],
  ['Havaianas Iguatemi Porto Alegre', -30.027, -51.164, 'Porto Alegre', 'RS'], ['Havaianas Praia de Belas', -30.049, -51.229, 'Porto Alegre', 'RS'],
  ['Havaianas Salvador Shopping', -12.979, -38.455, 'Salvador', 'BA'], ['Havaianas Shopping Barra', -13.0, -38.526, 'Salvador', 'BA'],
  ['Havaianas RioMar Recife', -8.086, -34.894, 'Recife', 'PE'], ['Havaianas Shopping Recife', -8.118, -34.904, 'Recife', 'PE'],
  ['Havaianas Iguatemi Fortaleza', -3.755, -38.489, 'Fortaleza', 'CE'], ['Havaianas ParkShopping Brasília', -15.833, -47.954, 'Brasília', 'DF'],
  ['Havaianas Iguatemi Brasília', -15.721, -47.886, 'Brasília', 'DF'], ['Havaianas Flamboyant', -16.71, -49.238, 'Goiânia', 'GO'],
];
const B2B = [
  ['Pão de Açúcar Brigadeiro', -23.571, -46.65, 'São Paulo', 'SP', 'Pão de Açúcar'], ['Pão de Açúcar Pinheiros', -23.566, -46.687, 'São Paulo', 'SP', 'Pão de Açúcar'],
  ['Pão de Açúcar Moema', -23.601, -46.665, 'São Paulo', 'SP', 'Pão de Açúcar'], ['Carrefour Pinheiros', -23.567, -46.705, 'São Paulo', 'SP', 'Carrefour'],
  ['Carrefour Campinas', -22.861, -47.07, 'Campinas', 'SP', 'Carrefour'], ['Carrefour Barra', -23.0, -43.38, 'Rio de Janeiro', 'RJ', 'Carrefour'],
  ['Assaí Interlagos', -23.67, -46.69, 'São Paulo', 'SP', 'Assaí'], ['Assaí Guarulhos', -23.45, -46.53, 'Guarulhos', 'SP', 'Assaí'],
  ['Assaí Recife', -8.06, -34.92, 'Recife', 'PE', 'Assaí'], ['Atacadão Osasco', -23.53, -46.78, 'Osasco', 'SP', 'Atacadão'],
  ['Atacadão Contagem', -19.92, -44.05, 'Contagem', 'MG', 'Atacadão'], ['Carrefour Recife', -8.04, -34.91, 'Recife', 'PE', 'Carrefour'], ['Extra Leblon', -22.984, -43.222, 'Rio de Janeiro', 'RJ', 'Extra'],
  ['St Marche Vila Nova', -23.588, -46.676, 'São Paulo', 'SP', 'St Marche'], ['Muffato Curitiba', -25.47, -49.28, 'Curitiba', 'PR', 'Muffato'],
  ['Angeloni Beira-Mar', -27.585, -48.545, 'Florianópolis', 'SC', 'Angeloni'], ['Zaffari Moinhos', -30.026, -51.2, 'Porto Alegre', 'RS', 'Zaffari'],
  ['BH Supermercados Savassi', -19.94, -43.93, 'Belo Horizonte', 'MG', 'BH Supermercados'], ['Pão de Açúcar Campo Belo', -23.623, -46.67, 'São Paulo', 'SP', 'Pão de Açúcar'],
];
const PESSOAS = [
  ['Juliana Martins', '11987451203', 'proprio'], ['Rafael Souza', '11991827364', 'proprio'], ['Camila Teixeira', '21998124570', 'proprio'],
  ['Bruno Almeida', '31997462018', 'proprio'], ['Larissa Pires', '41996358214', 'proprio'], ['Diego Fernandes', '48999127403', 'proprio'],
  ['Patrícia Rocha', '51998201456', 'proprio'], ['Thiago Lima', '71999635820', 'proprio'], ['Aline Costa', '81998452013', 'proprio'],
  ['Marcos Vieira', '11994518230', 'compartilhado'], ['Fernanda Oliveira', '11993287415', 'compartilhado'], ['Gustavo Nogueira', '21997541286', 'compartilhado'],
  ['Renata Barros', '41991238745', 'compartilhado'], ['Lucas Prado', '61998743210', 'proprio'],
];
const pessoaDe = (uf, tipo) => {
  const reg = { SP: [0, 1, 9, 10], RJ: [2, 11], MG: [3], PR: [4, 12], SC: [5], RS: [6], BA: [7], PE: [8], CE: [8], DF: [13], GO: [13] }[uf] || [0];
  const ok = reg.map((i) => PESSOAS[i]).filter((p) => !tipo || p[2] === tipo);
  return pega(ok.length ? ok : reg.map((i) => PESSOAS[i]));
};
const FOTOS_DTC = ['fmt-standard', 'fmt-light', 'fmt-premium', 'fmt-compacta', 'fmt-quiosque', 'fmt-antigo', 'flag-2', 'flag-4', 'flag-5', 'flag-6', 'vitrine'];
const FOTOS_B2B = ['esp-1', 'esp-2', 'esp-3', 'esp-4', 'esp-5'];
const AGORA = new Date('2026-10-27T16:40:00-03:00').getTime();
const DIA = 864e5;
const quando = (dMin, dMax) => {
  const d = new Date(AGORA - (dMin + rnd() * (dMax - dMin)) * DIA);
  if (d.getDay() === 0 && rnd() < 0.7) d.setDate(d.getDate() - 1);
  d.setHours(8 + Math.floor(rnd() * 11), Math.floor(rnd() * 60));
  return Math.min(d.getTime(), AGORA - 3600e3);
};
const instalacoes = [], fotos = {}, acessos = [];
let n = 0;
const registrar = (loja, projeto, pecas, tipo, t, foto, bandeira) => {
  const [nome, lat, lng, cidade, uf] = loja;
  const [pessoa, tel, tp] = pessoaDe(uf, tipo);
  const id = `demo${String(++n).padStart(3, '0')}`;
  const c = catalogo.find((x) => x.slug === projeto);
  instalacoes.push({ id, dados: {
    projeto, projetoNome: c.nome, cliente: 'Havaianas', nome: pessoa, telefone: tel, loja: nome, bandeira, tipoPromotor: tp, temFoto: true,
    geo: { lat: lat + (rnd() - 0.5) * 0.0006, lng: lng + (rnd() - 0.5) * 0.0006, precisao: Math.round(6 + rnd() * 22) }, geoStatus: 'ok',
    origem: rnd() < 0.92 ? 'qr' : 'link', pecas, cidade, uf, t } });
  fotos[id] = `/__foto/${foto}.webp`;
  acessos.push({ id: `a${id}`, dados: { projeto, etapa: 'abriu', origem: 'qr', so: rnd() < 0.55 ? 'Android' : 'iOS', sessao: id, t: t - 120e3 } });
  acessos.push({ id: `r${id}`, dados: { projeto, etapa: 'registrou', origem: 'qr', so: 'Android', sessao: id, t } });
};
// Natal DTC: quase toda a rede, ritmo crescente
DTC.forEach((l, i) => {
  if (i % 9 === 8) return; // lojas ainda sem registro
  const pecas = ['big-hello', 'testeira', ...(rnd() < 0.6 ? ['vitrine'] : []), ...(rnd() < 0.4 ? ['mesa'] : []), ...(rnd() < 0.3 ? ['cubo'] : [])];
  const bandeira = /Oscar Freire|Ipanema/.test(l[0]) ? 'Havaianas loja própria' : 'Havaianas franquia';
  registrar(l, 'havaianas-natal-dtc', pecas, 'proprio', quando(0.2, 24), FOTOS_DTC[i % FOTOS_DTC.length], bandeira);
});
// Verão Aura DTC: começou há 10 dias
DTC.filter((_, i) => i % 3 === 0).forEach((l, i) => {
  const bandeira = /Oscar Freire|Ipanema/.test(l[0]) ? 'Havaianas loja própria' : 'Havaianas franquia';
  registrar(l, 'havaianas-verao-aura-dtc', ['big-hello', ...(rnd() < 0.5 ? ['nicho'] : [])], 'proprio', quando(0.1, 10), FOTOS_DTC[(i + 4) % FOTOS_DTC.length], bandeira);
});
// Verão B2B alimentar
B2B.forEach((l, i) => {
  const pecas = ['display', ...(rnd() < 0.7 ? ['faixa'] : []), ...(rnd() < 0.5 ? ['wobbler'] : [])];
  registrar(l, 'havaianas-verao-b2b', pecas, rnd() < 0.75 ? 'compartilhado' : 'proprio', quando(0.3, 21), FOTOS_B2B[i % FOTOS_B2B.length], l[5]);
});
// quem abriu e não terminou
for (let i = 0; i < 14; i++) acessos.push({ id: `x${i}`, dados: { projeto: pega(catalogo).slug, etapa: 'abriu', origem: 'qr', so: 'iOS', sessao: `x${i}`, t: quando(0.1, 20) } });
instalacoes.sort((a, b) => b.dados.t - a.dados.t);
console.log('registros', instalacoes.length);

const DEMO = { colecoes: { instalacoes, acessos, paginas: [], senhas: catalogo.map((c) => ({ id: c.slug, dados: { senha: 'demo' } })), compartilhamentos: [], publicos: [] }, fotos };
const SDK = {
  'firebase-app.js': 'export const initializeApp = () => ({});',
  'firebase-auth.js': `export const getAuth = () => ({});
export function onAuthStateChanged(a, cb) { setTimeout(() => cb({ email: 'equipe@75lab.com.br', emailVerified: true }), 0); return () => {}; }
export class GoogleAuthProvider { setCustomParameters() {} }
export async function signInWithPopup() {} export async function signInWithRedirect() {} export async function signOut() {}`,
  'firebase-firestore.js': `const D = () => window.__DEMO;
const ts = (d) => d.t ? { ...d, criadoEm: { toDate: () => new Date(d.t) } } : d;
const snapDe = (l) => { const docs = l.map((x) => ({ id: x.id, data: () => ts(x.dados), exists: () => true })); return { docs, size: docs.length, empty: !docs.length, forEach: (f) => docs.forEach(f) }; };
export const getFirestore = () => ({});
export const collection = (db, ...p) => ({ path: p.join('/') });
export const doc = (db, ...p) => ({ path: p.join('/'), id: p[p.length - 1] });
export const query = (c) => c; export const orderBy = () => 0; export const limit = () => 0; export const where = () => 0;
export const serverTimestamp = () => new Date(); export const arrayUnion = (...a) => a; export const arrayRemove = (...a) => a;
export function onSnapshot(r, cb) { setTimeout(() => cb(snapDe(D().colecoes[r.path] || [])), 0); return () => {}; }
export async function getDocs(r) { return snapDe(D().colecoes[r.path] || []); }
export async function getDoc(r) { const [c, id] = r.path.split('/'); const img = c === 'fotos' ? D().fotos[id] : null; return { id, exists: () => !!img, data: () => (img ? { img } : undefined) }; }
export async function setDoc() {} export async function updateDoc() {} export async function deleteDoc() {} export async function addDoc() { return { id: 'x' }; }`,
};

const navegador = await chromium.launch({ channel: 'chrome' });
const ctx = await navegador.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, locale: 'pt-BR', timezoneId: 'America/Sao_Paulo' });
await ctx.addInitScript((d) => { window.__DEMO = d; }, DEMO);
await ctx.route(/gstatic\.com\/firebasejs\/.*\/(firebase-[a-z]+\.js)/, (route) => {
  const nome = route.request().url().match(/(firebase-[a-z]+\.js)/)[1];
  route.fulfill({ contentType: 'text/javascript', body: SDK[nome] || 'export {}' });
});
await ctx.route(/\/produtos\/projetos\.json/, (route) => route.fulfill({ contentType: 'application/json', body: JSON.stringify(catalogo) }));
await ctx.route(/\/__foto\//, (route) => {
  const f = route.request().url().split('/__foto/')[1];
  route.fulfill({ contentType: 'image/webp', body: readFileSync(IMG + f) });
});
await ctx.route(/nominatim\.openstreetmap\.org/, (route) => route.fulfill({ contentType: 'application/json', body: '{}' }));
const pg = await ctx.newPage();
pg.on('pageerror', (e) => console.log('erro na página:', e.message));
await pg.goto('https://projetos.75lab.com.br/produtos/painel/');
await pg.waitForTimeout(5000);
await pg.evaluate(() => { const u = document.querySelector('#usuario'); if (u) u.textContent = 'equipe@75lab.com.br'; });
await pg.screenshot({ path: OUT + 'painel-topo.png' });
const alturaTotal = await pg.evaluate(() => document.documentElement.scrollHeight);
console.log('altura', alturaTotal);
await pg.screenshot({ path: OUT + 'painel-inteiro.png', fullPage: true });
const caixa = async (sel) => (await pg.locator(sel).first().boundingBox());
const topo = await caixa('#intel-ritmo');
await pg.screenshot({ path: OUT + 'q-topo.png', fullPage: true, clip: { x: 0, y: 0, width: 1440, height: topo.y + topo.height + 50 } });
await pg.getByRole('button', { name: 'Estado', exact: true }).click().catch(() => {});
await pg.waitForTimeout(800);
const barras = await caixa('#intel-barras');
await pg.screenshot({ path: OUT + 'q-estados.png', fullPage: true, clip: { x: barras.x - 30, y: barras.y - 70, width: barras.width + 60, height: Math.min(barras.height + 90, 760) } });
const fach = await caixa('#intel-fachadas-bloco');
await pg.screenshot({ path: OUT + 'q-fachadas.png', fullPage: true, clip: { x: fach.x, y: fach.y, width: fach.width, height: fach.height } });
await pg.locator('#mapa').scrollIntoViewIfNeeded();
await pg.waitForTimeout(2500);
const mapa = await pg.evaluate(() => { const el = document.querySelector('#mapa').closest('section') || document.querySelector('#mapa'); const r = el.getBoundingClientRect(); return { x: r.x + scrollX, y: r.y + scrollY, width: r.width, height: r.height }; });
await pg.screenshot({ path: OUT + 'q-mapa.png', fullPage: true, clip: { x: mapa.x, y: mapa.y, width: mapa.width, height: mapa.height } });
await navegador.close();
