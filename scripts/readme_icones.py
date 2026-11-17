"""Gera os blocos de ícones do README (skillicons.dev + ícones próprios no mesmo formato), cada um com link."""
SKILL = "https://skillicons.dev/icons?i={}"
PROPRIO = "assets/icones/{}.svg"

GRUPOS = {
    "IA generativa e automação": [
        ("claude", "Claude", "https://www.anthropic.com/claude", PROPRIO),
        ("n8n", "n8n", "https://n8n.io", PROPRIO),
        ("python", "Python", "https://www.python.org", SKILL),
    ],
    "Desenvolvimento": [
        ("fastapi", "FastAPI", "https://fastapi.tiangolo.com", SKILL),
        ("sqlalchemy", "SQLAlchemy", "https://www.sqlalchemy.org", PROPRIO),
        ("pytest", "pytest", "https://docs.pytest.org", PROPRIO),
        ("react", "React", "https://react.dev", SKILL),
        ("ts", "TypeScript", "https://www.typescriptlang.org", SKILL),
        ("tailwind", "Tailwind CSS", "https://tailwindcss.com", SKILL),
        ("vite", "Vite", "https://vite.dev", SKILL),
        ("sqlite", "SQLite", "https://www.sqlite.org", SKILL),
        ("postgres", "PostgreSQL", "https://www.postgresql.org", SKILL),
        ("docker", "Docker", "https://www.docker.com", SKILL),
        ("githubactions", "GitHub Actions", "https://github.com/features/actions", SKILL),
        ("git", "Git", "https://git-scm.com", SKILL),
        ("github", "GitHub", "https://github.com/Luizamiller", SKILL),
    ],
    "Dados": [
        ("pandas", "pandas", "https://pandas.pydata.org", PROPRIO),
        ("numpy", "NumPy", "https://numpy.org", PROPRIO),
        ("sklearn", "scikit-learn", "https://scikit-learn.org", SKILL),
        ("duckdb", "DuckDB", "https://duckdb.org", PROPRIO),
        ("jupyter", "Jupyter", "https://jupyter.org", PROPRIO),
    ],
    "Produto e ferramentas": [
        ("notion", "Notion", "https://www.notion.so", SKILL),
        ("vscode", "VS Code", "https://code.visualstudio.com", SKILL),
        ("astro", "Astro", "https://astro.build", SKILL),
        ("cloudflare", "Cloudflare", "https://www.cloudflare.com", SKILL),
    ],
}


def icone(i, nome, url, fonte, tam=44):
    return f'<a href="{url}" title="{nome}"><img src="{fonte.format(i)}" width="{tam}" height="{tam}" alt="{nome}"></a>'


def bloco() -> str:
    partes = []
    for titulo, itens in GRUPOS.items():
        partes.append(f"<p><b>{titulo}</b><br>\n" + "&nbsp;\n".join(icone(*x) for x in itens) + "\n</p>")
    return "\n\n".join(partes)


if __name__ == "__main__":
    print(bloco())
