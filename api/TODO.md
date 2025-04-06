# PorQua Web API & JupyterLab UI - GSoC 2025 TODO List

This list outlines the tasks and timeline for the GSoC 2025 project based on the submitted proposal.

## Pre-Coding (Community Bonding Period: Before June 2, 2025)

- [x] familiarize with PorQua codebase.
- [x] Set up the local development environment (Python, PorQua dependencies).
- [ ] Run PorQua's existing test suite successfully.
- [ ] Discuss detailed API/UI design and expectations with mentors.
- [ ] Refine project plan based on mentor feedback.

## Coding Period (June 2, 2025 – August 31, 2025)

### Week 1 (June 2 – June 8): Setup, API Skeleton, and Data Upload Endpoint
- [x] Initialize FastAPI project structure (`api/`).
- [x] Define core Pydantic models for API requests/responses.
- [x] Implement `/health` endpoint.
- [ ] Implement `POST /data` endpoint:
    - [x] Handle file uploads (CSV/JSON).
    - [x] Parse data into pandas DataFrames (`X` and `y`).
    - [x] Store data temporarily (in-memory dict with UUID keys).
    - [x] Return metadata response upon success.
    - [ ] Add basic error handling for file parsing.
- [ ] Write initial unit tests for data parsing logic.

### Week 2 (June 9 – June 15): `/optimize` Endpoint - Part 1: Core Logic & LeastSquares
- [ ] Implement basic structure of `POST /optimize` endpoint.
    - [ ] Retrieve data using `data_id`.
    - [ ] Basic request validation (Pydantic).
- [ ] Implement logic path for `optimization_type="LeastSquares"`:
    - [ ] Integrate with PorQua's `OptimizationData`.
    - [ ] Integrate with PorQua's `Constraints` (start with `add_budget`, `add_box("LongOnly")`).
    - [ ] Integrate with PorQua's `LeastSquares` class.
    - [ ] Integrate with PorQua's `OptimizationParameter`.
    - [ ] Handle `l2_penalty` parameter.
    - [ ] Call `optim.solve()`.
    - [ ] Process results (`weights`, `status`).
- [ ] Implement backend calculation for metrics: `portfolio_volatility`, `tracking_error`.
- [ ] Write unit tests for the `LeastSquares` parameter mapping logic.
- [ ] Write integration tests simulating a `LeastSquares` API call (`POST /data` -> `POST /optimize`).
- **Milestone:** `/optimize` functional for `LeastSquares` with basic constraints.

### Week 3 (June 16 – June 22): `/optimize` Endpoint - Part 2: Other Optimization Types
- [ ] Implement logic path for `optimization_type="MeanVariance"`:
    - [ ] Handle `risk_aversion` parameter.
    - [ ] Integrate with `MeanEstimator` and `Covariance` classes.
    - [ ] Handle `covariance_method` parameter.
    - [ ] Calculate `expected_return` metric.
- [ ] Implement logic path for `optimization_type="WeightedLeastSquares"`:
    - [ ] Handle `tau` parameter.
    - [ ] Integrate with `WeightedLeastSquares` class.
- [ ] Implement logic path for `optimization_type="QEQW"`:
    - [ ] Integrate with relevant PorQua classes (potentially using `Covariance`).
    - [ ] Handle `covariance_method` parameter.
- [ ] Ensure `metrics` object in the API response adapts correctly based on `optimization_type`.
- [ ] Write unit tests for parameter mapping for new types.
- [ ] Write integration tests covering `MeanVariance`, `WLS`, `QEQW` calls.
- **Milestone:** `/optimize` supports all core optimization types.

### Week 4 (June 23 – June 29): `/optimize` Endpoint - Part 3: Advanced Constraints, Solvers & Error Handling
- [ ] Implement full support for `constraints` object:
    - [ ] `box_type="LongShort"`.
    - [ ] Custom `min_weight` / `max_weight`.
    - [ ] `budget` flag properly handled.
    - [ ] `max_leverage` L1 norm constraint (via `constraints.add_l1()`).
- [ ] Implement `solver` selection logic (using `OptimizationParameter`).
- [ ] Test with multiple QP solvers (e.g., `cvxopt`, `osqp`, `highs`).
- [ ] Implement robust error handling:
    - [ ] Check for missing benchmark data when required.
    - [ ] Handle invalid parameter combinations/values (via Pydantic and explicit checks).
    - [ ] Catch solver errors (infeasible, unbounded, crashes).
    - [ ] Return informative `422` / `500` responses with clear messages.
- [ ] Write extensive integration tests for constraint combinations, solver choices, and error conditions (including infeasible scenarios).
- **Milestone:** `/optimize` endpoint is feature-complete regarding parameters, constraints, and solvers. API is robust.

### Week 5 (June 30 – July 6): Begin UI Development (Notebook Widgets - Foundation)
- [x] Create Jupyter notebook for UI prototyping (`ui/prototype.ipynb`).
- [x] Set up basic UI layout using `ipywidgets` (sections: upload, config, run, results).
- [ ] Implement file upload section:
    - [x] `ipywidgets.FileUpload` for asset and benchmark files.
    - [x] "Upload Data" `ipywidgets.Button`.
    - [x] Callback logic to read file content.
    - [x] Make `POST /data` API call using `requests`.
    - [x] Display API response (success/error) using `ipywidgets.Output`
    - [x] Store `data_id` internally in the notebook's kernel state.
- [x] **Milestone:** UI prototype can upload data via the API and display feedback.

### Week 6 (July 7 – July 13): UI Development (Parameter Configuration & Basic Execution)
- [ ] Implement parameter configuration panel (`ipywidgets.VBox`, `Accordion`):
    - [ ] `optimization_type` dropdown.
    - [ ] Constraints widgets (`box_type` dropdown, `budget` checkbox, `max_leverage` float text).
    - [ ] General parameters widgets (`solver` dropdown).
    - [ ] Optimization-specific parameter widgets (`l2_penalty`, `risk_aversion`, `tau`, `covariance_method`).
- [ ] Implement dynamic visibility logic for parameter widgets based on `optimization_type`.
- [ ] Implement "Run Optimization" button (`ipywidgets.Button`):
    - [ ] Callback to gather widget states.
    - [ ] Construct JSON payload for `POST /optimize`.
    - [ ] Make API call using `requests`.
    - [ ] Consider basic async handling or threading for API call to avoid freezing UI.
- [ ] Display raw JSON response from `/optimize` in an `Output` widget.
- [ ] Add placeholder for weights bar chart (`plotly.graph_objects.FigureWidget`).
- **Milestone:** UI allows full configuration and triggers `/optimize` API call.

### Midterm Evaluation (around July 14)
- [ ] Ensure core API (`/data`, `/optimize`) is fully implemented and tested.
- [ ] Ensure UI prototype is functional for configuration and execution.
- [ ] Prepare demo/video for mentors.
- [ ] Document progress and push code to repository.
- [ ] Gather mentor feedback and adjust plan if necessary.

### Week 7 (July 14 – July 20): UI Development (Results Visualization & Polish)
- [ ] Implement results visualization:
    - [ ] Populate weights bar chart (Plotly) from API response.
    - [ ] Display key metrics using `Label` or `HTMLTable`, adapt based on `optimization_type`.
    - [ ] Display solver status (`Label`).
    - [ ] Add collapsible section (`Accordion`) for detailed solver statistics (`solver_details`).
- [ ] Refine UI/UX:
    - [ ] Add tooltips to parameter widgets.
    - [ ] Implement loading indicator / disable button during optimization.
    - [ ] Display API error messages clearly in the UI.
- [ ] (Optional) Add performance comparison plot (portfolio vs benchmark cumulative returns).
- **Milestone:** Polished, interactive UI prototype in notebook providing full workflow.

### Week 8 (July 21 – July 27): Docker, Deployment & CI Setup
- [x] Create `Dockerfile` for the API server (`api/Dockerfile`).
- [x] Create `Dockerfile` for the UI environment (`ui/Dockerfile` or similar).
    - [x] Include JupyterLab, ipywidgets, plotting libs, requests.
- [x] Create `docker-compose.yml` at the project root.
    - [x] Define `api` and `ui` services.
    - [x] Configure networking between services.
    - [x] Set up environment variables (e.g., API URL for UI).
    - [x] Define volumes for development (code mounting) and potentially data persistence.
    - [ ] Consider using Docker profiles (`ui` profile).
- [x] Test `docker-compose up` builds and runs both services correctly.
- [ ] Set up basic CI (GitHub Actions):
    - [ ] Build Docker images on push/PR.
    - [ ] Run linters (e.g., `ruff`, `black`).
    - [ ] Run unit tests (`pytest`).
- **Milestone:** Working Docker Compose setup. Basic CI pipeline operational.

### Week 9 (July 28 – Aug 3): Extended Testing & UI Packaging (JupyterLab Extension)
- [ ] Write additional API integration tests for edge cases.
- [ ] Test API and UI with diverse datasets (size, missing data, no benchmark).
- [ ] (Optional) Add simple data cleaning options if needed.
- [ ] Package the `ipywidgets`-based UI as a JupyterLab extension:
    - [ ] Research packaging methods (cookiecutter, custom Python package).
    - [ ] Create necessary package structure (`jupyterlab_porqua_ui/`).
    - [ ] Implement logic to register the widget UI in JupyterLab.
    - [ ] Configure extension to find the API URL (via env var or settings).
- [ ] Test the extension rigorously within the Dockerized JupyterLab environment.
- [ ] Perform manual system testing of the entire workflow using Docker.
- **Milestone:** Comprehensive test suite. UI packaged as a functional JupyterLab extension.

### Week 10 (Aug 4 – Aug 10): Performance Analysis & Potential Extensibility Improvements
- [ ] Profile `/optimize` endpoint with larger datasets.
- [ ] Identify bottlenecks (data load, solver, metrics).
- [ ] Implement performance optimizations if necessary and feasible.
- [ ] Investigate asynchronous execution for `/optimize` (FastAPI `BackgroundTasks` or `asyncio`).
    - [ ] Document findings/decision.
- [ ] Review API and UI codebase for modularity and extensibility.
- [ ] Add code comments and documentation regarding extension points.
- **Milestone:** Profiling report. Performance considerations addressed. Code reviewed for future maintenance.

### Week 11 (Aug 11 – Aug 17): Final Documentation and Tutorials
- [ ] Write detailed User Guide (`docs/user_guide.md` or Wiki):
    - [ ] Introduction, Installation (Docker).
    - [ ] Quick Start Tutorial (with UI screenshots/GIFs).
    - [ ] API Usage Examples (`curl`, `requests`, other languages).
    - [ ] Explanation of Outputs/Metrics.
    - [ ] Advanced Configuration.
    - [ ] Development Guide.
- [ ] Create example Jupyter notebooks:
    - [ ] Programmatic API usage (`examples/api_tutorial.ipynb`).
    - [ ] UI extension usage guide (`examples/ui_walkthrough.ipynb`).
- [ ] Refine API auto-documentation (FastAPI `/docs`):
    - [ ] Improve endpoint docstrings.
    - [ ] Add example requests/responses in schema.
    - [ ] Ensure error responses are documented.
- [ ] Proofread and polish all documentation (README, guides, comments).
- **Milestone:** Comprehensive, polished documentation suite.

### Week 12 (Aug 18 – Aug 24): Buffer, User Feedback & Fixes
- [ ] Address any slipped tasks from previous weeks.
- [ ] Incorporate mentor feedback.
- [ ] Conduct final User Acceptance Testing (UAT) with mentors/peers.
- [ ] Fix bugs identified during testing/feedback.
- [ ] Perform final code cleanup and refactoring.
- [ ] Ensure all tests (unit, integration, CI) are passing reliably.
- **Milestone:** Project feature-complete, stable, and incorporates feedback.

### Week 13 (Aug 25 – Aug 31): Final Integration, Submission & Wrap-up
- [ ] Finalize project repository: README, structure, licensing.
- [ ] Lock final dependencies (`requirements.txt`, dockerfiles, etc.)
- [ ] Tag final release version (e.g., `v1.0.0`).
- [ ] Prepare GSoC final submission materials (links, demo, summary).
- [ ] Assist mentors with final evaluations.
- [ ] Submit all required materials to Google.
- [ ] Document potential future work/extensions.
- [ ] Write final GSoC blog post.
- **Final Milestone:** Successful GSoC project submission.

## Post-GSoC
- [ ] Address any final feedback post-submission
- [ ] Handover activities