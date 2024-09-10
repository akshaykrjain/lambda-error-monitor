import os
import time
import logging
from datetime import datetime, timedelta, timezone
import boto3

# Configuration with environment variable support
DEFAULT_FUNCTION_NAME = os.environ.get("DEFAULT_FUNCTION_NAME", None)
MAX_ERROR_COUNT = int(os.environ.get("MAX_ERROR_COUNT", 20))
ERROR_WINDOW_MINUTES = int(os.environ.get("ERROR_WINDOW_MINUTES", 10))
POLL_INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL_SECONDS", 5))
AWS_REGION = os.environ.get("AWS_REGION", "eu-west-1")

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_lambda_error_count(cloudwatch, function_name=None):
    """
    Fetch the error count for a Lambda function or all Lambda functions.
    :param cloudwatch: boto3 CloudWatch client
    :param function_name: Name of the Lambda function (optional)
    :return: Error count
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=ERROR_WINDOW_MINUTES)
    metric_params = {
        "Namespace": "AWS/Lambda",
        "MetricName": "Errors",
        "StartTime": start_time,
        "EndTime": end_time,
        "Period": ERROR_WINDOW_MINUTES * 60,
        "Statistics": ["Sum"],
    }
    if function_name:
        metric_params["Dimensions"] = [{"Name": "FunctionName", "Value": function_name}]
    response = cloudwatch.get_metric_statistics(**metric_params)
    if not response["Datapoints"]:
        return 0
    return int(response["Datapoints"][0]["Sum"])


def monitor_errors(function_name=None):
    """
    Monitor Lambda function errors and exit if the error count exceeds the threshold.
    :param function_name: Name of the Lambda function to monitor (optional)
    """
    cloudwatch = boto3.client("cloudwatch", region_name=AWS_REGION)
    while True:
        error_count = get_lambda_error_count(cloudwatch, function_name)
        if error_count > MAX_ERROR_COUNT:
            logger.error(
                f"Error count {error_count} exceeds the limit of {MAX_ERROR_COUNT}"
            )
            # Trigger alert or notification mechanism here
            return 1
        else:
            logger.info(
                f"Error count {error_count} is within the limit of {MAX_ERROR_COUNT}"
            )
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        logger.info(f"Monitoring errors for Lambda function: {function_name}")
    else:
        function_name = DEFAULT_FUNCTION_NAME
        logger.info(
            "Monitoring errors via Cloudwatch for all Lambda Functions"
            if function_name is None
            else f"Monitoring errors for Lambda function: {function_name}"
        )
    sys.exit(monitor_errors(function_name))
