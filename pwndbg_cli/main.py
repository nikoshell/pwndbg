import argparse
import os
import shutil
import site
import subprocess
import sys
import signal

# Pass SIGINT to GDB
signal.signal(signal.SIGINT, lambda *_: None)


def main(args=None):
    if args is None:
        args = sys.argv

    print(f"Arguments: {args}")

    gdb_path = shutil.which("gdb")

    if gdb_path is None:
        print("GDB is not installed. Please install it and try again.")
        sys.exit(1)

    try:
        double_dash_index = args.index('--')
    except ValueError:
        double_dash_index = len(args)

    argparse_args = args[1:double_dash_index]
    gdb_args = args[double_dash_index + 1:]

    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        'action', nargs="?", choices=['run', 'profile'], default='run')
    parser_args = parser.parse_args(argparse_args)

    os.environ["PWNLIB_NOTERM"] = "1"

    # match parser_args.action:
    #     # case 'run':
    #     #     run_with_pi(gdb_args, 'import pwndbg')
    #     case 'run':
    #         run_with_file(gdb_args, 'run')
    #
    #     case 'profile':
    #         run_with_file(gdb_args, 'profile')
    run_with_file(gdb_args, parser_args.action)

def _run(init_args, gdb_args):
    gdb_path = shutil.which("gdb")
    print(f"GDB path: {gdb_path}")
    sp_dir = site.getsitepackages()[0]
    print(f"Site packages: {sp_dir}")
    gdb_command = [
        gdb_path,  '--quiet', '-nx',
        '-eiex', 'set charset UTF-8',
        '-eiex', 'set auto-load safe-path /',
        '-ex', f'pi import site; site.addsitedir(\'{sp_dir}\')'
    ]

    command_args = [*gdb_command, *init_args, *gdb_args]
    print(f"Running GDB with args: {command_args}")
    subprocess.run(command_args)

def run_with_pi(gdb_args, py_init=''):
    _run(['-ex', f'pi {py_init}'], gdb_args)


def run_with_file(gdb_args, name):
    file_name = f'_{name}.py'

    current_directory = os.path.dirname(__file__)
    full_file_path = os.path.join(current_directory, file_name) 

    _run(['-x', f'{full_file_path}'], gdb_args)


if __name__ == "__main__":
    main(sys.argv)
