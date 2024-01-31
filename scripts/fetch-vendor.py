import argparse
import logging
import json
import os
import platform
import subprocess


def get_platform():
    system = platform.system()
    machine = platform.machine()
    if system == "Linux":
        return f"manylinux_{machine}"
    elif system == "Darwin":
        # cibuildwheel sets ARCHFLAGS:
        # https://github.com/pypa/cibuildwheel/blob/5255155bc57eb6224354356df648dc42e31a0028/cibuildwheel/macos.py#L207-L220
        if "ARCHFLAGS" in os.environ:
            machine = os.environ["ARCHFLAGS"].split()[1]
        return f"macosx_{machine}"
    elif system == "Windows":
        if os.getenv("CIBW_ARCHS") == "AMD64":
            return "win_amd64"
        elif os.getenv("CIBW_ARCHS") == "x86":
            return "win32"
        elif os.getenv("CIBW_ARCHS") == "ARM64":
            return "win_arm64"
        elif machine.lower() in ("amd64", "x86_64", "x64"):
            return "win_amd64"
        elif machine.lower() in ("i386", "i686", "x86"):
            return "win32"
        else:
            return "win_arm64"
    else:
        raise Exception(f"Unsupported system {system}")


parser = argparse.ArgumentParser(description="Fetch and extract tarballs")
parser.add_argument("destination_dir")
parser.add_argument("--cache-dir", default="tarballs")
parser.add_argument("--config-file", default=os.path.splitext(__file__)[0] + ".json")
args = parser.parse_args()
logging.basicConfig(level=logging.INFO)

# read config file
with open(args.config_file, "r") as fp:
    config = json.load(fp)

# ensure destination directory exists
logging.info("Creating directory %s" % args.destination_dir)
if not os.path.exists(args.destination_dir):
    os.makedirs(args.destination_dir)

for url_template in config["urls"]:
    tarball_url = url_template.replace("{platform}", get_platform())

    # download tarball
    tarball_name = tarball_url.split("/")[-1]
    tarball_file = os.path.join(args.cache_dir, tarball_name)
    if not os.path.exists(tarball_file):
        logging.info("Downloading %s" % tarball_url)
        if not os.path.exists(args.cache_dir):
            os.mkdir(args.cache_dir)
        subprocess.check_call(
            ["curl", "--location", "--output", tarball_file, "--silent", tarball_url]
        )

    # extract tarball
    logging.info("Extracting %s" % tarball_name)
    subprocess.check_call(["tar", "-C", args.destination_dir, "-xf", tarball_file])
