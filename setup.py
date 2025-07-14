import glob
import os
import subprocess

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


class CustomBuild(_build_py):
    def run(self):
        subprocess.check_call(["python", "build.py"])

        for so_file in glob.glob("*.so") + glob.glob("*.pyd"):
            target = os.path.join("pyquartic", os.path.basename(so_file))
            os.rename(so_file, target)

        super().run()

setup(
    cmdclass={"build_py": CustomBuild},
)
