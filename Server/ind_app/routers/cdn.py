from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
import aiofiles
from os import listdir
from os.path import isfile, join

router = APIRouter(tags=["CDN-Javascript"], prefix="/cdn")

import os
import sys

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    dirname = os.path.dirname(sys.executable)
else:
    dirname = os.path.dirname(os.path.abspath(__file__))

ROOT_PATH = join(dirname, "js-libs/")

if not os.path.isdir(ROOT_PATH):
    os.mkdir(join(dirname, "js-libs/"))


@router.post("/upload_library/")
async def upload_report(lib_file: UploadFile):
    async with aiofiles.open(f"{ROOT_PATH}{lib_file.filename}", 'wb') as out_file:
        while content := await lib_file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk
    return {"Result": "Uploaded", "filename": lib_file.filename}


@router.get("/list_libraries/")
async def list_library():
    library_files = [f for f in listdir(ROOT_PATH) if isfile(join(ROOT_PATH, f))]
    # print(listdir(ROOT_PATH), ROOT_PATH)
    return library_files


@router.delete("/delete_library/{name}")
async def delete_library(name: str):
    # print(f"{ROOT_PATH}{name}")
    if isfile(f"{ROOT_PATH}{name}"):
        os.remove(join(ROOT_PATH, name))
        return {"Result": "Deleted", "filename": name}
    else:
        raise HTTPException(status_code=404, detail={"message": f"File not found: {name}"})


@router.get("/get_library/{name}", response_class=FileResponse)
async def get_library(name: str):
    # print(f"{ROOT_PATH}{name}")
    if isfile(f"{ROOT_PATH}{name}"):
        return (join(ROOT_PATH, name))
    else:
        raise HTTPException(status_code=404, detail={"message": f"File not found: {name}"})
