from importlib.metadata import entry_points
from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='2.12',
      description='Sorterer junk in folder',
      url='https://github.com/DenysTantsiura/Denys-hw-7.git',
      author='Tantsiura Denys',
      author_email='tdv@tesis.kiev.ua',
      license='MIT',
      packages=find_namespace_packages(),
      # install_requires=['logging', 'sys', 'shutil'],
      ## install_requires=['type_extensions', 'norma'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main', 'i = clean_folder.clean:fun_print_author']})
"""
The package is installed in the system by the command:
 pip install -e . 
 (or :
python setup.py install
, administrator rights are required!)
"""
