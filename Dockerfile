FROM apache/airflow:master-python3.8
USER root
RUN apt-get update
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

USER airflow
COPY ./requirements.txt /requirements.txt
RUN pwd
RUN ls -lstra
RUN pip install --no-deps --no-cache-dir -r /requirements.txt
COPY ./src/dist/cowin_search-0.1.1-py3-none-any.whl /cowin_search-0.1.1-py3-none-any.whl
RUN pip install --user /cowin_search-0.1.1-py3-none-any.whl

