# Week 1 (June 2 – June 8): Setup, API Skeleton, and Data Upload Endpoint

*   **[COMPLETED]** Initialize the FastAPI project structure (`api/app/main.py`).
*   **[COMPLETED]** Define Pydantic models for API requests/responses (`api/app/models/data_models.py` for data upload).
*   **[COMPLETED]** Implement the `/health` endpoint (`api/app/routers/health.py`).
*   **[COMPLETED]** Implement the `POST /data` endpoint fully (`api/app/routers/data.py`):
    *   Handle file uploads (CSV/JSON).
    *   Implement parsing logic (`api/app/utils/data_parsing.py`).
        *   **[COMPLETED]** Added logging to parsing function.
        *   **[COMPLETED]** Modified date parsing to handle `dayfirst=True`.
        *   **[COMPLETED]** Added logging to data router function.
        *   **[COMPLETED]** Fixed `data_store` access bug.
    *   Store data temporarily (in-memory dict in `api/app/routers/__init__.py`).
    *   Return metadata response (`DataUploadResponse`).

# Week 5 (June 30 – July 6): Begin UI Development (Notebook Widgets - Foundation)

*   **[COMPLETED]** Created Jupyter notebook UI prototype (`api/ui/porqua_ui_prototype.ipynb`).
*   **[COMPLETED]** Implemented data upload section using `ipywidgets`:
    *   `FileUpload` widgets for asset and benchmark files.
    *   `Button` to trigger upload.
    *   Callback function (`on_upload_button_clicked`) to:
        *   Read widget file data.
        *   Send `POST` request to `/data` API endpoint using `requests`.
        *   Display success (with `data_id` and metadata) or error messages in an `Output` widget.
*   **[COMPLETED]** Resolved runtime issues (widget state handling, Nginx `client_max_body_size` configuration for large files).

# Week 8 (July 21 – July 27): Docker, Deployment & CI Setup

*   **[COMPLETED]** Containerized the PorQua API and UI:
    *   Created `api/app.Dockerfile` for the FastAPI application.
    *   Created `api/ui.Dockerfile` for the JupyterLab UI environment.
    *   Created `api/docker-compose.yml` to orchestrate both services.
    *   Modified the UI Jupyter notebook to read API URL from environment variable.
*   **[COMPLETED]** Created comprehensive documentation (`api/RUNNING_LOCALLY.md`) explaining how to run in different configurations:
    *   UI only (connecting to external API)
    *   Both UI and API locally
    *   API only (for deployment as a standalone service)
*   **[COMPLETED]** Fixed configuration issues:
    *   Fixed YAML validation error in `docker-compose.yml` (empty volumes section)
    *   Fixed JupyterLab token authentication configuration
        *   Updated to use both `ServerApp` and `NotebookApp` parameters for broader version compatibility
        *   Added additional security parameters to ensure authentication is fully disabled

*   **[NEXT - API]** Write initial unit/integration tests for `/data` and `/health`.
*   **[NEXT - UI]** Implement Optimisation section in the UI prototype. 