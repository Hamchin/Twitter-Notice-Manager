#!/bin/bash

DIST_DIR="dist"

if [ -e ${DIST_DIR} ]; then
  rm -rf ${DIST_DIR}
fi

mkdir ${DIST_DIR}
cd backend

zip -r ../${DIST_DIR}/function.zip *.py

pip install -r requirements.txt -t ../${DIST_DIR}/python
cd ../${DIST_DIR}
zip -r package.zip python

echo ""
echo "File for Lambda Function: ${DIST_DIR}/function.zip"
echo "File for Lambda Layer: ${DIST_DIR}/package.zip"
