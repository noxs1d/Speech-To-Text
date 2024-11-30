import whisper
import torch
#import torchaudio
class ModelWrapper:
    """Model wrapper class."""
    def __init__(self, model,audio):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model=whisper.load_model(model,device=self.device)
        self.audio=whisper.load_audio(audio)

    def predict(self,task):
        audio = whisper.pad_or_trim(self.audio)
        mel = whisper.log_mel_spectrogram(audio, n_mels=self.model.dims.n_mels).to(self.model.device)
        options = whisper.DecodingOptions(temperature=0.0, task=task)
        result = whisper.decode(self.model, mel, options)
        return result.text
