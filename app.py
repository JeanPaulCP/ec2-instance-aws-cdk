from aws_cdk import App, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from constructs import Construct

class EC2Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear VPC (Virtual Private Cloud)
        vpc = ec2.Vpc(self, "MyVpc", max_azs=3) 

        # Crear un Security Group para la instancia EC2
        security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                           vpc=vpc,
                                           description="Allow SSH and HTTP access",
                                           allow_all_outbound=True)
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH access")  # puerto 22 (SSH)
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP access")  # puerto 80 (HTTP)

        # Definir el tipo de instancia (puedes ajustarlo según tus necesidades)
        instance_type = ec2.InstanceType("t2.micro")  

        # Usar la AMI de Cloud9ubuntu22 
        machine_image = ec2.MachineImage.generic_linux({
            "us-east-1": "ami-022ce79dc9cabea0c"  
        })
       # Crear la instancia EC2
        instance = ec2.Instance(self, "MyInstance",
        instance_type=instance_type, machine_image=machine_image,
        device_name="/dev/sda1", volume=ec2.BlockDeviceVolume.ebs(20), 
        role=iam.Role(self, "LabRole",
        assumed_by=iam.ArnPrincipal("arn:aws:iam::478701513931:role/LabRole")))  # ARN del rol LabRole

app = App()
app.synth(p, "EC2Stack")
