from setuptools import find_packages, setup
from glob import glob

package_name = 'Gazebo_world'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

         # Install meshes
        ('share/' + package_name + '/meshes', glob('meshes/*')),

        # Install launch files
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),

        # Install urdf
        ('share/' + package_name + '/urdf/forklift', glob('urdf/forklift/*.urdf.xacro')),

        # Install world files (specifically .world files)
        ('share/' + package_name + '/worlds', glob('worlds/*.sdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aditya',
    maintainer_email='aditya.jemshetty@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
