"""Gera o banner do perfil em duas versões (escura e clara): assets/banner-escuro.svg e assets/banner-claro.svg.

Composição: nome e chamada à esquerda; à direita, um anel molecular (farmácia) que se abre numa rede de
pontos de dados. Só fontes do sistema: o GitHub não carrega fontes externas em SVG.
"""
import math
from pathlib import Path

L, A = 1280, 320
TEMAS = {
    "escuro": {"fundo": "#0E1116", "fundo2": "#141A21", "tinta": "#F2EEE8", "suave": "#9AA4AF", "linha": "#2A333D",
               "ponto": "#3A4651", "destaque": "#4FB3A0", "quente": "#E3A857"},
    "claro": {"fundo": "#F7F4EF", "fundo2": "#EFEAE2", "tinta": "#1B1F24", "suave": "#5B6470", "linha": "#D9D2C6",
              "ponto": "#C9C0B2", "destaque": "#1F7A68", "quente": "#B7791F"},
}


def banner(t: dict) -> str:
    cx, cy, r = 1010, 160, 62
    hexa = [(cx + r * math.cos(math.radians(90 + 60 * i)), cy + r * math.sin(math.radians(90 + 60 * i))) for i in range(6)]
    # rede de dados: pontos em leque saindo do anel para a direita e para cima
    rede = [(1110, 92), (1160, 70), (1205, 104), (1180, 150), (1232, 176), (1150, 214), (1210, 236), (1100, 252),
            (905, 82), (870, 128), (884, 222), (930, 262)]
    ligacoes = [(6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (14, 15), (16, 17)]  # entre pontos da rede (índices +6)
    grade = "".join(f'<circle cx="{x}" cy="{y}" r="1.1" fill="{t["ponto"]}" opacity=".55"/>'
                    for x in range(700, L, 28) for y in range(20, A, 28))
    anel = " ".join(f"{x:.1f},{y:.1f}" for x, y in hexa)
    linhas = []
    for a, b in ligacoes:
        p = hexa[a] if a < 6 else rede[a - 6]
        if b < 6:
            q = hexa[b]
        else:
            q = rede[b - 6]
        linhas.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{t["linha"]}" stroke-width="1.4"/>')
    for i, (x, y) in enumerate(rede):
        j = min(range(6), key=lambda k: (hexa[k][0] - x) ** 2 + (hexa[k][1] - y) ** 2)
        linhas.append(f'<line x1="{hexa[j][0]:.1f}" y1="{hexa[j][1]:.1f}" x2="{x}" y2="{y}" stroke="{t["linha"]}" stroke-width="1"/>')
    nos = "".join(f'<circle cx="{x}" cy="{y}" r="{4.5 if i % 3 else 6}" fill="{t["fundo"]}" stroke="{t["suave"]}" stroke-width="1.4"/>'
                  for i, (x, y) in enumerate(rede))
    vertices = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{t["destaque"]}"/>' for x, y in hexa)
    serif = "Georgia, 'Times New Roman', serif"
    sans = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{A}" viewBox="0 0 {L} {A}" role="img" aria-label="Luiza Miller — Farmacêutica, Mestra em Ciências, AI Builder">
  <defs>
    <linearGradient id="f" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["fundo"]}"/><stop offset="1" stop-color="{t["fundo2"]}"/></linearGradient>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".45" stop-color="#fff" stop-opacity="1"/></linearGradient>
    <mask id="m"><rect x="700" width="580" height="{A}" fill="url(#g)"/></mask>
  </defs>
  <rect width="{L}" height="{A}" rx="18" fill="url(#f)"/>
  <g mask="url(#m)">{grade}</g>
  {"".join(linhas)}
  <polygon points="{anel}" fill="none" stroke="{t["destaque"]}" stroke-width="2.2"/>
  <circle cx="{cx}" cy="{cy}" r="{r * .55:.1f}" fill="none" stroke="{t["destaque"]}" stroke-width="1.4" opacity=".55"/>
  {vertices}{nos}
  <circle cx="{rede[1][0]}" cy="{rede[1][1]}" r="7" fill="{t["quente"]}"/>
  <rect x="72" y="86" width="36" height="3" rx="1.5" fill="{t["destaque"]}"/>
  <text x="120" y="92" font-family="{sans}" font-size="15" letter-spacing="3" fill="{t["suave"]}">DADOS · PRODUTO · IA GENERATIVA EM SAÚDE</text>
  <text x="70" y="168" font-family="{serif}" font-size="72" fill="{t["tinta"]}">Luiza Miller</text>
  <text x="72" y="214" font-family="{sans}" font-size="23" fill="{t["tinta"]}" opacity=".9">Farmacêutica · Mestra em Ciências · AI Builder</text>
  <text x="72" y="250" font-family="{sans}" font-size="17" fill="{t["suave"]}">Aplicações completas com Python, React e LLMs — do problema do usuário à demonstração no ar.</text>
</svg>
'''


for nome, tema in TEMAS.items():
    Path(f"assets/banner-{nome}.svg").write_text(banner(tema), encoding="utf-8")
    print(nome, "ok")
