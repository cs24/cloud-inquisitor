#!/bin/bash
set -e

# sudo pip3 install pytest==3.0.7
# pytest auth
pytest
pytest -v --cov awsaudits --cov-report=xml --cov-report=term


