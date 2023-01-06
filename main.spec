# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Main.pyw'],
             pathex=['C:\\Users\\TheKing\\PycharmProjects\\Gob-Fish'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='GobFish',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          version='file_version_info_gobfish.txt', icon='icon.ico')

a2 = Analysis(['test_controller.py'],
             pathex=['C:\\Users\\TheKing\\PycharmProjects\\Gob-Fish'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz2 = PYZ(a2.pure, a2.zipped_data,
             cipher=block_cipher)
exe2 = EXE(pyz2,
          a2.scripts,
          [],
          exclude_binaries=True,
          name='TestController',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='C:\\Users\\TheKing\\Documents\\NoMoskito\\venv-32\\Lib\\site-packages\\pygame\\pygame.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               exe2,
               a2.binaries,
               a2.zipfiles,
               a2.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='GobFish')
