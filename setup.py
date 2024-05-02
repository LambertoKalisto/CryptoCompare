from setuptools import setup

with open('README.md', encoding="utf-8") as f:
    readme = f.read()

setup(
    name='cryptocompare_fields',
    version='0.1.2',
    description='Wrapper for CryptoCompare.com',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/LambertoKalisto/CryptoCompare',
    author='lamberto',
    author_email='dhgdgjdjhd@gmail.com',
    keywords='crypto cryptocurrency wrapper cryptocompare',
    license='MIT',
    python_requires='>=3',
    packages=['cryptocompare-fields'],
    classifiers=['Programming Language :: Python :: 3'],
    install_requires=['requests']
)
