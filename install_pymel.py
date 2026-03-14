"""install_pymel.py

Obtain the latest pymel from https://github.com/LumaPictures/pymel and copy it to the maya/scripts folder in your user directory.
If a cache file for the latest Maya is not available, create a dummy file based on the latest cache file.

https://github.com/LumaPictures/pymel から最新の pymel を取得してユーザーフォルダの maya/scripts へコピーする。
最新のMaya用のキャッシュファイルが用意されていない場合は最新のキャッシュファイルを元にダミーファイルを作成する。
"""

import datetime
import os
import re
import shutil
import sys
import tempfile
import urllib.request
import zipfile


def main():
    url = "https://github.com/LumaPictures/pymel/archive/refs/heads/master.zip"

    tmpdir = tempfile.mkdtemp(prefix="pymel_install_")
    zip_path = os.path.join(tmpdir, "pymel-master.zip")

    success = False
    install_dest = None

    try:
        # github から最新コードのダウンロード
        print(f"Starting download: {url}")
        with urllib.request.urlopen(url) as resp, open(zip_path, "wb") as out:
            shutil.copyfileobj(resp, out)
        print("Download completed.")

        # zipを展開展開
        print("Extracting...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmpdir)

        pymel_src = None
        for root, dirs, _ in os.walk(tmpdir):
            if "pymel" in dirs:
                pymel_src = os.path.join(root, "pymel")
                break

        if pymel_src is None:
            raise RuntimeError("pymel folder not found in the extracted archive")

        # ユーザーフォルダの maya/scripts へコピーする
        # すでに pymel フォルダが存在すれば削除する
        userprofile = os.environ.get("USERPROFILE") or os.path.expanduser("~")
        dest_root = os.path.join(userprofile, "Documents", "maya", "scripts")
        os.makedirs(dest_root, exist_ok=True)
        dest = os.path.join(dest_root, "pymel")

        # 既存があれば削除
        if os.path.lexists(dest):
            if os.path.isdir(dest) and not os.path.islink(dest):
                shutil.rmtree(dest)
            else:
                os.remove(dest)

        # scripts へコピー
        print(f"Copying to scripts: {dest}")
        shutil.copytree(pymel_src, dest)

        # 最新の Maya 用のキャッシュファイルがなければ作成する
        target_year = datetime.datetime.now().year + 1
        cache_dir = os.path.join(dest, "cache")
        if os.path.isdir(cache_dir):
            pat = re.compile(r"^mayaApi(\d{4})\.py$")
            years = []
            for fname in os.listdir(cache_dir):
                m = pat.match(fname)
                if m:
                    try:
                        years.append(int(m.group(1)))
                    except ValueError:
                        pass

            if years:
                latest_year = max(years)
                created_years = []
                if latest_year < target_year:
                    src_name = f"mayaApi{latest_year:04d}.py"
                    src_path = os.path.join(cache_dir, src_name)
                    if os.path.exists(src_path):
                        for y in range(latest_year + 1, target_year + 1):
                            dst_name = f"mayaApi{y:04d}.py"
                            dst_path = os.path.join(cache_dir, dst_name)
                            if not os.path.exists(dst_path):
                                shutil.copy2(src_path, dst_path)
                                created_years.append(y)

                if created_years:
                    years_str = ", ".join(f"Maya{y}" for y in created_years)
                    print(f"Created cache files for {years_str} based on Maya{latest_year} cache file(s).")

        success = True
        install_dest = dest

    except Exception as exc:
        print("Error:", exc, file=sys.stderr)
        success = False

    finally:
        # 一時フォルダの削除
        try:
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
        except Exception:
            pass

    if success:
        print(f"pymel installation succeeded: {install_dest}")
    else:
        print("pymel installation failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
