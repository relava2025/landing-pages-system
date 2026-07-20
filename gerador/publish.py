#!/usr/bin/env python3
"""Publica uma LP exportada pelo editor no diretório do cliente.

O editor exporta um arquivo <slug>.html (auto-suficiente, com imagens embutidas).
Este script instala esse arquivo como /<slug>/index.html na raiz do repositório,
que é o que fica no ar em  lp.gruposystemdigital.com.br/<slug>.

Uso:
    python gerador/publish.py <arquivo.html> [slug]

- Se o slug não for informado, usa o nome do arquivo (ex.: fraciele.html -> fraciele).
Depois é só: git add . && git commit -m "LP <slug>" && git push
"""
import sys, shutil, pathlib, re

if len(sys.argv) < 2:
    print("Uso: python gerador/publish.py <arquivo.html> [slug]"); sys.exit(1)

src = pathlib.Path(sys.argv[1]).expanduser()
if not src.exists():
    print(f"[erro] arquivo não encontrado: {src}"); sys.exit(1)

raw = sys.argv[2] if len(sys.argv) > 2 else src.stem
slug = re.sub(r'[^a-z0-9-]', '', raw.strip().lower())
if not slug:
    print("[erro] slug inválido"); sys.exit(1)

repo = pathlib.Path(__file__).resolve().parent.parent
out  = repo / slug
out.mkdir(parents=True, exist_ok=True)
shutil.copy2(src, out / "index.html")

kb = (out / "index.html").stat().st_size // 1024
print(f"[ok] publicado: {out}/index.html ({kb} KB)")
print(f"     URL: lp.gruposystemdigital.com.br/{slug}")
print(f"     agora: git add . && git commit -m 'LP {slug}' && git push")
