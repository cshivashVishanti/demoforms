# demoforms
Forms used for demo written in HTML with python backend

## Folder structure:
```
├── api.py
├── app.py
├── README.md
├── static
│   ├── css
│   │   └── style.css
│   └── images
│       └── cloudLogo.png
└── templates
    ├── podsForm.html
    ├── vmForm.html
    ├── vmK8sDebian.j2
    ├── vmK8sLinux.j2
    ├── vmK8sWin.j2
    ├── vpcForm.html
    └── vpcK8s.j2

```

## Install requirements:
```
pip3 install -r requirements.txt
```

## Run the Flask app
```
python3 app.py
```

## URL
Open below URL in your browser
```
https://<ip>:5500/vm  --> VM Creation
https://<ip>:5500/pod --> POD Creation
```
