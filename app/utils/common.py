import json
import os
import re
import openai
import psycopg2
from pathlib import Path
from kiwipiepy import Kiwi
# from pinecone_text.sparse import BM25Encoder
from dotenv import load_dotenv

load_dotenv()

# OpenAI 임베딩 함수
def get_openai_embedding(text):

    ## open API 설정
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    model_name = 'text-embedding-ada-002'

    openai.api_key = OPENAI_API_KEY

    response = openai.embeddings.create(
        model = model_name,
        input = text
    )
    embedding = json.loads(response.data[0].to_json()).get('embedding',[])

    return embedding

def text_to_morpheme(text):
    kiwi = Kiwi()
    select_pos = ['NNG', 'NNP', 'NNB', 'SL', 'VV', 'VA', 'XR']

    tokens = kiwi.tokenize(text)
    tokenized_sentence = [token.form for token in tokens if token.tag in select_pos]
    morpheme = ' '.join(tokenized_sentence)

    return morpheme


def correct_sql_output(generated_sql):
    """
    Corrects common SQL errors in the generated output.
    """
    
    # Fix missing spaces around operators (e.g., `>=3and_<=4` → `>= 3 AND <= 4`)
    corrected_sql = re.sub(r'(\d)([<>=])', r'\1 \2', generated_sql)
    corrected_sql = re.sub(r'([<>=])(\d)', r'\1 \2', corrected_sql)
    corrected_sql = re.sub(r'and_', ' AND ', corrected_sql, flags=re.IGNORECASE)

    # Ensure proper logical operator formatting
    corrected_sql = re.sub(r'\s+and\s+', ' AND ', corrected_sql, flags=re.IGNORECASE)
    corrected_sql = re.sub(r'\s+or\s+', ' OR ', corrected_sql, flags=re.IGNORECASE)

    return corrected_sql




# def get_bm25_embedding_with_kiwi(text, encoder_name):
#     # 1. 형태소로 변환
#     kiwi = Kiwi()
#     select_pos = ['NNG', 'NNP', 'NNB', 'SL', 'VV', 'VA', 'XR']
#     tokens = kiwi.tokenize(text)
#     tokenized_sentence = [token.form for token in tokens if token.tag in select_pos]
#     morpheme = ' '.join(tokenized_sentence)
#     json_file_path = Path(__file__).parent.parent / 'encoder' / f'{encoder_name}.json'

#     # 2. bm25 계산
#     bm25 = BM25Encoder()
#     bm25.load(json_file_path)
#     bm25_value = bm25.encode_queries(morpheme)

#     # 3. sparse vec으로 변환
#     sparse_vec = json.dumps({str(index): value for index, value in zip(bm25_value['indices'], bm25_value['values'])})
#     return sparse_vec