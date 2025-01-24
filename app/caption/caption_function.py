import json

from app.utils.logger_utils import Logger
from app.engine.chat_completion import chatCompletion
from app.engine.chat_function import PromptManager, ChatProcessor
from app.models.model import ShortCaptionInputModel

LOGGER = Logger(log_type='model_infer')

class ShortCaptionProcessor:

    def __init__(self):
        self.api_name = 'short_caption'
        self.prompt_manager = PromptManager(
            prompt_file_path="app/engine/prompts",
            example_file_path="app/engine/examples"
        )
        self.chat_instance = chatCompletion()
        self.chat_processor = ChatProcessor(
            chat=self.chat_instance,
            prompt_manager=self.prompt_manager,
        )

    def get_short_caption(self, request: ShortCaptionInputModel):
        result = self.chat_processor.chat_short_caption(request=request)
        result_dict = {}
        result_content = result.content
        result_list = result_content.split('|')
        for res in result_list:
            key, value = res.split(':')
            key = key.replace('[','').replace(']','').strip()
            value = value.strip()
            result_dict[key] = value
        return result_dict