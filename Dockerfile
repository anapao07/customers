FROM python:3.6
ADD . /home/customers
RUN pip install -r /home/customers/requirements.txt
CMD python /home/customers/run.py
