from setuptools import setup, find_packages


setup(
    name='smtp_faker',
    description='SMTP Faker -- smtp server for development',
    version='0.1.0',
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP",
    ],
    url='https://github.com/zzzsochi/smtp-faker/',
    keywords=['asyncio', 'aiohttp', 'email', 'smtp', 'smtpd'],
    packages=find_packages(),
    install_requires=['aiohttp', 'aiosmtpd'],
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
