from flask import Flask, render_template, request, redirect, url_for, flash
import api
import threading
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

@app.route('/vpc')
def form_vpc():
    return render_template('vpcForm.html')

# Route to handle form submission
@app.route('/submit-vpc', methods=['POST'])
def submit_vpc_form():
    customer_name = request.form.get('customerName')
    vpc_name = request.form.get('vpcName')
    cpu = request.form['cpu']
    ram = request.form['ram']

    storage_in_gb = request.form.get('storageInGb')

    # For now, just print the form data to the console
    print(f"Customer Name: {customer_name}")
    print(f"VM Name: {vpc_name}")
    print(f"CPU:{cpu}, RAM:{ram}")
    print(f"Storage (in GB): {storage_in_gb}")

    json_data = {"customer_name":customer_name,
                 "vpc_name": vpc_name,
                 "cpu": cpu, "ram": ram,
                 "storage":storage_in_gb}

    parsed_data = json.dumps(json_data)

    thread = threading.Thread(target=api.create_vpc, args=(parsed_data,))
    thread.start()

    #Pop up msg
    flash('VPC creation data submitted successfully!!')

    # Here you can save the form data to a database, file, etc.
    return redirect(url_for('form_vpc'))  # Redirect back to the form

# Route to render the form
@app.route('/vm')
def form():
    return render_template('vmForm.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    customer_name = request.form.get('customerName')
    vpc_name = request.form.get('vpcName')
    vm_name = request.form.get('vmName')
    os = request.form.get('os')
    flavour = request.form.get('flavour')

    flavour_option = request.form['flavourOption']

    # Determine if the user selected a pre-defined or custom flavour
    if flavour_option == 'predefined':
        flavour = request.form['flavour']
        cpu = ram = None
    else:
        cpu = request.form['cpu']
        ram = request.form['ram']
        flavour = None


    storage_in_gb = request.form.get('storageInGb')

    # For now, just print the form data to the console
    print(f"Customer Name: {customer_name}")
    print(f"VPC Name: {vpc_name}")
    print(f"VM Name: {vm_name}")
    print(f"OS: {os}")
    print(f"Flavour: {flavour}")
    print(f"CPU:{cpu}, RAM:{ram}")
    print(f"Storage (in GB): {storage_in_gb}")

    json_data = {"customer_name":customer_name, "vpc_name":vpc_name, "vm_name":vm_name,
                 "os":os, "flavour":flavour, "cpu": cpu, "ram": ram,
                 "storage":storage_in_gb}

    parsed_data = json.dumps(json_data)

    thread = threading.Thread(target=api.create_vm, args=(parsed_data,))
    thread.start()

    #Pop up msg
    flash('VM creation data submitted successfully!!')

    # Here you can save the form data to a database, file, etc.
    return redirect(url_for('form'))  # Redirect back to the form

@app.route('/pod')
def pod_creation_form():
    return render_template('podsForm.html')

# Route to handle form submission for /submit-pod
@app.route('/submit-pod', methods=['POST'])
def submit_pod_form():
    customer_name = request.form.get('customerName')
    vpc_name = request.form.get('vpcName')

    manifestInputType = request.form.get('manifestInputType')
    if manifestInputType == 'url':
        manifest_url = request.form.get('manifestUrl')
        manifestYaml = None
    else:
        manifestYaml = request.form.get('yamlContent')
        manifest_url = None

    # Process the form data here (e.g., save to a database)
    print(f"Customer Name: {customer_name}")
    print(f"VPC Name: {vpc_name}")
    print(f"Manifest Type: {manifestInputType}")
    print(f"URL: {manifest_url}")
    print(f"YAML: {manifestYaml}")

    json_data = {"customer_name":customer_name, "vpc_name":vpc_name, "manifestInputType":manifestInputType,
                 "manifest_url":manifest_url, "manifestYaml":manifestYaml }

    parsed_data = json.dumps(json_data)

    thread = threading.Thread(target=api.create_pod, args=(parsed_data,))
    thread.start()

    flash('Pod creation data submitted successfully!!')

    # Redirect back to the form or to another page
    return redirect(url_for('pod_creation_form'))

@app.route('/vpn')
def vpn_form():
    return render_template('vpn.html')

@app.route('/submit-vpn', methods=['POST'])
def submit_vpn_form():
    action = request.form.get('action', 'add')
    
    if action == 'add':
        vpn_name = request.form.get('vpn_name')
        vpn_params = {
            'vpn_name': vpn_name,
            'local_ip': request.form.get('local_ip'),
            'local_subnet': request.form.get('local_subnet'),
            'remote_ip': request.form.get('remote_ip'),
            'remote_subnet': request.form.get('remote_subnet'),
            'auth_method': request.form.get('auth_method'),
            'pre_shared_key': request.form.get('pre_shared_key'),
            'esp_proposal': request.form.get('esp_proposal'),
        }
        flash("VPN configuration added successfully!")
    elif action == 'delete':
        vpn_name = request.form.get('delete_vpn_name')
        vpn_params = {
            'vpn_name': vpn_name,
        }
        flash("VPN configuration deleted successfully!")
    
    parsed_data = json.dumps(vpn_params)

    thread = threading.Thread(target=api.vpn_handler, args=(action, parsed_data,))
    thread.start()
    
    return redirect(url_for('vpn_form'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)
