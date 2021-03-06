#!/bin/bash
#
# Run project tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests.sh

# Use default environment vars for localhost if not already set
export DM_API_URL=${DM_API_URL:=http://localhost:5000}
export DM_ADMIN_FRONTEND_API_AUTH_TOKEN=${DM_ADMIN_FRONTEND_API_AUTH_TOKEN:=myToken}
export DM_ADMIN_FRONTEND_ENVIRONMENT="test"

echo "Environment variables in use:"
env | grep DM_

set -o pipefail

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo -e "\033[31m$TEST failed\033[0m"
    exit $EXIT_STATUS
  else
    echo -e "\033[32m$TEST passed\033[0m"
  fi
}

pep8 .
display_result $? 1 "Code style check"

nosetests -v -s --with-doctest
display_result $? 2 "Unit tests"
