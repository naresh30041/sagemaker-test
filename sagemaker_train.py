import boto3
import time

def trigger_training_job():
    # Set up the SageMaker client
    sagemaker_client = boto3.client('sagemaker', region_name='us-east-1')

    # Generate a unique training job name based on the current timestamp
    job_name = f"sagemaker-training-job-{int(time.time())}"

    # Define the training job parameters
    training_params = {
        "TrainingJobName": job_name,
        "AlgorithmSpecification": {
            "TrainingImage": "763104351884.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest",  # Example: XGBoost container
            "TrainingInputMode": "File",
        },
        "RoleArn": "arn:aws:iam::506236563550:role/SageMakerExecutionRole",  # Replace with your role ARN
        "InputDataConfig": [
            {
                "ChannelName": "train",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": "s3://sagemaker-artifacts-sample/data/",  # Replace with your S3 input path
                        "S3DataDistributionType": "FullyReplicated"
                    }
                },
                "ContentType": "text/csv"
            }
        ],
        "OutputDataConfig": {
            "S3OutputPath": "s3://sagemaker-artifacts-sample/model/"  # Replace with your S3 output path
        },
        "ResourceConfig": {
            "InstanceType": "ml.m5.large",  # Choose the instance type
            "InstanceCount": 1,
            "VolumeSizeInGB": 10
        },
        "StoppingCondition": {
            "MaxRuntimeInSeconds": 3600  # 1 hour
        }
    }

    # Start the training job
    response = sagemaker_client.create_training_job(**training_params)

    # Output the response for logging purposes
    print(f"Training job {job_name} started. Response: {response}")

# Execute the function to trigger the training job
if __name__ == "__main__":
    trigger_training_job()
