import os
import sys

from setuptools import setup

if sys.version_info >= (3, 0):
    README = open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8').read()
else:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

reqs = ['boto3>=1', ]

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-sns-mobile-push-notification',
    version='0.9',
    packages=['sns_mobile_push_notification'],
    include_package_data=True,
    license='MIT License',
    description='Send mobile push notification to IOS and android devices using Amazon SNS.',
    long_description=README,
    url='https://github.com/pythonicrubyist',
    author='Ramtin Vaziri',
    author_email='pythonicrubyist@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=reqs,
)