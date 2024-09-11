# Lambda Error Monitoring in Kubernetes

## Overview

This project monitors AWS Lambda errors using CloudWatch metrics and runs within a Kubernetes pod. It fetches error counts for one or more Lambda functions and reports their health. If Lambda errors exceed a predefined threshold, the app signals Kubernetes to mark the pod as unhealthy via liveness and readiness probes.

## Features

- Monitors Lambda error count via CloudWatch metrics.
- Tracks errors for a specified Lambda function or all Lambda functions.
- Uses Kubernetes liveness and readiness probes to report health status.
- Automatically restores healthy status when errors fall below the threshold.

## Requirements

- Docker
- Kubernetes Cluster
- AWS credentials with access to CloudWatch

## Configuration

The following environment variables are used to configure the behavior of the app:

| Variable                | Description                                                | Default     |
| ----------------------- | ---------------------------------------------------------- | ----------- |
| `DEFAULT_FUNCTION_NAME` | The Lambda function name to monitor. Monitors all if empty | None        |
| `MAX_ERROR_COUNT`       | Maximum allowed Lambda errors before marking unhealthy     | 20          |
| `ERROR_WINDOW_MINUTES`  | Time window (in minutes) to count Lambda errors            | 10          |
| `POLL_INTERVAL_SECONDS` | Time between each CloudWatch poll (in seconds)             | 5           |
| `AWS_REGION`            | AWS region of the Lambda functions                         | `eu-west-1` |
| `AWS_ACCESS_KEY_ID`     | Your AWS Access Key Id, (Skip if using IAM Roles)          |             |
| `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Access Key(Skip if using IAM Roles)        |             |

---
