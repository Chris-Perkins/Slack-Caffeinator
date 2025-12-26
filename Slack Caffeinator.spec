# -*- mode: python ; coding: utf-8 -*-
# Pyinstaller spec


a = Analysis(
    ['slack_caffeinator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['rumps', 'pyobjc-framework-Quartz', 'pyobjc-framework-Cocoa'],
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
    name='Slack Caffeinator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='Slack Caffeinator.app',
    icon=None,
    bundle_identifier=None,
)
