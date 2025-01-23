import os
from dotenv import load_dotenv

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

load_dotenv()

class chatCompletion:

    def __init__(self):
        self.OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        self.chat = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.4,
            openai_api_key=os.environ.get('OPENAI_API_KEY')
        )

    def fewshot(self, user_input, examples, prompt, model_name):
        chat = ChatOpenAI(
            model_name=model_name,
            temperature=0.4,
            openai_api_key=self.OPENAI_API_KEY
        )

        example_prompt = ChatPromptTemplate.from_messages(
          [
              ("human", "{question}"),
              ("ai", "{answer}")
          ]
        )

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=examples,
            input_variables=["question"]
        )

        final_prompt = ChatPromptTemplate.from_messages(
          [
              ("system", f"{prompt}"),
              few_shot_prompt,
              ("human", "{question}")
          ]
        )

        chain = final_prompt | chat
        response = chain.invoke({
          "question": user_input
        })
        return response