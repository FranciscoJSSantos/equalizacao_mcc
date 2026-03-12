"""
Script de build — gera o .exe via PyInstaller.
Execute com: uv run python build.py
"""
import os
import sys
import shutil
import subprocess
import streamlit

ST_DIR = os.path.dirname(streamlit.__file__)

# Arquivos de dados a incluir no exe: (origem, destino_dentro_do_bundle)
data_files = [
    # App principal
    (os.path.abspath("app.py"), "."),
    # Pasta com planilha padrão (opcional para o cliente)
    (os.path.abspath("sheet"), "sheet"),
    # Streamlit runtime / static
    (os.path.join(ST_DIR, "static"), "streamlit/static"),
    (os.path.join(ST_DIR, "runtime"), "streamlit/runtime"),
    (os.path.join(ST_DIR, "web"), "streamlit/web"),
]

add_data_args = []
for src, dst in data_files:
    if os.path.exists(src):
        add_data_args += ["--add-data", f"{src};{dst}"]
    else:
        print(f"[AVISO] Caminho não encontrado, pulando: {src}")

hidden_imports = [
    "streamlit",
    "streamlit.web",
    "streamlit.web.bootstrap",
    "streamlit.web.cli",
    "streamlit.runtime",
    "streamlit.runtime.scriptrunner",
    "pandas",
    "openpyxl",
    "openpyxl.styles",
    "openpyxl.utils",
    "altair",
    "pyarrow",
    "pydeck",
    "PIL",
    "PIL.Image",
    "importlib_metadata",
    "pkg_resources",
    "packaging",
    "click",
    "watchdog",
    "tornado",
    "tornado.web",
    "tornado.httpserver",
    "tornado.ioloop",
    "gitpython",
    "git",
]

hidden_import_args = []
for h in hidden_imports:
    hidden_import_args += ["--hidden-import", h]

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--name", "Equalizacao_MCC",
    "--onefile",
    "--icon", "NONE",
    "--distpath", "dist",
    *add_data_args,
    *hidden_import_args,
    "--collect-all", "streamlit",
    "--collect-all", "altair",
    "--collect-all", "pydeck",
    "run.py",
]

print("Iniciando build...\n")
print(" ".join(cmd))
print()
subprocess.run(cmd, check=True)
print("\nBuild concluído! Executável em: dist/Equalizacao_MCC.exe")
