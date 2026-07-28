# Vector Database Overview: Chroma vs. Pinecone

| Feature / Criteria | Chroma (Local) | Pinecone (Cloud) |
| :--- | :--- | :--- |
| **Local vs. Cloud** | Embedded / Local (runs directly inside the Python process on your local disk). | Fully Managed Cloud Service (hosted on cloud providers like AWS/GCP). |
| **Free-Tier Limits** | 100% free, open-source, and unlimited (constrained only by local computer hardware and disk space). | Starter Free Tier with limits (1 index, 2GB storage, 1M read units/month, auto-sleep on inactivity). |
| **Latency** | Ultra-low latency (< 10 ms) because vector lookups happen locally in memory/disk with zero network calls. | Low latency (~20–50 ms) depending on cloud region, internet speed, and API network roundtrips. |
| **Ease of Setup** | Extremely easy (`pip install chromadb` and 3 lines of Python code, no API keys or cloud accounts needed). | Easy to moderate (requires web dashboard signup, API key management, and cloud index configuration). |
| **Enterprise Access Control (Per-Member / Per-Plan)** | Handled at the application layer by filtering queries using metadata tags (e.g., `where={"plan_type": "gold"}`) or spinning up isolated local database instances per client. | Handled natively via cloud metadata filters (e.g., `filter={"member_id": "123"}`) or isolated cloud Namespaces/Indexes with role-based access control (RBAC). |

---

## Decision & Reasoning for Cohort Program

For this project, we choose **Chroma** as our primary vector database. Chroma is lightweight, 100% free, and runs entirely on local hardware without requiring third-party cloud API keys, credit cards, or external network connectivity. This eliminates rate limits and authentication headaches during development, allowing us to rapidly prototype our Retrieval-Augmented Generation (RAG) system offline before scaling to a cloud solution like Pinecone.
## Vector DB Selection & Reasoning

For this program, we choose **Chroma** as our primary vector database. Chroma is lightweight, 100% free, and runs locally on hardware without requiring external cloud accounts, credit cards, or API rate limits. Because it runs embedded directly within Python, it eliminates network latency and authentication complexity, allowing us to rapidly prototype and test our Retrieval-Augmented Generation (RAG) system offline before scaling to a cloud solution like Pinecone.