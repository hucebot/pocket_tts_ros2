from setuptools import setup
import os
from glob import glob

package_name = 'ros2_kyutai_tts'

# Automatically create the missing resource marker file for ament
os.makedirs('resource', exist_ok=True)
with open(os.path.join('resource', package_name), 'w') as f:
    pass

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py') if glob('launch/*.py') else []),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml') if glob('config/*.yaml') else []),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@email.com',
    description='Kyutai Pocket TTS node pushing to TIAGo audio_out/raw',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'kyutai_tts_node = ros2_kyutai_tts.kyutai_tts_node:main'
        ],
    },
)