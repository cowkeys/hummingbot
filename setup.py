#!/usr/bin/env python

from setuptools import setup
from cython.Cython.Build import cythonize
import numpy as np
import os
import subprocess
import sys

if os.name == "posix":
    os_name = subprocess.check_output("uname").decode("utf8")
    if "Darwin" in os_name:
        os.environ["CFLAGS"] = "-stdlib=libc++ -std=c++11"
    else:
        os.environ["CFLAGS"] = "-std=c++11"


def main():
    cpu_count = os.cpu_count() or 8
    version = "20190517"
    packages = [
        "wings",
        "wings.logger",
        "wings.model",
        "wings.watcher",
        "wings.data_source",
        "wings.orderbook",
        "wings.tracker",
        "wings.market",
        "wings.wallet",
        "hummingbot",
        "hummingbot.core",
        "hummingbot.data_feed",
        "hummingbot.cli",
        "hummingbot.cli.config",
        "hummingbot.cli.ui",
        "hummingbot.cli.utils",
        "hummingbot.logger",
        "hummingbot.management",
        "hummingbot.strategy",
        "hummingbot.strategy.arbitrage",
        "hummingbot.strategy.cross_exchange_market_making",
        "hummingbot.strategy.discovery",
        "hummingbot.templates",
    ]
    package_data = {
        "wings": [
            "abi/*.json",
        ],
        "hummingbot": [
            "core/cpp/*",
            "erc20_tokens.json",
            "VERSION",
            "templates/*TEMPLATE.yml"
        ],
    }
    install_requires=[
        "aioconsole",
        "aiokafka",
        "attrdict",
        "cytoolz",
        "eth-abi",
        "eth-account",
        "eth-hash",
        "eth-keyfile",
        "eth-keys",
        "eth-rlp",
        "eth-utils",
        "hexbytes",
        "kafka-python",
        "lru-dict",
        "parsimonious",
        "pycryptodome",
        "requests",
        "rlp",
        "toolz",
        "tzlocal",
        "urllib3",
        "web3",
        "websockets",
        "aiohttp",
        "async-timeout",
        "attrs",
        "certifi",
        "chardet",
        "cython==0.29.5",
        "idna",
        "idna_ssl",
        "multidict",
        "numpy",
        "pandas",
        "pytz",
        "pyyaml",
        "python-binance==0.6.9",
        "sqlalchemy",
        "ujson",
        "yarl",
    ]

    if "DEV_MODE" in os.environ:
        version += ".dev1"
        package_data[""] = [
            "*.pxd", "*.pyx", "*.h"
        ]
        package_data["wings"].append("cpp/*.cpp")

    if len(sys.argv) > 1 and sys.argv[1] == "build_ext":
        sys.argv.append(f"--parallel={cpu_count}")

    setup(name="hummingbot",
          version=version,
          description="CoinAlpha Hummingbot",
          url="https://github.com/CoinAlpha/hummingbot",
          author="Martin Kou",
          author_email="martin@coinalpha.com",
          license="Proprietary",
          packages=packages,
          package_data=package_data,
          install_requires=install_requires,
          ext_modules=cythonize([
              "hummingbot/**/*.pyx",
              "wings/**/*.pyx",
          ], language="c++", language_level=3, nthreads=cpu_count),
          include_dirs=[
              np.get_include(),
          ],
          scripts=[
              "bin/hummingbot.py"
          ],
          )


if __name__ == "__main__":
    main()
