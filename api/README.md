# Running PorQua API and UI Locally with Docker

This guide explains how to run the PorQua API and its JupyterLab UI prototype using Docker and Docker Compose in various configurations.

**Prerequisites:**

*   Docker installed ([https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/))


Navigate to the `api/` directory in your terminal for all commands below.

## Configuration 1: Running Only the UI (Connecting to an External API)

This is useful if the API is already running elsewhere (e.g., on a server, another Docker container, or directly on your host machine outside of this compose setup).

1.  **Build and Run UI Service:** Use `docker-compose` to build and run *only* the `ui` service defined in `docker-compose.yml`.
    ```bash
    docker-compose up --build ui
    ```

2.  **Access UI:** Open your web browser and navigate to `http://localhost:8888`. You should see the JupyterLab interface. Find the `porqua_ui_prototype.ipynb` notebook in the file browser (inside the `ui` folder) and open it. It will connect to the `API_BASE_URL` you specified.

3.  **Stop UI:** Press `Ctrl+C` in the terminal where `docker-compose` is running.

## Configuration 2: Running Both UI and API Locally (Default)

This runs both the FastAPI application and the JupyterLab UI using Docker Compose. They will communicate over the internal Docker network.

1.  **Build and Run All Services:**
    ```bash
    docker-compose up --build
    ```
    This command builds both the `api` and `ui` images (if they don't exist or need updating) and starts both containers.

2.  **Access API:**
    *   The API will be available at `http://localhost:8000`.
    *   You can check the health at `http://localhost:8000/health`.
    *   API docs are at `http://localhost:8000/docs`.

3.  **Access UI:**
    *   Open your web browser and navigate to `http://localhost:8888`.
    *   Find and open the `api/ui/porqua_ui_prototype.ipynb` notebook.
    *   The notebook is configured (via `docker-compose.yml` environment variable `API_BASE_URL=http://api:8000`) to communicate with the `api` service running in the other container.

4.  **Stop Services:** Press `Ctrl+C` in the terminal where `docker-compose` is running.

## Configuration 3: Deploying Only the API

This runs only the FastAPI application container, suitable for deploying the API as a standalone service.

1.  **Build and Run API Service:**
    ```bash
    docker-compose up --build api
    ```
    This command builds and runs *only* the `api` service.

2.  **Access API:**
    *   The API will be available at `http://localhost:8000`.
    *   Check health at `http://localhost:8000/health`.
    *   API docs are at `http://localhost:8000/docs`.

3.  **Stop API:** Press `Ctrl+C` in the terminal where `docker-compose` is running.

## Development Tips

*   **Live Reload:** The `docker-compose.yml` file includes commented-out `volumes` sections. Uncommenting these will mount your local `app` and `ui` directories into the respective containers. If you also run `uvicorn` with `--reload` (the default `CMD` in `app.Dockerfile` doesn't include it, you might need to override the command in `docker-compose.yml` or rebuild the image with the CMD changed) and save changes locally, the services *inside* the containers should reflect the changes without rebuilding the image.
*   **Cleaning Up:** To remove the containers, networks, and volumes created by `docker-compose`, run:
    ```bash
    docker-compose down --volumes # Add --volumes to remove named volumes if any were used
    ``` 