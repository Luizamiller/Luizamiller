// Gera ícones no mesmo formato do skillicons.dev (quadrado escuro 256×256, cantos de 60) para as
// tecnologias que o skillicons não tem. Logos do Simple Icons (CC0).
// Uso: node scripts/icones.mjs  (precisa do pacote simple-icons; ex.: npx -p simple-icons node scripts/icones.mjs)
import { mkdirSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire(process.env.SIMPLE_ICONS_DE ?? import.meta.url);
const si = require("simple-icons");

const FUNDO = "#242938";
const ICONES = { pandas: "siPandas", numpy: "siNumpy", jupyter: "siJupyter", claude: "siClaude", n8n: "siN8n", duckdb: "siDuckdb", pytest: "siPytest", sqlalchemy: "siSqlalchemy" };

const lum = (hex) => {
  const c = [0, 2, 4].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
};
const contraste = (a, b) => (Math.max(lum(a), lum(b)) + 0.05) / (Math.min(lum(a), lum(b)) + 0.05);

mkdirSync("assets/icones", { recursive: true });
for (const [nome, chave] of Object.entries(ICONES)) {
  const i = si[chave];
  const cor = contraste(i.hex, FUNDO.slice(1)) >= 3 ? `#${i.hex}` : "#FFFFFF"; // logos escuros ficam brancos no fundo escuro
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 256 256"><title>${i.title}</title>` +
    `<rect width="256" height="256" rx="60" fill="${FUNDO}"/>` +
    `<g transform="translate(56 56) scale(6)" fill="${cor}"><path d="${i.path}"/></g></svg>`;
  writeFileSync(`assets/icones/${nome}.svg`, svg);
  console.log(nome, cor);
}
