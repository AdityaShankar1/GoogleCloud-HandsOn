# Google Cloud Platform: Core Foundations Lab

A comprehensive, hands-on repository documenting the deployment, security, and observability of a modern cloud ecosystem on GCP. This project emphasizes a **CLI-first** approach and **SRE (Site Reliability Engineering)** mindset.

## 🚀 Project Overview
This repository serves as a technical log of core GCP services integrated to form a functional, event-driven infrastructure. Each module includes deployment logs, troubleshooting steps, and architectural insights.

## 📁 Repository Structure

- **[01-cloud-storage](./01-cloud-storage):** Object storage management, GCS bucket policies, and public access configurations.
- **[02-event-driven-pubsub](./02-event-driven-pubsub):** Asynchronous messaging and decoupling using Pub/Sub topics and subscriptions.
- **[03-serverless-logic](./03-serverless-logic):** Deploying 2nd Gen Cloud Functions (Python) triggered by infrastructure events.
- **[04-observability](./04-observability):** Proactive health monitoring via Uptime Checks and Cloud Monitoring API integration.

## 🛠️ Key Technical Skills Demonstrated

- **Infrastructure as Code (Thinking):** Moving from manual console clicks to reproducible CLI and REST API calls.
- **Identity & Access Management (IAM):** Resolving 2nd Gen Cloud Build permission bottlenecks (iam.serviceAccountUser and artifactregistry.writer).
- **Observability:** Setting up global uptime monitors to ensure high availability.
- **Troubleshooting:** Navigating CLI version discrepancies and API-level constraints through direct RESTful interaction (cURL).

---
*Created as part of the 2026 Cloud Engineering Foundations track.*
