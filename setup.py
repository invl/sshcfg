import setuptools


setuptools.setup(
    name="sshcfg",
    version="0.1.0",
    py_modules=["sshcfg"],
    entry_points={
        'console_scripts': [
            'sshcfg = sshcfg:main',
        ],
    },
    install_requires=[
        'paramiko',
        'argh',
    ]
)
