# build.spec

block_cipher = None

a = Analysis(
    ['date_calculator.py'],  # Имя вашего скрипта
    pathex=['.'],            # Текущая директория
    binaries=[],             # Дополнительные бинарники (не нужны для --onefile)
    datas=[],                # Дополнительные файлы данных
    hiddenimports=['PyQt6', 'PyQt6.QtWidgets', 'PyQt6.QtCore', 'PyQt6.QtGui'],  # PyQt6 зависимости
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,              # Включаем все бинарники
    a.zipfiles,
    a.datas,
    name='DateCalculator',   # Имя выходного файла
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                # Сжатие с UPX (если установлен)
    console=False            # Без консоли для GUI
)
