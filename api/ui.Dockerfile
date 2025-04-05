# Use an official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /workspace

# Install JupyterLab and necessary UI libraries
# We need requests to talk to the API, ipywidgets for UI, pandas for potential data handling in notebook
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir jupyterlab ipywidgets requests pandas

# Copy the UI notebook(s) into the container
COPY ./ui /workspace/ui

# Expose the JupyterLab port
EXPOSE 8888

# Set default command to run JupyterLab with authentication disabled
# Using both NotebookApp and ServerApp to support different JupyterLab versions
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", \
     "--ServerApp.token=''", "--ServerApp.password=''", \
     "--ServerApp.disable_check_xsrf=True", "--ServerApp.authenticate_prometheus=False", \
     "--NotebookApp.token=''", "--NotebookApp.password=''"] 