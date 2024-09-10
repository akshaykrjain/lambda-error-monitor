# Lambda Error Monitor

Lambda Error Monitor is an open-source tool designed to monitor AWS Lambda function errors in real-time. It provides a simple and efficient way to keep track of error counts across your Lambda functions and alert you when error thresholds are exceeded.

## Features

- Monitor error counts for a specific Lambda function or all Lambda functions in your AWS account
- Configurable error threshold and monitoring window
- Environment variable support for easy configuration
- Docker support for simple deployment and scaling
- Built-in unit tests to ensure reliability

## Prerequisites

- AWS account with appropriate permissions to access CloudWatch metrics for Lambda functions
- Docker (for running the containerized version)
- Python 3.9 or later (for running the script directly)

## Installation

### Using Docker (Recommended)

Pull the Docker image:

```bash
docker pull akshaykrjain/lambda-error-monitor
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lambda-error-monitor.git
   cd lambda-error-monitor
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application can be configured using environment variables:

- `DEFAULT_FUNCTION_NAME`: The name of the Lambda function to monitor (optional, set to `None` to monitor all functions)
- `MAX_ERROR_COUNT`: Maximum number of errors allowed before alerting (default: 20)
- `ERROR_WINDOW_MINUTES`: Time window for error monitoring in minutes (default: 10)
- `POLL_INTERVAL_SECONDS`: Interval between error checks in seconds (default: 5)

## Usage

### Running with Docker

```bash
docker run -e AWS_ACCESS_KEY_ID=your_access_key \
           -e AWS_SECRET_ACCESS_KEY=your_secret_key \
           -e AWS_DEFAULT_REGION=your_aws_region \
           -e MAX_ERROR_COUNT=30 \
           -e ERROR_WINDOW_MINUTES=15 \
           akshaykrjain/lambda-error-monitor
```

### Running with Kubernetes

```
kubectl run lambda-error-monitor --image akshaykrjain/lambda-error-monitor --env AWS_ACCESS_KEY_ID=your_access_key --env AWS_SECRET_ACCESS_KEY=your_secret_key --env AWS_DEFAULT_REGION=your_aws_region --env MAX_ERROR_COUNT=30 --env ERROR_WINDOW_MINUTES=15
```

### Running the Python Script Directly

```bash
python lambda_error_monitor.py [function_name]
```

If `function_name` is not provided, it will monitor all Lambda functions.

## Development

### Running Tests

To run the unit tests:

```bash
pytest test_lambda_monitor.py
```

### Building the Docker Image

To build the Docker image locally:

```bash
docker build -t lambda-error-monitor .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the AWS SDK for Python (Boto3) team for their excellent library
- Inspired by the need for simple, real-time Lambda function monitoring

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.
