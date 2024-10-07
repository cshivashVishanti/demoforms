# demoforms
Forms used for demo written in HTML with python backend

## Folder structure:
```
├── README.md
├── api.py
├── app.py
├── config
│   └── variables.py
├── requirements.txt
├── static
│   ├── css
│   │   └── style.css
│   └── images
│       └── cloudLogo.png
└── templates
    ├── podsForm.html
    ├── site2siteVPNAdd.j2
    ├── vmForm.html
    ├── vmK8sDebian.j2
    ├── vmK8sLinux.j2
    ├── vmK8sWin.j2
    ├── vpcForm.html
    ├── vpcK8s.j2
    └── vpn.html


```

## Install requirements
```
pip3 install -r requirements.txt
```

## SONiC API Server
Change SONiC API server details in `config/variables.py` file

## Run the Flask app
```
python3 app.py
```

## URL
Open below URL in your browser
```
https://<ip>:5500/vpc  --> VPC Creation
https://<ip>:5500/vm  --> VM Creation
https://<ip>:5500/pod --> POD Creation
https://<ip>:5500/vpn --> Site to Site VPN Creation/Deletion
```
