"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

# Create an S3 bucket
bucket = aws.s3.Bucket("pulumi-bucket-pete")

# Create AWS Dynamo table

basic_dynamodb_table = aws.dynamodb.Table("basic-dynamodb-table",
    name="Pulumi_Objects",
    billing_mode="PROVISIONED",
    read_capacity=2,
    write_capacity=2,
    hash_key="ObjectKey",
    attributes=[
        aws.dynamodb.TableAttributeArgs(
            name="ObjectKey",
            type="S",
        ),
    ],
    ttl=aws.dynamodb.TableTtlArgs(
        attribute_name="TimeToExist",
        enabled=False,
    ),
    tags={
        "Name": "dynamodb-table-pulumi",
        "Environment": "dev",
    })



# Create an IAM role for the Lambda function
lambda_role = aws.iam.Role("lambdaRole",
    assume_role_policy={
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
        }]
    })

# Attach the AWSLambdaExecute policy to the role
lambda_policy_attachment = aws.iam.RolePolicyAttachment("lambdaPolicyAttachment",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/AWSLambdaExecute"
)

# Create the Lambda function
# reading zip file not working so have .py file
lambda_function = aws.lambda_.Function("S3toDyna",
    code=pulumi.FileArchive("./lambda"),
    handler="index.handler",
    role=lambda_role.arn,
    runtime="python3.10",
)


# Grant the Lambda permission to access the S3 bucket
lambda_permission = aws.lambda_.Permission("lambdaPermission",
    action="lambda:InvokeFunction",
    function=lambda_function,
    principal="s3.amazonaws.com",
    source_arn=bucket.arn,
)

# Set the S3 bucket notification to trigger the Lambda function
# Getting 400 error, but roles/permissions look good
bucket_notification = aws.s3.BucketNotification("bucketNotification",
    bucket=bucket.id,
    lambda_functions=[aws.s3.BucketNotificationLambdaFunctionArgs(
        lambda_function_arn=lambda_function.arn,
        events=["s3:ObjectCreated:*"],
    )]
)

# Export the names and ARNs of created resources
pulumi.export("bucket_name", bucket.id)
pulumi.export("lambda_function_name", lambda_function.name)
pulumi.export("lambda_role_name", lambda_role.name)
pulumi.export("lambda_role_arn", lambda_role.arn)
