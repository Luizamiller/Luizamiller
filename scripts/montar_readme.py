"""Monta o README do perfil: banner, contatos, projetos, estatísticas, tecnologias e formação."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from readme_icones import bloco, icone  # noqa: E402

atual = Path("README.md").read_text(encoding="utf-8")
projetos = re.search(r"(## Projetos\n.*?)\n---\n", atual, re.S).group(1).strip()
formacao = re.search(r"(## Formação e experiência\n.*)", atual, re.S).group(1).strip()


def picture(nome: str, alt: str, largura: str = "100%") -> str:
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/{nome}-escuro.svg">\n'
            f'  <img src="assets/{nome}-claro.svg" alt="{alt}" width="{largura}">\n</picture>')


SKILL = "https://skillicons.dev/icons?i={}"
contatos = "&nbsp;&nbsp;\n".join([
    icone("gmail", "E-mail", "mailto:lmiller.luiza@gmail.com", SKILL, 46),
    icone("linkedin", "LinkedIn", "https://www.linkedin.com/in/luiza-miller", SKILL, 46),
    icone("github", "GitHub", "https://github.com/Luizamiller", SKILL, 46),
])

readme = f"""<div align="center">

{picture("banner", "Luiza Miller — Farmacêutica, Mestra em Ciências, AI Builder")}

<br>

{contatos}

</div>

<br>

Sou farmacêutica e mestra em Bioquímica e Bioprospecção (UFPel), com experiência em farmácia hospitalar, pesquisa em IA aplicada à saúde e gestão de produto como Product Owner. Construo aplicações completas que unem **dados, produto e IA generativa**: do problema do usuário às regras de negócio, ao código testado e à demonstração no ar.

{projetos}

---

## Em números

<table>
<tr>
<td width="50%" valign="top">

{picture("linguagens", "Linguagens mais usadas, por linhas de código")}

</td>
<td width="50%" valign="top">

{picture("numeros", "Projetos, linhas de código, testes e demonstrações")}

</td>
</tr>
</table>

<sub>Calculado a partir do código dos repositórios públicos por um GitHub Action que roda todo dia (<a href="scripts/estatisticas.py">script</a>). Notebooks Jupyter ficam fora da porcentagem, porque as saídas salvas inflariam a conta.</sub>

---

## Tecnologias

<sub>Clique em um ícone para abrir o site da tecnologia.</sub>

{bloco()}

**Também:** engenharia de prompt, saída estruturada (JSON), RAG com citação verificada, agentes com validação determinística, avaliação de respostas e humano no circuito · ChatGPT, Gemini, Whisper, Make, Zapier · Playwright, Alembic · bioinformática (PyDESeq2, lifelines, WGCNA) · Scrum, Kanban, métricas e KPIs, design de interface · LGPD e privacidade desde o desenho

---

{formacao}
"""
Path("README.md").write_text(readme, encoding="utf-8")
print("README montado:", len(readme), "caracteres")
