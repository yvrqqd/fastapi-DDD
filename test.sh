#!/bin/sh
pwd
ls

python -m pytest --cov-config=./test/.coveragerc ./test/unit_tests --cov=app --cov-report=term-missing -p no:cacheprovider -vv test/
