from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in non_profit/__init__.py
from non_profit import __version__ as version

setup(
	name="non_profit",
	version=version,
	description="Non Profit",
	author="Frappe",
	author_email="pandikunta@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
