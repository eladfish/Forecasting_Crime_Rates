# -*- mode: python -*-

block_cipher = None


a = Analysis(['cprofiles_lmfit.py'],
             pathex=['C:\\Users\\eladf\\Desktop\\New folder (2)\\6.24'],
             binaries=[],
             datas=[('Logo.ico', '.'), ('chicago map.jpg', '.')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='cprofiles_lmfit',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=True )
