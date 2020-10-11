#!/bin/sh
gunicorn panoptique.wsgi --log-level debug --workers 1 --threads 4 -k gevent
