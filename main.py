from starlette.responses import HTMLResponse

from data_preparator.data_preparator import DataPreparator
from enum import Enum
#from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from model.model_wrapper import ModelWrapper

# from config import PREPARED_DATA_PATH
# from config import RAW_DATA_DICT
# from config import FEATURE_IMPORTANCES_PATH
# from config import SUBMISSION_PATH
# Server
# import pandas as pd
class TimeOfRecord(int, Enum):
    seconds5=5
    seconds10=10
    seconds15=15
    seconds20=20
    seconds25=25
    seconds30=30

class ModelsName(str, Enum):
    base='base'
    tiny= "tiny"
    small="small"
    medium="medium"
class TaskName(str, Enum):
    transcribe="transcribe"
    translate="translate"

app = FastAPI(
    title="Probability default model.",
    description="A simple pipeline to train and use probability default models.",
    version="1.0",
)

global audio_recorded
# Read and prepare data

@app.post("/record_audio/{recording_duration}")
def prepare_data(recording_duration: TimeOfRecord):
    global audio_recorded
    data_preparator = DataPreparator()
    print("Data preparator was initialized.")
    audio_recorded=data_preparator.record_audio(recording_duration)

    # prepared_df = data_preparator.prepare_data()
    # prepared_df.to_parquet(PREPARED_DATA_PATH, index=False)



@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(file.filename, "wb") as f:
        while chunk := await file.read(1024):
            f.write(chunk)

    data_preparator = DataPreparator()
    global audio_recorded
    # audio_recorded=data_preparator.add_audio(file.filename)
    audio_recorded=file.filename
    return {"filename": file.filename}

@app.get("/listen")
async def liste_audio():
    global audio_recorded
    data=f'<audio controls><source src="{audio_recorded}" type="audio/wav">Your browser does not support the audio element.</audio>'
    return HTMLResponse(data)

@app.post("/predict/{model_name}/{task}")
def predict(model_name:ModelsName, task:TaskName):
    global audio_recorded
    model_wrapper = ModelWrapper(model_name,audio_recorded)
    submission = model_wrapper.predict(task)
    return submission
