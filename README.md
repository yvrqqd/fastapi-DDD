# FastAPI DDD

Implementation of Domain Driven Design architecture using FastAPI.
The to-do list API is realized as an example.

## Running locally

To launch the project locally, run the following commands:

```bash
git clone https://github.com/yvrqqd/fastapi-DDD.git
```
```bash
cd fastapi-DDD/
```
```bash
sudo docker compose up --build
```

Then follow http://0.0.0.0:8000/docs

### Running tests

After launching app locally:

1. Create and activate venv
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
2. Run unit tests:
    ```bash
    sh test.sh
    ```
3. Integration tests:
    ```bash
    # TODO
    ```

## TODO

- [ ] Unit tests` coverage >85%.
- [ ] Integration tests: cover CRUD operations.
- [ ] Refactoring: fix docstrings, logging.

