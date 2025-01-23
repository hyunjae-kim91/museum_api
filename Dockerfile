FROM python:3.12

WORKDIR /app
# 소스 복사
COPY . .

# 시간 세팅 (KST 기준)
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# python 라이브러리 설치
RUN pip3 install -r requirements.txt --no-cache-dir

# 로그 디렉토리 생성
RUN mkdir -p logs

# run service
RUN chmod 777 run.sh
CMD bash run.sh