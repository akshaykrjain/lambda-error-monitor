import os
import logging
from datetime import datetime, timedelta, timezone
import boto3
from flask import Flask, jsonify

# Flask app for liveness/readiness probes
app = Flask(__name__)

# Configuration with environment variable support
DEFAULT_FUNCTION_NAME = os.environ.get("DEFAULT_FUNCTION_NAME", None)
MAX_ERROR_COUNT = int(os.environ.get("MAX_ERROR_COUNT", 20))
ERROR_WINDOW_MINUTES = int(os.environ.get("ERROR_WINDOW_MINUTES", 10))
AWS_REGION = os.environ.get("AWS_REGION", "eu-west-1")

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_lambda_error_count(cloudwatch, function_name=None):
    try:
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
            metric_params["Dimensions"] = [
                {"Name": "FunctionName", "Value": function_name}
            ]
        response = cloudwatch.get_metric_statistics(**metric_params)
        if not response["Datapoints"]:
            return 0
        return int(response["Datapoints"][0]["Sum"])
    except boto3.exceptions.Boto3Error as e:
        logger.error(f"Error fetching CloudWatch metrics: {e}")
        return None


@app.route("/healthz", methods=["GET"])
def health_check():
    cloudwatch = boto3.client("cloudwatch", region_name=AWS_REGION)
    function_name = DEFAULT_FUNCTION_NAME

    error_count = get_lambda_error_count(cloudwatch, function_name)
    if error_count is None:
        logger.error("Error fetching CloudWatch metrics")
        return jsonify({"status": "unhealthy"}), 503

    if error_count > MAX_ERROR_COUNT:
        logger.error(
            f"Error count {error_count} exceeds the limit of {MAX_ERROR_COUNT}"
        )
        return jsonify({"status": "unhealthy"}), 503

    logger.info(f"Error count {error_count} is within the limit of {MAX_ERROR_COUNT}")
    return jsonify({"status": "healthy"}), 200
