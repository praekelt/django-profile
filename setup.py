from setuptools import setup, find_packages

setup(
    name='django-profile',
    version='0.0.2',
    description='Django user profile app.',
    long_description = open('README.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/django-profile',
    packages = find_packages(),
    dependency_links = [
        'http://github.com/praekelt/django-photologue/tarball/master#egg=django-photologue',
        'https://github.com/downloads/praekelt/eggs/django_registration-0.8_alpha_1-py2.6.egg#egg=django-registration'
    ],
    install_requires = [
        'django-photologue',
        'django-registration',
    ],
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
