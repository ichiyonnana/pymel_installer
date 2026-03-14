[English](#Overview) | [日本語](#概要)

***

# Overview
This repository contains a simple installer that downloads `pymel` and installs it into the user's Maya scripts folder.
During installation, it automatically creates any missing cache files according to https://www.autodesk.com/support/technical/article/caas/tsarticles/ts/6gfZgdPquwZ2qCVxfAkb1n.html

# Usage
If Python is installed on your system, run install_pymel.py directly.
```powershell
python install_pymel.py
```

If Python is not installed on your system, or if running the command is inconvenient, drag and drop maya_dropper.py into Maya.
This will be available in all versions of Maya, regardless of the version currently running.
Note: Depending on your Maya environment, a dialog or warning may be displayed.

# Note
This repository does not include the pymel core. A network connection is required to download the latest code from the official repository.

***

# 概要
このリポジトリは `pymel` をダウンロードしてユーザーの Maya スクリプトフォルダへインストールする簡易インストーラを収めています。
インストール時に https://www.autodesk.com/support/technical/article/caas/tsarticles/ts/6gfZgdPquwZ2qCVxfAkb1n.html に従い不足したキャッシュファイルを自動で作成します。

# 使い方
システムに Python がインストールされている場合は install_pymel.py を直接実行してください。
```powershell
python install_pymel.py
```

もしシステムに Python がインストールされていない場合や、コマンドの実行が面倒な場合は maya_dropper.py を Maya へ D&D してください。
起動している Maya のバージョンによらず全バージョンに対してインストールされます。
※ Maya の環境によってはダイアログや警告が表示されます。

# 注意点
このリポジトリには pymel 本体は含まれていません。公式リポジトリから最新のコードをダウンロードするためネットワーク環境が必要です。

