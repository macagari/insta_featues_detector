from typing import Dict

from fastapi import FastAPI, UploadFile , File

from business.autologin import extract_images
from utils.logger_utils import stream_logger
import json
app = FastAPI()
from loko_client.business.fs_client import FSClient
from loko_client.utils.requests_utils import URLRequest
logger = stream_logger(__name__)
'''
fsclient = FSClient()
content = b'ciao ciao'
fsclient.u = URLRequest('http://gateway:8080/routes/').orchestrator
logger.debug(fsclient.ls('data/data'))
fsclient.save('data/data/test/test.txt', content)
'''



@app.post("/download_images", response_model= Dict)
def download_images(example_body: Dict):

    args = example_body.get('args')

    username = args.get("username")
    password = args.get("password")
    images_number = args.get("images_number")
    timeout = args.get("timeout")
    profiles = args.get("profiles")
    #images_directory = args.get("images_directory")

    with open('config.txt', 'w') as f:
        f.write(f'username:{username}\n')
        f.write(f'password:{password}\n')
        f.write(f'images_number:{images_number}\n')
        f.write(f'timeout:{timeout}\n')
        f.write(f'profiles:{profiles}\n')
        #f.write(f'images_directory:{images_directory}')

    logger.debug("done!")
    result = extract_images()
    logger.debug("Result of extract_images "+str(result))
    return dict(msg="ok")

