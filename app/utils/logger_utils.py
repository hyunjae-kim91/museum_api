import json
import os
import os.path
import datetime
import logging
import logging.handlers
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine.url import URL
from datetime import datetime, date

from app.db.db_connector import DBConnector

Base = declarative_base()

#오늘날자 :: yyyy-mm-dd
def today()->str:
    return date.today().isoformat()

# 로그 모델 정의
class SystemLog(Base):
    __table_args__ = {'schema': 'dev_aihr'}
    __tablename__ = 'sys_logs'

    id = Column(Integer, primary_key=True)
    log_dt = Column(DateTime, default=datetime.now)
    level = Column(String(10))
    message = Column(Text)

class ModelInferLog(Base):
    __table_args__ = {'schema': 'dev_aihr'}
    __tablename__ = 'model_logs'

    id = Column(Integer, primary_key=True)
    log_dt = Column(DateTime, default=datetime.now)
    api_nm = Column(String(20))
    actn_nm = Column(String(20))
    user_nm = Column(String(20))
    inpt_data = Column(Text)
    otpt_data = Column(Text)
    trc_cd = Column(String(100))

class SQLAlchemyHandler(logging.Handler):
    def __init__(self, log_type):
        super().__init__()
        self.session = DBConnector().create_session()
        self.log_type = log_type

    def emit(self, record):
        if self.log_type == 'system':
            log_entry = SystemLog(
                level=record.levelname,
                message=self.format(record)
            )
        else : # 'model_infer':
            message = json.loads(record.msg)
            log_entry = ModelInferLog(
                api_nm=message.get('api_name'),
                actn_nm=message.get('action_name'),
                user_nm=message.get('user_name'),
                inpt_data=str(message.get('input_data')),
                otpt_data=str(message.get('output_data')),
                trc_cd=str(message.get('trace_code'))
            )
        self.session.add(log_entry)
        self.session.commit()

class Logger:
    def __init__(self, log_type):
        self.log_type = log_type

    def __call__(self) -> logging.Logger:
        logger = logging.getLogger(self.log_type)
        if not logger.hasHandlers():  # Prevent duplicate handlers
            logger.setLevel(logging.INFO)

            sqlalchemy_handler = SQLAlchemyHandler(self.log_type)
            logger.addHandler(sqlalchemy_handler)

        return logger

class FileLogger:

    def __call__(self) -> logging:

        logger = logging.getLogger('log')

        if len(logger.handlers) > 0:
            return logger  # Logger already exists

        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] (%(filename)s:%(lineno)d) > %(message)s')

        log_path = 'logs/{}.log'.format(today())
        if not os.path.exists('logs'):
            os.mkdir('logs')

        fileHandler = logging.FileHandler(log_path)
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.addHandler(streamHandler)

        return logger