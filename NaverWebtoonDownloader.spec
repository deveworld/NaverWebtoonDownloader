# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['NaverWebtoonDownloader.py'],
             pathex=['C:\\Users\\sgh20\\OneDrive\\바탕 화면\\코딩\\파이썬\\NaverWebtoonDownloader'],
             binaries=[],
             datas=[('./images/*','./images')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='NaverWebtoonDownloader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='NaverWebtoonDownloader.ico')
