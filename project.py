import boto3
import sys

session = boto3.Session(profile_name='jbk0418')
ec2 = session.resource('ec2')
ec21 = session.client('ec2')


def list_instances():
    for i in ec2.instances.all():

        print(i.id, i.state['Name'], i.instance_type, i.monitoring['State'], i.image_id)


def available_zone():
    response = ec21.describe_availability_zones()
    
    result = response['AvailabilityZones']

    for i in result:
        print(i['ZoneId'] , i['RegionName'] , i['ZoneName'])

def available_region():
    response = ec21.describe_regions()

    result = response['Regions']

    for i in result:
        print(i['RegionName'],  i['Endpoint'])

if __name__ == '__main__':
    print(sys.argv)

    print('리스트')
    list_instances()

    print('존')
    available_zone()

    print('리젼')
    available_region()




    