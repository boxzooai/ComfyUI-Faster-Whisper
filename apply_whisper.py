from tqdm import tqdm

from faster_whisper import WhisperModel
import os
import folder_paths
import uuid
import torchaudio


class ApplyWhisperNode:

    def __init__(self):
        self.model = None
        self.model_name = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",),
                "model": (["base", "tiny", "small", "medium", "large"],),
                "language": (["auto", "en", "zh", "ja", "fr", "de", "es", "ru", "ko", "it", "pt", "nl", "tr", "pl", "ar", "hi"], {"default": "auto"}),
            }
        }

    RETURN_TYPES = ("STRING", "whisper_alignment", "whisper_alignment")
    RETURN_NAMES = ("text", "segments_alignment", "words_alignment")
    FUNCTION = "apply_whisper"
    CATEGORY = "faster-whisper"

    def apply_whisper(self, audio, model, language):

        # save audio bytes from VHS to file
        temp_dir = folder_paths.get_temp_directory()
        os.makedirs(temp_dir, exist_ok=True)
        audio_save_path = os.path.join(temp_dir, f"{uuid.uuid1()}.wav")
        torchaudio.save(audio_save_path, audio['waveform'].squeeze(
            0), audio["sample_rate"])

        # transribe using whisper
        if self.model_name != model:
            self.model = None
            self.model_name = model
            
        if self.model == None:
            model_dir = os.path.join(os.path.dirname(__file__), "models")
            os.makedirs(model_dir, exist_ok=True)
            self.model = WhisperModel(model,download_root=model_dir)
        
        segments, _ = self.model.transcribe(audio_save_path, word_timestamps=True, language=None if language == "auto" else language)
        full_text = ' '.join([s.text for s in segments])
        result = {
            'text': full_text.strip(),
            'segments': [{'text': s.text, 'start': s.start, 'end': s.end, 'words': [{'word': w.word, 'start': w.start, 'end': w.end} for w in s.words]} for s in segments]
        }

        segments = result['segments']
        segments_alignment = []
        words_alignment = []

        for segment in segments:
            # create segment alignments
            segment_dict = {
                'value': segment['text'].strip(),
                'start': segment['start'],
                'end': segment['end']
            }
            segments_alignment.append(segment_dict)

            # create word alignments
            for word in segment["words"]:
                word_dict = {
                    'value': word["word"].strip(),
                    'start': word["start"],
                    'end': word['end']
                }
                words_alignment.append(word_dict)

        return (result["text"].strip(), segments_alignment, words_alignment)
