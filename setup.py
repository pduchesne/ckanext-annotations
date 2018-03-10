from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-annotations',
	version=version,
	description="CKAN extension for resource annotations",
	long_description="""\
	""",
	classifiers=[],
	keywords='',
	author='Philippe Duchesne',
	author_email='phd@highlatitud.es',
	url='http://highlatitud.es',
	license='AGPLv3',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.annotations'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
	annotations=ckanext.annotations.plugin:AnnotationPlugin
	""",
)
