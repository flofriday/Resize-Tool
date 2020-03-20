# If you want to build a package with pyinstaller this is the command.
# However on macOS you must have python insatlled via homebrew and not form
# python.org
pyinstaller --onedir --windowed --icon Logo.icns --strip --name Resize\ Tool main.py
