#!/bin/bash

pyflakes simulacrum.py || exit $?

coverage run simulacrum.py --verbose
status=$?

coverage html

exit $status
