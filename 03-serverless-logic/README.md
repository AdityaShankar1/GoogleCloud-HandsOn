# GCP Hands-On:

## Hands-on experience of core Google Cloud features.

# Serverless Low-Code FaaS:

## **Module 1: Initial Setup:**

`$ gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com logging.googleapis.com`

`![][image1]`

`shankaraditya75@cloudshell:~ (gcp-hands-on-490407)$ gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com logging.googleapis.com`

`Operation "operations/acf.p2-130288429366-6a90847b-f16e-4d16-8295-23582cdc5d1a" finished successfully.`

`shankaraditya75@cloudshell:~ (gcp-hands-on-490407)$ gcloud pubsub topics create cloud-func-topic`

`Created topic [projects/gcp-hands-on-490407/topics/cloud-func-topic].`

## **Module 2: Common Errors and Troubleshooting:**

`shankaraditya75@cloudshell:~ (gcp-hands-on-490407)$ gcloud functions deploy hello-pubsub-func \`

  `--runtime=python310 \`

  `--trigger-topic=cloud-func-topic \`

  `--entry-point=hello_pubsub \`

  `--region=asia-southeast1 \`

  `--allow-unauthenticatedgcloud functions deploy hello-pubsub-func \`

  `--runtime=python310 \`

  `--trigger-topic=cloud-func-topic \`

  `--entry-point=hello_pubsub \`

  `--region=asia-southeast1 \`

  `--allow-unauthenticated`

`ERROR: (gcloud.functions.deploy) unrecognized arguments:`

  `--allow-unauthenticatedgcloud (did you mean '--allow-unauthenticated'?)`

  `functions`

  `deploy`

  `hello-pubsub-func`

  `To search the help text of gcloud commands, run:`

  `gcloud help -- SEARCH_TERMS`

`shankaraditya75@cloudshell:~ (gcp-hands-on-490407)$` 

I’ve hit an error\!

**Issue:** It is a mere typo issue caused due to accidentally double pasting.

`shankaraditya75@cloudshell:~ (gcp-hands-on-490407)$ gcloud functions deploy hello-pubsub-func --runtime=python310 --trigger-topic=cloud-func-topic --entry-point=hello_pubsub --region=asia-southeast1 --allow-unauthenticated`  
`As of Cloud SDK 492.0.0 release, new functions will be deployed as 2nd gen functions by default. This is equivalent to currently deploying new with the --gen2 flag. Existing 1st gen functions will not be impacted and will continue to deploy as 1st gen functions.`  
`You can disable this behavior by explicitly specifying the --no-gen2 flag or by setting the functions/gen2 config property to 'off'.`  
`To learn more about the differences between 1st gen and 2nd gen functions, visit:`  
[`https://cloud.google.com/functions/docs/concepts/version-comparison`](https://cloud.google.com/functions/docs/concepts/version-comparison)   
`ERROR: (gcloud.functions.deploy) Invalid value for [--source]: Provided source directory does not have file [main.py] which is required for [python310]. Did you specify the right source?`  
`shankaraditya75@cloudshell:~ (gcp-hands-on-490407)$` 

**Issue:** Nothing major to worry about\! Since I had started in a fresh (empty) directory, it couldn’t find the file it was searching for. 

`shankaraditya75@cloudshell:~ (gcp-hands-on-490407)$ mkdir my-function && cd my-function`  
`shankaraditya75@cloudshell:~/my-function (gcp-hands-on-490407)$ cat <<EOF > main.py`  
`import base64`  
`import functions_framework`

`@functions_framework.cloud_event`  
`def hello_pubsub(cloud_event):`  
    `# Print out the data from Pub/Sub to prove it worked`  
    `if 'message' in cloud_event.data:`  
        `message_data = base64.b64decode(cloud_event.data['message']['data']).decode('utf-8')`  
        `print(f"Cloud Function received: {message_data}")`  
    `else:`  
        `print("No message data found in the event.")`  
`EOF`  
`shankaraditya75@cloudshell:~/my-function (gcp-hands-on-490407)$ echo "functions-framework==3.*" > requirements.txt`  
`shankaraditya75@cloudshell:~/my-function (gcp-hands-on-490407)$ gcloud functions deploy hello-pubsub-func \`  
  `--runtime=python310 \`  
  `--trigger-topic=cloud-func-topic \`  
  `--entry-point=hello_pubsub \`  
  `--region=asia-southeast1 \`  
  `--allow-unauthenticated`

If it asks `“API [run.googleapis.com] not enabled on project [gcp-hands-on-490407]. Would you like to enable and retry (this will take a few minutes)? (y/N)?”` answer y and proceed. 

Here is the clean, professionally formatted content for your documentation. I have removed the specific project numbers and blurred sensitive identifiers while keeping your email prefix intact to maintain "Proof of Work."

---

## **Module 3: Serverless Logic & Event-Driven Architecture**

**Objective:** Deploy a Cloud Function that automatically triggers in response to a Pub/Sub event, demonstrating "Cloud Glue" integration.

### 1\. Environment Setup & API Enablement

To support 2nd Gen Cloud Functions, the following service APIs were enabled:

* `cloudfunctions.googleapis.com`  
* `cloudbuild.googleapis.com`  
* `artifactregistry.googleapis.com`  
* `run.googleapis.com` (Required for 2nd Gen)  
* `eventarc.googleapis.com` (Required for Event Triggers)

### 2\. Infrastructure Troubleshooting: IAM & Build Permissions

During the initial deployment, a **Build Failure (Code 3\)** occurred.

* **The Error:** `Build failed with status: FAILURE. Could not build the function due to a missing permission on the build service account.`  
* **The Root Cause:** In newer GCP projects, the default Cloud Build service account lacks the necessary permissions to impersonate the runtime identity and write to the Artifact Registry.  
* **The Fix:** Used the CLI to bind the necessary IAM roles to the project-specific Cloud Build service account.

Bash  
\# Capturing project number for reusable IAM binding  
PROJECT\_NUMBER=$(gcloud projects describe $(gcloud config get-value project) \--format='value(projectNumber)')

\# Granting "Act As" permission  
gcloud projects add-iam-policy-binding \[PROJECT\_ID\] \\  
  \--member="serviceAccount:${PROJECT\_NUMBER}@cloudbuild.gserviceaccount.com" \\  
  \--role="roles/iam.serviceAccountUser"

\# Granting Registry Writer permission  
gcloud projects add-iam-policy-binding \[PROJECT\_ID\] \\  
  \--member="serviceAccount:${PROJECT\_NUMBER}@cloudbuild.gserviceaccount.com" \\  
  \--role="roles/artifactregistry.writer"

### 3\. Function Deployment

**Runtime:** Python 3.10

**Trigger:** Pub/Sub Topic (`cloud-func-topic`)

**Region:** `asia-southeast1` (Singapore)

**Deployment Command:**

Bash  
gcloud functions deploy hello-pubsub-func \\  
  \--runtime=python310 \\  
  \--trigger-topic=cloud-func-topic \\  
  \--entry-point=hello\_pubsub \\  
  \--region=asia-southeast1 \\  
  \--allow-unauthenticated

### 4\. Execution & Observability (The Proof)

To verify the end-to-end flow, a message was published to the topic, and the function logs were inspected.

* **Publishing Event:** `gcloud pubsub topics publish cloud-func-topic --message="Serverless Trigger Success!"`  
* **Log Inspection:** `gcloud functions logs read hello-pubsub-func --region=asia-southeast1`

**Log Output Snippet:** `Cloud Function received: Serverless Trigger Success!`

### 5\. Deletion & Resource Lifecycle

To ensure no recurring charges and maintain a clean environment:

Bash  
gcloud functions delete hello-pubsub-func \--region=asia-southeast1 \--quiet  
gcloud pubsub topics delete cloud-func-topic

---

## Final Lab Conclusion

This series of hands-on exercises successfully covered the **Core Trifecta of Cloud Engineering**:

1. **Storage & Persistence:** Managing GCS Buckets and public access logic.  
2. **Messaging & Decoupling:** Utilizing Pub/Sub for asynchronous data flow.  
3. **Compute & Automation:** Deploying 2nd Gen Cloud Functions to act as the "connective tissue" of the infrastructure.

**Key Technical Skill Acquired:** Beyond basic deployment, the ability to diagnose and resolve **IAM Permission Errors** via the GCloud CLI which is a critical skill for any SRE or Cloud Developer managing enterprise-level projects.

[image1]: <data:image/png;base64,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>