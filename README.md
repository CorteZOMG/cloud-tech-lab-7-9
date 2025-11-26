# FastAPI Project with Logging, Testing, and CI/CD

This project is a FastAPI application integrated with advanced logging (Sentry), automated testing (pytest), code quality tools (Black, Flake8, isort), and a CI/CD pipeline (GitHub Actions).

## 🚀 Technologies & Features

### 1. Cloud Logging (Sentry)
- **What it does**: Captures errors, exceptions, and performance traces in real-time.
- **How it works**:
  - The `src/core/logging/sentry.py` module initializes the Sentry SDK with FastAPI and Starlette integrations.
  - It automatically captures unhandled exceptions.
  - We also manually capture handled exceptions in `try/except` blocks using `sentry_sdk.capture_exception(e)`.
  - **Why**: To monitor application health and debug issues in production without SSH-ing into servers.

### 2. Automated Testing (Pytest)
- **What it does**: Verifies that the code works as expected.
- **How it works**:
  - **Unit Tests** (`tests/test_common_routes.py`): Test individual functions and endpoints in isolation.
  - **Integration Tests** (`tests/test_external_api.py`): Test how different parts of the system work together. We use `unittest.mock` to mock external API calls, ensuring tests are fast and reliable (no rate limits).
  - **Coverage**: `pytest-cov` measures how much of the code is executed during tests. We enforce a minimum coverage of 30%.
  - **Why**: To prevent regressions and ensure new features don't break existing functionality.

### 3. Code Quality (Linting & Formatting)
- **Black**: An uncompromising code formatter. It automatically formats code to PEP 8 standards (line length 120).
- **Isort**: Sorts imports alphabetically and by type (standard lib, third party, local).
- **Flake8**: Checks for style violations, unused variables, and potential bugs.
- **Why**: To maintain a consistent code style across the team and catch errors early.

### 4. Pre-commit Hooks
- **What it does**: Runs checks automatically *before* you commit code.
- **How it works**:
  - When you run `git commit`, the hooks defined in `.pre-commit-config.yaml` are executed.
  - It runs Black, Isort, Flake8, and Pytest.
  - If any check fails, the commit is blocked.
  - **Why**: To ensure that no broken or unformatted code ever enters the repository.

### 5. CI/CD (GitHub Actions)
- **What it does**: Automates the testing and deployment process.
- **How it works**:
  - Triggered on Pull Requests merged to `main` or `lab16-22`.
  - **Lint Job**: Runs linters to verify code style.
  - **Test Job**: Runs tests and uploads coverage reports.
  - **Deploy Job**: Triggers a webhook to deploy the application to Render.
  - **Healthcheck Job**: Verifies the deployed application is responding (200 OK).
  - **Why**: To enable continuous delivery and ensure production stability.

---

## 🛠️ Setup & Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd cloud-tech-lab-7-9
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install pre-commit hooks**:
    ```bash
    pre-commit install
    ```

5.  **Environment Configuration**:
    Create a `.env` file in the project root:
    ```bash
    SENTRY_DSN=your_sentry_dsn_here
    ```

---

## 🏃‍♂️ Running Locally

Start the development server:
```bash
uvicorn src.main:app --reload
```
Access the API documentation at: `http://localhost:8000/docs`

---

## 🧪 Testing

Run all tests with coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

Run a specific test file:
```bash
pytest tests/test_external_api.py
```

---

## 🚢 Deployment (Render)

To deploy from the `lab16-22` branch:

1.  **Configure Render**:
    - Go to your Service Settings on Render.
    - Change **Branch** to `lab16-22`.
    - Copy the **Deploy Hook URL**.

2.  **Configure GitHub Secrets**:
    - Go to Repo Settings -> Secrets and variables -> Actions.
    - Add `RENDER_DEPLOY_HOOK`: The URL you copied.
    - Add `RENDER_HEALTHCHECK_URL`: Your app's public URL (e.g., `https://your-app.onrender.com/common/healthcheck`).

3.  **Trigger Deployment**:
    - Push changes to `lab16-22`.
    - Create a Pull Request to `lab16-22` (or `main` if merging there).
    - Merge the PR.
    - GitHub Actions will run tests and trigger the deployment.
