"""Maya drop handler to run the install_pymel script.

Place this file (or drop it into Maya). When Maya calls
`onMayaDroppedPythonFile`, it will try to load `install_pymel.py` from the
same directory and call its `main()` function.

This is intended for users who run the installer from inside Maya (no system
Python required).
"""

import importlib.util
import os
import traceback

try:
    import maya.cmds as cmds
except Exception:
    cmds = None


def _notify(msg: str, title: str = "pymel installer") -> None:
    """Show a simple message in Maya if possible, otherwise print."""
    if cmds:
        try:
            cmds.confirmDialog(title=title, message=msg, button=["OK"])
        except Exception:
            try:
                cmds.warning(msg)
            except Exception:
                print(msg)
    else:
        print(msg)


def onMayaDroppedPythonFile(filepaths, *args):
    """Maya entry point called when this script is dropped into Maya.

    It looks for `install_pymel.py` in the same directory as this file and
    executes its `main()` function.
    """
    # Determine directory where this dropper lives
    try:
        base_dir = os.path.dirname(__file__) or os.getcwd()
    except Exception:
        base_dir = os.getcwd()

    install_path = os.path.join(base_dir, "install_pymel.py")
    if not os.path.exists(install_path):
        _notify(f"install_pymel.py not found in {base_dir}")
        return

    try:
        spec = importlib.util.spec_from_file_location("install_pymel_drop", install_path)
        module = importlib.util.module_from_spec(spec)
        # Ensure module can import standard libs from Maya's Python
        if spec and spec.loader:
            spec.loader.exec_module(module)

        if hasattr(module, "main"):
            _notify("Starting pymel installation (will run inside Maya).")
            try:
                module.main()
            except Exception:
                tb = traceback.format_exc()
                print(tb)
                _notify("Installation failed: see Script Editor for details.")
                return
            _notify("pymel installation finished.")
        else:
            _notify("install_pymel.py does not define main()")

    except Exception:
        tb = traceback.format_exc()
        print(tb)
        _notify("Failed to load or run install_pymel.py. See Script Editor for details.")
