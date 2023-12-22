from setuptools import setup, find_packages

setup(
    name='naverpaper',
    version='0.1',
    author='stateofai',
    author_email='tellme@duck.com',
    description='Naver Paper Machine',
    packages=find_packages(),
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'lxml',
        'pyc',
        'rsa',
        'urllib3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
