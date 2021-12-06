import boto3
import sys

import datetime

# session = boto3.Session(profile_name='jbk0418')
# ec2 = session.resource('ec2')
# ec21 = session.client('ec2')
ec2 = boto3.resource('ec2')
ec21 = boto3.client('ec2')
ssm_client = boto3.client('ssm')
cloud_client = boto3.client('cloudwatch')



def list_instances():
    print('Listining instance ...')
    for i in ec2.instances.all():

        print('[id] ', i.id,', [AMI]', i.image_id, ', [type] ', i.instance_type,', [state]', i.state['Name'], ', [monitoring state] ', i.monitoring['State'] )


def available_zone():
    response = ec21.describe_availability_zones()
    
    result = response['AvailabilityZones']
    print('available zone ...')
    for i in result:
        print('[id] ',i['ZoneId'],', [region] ', i['RegionName'],', [zone]', i['ZoneName'])
    print('You have access to ', len(result), 'Availability zones' )

def available_region():
    print('available region ...')
    response = ec21.describe_regions()

    result = response['Regions']

    for i in result:
        print(i['RegionName'],  i['Endpoint'])


def list_image():

    images = ec21.describe_images(Owners=['self'])
    image_list = images['Images']
    print('Listining image ...')
    for i in image_list:
        print('[ImageID] ', i['ImageId'],', [Name] ', i['Name'],', [Owner] ', i['OwnerId'])


def start_instance():
    id = input('Enter instance id :')
    print('Starting .... ', id)
    response = ec21.start_instances(InstanceIds=[id])
    result = response['StartingInstances']
    # print(result[0]['CurrentState']['Name'], result[0]['InstanceId']) #pending 이면 성공
    if result[0]['CurrentState']['Name'] == 'pending':
        print('Successfully started instance ', id)
    

def stop_instance():
    id = input('Enter instance id : ')
    print('Stopping .... ', id)
    response = ec21.stop_instances(InstanceIds=[id])
    result = response['StoppingInstances']
    # print(result[0]['CurrentState']['Name'], result[0]['InstanceId']) # stopping 이면 성공
    if result[0]['CurrentState']['Name'] == 'stopping':
        print('Successfully stopped instance ', id)

def reboot_instance():
    id = input('Enter instance id : ')
    print('Rebooting .... ', id)
    response = ec21.reboot_instances(InstanceIds=[id])
    result = response['ResponseMetadata']
    

def create_instance():
    id = input('Enter image id : ')
    instance = ec2.create_instances(ImageId=id, MaxCount = 1, MinCount = 1, InstanceType = 't2.micro', KeyName = 'cloud-project', SecurityGroups = ['htcondor-security'])
    print('Successfully started EC2 instance ',instance[0].instance_id,' based on', id)

def terminate_instance():
    id = input('Enter instance id : ')
    print('Are you sure to terminate', id, '?')
    ask = input('y/n  ')
    if  ask == 'y':
        instance = ec21.terminate_instances(InstanceIds =[id])

        if instance['TerminatingInstances'][0]['CurrentState']['Name'] == 'shutting-down':
            print('Successfully terminate instance ', id)
        

def CPU_Usage():
    now = datetime.datetime.now()
    today = str(now)
    today = today.split(' ')[0]
    yesterday = str(now + datetime.timedelta(days=-1))
    yesterday = yesterday.split(' ')[0]
    id = input('Enter instance id : ')
    cpu_limit = 100 #100미만
    response = cloud_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                'Name': 'InstanceId',
                'Value': id
                },
            ],
            StartTime=yesterday ,
            EndTime=today,
            Period=86400,    #24시간 (
            Statistics=['Minimum','Maximum','Average'], 
            Unit='Percent'
            )
    for cpu in response['Datapoints']:
        if 'Average' in cpu:
            result = 'CPU-Usage'+'/'+str(cpu['Average'])+'/'+str(cpu['Timestamp'])[0:16]+'/'+str(cpu['Minimum'])+'/'+str(cpu['Maximum'])
            metric_type = result.split('/')[0]
            cpu_persent = result.split('/')[1]
            timestamp = result.split('/')[2]
            cpu_min = result.split('/')[3]
            cpu_max = result.split('/')[4]
            print('[Timestamp] ',timestamp , ', [Average] ', cpu_persent, ', [cpu-max] ', cpu_max, ', [cpu-min] ', cpu_min)


if __name__ == '__main__':
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
        print('9. cpu usage                   10. terminate instance')
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
        elif a=='9':
            CPU_Usage()
        elif a=='10':
            terminate_instance()
   


    



    