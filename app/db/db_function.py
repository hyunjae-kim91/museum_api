import pandas as pd
from typing import List, Union
import sqlalchemy
from sqlalchemy import text
from functools import reduce

from .db_connector import DBConnector

def bulk_insert(df: pd.DataFrame, schema: str, table_name: str):
    df = df.drop_duplicates()
    dbConnector = DBConnector()
    try:
        df.to_sql(
            name=table_name,
            schema=schema,
            con=dbConnector.engine,
            index=False,
            if_exists='append',
            chunksize=10000,
            method='multi'
        )
    except sqlalchemy.exc.SQLAlchemyError as sQLAlchemyError:
        raise Exception(str(sQLAlchemyError)[:2000])
    except Exception as e:
        raise Exception(str(e)[:2000])

def execute_all_sql(query: str) -> None:
    """sql파일에서 읽어온 쿼리를 실행합니다."""
    session = DBConnector().create_session()
    try:
        all_data = session.execute(text(query))
        all_data = all_data.all()
        # all_data = pd.DataFrame(all_data)
        return all_data
    except sqlalchemy.exc.SQLAlchemyError as sQLAlchemyError:
        raise Exception(sQLAlchemyError)
    except Exception as e:
        raise Exception(e)
    finally:
        session.close()
        DBConnector().engine.dispose()
        DBConnector().engine = None

def execute_batch_sql(query: str, params: tuple) -> pd.DataFrame():
    session = DBConnector().create_session()
    try:
        if params :
            result = session.execute(text(query), params).fetchall()
            return pd.DataFrame(result)
        else :
            result = session.execute(text(query)).fetchall()
            return pd.DataFrame(result)
    except sqlalchemy.exc.SQLAlchemyError as sQLAlchemyError:
        raise Exception(sQLAlchemyError)
    except Exception as e:
        raise Exception(e)
    finally:
        session.close()
        DBConnector().engine.dispose()

def get_query(SQL_PATH, SQL_FILE):
    with open(f"{SQL_PATH}/{SQL_FILE}", "r", encoding="utf-8") as file:
        query = reduce(lambda x, y: x+y, file.readlines())
    return query
