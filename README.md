# AWS Automated YouTube Highlights

An AWS serverless project that processes YouTube video transcripts, extracts key highlights, and delivers concise summaries through email notifications.

## Overview

Watching long YouTube videos to find important information can be time-consuming. This project demonstrates a cloud-based workflow that extracts meaningful highlights from video transcripts and delivers them directly to users through email.

The system uses Amazon S3 for storage, AWS Lambda for transcript processing, and Amazon SNS for email notifications.

## Architecture

```text
YouTube Video
      |
      v
Download Available Captions
      |
      v
yt-dlp + Local Python Script
      |
      v
Transcript JSON
      |
      v
Upload to Amazon S3
(transcripts/demo1.json)
      |
      v
S3 Object-Created Event
      |
      v
AWS Lambda
highlight-summarize
      |
      v
Extractive Highlight Generation
      |
      v
Amazon SNS
      |
      v
Email Notification
```

## AWS Services Used

| Service           | Purpose                                                    |
| ----------------- | ---------------------------------------------------------- |
| Amazon S3         | Stores video metadata and transcript JSON files            |
| AWS Lambda        | Processes uploaded transcripts and extracts highlights     |
| Amazon SNS        | Publishes generated highlights through email notifications |
| Amazon CloudWatch | Monitors Lambda execution and captures logs                |

## Workflow

1. **Video selection:** Select a YouTube video for processing.
2. **Caption extraction:** Use `yt-dlp` to download available captions locally.
3. **Transcript conversion:** Run `captions_to_transcript.py` to convert the caption file into the required transcript JSON format.
4. **Metadata upload:** Upload the video's metadata JSON file to the `meta/` prefix in S3.
5. **Transcript upload:** Upload the generated transcript JSON file to the `transcripts/` prefix in S3.
6. **Event trigger:** Uploading the transcript triggers the configured S3 event notification, invoking the `highlight-summarize` Lambda function.
7. **Highlight generation:** Lambda processes the transcript and extracts key highlights using the implemented extractive summarization logic.
8. **Email delivery:** The generated highlights are published to the configured SNS topic, which sends an email notification to its confirmed subscribers.
9. **Monitoring:** CloudWatch logs help track Lambda execution and troubleshoot errors.

## Project Structure

```text
aws-youtube-highlights/
├── captions_to_transcript.py
├── lambda_function.py
├── README.md
```

*This is a suggested minimal structure. Update the filenames to match the actual files in your repository.*

## Technologies

- Python
- Amazon S3
- AWS Lambda
- Amazon SNS
- Amazon CloudWatch
- yt-dlp

## Configuration

Before running the project, ensure that:

- The S3 bucket and required prefixes are configured.
- The Lambda function has permission to read the uploaded transcript and publish to SNS.
- The S3 event notification is configured to invoke the Lambda function for transcript uploads.
- The SNS topic has an email subscription that has been confirmed.
- The Lambda function's environment variables and resource identifiers match your AWS configuration.

## Running the Demo

1. Download available YouTube captions using `yt-dlp`.
2. Convert the captions into transcript JSON using the Python conversion script.
3. Upload the video's metadata JSON file to `meta/` in the configured S3 bucket.
4. Upload the transcript JSON file to `transcripts/`.
5. Verify the Lambda invocation in Amazon CloudWatch.
6. Check the subscribed email inbox for the generated highlights.

## Current Implementation

The current demonstration uses locally downloaded captions and manual transcript uploads to Amazon S3. Highlight generation uses extractive summarization logic in a single Lambda function.

Amazon Transcribe and Amazon Bedrock are not part of the current working implementation.

## Security

- Never commit AWS access keys, secret keys, or passwords.
- Exclude `.env` files and other files containing credentials.
- Avoid uploading private videos, sensitive transcripts, or personal information.
- Use IAM roles with least-privilege permissions.

## Future Enhancements

- Automate caption retrieval and transcript ingestion.
- Explore managed speech-to-text services.
- Integrate AI-powered summarization.
- Add timestamped highlights and structured output.
- Improve error handling and monitoring.

##

---

*Built to explore event-driven serverless processing and automated content summarization using AWS.*
