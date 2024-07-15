# Binotel Call Record to Google Drive 🌐📞📂

This project is designed for users with a Binotel telephony connection who want to save their call recordings to Google Drive automatically. 

## Project Structure

```
├── api
│ ├── Dockerfile
│ ├── main.py
│ ├── requirements.txt
│ └── utils.py
├── docker-compose.yml
└── nginx
├── nginx.conf
└── sslcerts
```

## Getting Started

Follow these steps to set up and run the project:

### 1. Purchase a Server 💻

Acquire a server from a hosting provider of your choice.

### 2. Purchase a Domain 🌐

Buy a domain name to associate with your server.

### 3. Link Server to Domain 🔗

Point your domain to the server's IP address.

### 4. Generate SSL Certificate using Let's Encrypt 🔐

Install Certbot and generate an SSL certificate for your domain:

```bash
sudo apt install certbot
sudo apt-get install python3-certbot-nginx
sudo certbot certonly --nginx -d <your_domain.com> -d <www.your_domain.com>
```

Move the generated SSL certificates to the /nginx/sslcerts/ directory.

### 5. Update your package list and install Docker:
```bash
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt install docker-ce
```
Then, install Docker Compose:
```bash
sudo apt install docker-compose
```
### 6. Update Domain in Configuration 📄
Edit nginx.conf and replace <your_domain_here> with your domain in the format www.<domain.com>.

### 7. Add Google API Credentials 🔑
Place the JSON file with your Google API credentials into the /api/ directory.

### 8. Update API Keys and Configuration in utils.py 🛠️
Edit the following fields in /api/utils.py:
```python
BINOTEL_API_KEY = "<YOUR_BINOTEL_API_KEY_HERE>" 
BINOTEL_API_SECRET = "<YOUR_BINOTEL_API_SECRET_HERE>"
FOLDER_ID = None # Set up this field if necessary
SERVICE_ACCOUNT_FILE = '<google_key_name>.json' # Set up the name of .json secret key here
TIMEZONE = 'Europe/Kyiv'  # Change timezone if needed
```
### 9. Run Docker Compose 🚀
```bash
docker-compose up -d
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.
