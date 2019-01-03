import botocore
import boto3

from botocore.exceptions import ClientError

def lambda_handler(event, context):

    rds = boto3.client('rds')
    lambdaFunc = boto3.client('lambda')
    print('Trying to get Environment variable')

    def rds_start(instance):
        try:
            response = rds.start_db_instance(DBInstanceIdentifier=instance)
            print('Start RDS instance :: ' + instance)
            return response
        except ClientError as e:
            print(e)
            
    try:
        funcResponse = lambdaFunc.get_function_configuration(FunctionName='RDSInstanceStop')
        rdsInstances = funcResponse['Environment']['Variables']['DBInstanceName']
        print('Starting RDS service for DBInstances : ' + rdsInstances)

        for instance in rdsInstances.split(","):
            rds_start(instance)
    except ClientError as e:
        print(e)
    return {
        'message' : "Script execution completed. See Cloudwatch logs for complete output"
    }
