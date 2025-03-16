# import os
# import subprocess
# import sys
#
# try:
#     from faster_whisper import WhisperModel
# except ImportError:
#     requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
#     try:
#         subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
#         from faster_whisper import WhisperModel
#     except Exception as e:
#         print(f'自动安装依赖失败，请手动执行: pip install -r {requirements_path}')
#         raise

from .apply_whisper import ApplyWhisperNode
from .add_subtitles_to_frames import AddSubtitlesToFramesNode
from .add_subtitles_to_background import AddSubtitlesToBackgroundNode
from .resize_cropped_subtitles import ResizeCroppedSubtitlesNode

NODE_CLASS_MAPPINGS = { 
    "Faster Whisper" : ApplyWhisperNode,
    "Add Subtitles To Frames": AddSubtitlesToFramesNode,
    "Add Subtitles To Background": AddSubtitlesToBackgroundNode,
    "Resize Cropped Subtitles": ResizeCroppedSubtitlesNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
     "Faster Whisper" : "Faster Whisper", 
     "Add Subtitles To Frames": "Add Subtitles To Frames",
     "Add Subtitles To Background": "Add Subtitles To Background",
     "Resize Cropped Subtitles": "Resize Cropped Subtitles"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']