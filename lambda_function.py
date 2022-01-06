import boto3
from urllib.parse import unquote_plus
import os, json
import dat2_decoder as decoder

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        download_path = f"/tmp/{key}"
        upload_path = os.path.splitext(download_path)[0] + ".csv"
        os.makedirs(os.path.dirname(download_path), exist_ok=True)

        try:
            s3_client.download_file(bucket, key, download_path)

            bytes = decoder.read_bytes(download_path)
            data = decoder.decode_bytes(bytes)
            decoder.write(data, upload_path)

            s3_client.upload_file(upload_path, "cmcsv", upload_path[5:]) #[5:] gets rid of /tmp/
        except Exception as error:
            print(error)
            response = {
                "status": "failure",
                "file": key,
                "lambda": "dat2csv",
                "reason": error,
            }
            with open("/tmp/er.json", "w") as f:
                json.dump(response, f, indent=2)
                s3_client.upload_file("/tmp/er.json", "cmfail", key.replace("/", ""))