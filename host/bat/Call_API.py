import requests,json

project = 'esoteric-kiln-376000'
### us-west4-b(Las Vegas)|asia-northeast1-b(Tokyo)|asia-east2-a(Hong Kong)
zone = 'asia-east2-a'
instance_name='frompythonapi'

### Use 'gcloud auth print-access-token' command to get access token
### https://cloud.google.com/docs/authentication/rest
token='ya29.a0AVvZVsoXp1Ifk7D8CqViL97huGI4daIlodW3eckk6ED0xWhnBEvxHAUxzxOXLUM_WOpJxioe_Mp4Lbb8iYfnwXfAOdsMEouDZ6mJcePiHsHbkJNT7MwfkLC8-CWLvMqBidThAovPzhceXdnwRf3an7QRaJ8QPrr1YDMldAaCgYKAT0SARMSFQGbdwaIoMA3FTYQwB1_SdWDuD1haA0173'

### Passing a Linux startup script directly to an existing VM 
### https://cloud.google.com/compute/docs/instances/startup-scripts/linux#passing-directly
### Step 1: Get fingerprint
url=f'https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances/{instance_name}'
response=requests.get(url,headers={"Authorization":f"Bearer {token}"})
dict=json.loads(response.text)
fingerprint=dict['tags']['fingerprint']
### Step 2: Pass the startup script by using the fingerprint value
url=f'https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances/{instance_name}/setMetadata'
body=f'''
{{
  "fingerprint": "{fingerprint}",
  "items": [
    {{
      "key": "startup-script",
      "value": "#! /bin/bash\napt update\napt -y install apache2\ncat <<EOF > /var/www/html/index.html\n<html><body><p>Linux startup script added directly.</p></body></html>\nEOF"
    }}
  ],
}}
'''
print(body)
response=requests.post(url,data=body,headers={"Authorization":f"Bearer {token}"})
print(response.text)
print('done')