import boto3
import os

client = boto3.client('lightsail')
def lambda_handler(event, context):
    
    try:
        #Grab environmental variables
        myInstanceSnapshotName = os.environ['INSTANCE_SNAPSHOT_NAME']
        zoneToDeploy = os.environ['ZONE_TO_DEPLOY']
        
        snapshot = client.get_instance_snapshot(
            instanceSnapshotName = myInstanceSnapshotName
        )['instanceSnapshot']
        
        snapshotName = snapshot['name']
        
        result = client.create_instances_from_snapshot(
            instanceSnapshotName = myInstanceSnapshotName,
            availabilityZone = zoneToDeploy,
            instanceNames = createNewInstanceNames(snapshotName),
            bundleId = snapshot["fromBundleId"]
        )
        
        return "Success in creating: " + os.environ['NUMBER_TO_DEPLOY'] + " instances!"
    except Exception as e:
        return (str(e))
    

#Create unique ID's for the new instance names
def createNewInstanceNames(baseName):
    numToDeploy = int(os.environ['NUMBER_TO_DEPLOY']) + 1
    newInstanceNames = []
    for currInstance in range(1,numToDeploy):
        newInstanceNames.append(baseName + '_' + str(currInstance))
    return newInstanceNames
