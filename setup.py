from setuptools import find_packages, setup

VERSION = "2.0.1"
LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/phileo-design/patches/phileo-badges.svg
    :target: https://pypi.python.org/pypi/phileo-badges/

============
Pinax Badges
============

.. image:: https://img.shields.io/pypi/v/phileo-badges.svg
    :target: https://pypi.python.org/pypi/phileo-badges/

\ 

.. image:: https://img.shields.io/circleci/project/github/phileo/phileo-badges.svg
    :target: https://circleci.com/gh/phileo/phileo-badges
.. image:: https://img.shields.io/codecov/c/github/phileo/phileo-badges.svg
    :target: https://codecov.io/gh/phileo/phileo-badges
.. image:: https://img.shields.io/github/contributors/phileo/phileo-badges.svg
    :target: https://github.com/phileo/phileo-badges/graphs/contributors
.. image:: https://img.shields.io/github/issues-pr/phileo/phileo-badges.svg
    :target: https://github.com/phileo/phileo-badges/pulls
.. image:: https://img.shields.io/github/issues-pr-closed/phileo/phileo-badges.svg
    :target: https://github.com/phileo/phileo-badges/pulls?q=is%3Apr+is%3Aclosed

\ 

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT/

\ 

``phileo-badges`` is a a reusable Django badges application.
 
Supported Django and Python Versions
------------------------------------

+-----------------+-----+-----+-----+-----+
| Django / Python | 2.7 | 3.4 | 3.5 | 3.6 |
+=================+=====+=====+=====+=====+
|  1.11           |  *  |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
|  2.0            |     |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
"""

setup(
    author="Pinax Team",
    author_email="team@pinaxprojects.com",
    description="a reusable Django badges application",
    name="phileo-badges",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url="http://github.com/phileo/phileo-badges/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "badges": []
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=1.11",
    ],
    tests_require=[
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)
