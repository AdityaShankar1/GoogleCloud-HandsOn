# 🚀 Cloud Automation & Monitoring Lab
**Author:** Aditya Shankar

**Environment:** MacBook Air M4 (Control Node) -> Google Cloud Platform (Managed Node)

## 🛠️ Project Overview
This repository documents my journey in mastering **Ansible**, **Prometheus**, and **Grafana**. 
The goal is to move from manual server management to "Infrastructure as Code" (IaC).

## 🏗️ Phase 1: Infrastructure & Connectivity
In this phase, I provisioned a cloud environment and established a secure connection between my local machine and a GCP instance.

### 1. Provisioning
- **Cloud Provider:** GCP (Google Cloud Platform)
- **Instance:** `e2-micro` (Ubuntu 22.04 LTS)
- **Location:** `asia-south1-a` (Mumbai)
- **Method:** Deployed via `gcloud` CLI for repeatable infrastructure.

### 2. Security & Access
- Generated an **Ed25519 SSH Keypair** on macOS.
- Injected the public key into GCP Project Metadata to allow passwordless (but passphrase-protected) access.
- Configured `ssh-agent` on macOS to manage the key passphrase.

### 3. Verification
Verified connectivity using the Ansible `ping` module:
```bash
ansible all -i inventory.ini -m ping
```
**Result:** Successfully received `"ping": "pong"`.

## 🔍 Troubleshooting (The "Learning" Part)
- **Billing Quotas:** Encountered `FAILED_PRECONDITION` errors due to project limits on student credits. Resolved by auditing and deleting unused projects via a Bash loop.
- **Host Key Verification:** Handled the `Host key verification failed` error by manually verifying the server's SSH fingerprint on the first handshake.

---
*Next Step: Writing the first Playbook to automate software installation.*

## 🛡️ Phase 2.5: Cloud Networking & Firewalls
Even with services running, they were inaccessible due to GCP's "Deny All" ingress policy.

### 1. Firewall Configuration
I used the `gcloud` CLI to open specific "holes" in the network:
- **Port 80:** Allowed HTTP traffic for the Nginx Web Server.
- **Port 9100:** Allowed Prometheus to scrape metrics from the Node Exporter.

### 2. Commands Used:
```bash
gcloud compute firewall-rules create allow-http --allow tcp:80
gcloud compute firewall-rules create allow-node-exporter --allow tcp:9100
```

---
*Next Step: Installing the Prometheus "Brain" to collect these metrics.*

## ✅ Final Project Milestone: Full Stack Integration
The Prometheus-Grafana stack is fully automated and operational.

### 📈 Metrics Visualized:
- **CPU Usage:** Real-time tracking of user/system/iowait cycles.
- **Memory Management:** Visualizing available vs. cached RAM.
- **Disk I/O:** Monitoring read/write throughput on the GCP boot disk.

### 🧪 Final Commands Used:
- `ansible-playbook install-grafana.yml`
- Dashboard ID `1860` imported for Node Exporter visualization.

---
**Project Status:** 🏆 Complete
