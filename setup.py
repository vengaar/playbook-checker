#pip3 install /home/vengaar/playbook-checker

# python3 setup.py sdist
# twine upload dist/*

from setuptools import find_packages, setup


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='playbook-checker',
    version='0.1.2',
    author='Olivier Perriot',
    author_email='',
    description='TODO',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vengaar/playbook-checker',
    license='GPLv3',
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
             'playbook_checker = playbook_checker.__main__:main'
        ]
    },
    python_requires='>=3.6',
)