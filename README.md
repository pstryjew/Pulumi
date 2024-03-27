# Pulumi
Pulumi - SE/CX Coding Exercise

Please find my code for Option 1
It does not execute completely.

While all the of pieces work correctly outside of my Pulumi code, I can get them to deploy correctly

Bucket - no issues

DynamoDB table - no issues

Lambda task - created with minor issue  (can't get Pulumi to read the .zip file, but it will read the Python version)

Bucket Notification - getting a '400' Error that I can't figure out and hit the timebox (well, went over)

ComonentResource - did not get to this portion

Had a couple other IAM issues with the iam:CreateRole action, to get past that I gave my Pulumi user Admin rights, I didn't have time to figure the correct permission
wanting to move to get the environment operational.

The lambda_function.py file should be located in the ./lambda directory    (I included the .zip downloaded from AWS)
