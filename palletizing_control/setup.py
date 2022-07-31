import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'palletizing_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
             ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.py')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='seok2',
    maintainer_email='junghs1040@naver.com',
    description='palletizing control package',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'palletizing_control       = palletizing_control.palletizing_control:main',
        'spawnbox_service_client = palletizing_control.palletizing_control:main',
        'vacuum_gripper_controller = palletizing_control.palletizing_control:main'
        'get_pallet_pos = palletizing_control.palletizing_control:main'
        ],
    },
)
