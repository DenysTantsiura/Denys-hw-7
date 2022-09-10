"""
Пакет встановлюється в систему командою:
 pip install -e
  . (або :
  python setup.py install
  , потрібні права адміністратора)
"""
from importlib.metadata import entry_points
from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='2.12',
      description='Sorterer junk in folder',
      url='May be added later',
      author='Tantsiura Denys',
      author_email='tdv@tesis.kiev.ua',
      license='MIT',
      packages=find_namespace_packages(),
      # install_requires=['logging', 'os','sys','re','datetime','shutil'],
      ## install_requires=['k_exten', 'norma'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main', 'i = clean_folder.clean:fun_print_author']})
