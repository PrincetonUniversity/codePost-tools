from setuptools import setup

# The text of the README file
README = open("README.md").read()

# This call to setup() does all the work
setup(
    name="codePost-princeton-tools",
    version="1.0.2",
    description="Custom terminal tools for Princeton University to manage codePost.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/PrincetonUniversity/codePost-tools",
    author="codePost",
    author_email="team@codepost.io",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[],
    scripts=[
        "bin/push-to-codePost",
        "bin/ls-tigerfile-groups",
        "bin/export-codePost-grades"
    ],
    install_requires=[
        "codePost-api",
        "codePost-tools",
        "PyYAML",
        "requests"
    ],
    include_package_data=True,
)
