import os
import site
import sys
import shutil
import pathlib


def main():
    args = ' '.join(sys.argv[1:])
    gdb_path = shutil.which("gdb")
    if gdb_path is None:
        print("GDB is not installed. Please install it and try again.")
        sys.exit(1)
    else:
        print("GDB path:", gdb_path)

    sp_dir = site.getsitepackages()[0]
    working_dir = pathlib.Path(sp_dir).parent.parent.parent
    print("Working path:", working_dir)

    os.environ["PWNLIB_NOTERM"] = "1"
    # os.environ["PWNDBG_VENV_PATH"] = str(working_dir)

    gdb_command = f'{gdb_path} --quiet -nx \
        -eiex="set charset UTF-8" \
        -eiex="set auto-load safe-path /" \
        -ex "pi import site; site.addsitedir(\'{sp_dir}\'); import pwndbg" \
        {args}'
    os.system(gdb_command)


if __name__ == "__main__":
    main()
