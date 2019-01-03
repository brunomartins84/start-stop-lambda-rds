import botocore
import boto3

from botocore.exceptions import ClientError

def lambda_handler(event, context):

    rds = boto3.client('rds')
    lambdaFunc = boto3.client('lambda')
    print('Trying to get Environment variable')

    def rds_stop(instance):
        try:
            response = rds.stop_db_instance(DBInstanceIdentifier=instance)
            print('Stop RDS instance :: ' + instance)
            return response
        except ClientError as e:
            print(e)
            
    try:
        funcResponse = lambdaFunc.get_function_configuration(FunctionName='RDSInstanceStop')
        rdsInstances = funcResponse['Environment']['Variables']['DBInstanceName']
        print('Stopping RDS service for DBInstances : ' + rdsInstances)

        for instance in rdsInstances.split(","):
            rds_stop(instance)
    except ClientError as e:
        print(e)
    return {
        'message' : "Script execution completed. See Cloudwatch logs for complete output"
    }
