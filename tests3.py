# from drive.settings import *
from botocore.config import Config
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime, timedelta
import pytz

AWS_ACCESS_KEY_ID = "AKIAVHNKLCXS3CEPE4UU"
AWS_SECRET_ACCESS_KEY = "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"
REGION = "us-east-2"
def generate_presigned_url(bucket_name, object_key, expiration=36000):

    my_config = Config(
        region_name = REGION,#STORAGES['default']["OPTIONS"]["AWS_S3_REGION_NAME"],
        signature_version = 's3v4',
    )

    # expiration_time_utc = datetime.utcnow() + timedelta(hours=expiration_hours)
    # expiration_time_local = expiration_time_utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(local_timezone))
        

    # s3 = boto3.client('s3',
    #                 aws_access_key_id=AWS_ACCESS_KEY_ID,
    #                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    #                 config=my_config,
    #                 )
    s3 = boto3.client('s3', 
                      region_name='us-east-2',
                      aws_access_key_id=AWS_ACCESS_KEY_ID, 
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      config=Config(signature_version='s3v4'),
                      endpoint_url='https://s3.us-east-2.amazonaws.com'
)
    
    try:
        # Generate a presigned URL for the S3 object
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
            # ExpiresIn=int((expiration_time_local - datetime(1970, 1, 1, tzinfo=pytz.timezone(local_timezone))).total_seconds())        
            )
        return presigned_url,s3
    except NoCredentialsError as e:
        print(f"Credentials error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
bucket_name = 'felisdrive'
object_key = 'static/materialize/css/materialize.css'

# Generate a presigned URL for the S3 object
presigned_url,conn = generate_presigned_url(bucket_name, object_key)

# Print the presigned URL
print("Presigned URL:", presigned_url)



# for key in conn.list_objects(Bucket=bucket_name)['Contents']:
#     print(key['Key'])