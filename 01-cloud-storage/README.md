# GCP Hands-On:

## Hands-on experience \+ documentation of core GCP features 

# Buckets:

## Pre-Requisite Steps:

![][image1]  
![][image2]  
I’ve created a new project named GCP Hands On  
![][image3]  
The Portfolio project is still ticked because I was navigating from that project’s root. I’ll navigate to the newly created project. Now as you can see we’re in the GCP Hands On project.   
![][image4]

## Bucket Creation:

Now I’ll head over to the buckets section in the navbar and create a bucket. This helps me store data in buckets in cloud storage.  
![][image5]  
Choose the location nearest to you and is stable/available:

*Note: I’ve chosen Singapore although Mumbai is closer to me because of availability issues in the Indian, Middle East, and European servers. Eastern Asia (Tokyo, Seoul, etc.) have a longer RTT, so among the stable options I have, Singapore is the closest geographically.* 

![][image6]

## Data Upload & File Organization:

I’ve successfully uploaded an image of a kitten, named kitten.png using the upload button.   
![][image7]  
![][image8]  
Now to move the image into a dedicated folder, I’ll first create a folder using the create folder button, and then click on the three vertical dots next to the kitten.png file and click move, and then browse and select my destination folder and move it.   
*I’ve opened the gsutil equivalent snippet if you’re curious to try this on a terminal.*   
![][image9]  
![][image10]  
![][image11]  
When you make Cloud Storage buckets publicly readable, anyone on the internet can list and view their objects and view their metadata (excluding ACLs). *Don't include sensitive info here*\!

## Access Management:

### GCP Web GUI:

![][image12]

I am trying to grant access to everyone i.e. the public by listing allUsers but as you can see it is throwing an exception, because I had enabled public access prevention while creating this bucket. Since this project is not linked to any organization, the bucket settings page is slightly different as compared to what would’ve been the case otherwise. Hence, the obvious next step is to utilize the terminal that GCP provides built in. 

## GCloud CLI:

![][image13]  
As you can see, allUsers is granted viewing permission regardless of what the GUI tells. The GUI may still show the old issue, this is a normal cache related issue. Below you can see the kitten.png opened using the public link a private tab in a different browser. This means the terminal fix has worked perfectly\!

![][image14]  
Since this hands-on exercise is done, I’ve deleted the folder. Note that these will be in a soft delete state, that is, not permanently deleted until next week.   
But to prevent recurring charges, it is **IMPORTANT** to delete the bucket itself if there’s no more files/folders to be added in this bucket.

## Deletion & Clean-Up:

# Conclusion:

This hands-on exercise served as a deep dive into the practicalities of **Google Cloud Storage (GCS)**, **Identity & Access Management (IAM)**, and the **GCloud CLI**. It moved beyond theoretical knowledge to solve real-world configuration challenges.

#### **Key Takeaways**

* **Cloud Architecture & Latency Optimization:** Strategically selected the `asia-southeast1` (Singapore) region over closer alternatives. This decision was based on a calculated trade-off between physical distance (RTT) and regional infrastructure stability, demonstrating an SRE-mindset toward service availability.  
* **CLI vs. GUI (Source of Truth):** Encountered a critical discrepancy where the GCP Web Console (GUI) enforced "Public Access Prevention" due to stale state/caching. Successfully bypassed this by utilizing the **GCloud CLI** to modify IAM policy bindings directly. This reinforced the principle that the **API is the source of truth** in GCP and other cloud environments.  
* **Security & IAM Governance:** Practiced the principle of public exposure management by navigating the transition from a private, "Enforced" bucket state to a public-serving state using the `allUsers` principal. Gained a clear understanding of how Organization-level policies impact project-level permissions.  
* **Resource Lifecycle Management:** Implemented proactive cleanup by utilizing `gsutil` and console commands to delete objects and buckets. Recognized the implications of **Soft Delete** policies and the importance of resource termination to prevent "cloud bill sprawl."
