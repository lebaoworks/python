import os
import argparse
import random, string
import shutil
import stat
from lib.os import morph_dir

def fix_perm(abs_path):
    if os.name == 'nt':
        os.chmod(abs_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    else:
        os.chmod(abs_path, 0o777)

def fix(abs_path):
    assert os.path.isabs(abs_path) and os.path.isdir(abs_path)
    
    # If root, fix sub dirs (root does not need to be fixed)
    if os.path.dirname(abs_path) == abs_path:
        dirs = [dir_name for dir_name in os.listdir(abs_path) if os.path.isdir(os.path.join(abs_path, dir_name))]
        for dir_name in dirs:
            fix(dir_name)
    else:
        parent_dir = os.path.dirname(abs_path)
        temp_dir = os.path.join(parent_dir, ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)))
        while os.path.isdir(temp_dir):
            temp_dir = os.path.join(parent_dir, ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)))
        os.makedirs(temp_dir)

        for path, dirs, files in os.walk(abs_path):
            temp_path = path.replace(abs_path, temp_dir)
            for dir_name in dirs:
                print(f"[*] mkdir {os.path.join(temp_path, dir_name)}")
                fix_perm(os.path.join(path, dir_name))
                os.makedirs(os.path.join(temp_path, dir_name))
            for file_name in files:
                if not file_name.endswith(".db") and not file_name.endswith(".ini"):
                    src = os.path.join(path, file_name)
                    dst = os.path.join(temp_path, file_name)
                    shutil.move(src, dst)
                    print(f"\t[*] move {src}")
        fix_perm(abs_path)        
        shutil.rmtree(abs_path, ignore_errors=False)
        os.rename(temp_dir, abs_path)

def check(abs_path):
    for path, dirs, files in os.walk(abs_path):
        for dir_name in dirs:
            if os.path.islink(os.path.join(path, dir_name)):
                raise Exception("[!] Found a link directory. check \"--force\"")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fix Tool')
    parser.add_argument('--path', type=str, required=True)
    parser.add_argument("--force", action='store_true', help="force copy file(s) from link directory")
    args = parser.parse_known_args()[0]

    path = os.path.abspath(args.path)
    print(f"[*] path: {path}")
    if not args.force:
        check(path)
    fix(path)