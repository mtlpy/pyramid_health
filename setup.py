import setuptools

setup_requires = [
    'd2to1',
    'coverage',
    'mock',
    'nose',
    'nosexcover',
    'webtest',
    'yanc',
    ]

dependency_links = [
    ]

setuptools.setup(
    setup_requires=setup_requires,
    d2to1=True,
    dependency_links=dependency_links,
    )
