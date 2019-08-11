@echo off
pyinstaller --icon=D:\Project\gafy\decrypt\decrypt.ico --clean --onefile --add-data "templates;templates" --add-data "static;static"   "decrypt.spec"