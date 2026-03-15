# AWS Intelligent Document Processing

An AI-powered document processing pipeline that extracts text from identity and financial documents using AWS cloud services.

This project demonstrates how to automate document text extraction using AWS Textract and process the results using Python in Amazon SageMaker.

---

## Project Overview

Manual document processing is slow and error-prone. This project automates the extraction of text from documents such as passports, invoices, and employment verification forms.

The system uses Amazon Textract to detect and extract text from uploaded images and converts the output into structured text files.

---

## Technologies Used

* Amazon Textract
* Amazon S3
* Amazon SageMaker
* Python
* Boto3 (AWS SDK for Python)

---

## Project Architecture

Document Image → AWS Textract → Python Processing → Extracted Text Output

1. A document image is uploaded.
2. Amazon Textract detects and extracts text.
3. Python processes the response.
4. Extracted text is saved as `.txt` output.

---

## Supported Document Types

* Passport
* Invoice
* Employment Verification

---

## Repository Structure

```
aws-intelligent-document-processing
│
├── sample-documents
│   ├── Passport.png
│   ├── invoice.png
│   └── Employment_verification.png
│
├── outputs
│   ├── Passport.txt
│   ├── invoice.txt
│   └── Employment_verification.txt
│
├── src
│   └── textract_pipeline.py
│
└── README.md
```

---

## How It Works

1. The script scans the folder for `.png`, `.jpg`, or `.jpeg` images.
2. Each image is sent to Amazon Textract.
3. Textract detects text blocks from the document.
4. Extracted text is saved to a `.txt` file with the same name as the image.

---

## Example Usage

Run the processing script:

```
python textract_pipeline.py
```

Example output:

```
Processing: Passport.png
✓ Success: Text saved to Passport.txt
```

---

## Future Improvements

* Automatic document classification
* Deploy as an API using AWS Lambda
* Store structured results in DynamoDB
* Add OCR confidence filtering
* Build a document processing dashboard

---

## Author

Sania Hashmi
AWS + AI Enthusiast
