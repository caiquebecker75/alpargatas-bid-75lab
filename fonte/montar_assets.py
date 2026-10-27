"""Monta assets/ do deck: fotos do briefing em WebP, logos de clientes e cases do deck anterior, marcas.

python3 fonte/montar_assets.py <pasta-imagens-briefing> <pasta-imagens-deck-anterior>
"""
import shutil
import sys
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
A = RAIZ / 'assets'
briefing, anterior = Path(sys.argv[1]), Path(sys.argv[2])

FOTOS = {
    'capa': 'p01_00_2669x1505.jpeg',
    'fmt-premium': 'p06_08_561x316.jpeg', 'fmt-antigo': 'p06_06_401x406.jpeg', 'fmt-quiosque': 'p06_07_614x345.jpeg',
    'fmt-light': 'p06_05_520x413.jpeg', 'fmt-compacta': 'p06_04_594x405.jpeg', 'fmt-standard': 'p06_09_327x246.jpeg',
    'flag-1': 'p07_04_735x346.jpeg', 'flag-2': 'p07_05_878x521.jpeg', 'flag-3': 'p07_06_768x377.jpeg',
    'flag-4': 'p07_07_761x373.jpeg', 'flag-5': 'p07_08_761x372.jpeg', 'flag-6': 'p07_09_769x390.jpeg',
    'vis-bighello': 'p05_00_601x476.jpeg', 'vis-mesa': 'p05_01_514x477.jpeg', 'vis-painel': 'p05_02_706x477.jpeg',
    'vis-vitrine': 'p05_03_493x534.jpeg', 'vis-planta': 'p05_04_722x793.jpeg',
    'esp-1': 'p27_00_1044x426.jpeg', 'esp-2': 'p27_01_1162x450.jpeg', 'esp-3': 'p27_02_788x577.jpeg',
    'esp-4': 'p27_03_497x589.jpeg', 'esp-5': 'p27_04_874x519.jpeg', 'vitrine': 'p10_03_935x529.jpeg',
}
(A / 'img').mkdir(parents=True, exist_ok=True)
for nome, arq in FOTOS.items():
    im = Image.open(briefing / arq).convert('RGB')
    im.thumbnail((1920, 1920))
    im.save(A / 'img' / f'{nome}.webp', 'WEBP', quality=82)

CLIENTES = ['whiskas', 'pedigree', 'seara', 'lactalis', 'parmalat', 'unilever', '3coracoes', 'madalena',
            'boticario', 'petz', 'brastemp', 'consul', 'drogaria-sao-paulo', 'dpsp', 'loungerie', 'evino',
            'grand-cru', 'eudora', 'quem-disse-berenice', 'premierpet', 'kelcat', 'keldog', 'pipicat']
(A / 'clientes').mkdir(exist_ok=True)
for i, nome in enumerate(CLIENTES, start=4):
    shutil.copy(anterior / f'i{i:02d}.png', A / 'clientes' / f'{nome}.png')

(A / 'cases').mkdir(exist_ok=True)
for i, nome in enumerate(['panasonic', 'semp', 'alltak'], start=1):
    shutil.copy(anterior / f'i{i:02d}.jpg', A / 'cases' / f'{nome}.jpg')

# Alpargatas em versão clara para fundo escuro: o cinza do nome vira papel
svg = (A / 'logos' / 'Alpargatas-logo.svg').read_text()
(A / 'logos' / 'alpargatas.svg').write_text(svg)
(A / 'logos' / 'alpargatas-claro.svg').write_text(svg.replace('#77787b', '#F2F1E9'))
shutil.copy(A / 'logos' / 'Logotipo_da_Havaianas.svg', A / 'logos' / 'havaianas.svg')

for f in ('75lab-lime.png', '75lab-black.png'):
    shutil.copy(Path.home() / 'bombril-pitch-75lab' / 'assets' / f, A / f)
print('ok')
