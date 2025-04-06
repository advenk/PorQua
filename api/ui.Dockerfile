# Use an official Python base image
FROM python:3.10-slim
WORKDIR /workspace
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir jupyterlab ipywidgets requests pandas
COPY ./ui /workspace/ui
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.token=''", "--ServerApp.password=''"]