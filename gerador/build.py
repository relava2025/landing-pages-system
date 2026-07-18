#!/usr/bin/env python3
"""Gera a LP de um cliente.
Uso:  python gerador/build.py <slug>       (ex.: python gerador/build.py daliene)
Saída: pasta /<slug>/ na raiz do repositório (index.html + imagens).
"""
import json, sys, shutil, pathlib, re

if len(sys.argv) < 2:
    print("Uso: python gerador/build.py <slug>"); sys.exit(1)

slug = sys.argv[1].strip("/").lower()
root = pathlib.Path(__file__).resolve().parent
repo = root.parent
cli  = root / "clientes" / slug
if not cli.exists():
    print(f"[erro] não achei {cli}"); sys.exit(1)

cfg  = json.loads((cli / "config.json").read_text(encoding="utf-8"))
html = (root / "template.html").read_text(encoding="utf-8")

# 1) DEPOIMENTOS (lista) -> cards (duplicados p/ o scroll contínuo no mobile)
def card(d):
    stars = '<i class="ph-fill ph-star"></i>' * 5
    return ('                    <div class="card testimonial-card">\n'
            f'                        <div class="stars">{stars}</div>\n'
            f'                        <p class="testimonial-text">"{d["texto"]}"</p>\n'
            f'                        <p class="testimonial-author">- {d["autor"]}</p>\n'
            '                    </div>')
deps  = cfg.pop("DEPOIMENTOS", [])
cards = "\n".join(card(d) for d in deps)
html  = html.replace("<!--DEPOIMENTOS-->", cards + "\n" + cards)   # 2x = loop suave

# 2) FAQ (lista) -> itens
def faq(f):
    return ('                <div class="faq-item">\n'
            '                    <button class="faq-question">\n'
            f'                        <span>{f["pergunta"]}</span>\n'
            '                        <i class="ph-bold ph-caret-down"></i>\n'
            '                    </button>\n'
            '                    <div class="faq-answer">\n'
            f'                        <p>{f["resposta"]}</p>\n'
            '                    </div>\n'
            '                </div>')
faqs = cfg.pop("FAQ", [])
html = html.replace("<!--FAQ-->", "\n".join(faq(f) for f in faqs))

# 3) tokens simples ({{NOME}}, {{WHATSAPP}}...) — depois, p/ resolver tokens dentro dos textos
for k, v in cfg.items():
    html = html.replace("{{" + k + "}}", str(v))

faltando = sorted(set(re.findall(r"{{(\w+)}}", html)))
if faltando:
    print(f"[aviso] tokens sem valor: {faltando}")

out = repo / slug
out.mkdir(parents=True, exist_ok=True)
(out / "index.html").write_text(html, encoding="utf-8")

assets = cli / "assets"
if assets.exists():
    for item in assets.iterdir():
        dest = out / item.name
        shutil.copytree(item, dest, dirs_exist_ok=True) if item.is_dir() else shutil.copy2(item, dest)
    print("[ok] imagens copiadas")
else:
    print(f"[aviso] sem pasta assets em {cli}")

print(f"[pronto] {out}/  ->  lp.gruposystemdigital.com.br/{slug}  ({len(deps)} depoimentos, {len(faqs)} FAQs)")
