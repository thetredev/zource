#!/bin/bash

rm -rf \
  .venv \
  .zig-cache \
  zig-out \
  dist \
  zource/*.so

find . -name __pycache__ | xargs rm -rf
find . -name '\.pytest_cache' | xargs rm -rf
