from setuptools import find_packages, setup

package_name = 'cengaver_pose_estimator'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kisalp',
    maintainer_email='kisalp@example.com',  # Güncel bir e-posta adresi
    description='A package for estimating pose using ArUco markers.',
    license='MIT',  # Kullanılan lisans
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pose_estimator = cengaver_pose_estimator.pose_estimator:main'
        ],
    },
)
