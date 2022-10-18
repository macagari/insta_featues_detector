from typing import Dict

from fastapi import FastAPI, UploadFile , File
from utils.logger_utils import stream_logger
import json
app = FastAPI()
from loko_client.business.fs_client import FSClient
from loko_client.utils.requests_utils import URLRequest
logger = stream_logger(__name__)

fsclient = FSClient()
content = b'ciao ciao'
fsclient.u = URLRequest('http://gateway:8080/routes/').orchestrator
logger.debug(fsclient.ls('data/data'))
fsclient.save('data/data/test/test.txt', content)


@app.post("/download_images", response_model= Dict)
async def get_collections(example_body: Dict):

    args = example_body.get('args')

    username = args.get("username")
    password = args.get("password")
    images_numbers = args.get("images_numbers")
    timeout = args.get("timeout")
    profile_name = args.get("profile_name")
    images_directory = args.get("images_directory")

    with open('config.txt', 'w') as f:
        f.write(f'username:{username}')
        f.write(f'password:{password}')
        f.write(f'images_numbers:{images_numbers}')
        f.write(f'timeout:{timeout}')
        f.write(f'profile_name:{profile_name}')
        f.write(f'images_directory:{images_directory}')

    logger.debug("done!")
    return dict(msg="ok")