# agents.py
import boto3
import time
import logging
from botocore.exceptions import ClientError

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Bedrock client with the specific region
bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')

# Model IDs for different agents
WRITER_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
CRITIC_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

def converse_with_retry(messages, system=None, max_tokens=1000, model_id=WRITER_MODEL_ID, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            request_body = {
                "modelId": model_id,
                "messages": messages,
                "inferenceConfig": {
                    "maxTokens": max_tokens,
                    "temperature": 0.7,
                    "topP": 1,
                }
            }

            if system:
                request_body["system"] = [{"text": system}]

            logger.info(f"Sending request to model: {model_id}")
            response = bedrock.converse(**request_body)
            logger.info("Received response from API")

            return response['output']['message']['content'][0]['text']
        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                wait_time = (2 ** retries) * 0.1
                logger.warning(f"Rate limited. Retrying in {wait_time} seconds.")
                time.sleep(wait_time)
                retries += 1
            else:
                logger.error(f"ClientError: {str(e)}")
                raise
        except Exception as e:
            logger.error(f"Error in converse_with_retry: {str(e)}")
            raise
    raise Exception("Max retries reached")
