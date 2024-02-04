FROM python:3.8.5
RUN apt-get update

RUN python -m pip install --upgrade setuptools pip
RUN apt-get install git

RUN python -m pip install mlflow==2.2.2
RUN python -m pip install boto3
RUN python -m pip install protobuf==3.20.*
RUN python -m pip install psycopg2

RUN pip3 install pandas
RUN pip3 install numpy
RUN pip3 install scikit-learn
RUN pip3 install matplotlib
RUN pip3 install seaborn
RUN pip3 install jupyter
RUN pip3 install pyspark

