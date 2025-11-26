# Lab Report: Logging, Testing, Linting, CI/CD

## 1. Cloud Logging Connection (Sentry)

We integrated Sentry for real-time error tracking and monitoring.

### Implementation Details
- **Library**: `sentry-sdk[fastapi]`
- **Configuration**: `src/core/logging/sentry.py` initializes Sentry with:
  - `FastApiIntegration` for request handling
  - `StarletteIntegration` for core web server events
  - `traces_sample_rate=1.0` for full performance tracing
  - `profile_session_sample_rate=1.0` for profiling

### Logging Setup
We configured Python's standard logging in `src/core/logging/logging_config.py` to output formatted logs to the console.
We added logging to:
- **Routers**: Log incoming requests and responses
- **Services**: Log external API calls and data processing
- **Exception Handlers**: Capture exceptions and send them to Sentry

Example log output:
```
[2024-03-20 10:00:00,123] [INFO] src.external_api.router: [EXTERNAL_API][DRIVERS] Request - session_key=9158, driver_number=None
[2024-03-20 10:00:00,456] [INFO] src.external_api.service: [SERVICE][GET_DRIVERS] Calling OpenF1 API - url=https://api.openf1.org/v1/drivers, params={'session_key': 9158}
[2024-03-20 10:00:01,789] [INFO] src.external_api.service: [SERVICE][GET_DRIVERS] Received 20 drivers from API
[2024-03-20 10:00:01,790] [INFO] src.external_api.router: [EXTERNAL_API][DRIVERS] Successfully fetched 20 drivers
```

## 2. Testing Results

We implemented a comprehensive test suite using `pytest`.

### Test Coverage
- **Unit Tests**: `tests/test_common_routes.py` covers healthcheck and utility endpoints.
- **Integration Tests**: `tests/test_external_api.py` covers external API interactions (mocked).

### Execution Result
```
tests/test_common_routes.py ......                                       [ 46%]
tests/test_external_api.py .......                                       [100%]

================================ tests coverage ================================
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
src/__init__.py                          0      0   100%
src/core/router.py                      31      1    97%
src/external_api/router.py              46      3    93%
src/external_api/service.py             66      8    88%
src/main.py                             20      6    70%
...
--------------------------------------------------------
TOTAL                                  233     22    91%
```
Total coverage achieved: **91%**

## 3. Static Analysis & Pre-commit Hooks

We configured `pre-commit` to automatically enforce code quality:
- **Black**: Formats code to PEP 8 standards (line length 120).
- **isort**: Sorts imports alphabetically and by type.
- **Flake8**: Checks for style violations and bugs.
- **Pytest**: Runs tests and ensures coverage > 30% before every commit.

Configuration file: `.pre-commit-config.yaml`

## 4. CI/CD Pipeline (GitHub Actions)

We created a GitHub Actions workflow `.github/workflows/ci-cd.yml` that runs on every Pull Request to `main`.

### Jobs
1. **Lint**: Runs Black, isort, and Flake8 to verify code style.
2. **Tests**: Runs pytest with coverage and uploads the report.

This ensures that no broken or unformatted code can be merged into the main branch.
