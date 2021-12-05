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


def list_image():

    images = ec21.describe_images(Owners=['self'])
    image_list = images['Images']

    for i in image_list:
        print(i['ImageId'], i['Name'], i['OwnerId'])


def start_instance(id):
    response = ec21.start_instances(InstanceIds=[id])
    result = response['StartingInstances']
    print(result[0]['CurrentState']['Name'], result[0]['InstanceId']) #pending 이면 성공
    

def stop_instance(id):
    response = ec21.stop_instances(InstanceIds=[id])
    result = response['StoppingInstances']
    print(result[0]['CurrentState']['Name'], result[0]['InstanceId']) # stopping 이면 성공

def reboot_instance(id):
    response = ec21.reboot_instances(InstanceIds=[id])
    result = response['ResponseMetadata']
    print(response)

if __name__ == '__main__':
    print(sys.argv)

    print('리스트')
    list_instances()

    print('존')
    available_zone()

    print('리젼')
    available_region()
   
    print('이미지')

    list_image()
    print("id 입력:")
    a= input()
    # start_instance(a)
    # stop_instance(a)
    # reboot_instance(a)



    



    