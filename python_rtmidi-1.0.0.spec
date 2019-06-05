# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\Josh\\Miniconda3\\Lib\\site-packages\\python_rtmidi-1.0.0.dist-info'],
             pathex=['/path/to/thisdir', 'C:\\Users\\Josh\\Programming\\CI102\\Code'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='python_rtmidi-1.0.0',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='python_rtmidi-1.0.0')
