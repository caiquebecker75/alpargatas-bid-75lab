"""Dimensionamento do time Alpargatas (DTC e B2B) a partir das horas reais do Ariuno.

Horas por tipo de entrega: apontamentos do Ariuno da 75 LAB, jul a out/2026 (11.060 registros).
Volumes: Escopo de Contratação DTC e B2B 2027 da Alpargatas.

FTE = horas/ano x folga de simultaneidade / (12 meses x 140 h produtivas por pessoa)

Rodar: python3 fonte/dimensionamento.py
"""
import json

H_PRODUTIVAS_MES = 140      # 80% de 176 h; os designers da 75 LAB apontam 150 a 200 h/mês
FOLGA = 1.25                # pico de 6 a 7 campanhas simultâneas contra média de ~4,5
REVISAO_MARCA = 1.15        # rodadas de aprovação de marca grande sobre a criação

# horas por unidade, medidas no Ariuno (média por tarefa apontada)
U = {
    'arte_rapida': 2.5,        # 62 tarefas de post e arte rápida
    'peca_tatica': 3.2,        # 24 arte-finais e adaptações
    'peca_estrutural': 8.6,    # 24 executivos e engenharias
    'kv': 10.0,                # KV com desdobramento base (Campari 8,6 h, Cacau Show 10,5 h)
    'projeto_especial': 72.0,  # mediana de 4 stands e cenografias (45 a 137 h)
    'ambientacao_gc': 19.7,    # média dos jobs de display
    'ar_formato': 2.5,         # mediana dos renders 3D e AR
    'orcamento': 3.5,          # 57 tarefas de orçamento
    'acompanhamento': 4.1,     # 13 tarefas de produção e acompanhamento
}
ITEM_ESTRUTURAL = 10.0   # orçamento com 3 fornecedores + protótipo + QA (3,5 + 4,1 + 30%)
ITEM_TATICO = 4.0        # item repetido de enxoval: orçamento e acompanhamento


def fte(h):
    return h * FOLGA / (12 * H_PRODUTIVAS_MES)


# ---------------------------------------------------------------- DTC
# 23 campanhas: 10 primárias, 9 secundárias, 4 táticas (calendário 2027 do escopo)
prim, sec, tat = 10, 9, 4
dtc = {}
criacao = (
    prim * (U['kv'] + 15 * U['peca_estrutural'] + 3 * 2 * U['peca_tatica'])   # big hello x7, quiosque, vitrine, prateleira x3, nicho
    + sec * (5 + 2 * U['peca_estrutural'] + 3 * 2 * U['peca_tatica'])
    + tat * (3 * 2 * U['peca_tatica'])
    + 3 * U['projeto_especial']                 # corner, ilha, ceno
    + prim * 7 * U['ar_formato']                # aprovação em AR por formato
    + 8 * 8                                     # modelagem inicial dos 8 formatos
)
dtc['Criação, engenharia e AR'] = criacao * REVISAO_MARCA
dtc['Produção'] = (prim * (15 * ITEM_ESTRUTURAL + 3 * ITEM_TATICO)
                   + sec * (2 * ITEM_ESTRUTURAL + 3 * ITEM_TATICO)
                   + tat * 3 * ITEM_TATICO + 3 * 40)
dtc['Logística e rede'] = (prim * 52 + sec * 38 + tat * 34          # plano por loja, operador, ocorrências, fechamento
                           + 728 * 23 * 0.05 * 0.75 + 96)          # SAC: 5% das lojas-campanha, 45 min cada; base de lojas
dtc['Atendimento e planejamento'] = prim * 30 + sec * 15 + tat * 8 + 40 * 12 + 25 * 8
dtc['Fiscal'] = prim * 10 + sec * 6 + tat * 4 + 10 * 12
dtc['Direção de criação'] = 0.10 * dtc['Criação, engenharia e AR'] + prim * 8

# ---------------------------------------------------------------- B2B
camp = 12
b2b = {}
criacao_b = (
    camp * (U['kv'] + 12 * U['peca_tatica'] + 4 * U['peca_estrutural'])
    + 8 * 48 * U['arte_rapida']                 # 8 artes rápidas por semana
    + 25 * U['peca_tatica']                     # MPDVs institucionais
    + 30 * U['ambientacao_gc']                  # ambientações de GC
    + 3 * 83                                    # kits de ativação (3 períodos)
)
b2b['Criação, engenharia e AR'] = criacao_b * REVISAO_MARCA
b2b['Produção'] = camp * (4 * ITEM_ESTRUTURAL + 12 * ITEM_TATICO) + 30 * 10 + 25 * ITEM_TATICO + 3 * 30
b2b['Logística e implementação'] = camp * 15 + 60 + 30 * 8 + 90 * 4
b2b['Atendimento e planejamento'] = camp * 25 + 384 * 0.25 + 30 * 4 + 3 * 20 + 40 * 12
b2b['Fiscal'] = camp * 6 + 30 + 10 * 12
b2b['Direção de criação'] = 0.10 * b2b['Criação, engenharia e AR'] + camp * 8

for nome, d in (('DTC', dtc), ('B2B', b2b)):
    tot = sum(d.values())
    print(f'\n{nome}: {tot:,.0f} h/ano · {tot / 12:,.0f} h/mês · {fte(tot):.2f} FTE com folga')
    for k, v in d.items():
        print(f'  {k:28} {v:7,.0f} h/ano  {fte(v):.2f} FTE')

json.dump({'dtc': dtc, 'b2b': b2b, 'unidades': U}, open('fonte/dimensionamento.json', 'w'), ensure_ascii=False, indent=1)
