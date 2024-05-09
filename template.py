import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = 'rcs'
list_of_files = [
    '.github/workflows/.gitkeep',
    f'src/{project_name}/__init__.py',
    f'src/{project_name}/components/__init__.py',
    f'src/{project_name}/utils/__init__.py',
    f'src/{project_name}/utils/common.py',
    f'src/{project_name}/pipeline/__init__.py',
    f'src/{project_name}/config/__init__.py',
    f'src/{project_name}/config/configuration.py',
    f'src/{project_name}/constants/__init__.py',
    f'src/{project_name}/entity/__init__.py',
    f'src/{project_name}/entity/config_entity.py',
    'config/config.yaml',
    'params.yaml',
    'schema.yaml',
    'requirements.txt',
    'Dockerfile',
    'app.py',
    'main.py',
    'setup.py',
    'research/trials.ipynb',
    'templates/index.html'
]


for file_path in list_of_files:
    file_path = Path(file_path)
    filedir, file = os.path.split(file_path)

    if (filedir != ''):
        os.makedirs(filedir, exist_ok=True)
        logging.info(f'Created {filedir} for filename {file}')

    if (not os.path.exists(file_path) or os.path.getsize(file_path) == 0):
        with open(file_path, 'w') as f:
            pass
            logging.info(f'Created empty file: {file_path}')

    else:
        logging.info(f'{file} already exists')
