import json

class PromptManager:
    def __init__(self, prompt_file_path: str, example_file_path: str):
        self.prompt_file_path = prompt_file_path
        self.example_file_path = example_file_path

        # 텍스트 파일 읽기
        self.short_caption_prompt = self._load_text("short_caption_prompt.txt")

        # JSON 파일 읽기
        self.short_caption_list = self._load_json("short_caption_list.json")

    def _load_text(self, file_name: str) -> str:
        """지정된 텍스트 파일을 읽어서 반환"""
        file_path = f"{self.prompt_file_path}/{file_name}"
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            return f.read()

    def _load_json(self, file_name: str) -> dict:
        """지정된 JSON 파일을 읽어서 반환"""
        file_path = f"{self.example_file_path}/{file_name}"
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)


class ChatProcessor:
    def __init__(self, chat, prompt_manager: PromptManager):
        self.chat = chat
        self.prompt_manager = prompt_manager

    def chat_short_caption(self, request):
        """
        캡션 짧은 버전 생성
        """
        model_name = 'gpt-4o-mini'
        prompt = self.prompt_manager.short_caption_prompt
        examples = self.prompt_manager.short_caption_list

        response = self.chat.fewshot(request, examples, prompt, model_name)
        
        return response