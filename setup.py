from setuptools import setup, find_packages

setup(
    name='django-profile',
    version='dev',
    description='Django user profile app.',
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    url='https://github.com/praekelt/django-profile',
    packages = find_packages(),
    include_package_data=True,
)
