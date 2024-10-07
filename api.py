import json
import os
from jinja2 import Environment, FileSystemLoader
import yaml
import requests

import config.variables as configVar

def get_flavour_data(flavour):
    if flavour == "mini" :
        return 1, 2
    elif flavour == "medium" :
        return 2, 4
    elif flavour == "large" :
        return 2, 8
    elif flavour == "xlarge" :
        return 4,16


def create_vm(data):
    print(f"<create_vm>: Received data : {data}")
    context = json.loads(data)
    print("<create_vm>: Customer Name ", context["customer_name"])
    context["vpc_name"] = context["vpc_name"].lower()
    context["vm_name"] = context["vm_name"].lower()
    context["data_volume_name"] = context["vpc_name"]+context["vm_name"]

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    # Load the template

    if context["os"] == "windows" :
        template = env.get_template('vmK8sWin.j2')
    elif context["os"] == "ubuntu2204" :
        context["url"] = "https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img"
        template = env.get_template('vmK8sLinux.j2')
    else :
        context["url"] = "https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-amd64.qcow2"
        template = env.get_template('vmK8sLinux.j2')

    if context["flavour"] != None:
        context["cpu"], context["ram"] = get_flavour_data(context["flavour"])

    context["ram"] = str(context["ram"])+"G"
    context["storage"] = str(context["storage"])+"Gi"
    print(context)

    # Render the template with context
    config_content = template.render(context)

    fileName = '/tmp/orch_vm_creation.yaml'
    with open(fileName, 'w+') as config_file:
        config_file.write(config_content)

    os.system(f"kubectl apply -f {fileName}")


def create_vpc(data):
    context = json.loads(data)
    print(f"<create_vpc>: Received data : {data}")
    print("<create_vpc>: Customer Name: ", context["customer_name"])
    context["pvClaims"] = 5
    context["vpc_name"] = context["vpc_name"].lower()
    context["customer_name"] = context["customer_name"].lower()

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    # Load the template
    template = env.get_template('vpcK8s.j2')
    # Render the template with context
    config_content = template.render(context)

    fileName = '/tmp/orch_vpc_creation.yaml'
    with open(fileName, 'w+') as config_file:
        config_file.write(config_content)

    os.system(f"kubectl apply -f {fileName}")



def create_pod(data):
    print(f"<create_pod>: Received data : {data}")
    json_data = json.loads(data)
    print("<create_pod>: Customer Name ", json_data["customer_name"])

    fileName = "/tmp/orch_pod_creation.yaml"
    if json_data["manifestInputType"] == "yaml" :
        yaml_data = yaml.safe_load_all(json_data["manifestYaml"])
        with open(fileName, 'w+') as yamlfile:
            for doc in yaml_data:
                yaml.dump(doc, yamlfile)
                fileSeperator = '---\n'
                yamlfile.write(fileSeperator)

        os.system(f"kubectl apply -f {fileName}")
    else:
        os.system(f"kubectl apply -f {json_data['manifest_url']}")


def vpn_handler(action, data):
    print(f"<vpn_handler>: Received data : {data}")
    json_data = json.loads(data)
    print("<vpn_handler>: action ", action)
    print("<vpn_handler>: vpn_name ", json_data["vpn_name"])
    
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    # Load the template
    if action == "add":
        print("<vpn_handler>: local_ip ", json_data["local_ip"])
        template = env.get_template('site2siteVPNAdd.j2')
        
    sonic_device = configVar.sonic_ip + ':' + configVar.sonic_port
    
    api_url = configVar.sonic_ipsec_url.replace("%%sonic_device%%", sonic_device)
    print(api_url)


    if action == "add":
        config_context = template.render(json_data)
        data = json.loads(config_context.replace("\'","\""))
        print(data)
        
        # os.system(f"curl -k -X PATCH {config_content}")
        response = requests.patch(api_url, json=data, verify=False)

    else:
        # os.system(f"curl -k -X DELETE {config_content}")
        api_url = api_url+ "=" +json_data["vpn_name"]
        print(api_url)
        response = requests.delete(api_url, verify=False)

    print(response.json())
    
    
