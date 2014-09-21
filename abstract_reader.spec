# -*- mode: python -*-
a = Analysis(['abstract_reader.py'],
             pathex=['/home/yzhou/Documents/Reader'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='abstract_reader',
          debug=False,
          strip=None,
          upx=True,
          console=False )
