import boto3
s3_resource = boto3.resource('s3')


bucket_name = 'accredited-online-colleges-in-us'
bucket_response = s3_resource.create_bucket(
       Bucket=bucket_name,
    )
print(bucket_response)

s3_resource.Object(bucket_name, 'school_data.json').upload_file(
    Filename = 'school_data.json'
)