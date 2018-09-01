from setuptools import setup, find_packages


VERSION = '0.1.2'
DESCRIPTION = 'SMTP Faker -- smtp server for development'
LONG_DESCRIPTION = open('README.rst', 'rb').read().decode('utf8')


setup(
    name='smtp_faker',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ],
    url='https://github.com/zzzsochi/smtp-faker/',
    keywords=['asyncio', 'aiohttp', 'email', 'smtp', 'smtpd'],
    packages=find_packages(),
    install_requires=['aiohttp>=3', 'aiosmtpd'],
    package_data={
        'smtp_faker': ['static/index.html',
                       'static/styles.css',
                       'static/app.js',
                       'static/favicon.ico'],
    },
    entry_points={
        'console_scripts': [
            'smtp-faker = smtp_faker.__main__:main',
        ],
    },
)
