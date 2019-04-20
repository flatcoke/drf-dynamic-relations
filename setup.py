from setuptools import setup

readme = open('README.me').read()

setup(name='drf_dynamic_relations',
      version='0.0.1',
      description='Dynamically set eager load in Django REST Framework.',
      author='flatcoke',
      author_email='flatcoke89@gmail.com',
      url='https://github.com/flatcoke/drf-dynamic-relations',
      packages=['drf_dynamic_relations'],
      zip_safe=True,
      include_package_data=True,
      license='MIT',
      keywords=('drf restframework rest_framework '
                'django_rest_framework relation eager_load'),
      long_description=readme,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Framework :: Django',
      ],
)
