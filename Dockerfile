FROM python:3.8

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#ENV PYTHONPATH /utils
#ENV PYTHONPATH /db


# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
#COPY utils/functions.py .
#COPY db/beer.db .
#COPY main.py .
COPY ./ .
#ENTRYPOINT ["python", "main.py"]