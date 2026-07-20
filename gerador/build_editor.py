#!/usr/bin/env python3
"""Monta o editor visual (arquivo unico e autossuficiente).

Le o template.html, embute-o (em base64) dentro da casca do editor
(_editor_shell.html) e gera:
  - editor.html            (na raiz do repo -> lp.gruposystemdigital.com.br/editor.html)
  - gerador/editor.html    (copia para referencia)

Rode sempre que mudar o template ou a casca:
    python gerador/build_editor.py
"""
import base64, pathlib

root  = pathlib.Path(__file__).resolve().parent      # .../gerador
repo  = root.parent

tpl   = (root / "template.html").read_text(encoding="utf-8")
shell = (root / "_editor_shell.html").read_text(encoding="utf-8")

b64 = base64.b64encode(tpl.encode("utf-8")).decode("ascii")
out = shell.replace("__TEMPLATE_B64__", b64)

if "__TEMPLATE_B64__" in shell and b64 not in out:
    raise SystemExit("[erro] falha ao injetar o template")

(repo / "editor.html").write_text(out, encoding="utf-8")

print(f"[ok] editor gerado ({len(out)//1024} KB)")
print(f"     -> {repo/'editor.html'}")
