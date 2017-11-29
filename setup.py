from setuptools import setup
from codecs import open
from os import path

cwd = path.abspath(path.dirname(__file__))

with open(path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='simplesql-python',
        version='0.1.0',
        description='Simple SQL tool with Python',
        long_description=long_description,
        url='https://github.com/youmu257/SimpleSQL',
        author='GuanLin Li',
        author_email='youmu257@gmail.com',
        license='MIT License',
        classifiers=[
            'Development Status :: 3 -Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: SQL tool',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',

        ],
        keywords='sql',
        packages=['simplesql'],
        package_dir={'SimpleSQL':'simplesql'},
        install_requires=[
            'pymysql',
            'configparser',
            ],
        package_data={
            'simplesql': [
                '*.*',
            ]
        },
)
