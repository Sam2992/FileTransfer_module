from setuptools import setup

setup(
    name='FileTransfer_module',
    version='1.0.0', 
    description='A Python tool for transferring files from a local directory to AWS S3 and Google Cloud Storage.',
    url='https://github.com/your_username/FileTranfer_module', 
    py_modules=['FileTranfer_module'], 
    python_requires='>=3.6', 
    install_requires=[  
        'boto3>=1.26.0',
        'google-cloud-storage>=2.11.0',
        'python-dotenv>=1.0.0',
    ],
    entry_points={  
        'console_scripts': [
            'file-transfer=file_transfer_tool:main', 
        ],
    },
)

