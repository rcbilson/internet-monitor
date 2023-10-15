import boto3
import logging

def send(message):
  logging.info(f"notification: {message}")
  client = boto3.client('sns')
  response = client.publish(
      TopicArn='arn:aws:sns:ca-central-1:365935231626:internet-alert',
      Message=message,
      Subject=message
  )
  logging.debug(response)
