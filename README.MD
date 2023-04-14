# Text processor

## [Task](https://docs.google.com/document/d/1cap7ZmV_wIXWuXpWHjpANZ91vF-1-AouBmDNkbmhSGM/edit#)

## Architecture

![scheme](https://i.imgur.com/fwq6klf.png)

## How to use

### Request example

```json
{
 "fileUrl": "https://previews.123rf.com/images/happyroman/happyroman1611/happyroman161100004/67968361-atm-transaction-printed-paper-receipt-bill-vector.jpg"
}
```

### Endpoints

#### <https://887dle4970.execute-api.us-east-1.amazonaws.com/api/>

Main endpoint. Simply sends image url to the queue

Response example:

```json
{
    "message": "File uploaded successfully",
    "file_url": "https://previews.123rf.com/images/happyroman/happyroman1611/happyroman161100004/67968361-atm-transaction-printed-paper-receipt-bill-vector.jpg"
}
```

#### <https://9glneuz949.execute-api.us-east-1.amazonaws.com/api/>

Endpoint for OCR demonstration purposes. Returns the text found in the image.

Response example:

```json
{
    "image_url": "https://previews.123rf.com/images/happyroman/happyroman1611/happyroman161100004/67968361-atm-transaction-printed-paper-receipt-bill-vector.jpg",
    "text": "R ATM TRANSACTION TERMINAL # 65425899 SEQUNCE # 8564 DATE 15:18 08/10/2016 CARD NUMBER XXXXXXXXXXXX5698 CUSTOMER NAME JOHN EMPTY REQUSTED AMOUNT $100.00 TERMINAL FEE $1.25 TOTAL AMOUNT $101.25 "
}
```

## How to deploy

### Requirements

- Python 3.9
- Pipenv
- Pytest
- AWS CLI
- Chalice
- 1 S3 Bucket, 2 SQS, and Textract subscription

It's important to configure role permissions for file-processor lambda so that it can read from S3.

### Tests

```console
foo@bar:~$ py.test api/tests/tests.py
foo@bar:~$ py.test file-processor/tests/tests.py
```

### Deploy

```console
foo@bar:~$ cd api && chalice deploy && cd ..
foo@bar:~$ cd file-processor && chalice deploy && cd ..
foo@bar:~$ cd text-receiver && chalice deploy && cd ..
```
