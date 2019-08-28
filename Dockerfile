FROM python:3.6
ADD . /customers
RUN pip install -r customers/requirements.txt
CMD python customers/run.py
