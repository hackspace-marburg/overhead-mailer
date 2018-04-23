from setuptools import setup, find_packages

setup(
    name='overhead-mailer',
    version='0.1',
    description='Announce next Overhead\'s topic on the mailing list',
    url='https://github.com/hackspace-marburg/overhead-mailer',
    packages=find_packages(),
    install_requires=['beautifulsoup4'],
    entry_points={
      'console_scripts': ['overhead_mailer=om.overhead_mailer:main']
    }
)
