from setuptools import setup, find_packages
 
setup(
    name='csvimporter',
    version=__import__('csvimporter').__version__,
    description='Arbitrary CSV data importer for Django',
    author='Luke Hutscal',
    author_email='luke@creaturecreative.com',
    url='http://github.com/girasquid/django-csv-importer/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)