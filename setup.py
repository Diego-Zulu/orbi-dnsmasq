import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  author="Diego-Zulu",
  classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Information Technology",
    "Topic :: Internet :: Name Service (DNS)",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
  ],
  description="Use selenium and telnet to automate orbi router's dnsmasq",
  download_url="https://github.com/Diego-Zulu/orbi-dnsmasq/archive/v1.1.0.tar.gz",
  entry_points={"console_scripts": ["orbi-dnsmasq = orbi_dnsmasq:command_line_main"]},
  install_requires=[
    "keyboard",
    "selenium",
  ],
  keywords=["orbi", "dnsmasq"],
  license="MIT",
  long_description=long_description,
  long_description_content_type="text/markdown",
  name="orbi-dnsmasq",
  packages=["orbi_dnsmasq"],
  python_requires=">=2.7",
  url="https://github.com/Diego-Zulu/orbi-dnsmasq",
  version="1.1.0",
)
