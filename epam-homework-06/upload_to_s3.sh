#!/bin/bash

set -e

YEAR=$1
MONTH=$2

if [[ -z "$YEAR" || -z "$MONTH" ]]; then
  echo "Usage: ./upload_to_s3.sh <year> <month>"
  exit 1
fi

FILE_NAME=$(printf "yellow_tripdata_%04d-%02d.parquet" "$YEAR" "$MONTH")
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/${FILE_NAME}"
LOCAL_PATH="input/${FILE_NAME}"
S3_BUCKET="nyc-duration"
S3_KEY=$(printf "in/%04d-%02d.parquet" "$YEAR" "$MONTH")
ENDPOINT_URL="http://localhost:4566"

mkdir -p input

if [ -f "$LOCAL_PATH" ]; then
  echo "File already exists locally: $LOCAL_PATH"
else
  echo "Downloading $URL"
  curl -o "$LOCAL_PATH" "$URL"
  echo "Downloaded to $LOCAL_PATH"
fi

if ! aws --endpoint-url="$ENDPOINT_URL" s3 ls "s3://$S3_BUCKET" >/dev/null 2>&1; then
  echo "Creating S3 bucket: $S3_BUCKET"
  aws --endpoint-url="$ENDPOINT_URL" s3 mb "s3://$S3_BUCKET"
fi

echo "☁️  Uploading to s3://$S3_BUCKET/$S3_KEY"
aws --endpoint-url="$ENDPOINT_URL" s3 cp "$LOCAL_PATH" "s3://$S3_BUCKET/$S3_KEY"
echo "Uploaded to s3://$S3_BUCKET/$S3_KEY"
