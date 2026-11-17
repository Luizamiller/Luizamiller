"""Estatísticas do perfil, calculadas a partir do código dos repositórios públicos (sem serviços de terceiros).

- Linguagens: linhas de código por extensão, em todos os repositórios públicos que não são fork.
  Notebooks Jupyter ficam fora da porcentagem (as saídas salvas inflariam a conta) e aparecem contados à parte.
- Números: projetos, linhas de código, testes automatizados (funções `test_*` no Python e `test(...)` no
  Playwright/Vitest) e projetos com demonstração online (site do GitHub Pages configurado).

Gera assets/linguagens-{escuro,claro}.svg e assets/numeros-{escuro,claro}.svg.
Uso: python scripts/estatisticas.py   (GITHUB_TOKEN opcional, só para não esbarrar no limite da API)
"""
import json
import os
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path

USUARIO = "Luizamiller"
IGNORAR_REPOS = {USUARIO}
IGNORAR_CAMINHOS = re.compile(r"(^|/)(docs|node_modules|dist|public/demo|test-results|\.venv|alembic/versions)(/|$)|\.min\.js$|lock|\.lock$")
EXT = {".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
       ".css": "CSS", ".html": "HTML", ".sql": "SQL", ".sh": "Shell", ".ps1": "PowerShell", ".astro": "Astro", ".r": "R"}
CORES = {"Python": "#E8B23A", "TypeScript": "#3178C6", "JavaScript": "#F1E05A", "CSS": "#663399", "HTML": "#E34C26",
         "SQL": "#E38C00", "Shell": "#89E051", "PowerShell": "#012456", "Astro": "#FF5A03", "R": "#198CE7", "Outras": "#8B949E"}
TEMAS = {
    "escuro": {"fundo": "#0E1116", "borda": "#232A33", "tinta": "#F2EEE8", "suave": "#9AA4AF", "trilho": "#1C232B", "destaque": "#4FB3A0"},
    "claro": {"fundo": "#FBF9F5", "borda": "#E4DDD2", "tinta": "#1B1F24", "suave": "#5B6470", "trilho": "#ECE6DC", "destaque": "#1F7A68"},
}
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"


def api(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "estatisticas-perfil"})
    if tok := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def medir(pasta: Path) -> tuple[dict, int, int]:
    arquivos = subprocess.run(["git", "-C", str(pasta), "ls-files"], capture_output=True, text=True, check=True).stdout.splitlines()
    linhas, notebooks, testes = {}, 0, 0
    for rel in arquivos:
        if IGNORAR_CAMINHOS.search(rel):
            continue
        ext = Path(rel).suffix.lower()
        if ext == ".ipynb":
            notebooks += 1
            continue
        lang = EXT.get(ext)
        if not lang:
            continue
        try:
            texto = (pasta / rel).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        n = sum(1 for l in texto.splitlines() if l.strip())
        linhas[lang] = linhas.get(lang, 0) + n
        if ext == ".py":
            testes += len(re.findall(r"^\s*(?:async\s+)?def test_\w+", texto, re.M))
        elif ext in (".ts", ".tsx") and ("/e2e/" in f"/{rel}" or ".test." in rel or ".spec." in rel):
            testes += len(re.findall(r"^\s*(?:test|it)\(\s*[\"'`]", texto, re.M))
    return linhas, notebooks, testes


def coletar() -> dict:
    repos = [r for r in api(f"https://api.github.com/users/{USUARIO}/repos?per_page=100&type=owner")
             if not r["fork"] and not r["archived"] and r["name"] not in IGNORAR_REPOS]
    total, notebooks, testes, demos = {}, 0, 0, 0
    with tempfile.TemporaryDirectory() as tmp:
        for r in repos:
            destino = Path(tmp) / r["name"]
            subprocess.run(["git", "clone", "--quiet", "--depth", "1", r["clone_url"], str(destino)], check=True)
            l, nb, t = medir(destino)
            for k, v in l.items():
                total[k] = total.get(k, 0) + v
            notebooks += nb
            testes += t
            demos += bool(r.get("homepage") and "github.io" in r["homepage"])
            print(f"{r['name']}: {sum(l.values())} linhas, {t} testes, {nb} notebooks")
    return {"projetos": len(repos), "linhas": total, "notebooks": notebooks, "testes": testes, "demos": demos}


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def cartao_linguagens(d: dict, t: dict) -> str:
    soma = sum(d["linhas"].values()) or 1
    ordem = sorted(d["linhas"].items(), key=lambda x: -x[1])
    principais = ordem[:6]
    resto = sum(v for _, v in ordem[6:])
    if resto:
        principais.append(("Outras", resto))
    W, x0, larg = 600, 32, 536
    barra, x = [], x0
    for nome, v in principais:
        w = larg * v / soma
        barra.append(f'<rect x="{x:.2f}" y="78" width="{max(w - 2, 1):.2f}" height="10" fill="{CORES.get(nome, CORES["Outras"])}"/>')
        x += w
    legenda = []
    for i, (nome, v) in enumerate(principais):
        cx, cy = x0 + (i % 2) * 272, 124 + (i // 2) * 30
        legenda.append(f'<circle cx="{cx + 5}" cy="{cy - 5}" r="5" fill="{CORES.get(nome, CORES["Outras"])}"/>'
                       f'<text x="{cx + 18}" y="{cy}" font-size="14" fill="{t["tinta"]}">{nome}</text>'
                       f'<text x="{cx + 250}" y="{cy}" font-size="14" fill="{t["suave"]}" text-anchor="end">{v * 100 / soma:.1f}%</text>')
    H = 124 + ((len(principais) + 1) // 2) * 30 + 22
    nota = f'+ {d["notebooks"]} notebooks Jupyter de análise, contados à parte' if d["notebooks"] else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Linguagens mais usadas" font-family="{SANS}">
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t["fundo"]}" stroke="{t["borda"]}"/>
  <text x="{x0}" y="44" font-size="13" letter-spacing="2" fill="{t["suave"]}">LINGUAGENS MAIS USADAS</text>
  <text x="{W - x0}" y="44" font-size="12" fill="{t["suave"]}" text-anchor="end">por linhas de código</text>
  <clipPath id="c"><rect x="{x0}" y="78" width="{larg}" height="10" rx="5"/></clipPath>
  <rect x="{x0}" y="78" width="{larg}" height="10" rx="5" fill="{t["trilho"]}"/>
  <g clip-path="url(#c)">{"".join(barra)}</g>
  {"".join(legenda)}
  <text x="{x0}" y="{H - 18}" font-size="12" fill="{t["suave"]}">{nota}</text>
</svg>
'''


def cartao_numeros(d: dict, t: dict, altura: int) -> str:
    W = 600
    itens = [(fmt(d["projetos"]), "projetos públicos"), (fmt(sum(d["linhas"].values())), "linhas de código"),
             (fmt(d["testes"]), "testes automatizados"), (fmt(d["demos"]), "demonstrações online")]
    blocos = []
    for i, (n, rot) in enumerate(itens):
        x, y = 32 + (i % 2) * 272, 104 + (i // 2) * (altura - 150)
        blocos.append(f'<text x="{x}" y="{y}" font-size="32" font-family="Georgia, serif" fill="{t["tinta"]}">{n}</text>'
                      f'<text x="{x}" y="{y + 21}" font-size="13.5" fill="{t["suave"]}">{rot}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{altura}" viewBox="0 0 {W} {altura}" role="img" aria-label="Números do GitHub" font-family="{SANS}">
  <rect x=".5" y=".5" width="{W - 1}" height="{altura - 1}" rx="16" fill="{t["fundo"]}" stroke="{t["borda"]}"/>
  <text x="32" y="44" font-size="13" letter-spacing="2" fill="{t["suave"]}">EM NÚMEROS</text>
  <rect x="32" y="56" width="28" height="3" rx="1.5" fill="{t["destaque"]}"/>
  {"".join(blocos)}
</svg>
'''


if __name__ == "__main__":
    dados = coletar()
    Path("assets").mkdir(exist_ok=True)
    for nome, tema in TEMAS.items():
        ling = cartao_linguagens(dados, tema)
        Path(f"assets/linguagens-{nome}.svg").write_text(ling, encoding="utf-8")
        altura = int(re.search(r'height="(\d+)"', ling)[1])
        Path(f"assets/numeros-{nome}.svg").write_text(cartao_numeros(dados, tema, altura), encoding="utf-8")
    print(json.dumps({**dados, "linhas": dict(sorted(dados["linhas"].items(), key=lambda x: -x[1]))}, ensure_ascii=False))
