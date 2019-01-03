from setuptools import setup
import versioneer

requirements = [
    # package requirements go here
]

setup(
    name='conda-prefix-replacement',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="CPR resuscitates packages in new locations",
    author="Anaconda, Inc.",
    author_email='conda@anaconda.com',
    url='https://github.com/conda/conda-prefix-replacement',
    packages=['cpr'],
    entry_points={
        'console_scripts': [
            'cpr=cpr.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='conda-prefix-replacement',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
