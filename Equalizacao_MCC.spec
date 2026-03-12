# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('D:\\SUZANO\\dev\\equalizacoes\\edu\\app.py', '.'), ('D:\\SUZANO\\dev\\equalizacoes\\edu\\sheet', 'sheet'), ('D:\\SUZANO\\dev\\equalizacoes\\edu\\.venv\\Lib\\site-packages\\streamlit\\static', 'streamlit/static'), ('D:\\SUZANO\\dev\\equalizacoes\\edu\\.venv\\Lib\\site-packages\\streamlit\\runtime', 'streamlit/runtime'), ('D:\\SUZANO\\dev\\equalizacoes\\edu\\.venv\\Lib\\site-packages\\streamlit\\web', 'streamlit/web')]
binaries = []
hiddenimports = ['streamlit', 'streamlit.web', 'streamlit.web.bootstrap', 'streamlit.web.cli', 'streamlit.runtime', 'streamlit.runtime.scriptrunner', 'pandas', 'openpyxl', 'openpyxl.styles', 'openpyxl.utils', 'altair', 'pyarrow', 'pydeck', 'PIL', 'PIL.Image', 'importlib_metadata', 'pkg_resources', 'packaging', 'click', 'watchdog', 'tornado', 'tornado.web', 'tornado.httpserver', 'tornado.ioloop', 'gitpython', 'git']
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('altair')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pydeck')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Equalizacao_MCC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NONE',
)
