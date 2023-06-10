import os
from bark import generate_audio, preload_models, SAMPLE_RATE
from scipy.io.wavfile import write as write_wav
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel

#set env variables
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["SUNO_USE_SMALL_MODELS"] = "1"

#preload bark models
preload_models()

#define FastAPI app
app = FastAPI()

#Define ScoringItem
class ScoringItem(BaseModel):
    TextPrompt: str 

#define common parameters
def common_params(
    format: str = Query("wav", description="The audio format to return"),
    rate: int = Query(SAMPLE_RATE, description="The sample rate of the audio")
):
    return {"format": format, "rate": rate}

#Define generate endpoint
@app.post("/generate")
async def generate_endpoint(item: ScoringItem, params: dict = Depends(common_params)):
    text = item.TextPrompt
    audio_array = generate_audio(text)
    if params["format"] == "wav":
        write_wav("bark_generation.wav", params["rate"], audio_array)
        with open("bark_generation.wav", "rb") as f:
            return f.read()
    elif params["format"] == "array":
        return {"result": audio_array.tolist()}
    else:
        return {"error": f"Invalid format: {params['format']}"}

#playig audio in notebook
@app.get("/play")
async def play_endpoint(item: ScoringItem):

    text = item.TextPrompt
    audio_array = generate_audio(text)
    from IPython.display import Audio
    return Audio(audio_array, rate=SAMPLE_RATE)

#Root endpoint
@app.get("/")
async def root():
    message = '''
	Welcome to the bark API!
	To generate audio from text, use the /generate endpoint with a POST request.
	To play audio in notebook, use the /play endpoint with a GET request.
	You can also customize the audio format and sample rate using query parameters.
	For more details, go to http://0.0.0.0:8000/docs
	'''
	
    return {"message": message}
