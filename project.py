import boto3
import sys

session = boto3.Session(profile_name='jbk0418')
ec2 = session.resource('ec2')
ec21 = session.client('ec2')


def list_instances():
    for i in ec2.instances.all():

        print('[id] ', i.id,', [AMI]', i.image_id, ', [type] ', i.instance_type,', [state]', i.state['Name'], ', [monitoring state] ', i.monitoring['State'] )


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


def start_instance():
    id = input()
    response = ec21.start_instances(InstanceIds=[id])
    result = response['StartingInstances']
    print(result[0]['CurrentState']['Name'], result[0]['InstanceId']) #pending 이면 성공
    

def stop_instance():
    id = input()
    response = ec21.stop_instances(InstanceIds=[id])
    result = response['StoppingInstances']
    print(result[0]['CurrentState']['Name'], result[0]['InstanceId']) # stopping 이면 성공

def reboot_instance():
    id = input()
    response = ec21.reboot_instances(InstanceIds=[id])
    result = response['ResponseMetadata']
    print(response)

def create_instance():
    id = input()
    instance = ec2.create_instances(ImageId=id, MaxCount = 1, MinCount = 1, InstanceType = 't2.micro')
    



if __name__ == '__main__':
    # print(sys.argv)

    # print('리스트')
    # list_instances()

    # print('존')
    # available_zone()

    # print('리젼')
    # available_region()
   
    # print('이미지')

    # list_image()
    # print("id 입력:")
    # a= input()
    # start_instance(a)
    # stop_instance(a)
    # reboot_instance(a)
    # create_instance(a)
    a = 0 
    while(a != '99'):
        print('------------------------------------------------------------')
        print('            Amazon AWS Control Panel using SDK')
        print('')
        print('Cloud Computing, Computer Science Department')
        print('                         at Chungbuk National University')
        print('------------------------------------------------------------')
        print('1. list instance                2. available zones ')
        print('3. start instance               4. available regions ')
        print('5. stop instance                6. create instance ')
        print('7. reboot instance              8. list images ')
        print('                               99. quit ')
        a = input('Enter an integer: ')

        if a=='1':
            list_instances()
        elif a=='2':
            available_zone()
        elif a=='3':
            start_instance()
        elif a=='4':
            available_region()
        elif a=='5':
            stop_instance()
        elif a=='6':
            create_instance()
        elif a=='7':
            reboot_instance()
        elif a=='8':
            list_image()

    



    