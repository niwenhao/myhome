To retrieve all Maven `groupId`, `artifactId`, and `version` from a Nexus server, you'll need to interact with its REST API.

This script is compatible with **Nexus Repository Manager 3.x**, which exposes a **Search API** that supports pagination.

---

### ✅ Requirements

* Nexus must be accessible over HTTP(S).
* You need credentials if the repository isn't public.
* You must know the repository name you're querying (`maven-releases`, `maven-public`, etc.).

---

### 🔧 Script: `fetch_nexus_maven_artifacts.py`

```python
import requests
import json

NEXUS_URL = "http://your-nexus-server.com"  # Without trailing slash
REPOSITORY = "maven-releases"               # Change to your repo name
USERNAME = "admin"                          # Or leave as None for anonymous access
PASSWORD = "admin123"                       # Or leave as None for anonymous access

OUTPUT_FILE = "maven_artifacts.json"

def fetch_maven_components(nexus_url, repository, username=None, password=None):
    url = f"{nexus_url}/service/rest/v1/search"
    params = {
        "repository": repository,
        "format": "maven2"
    }
    headers = {
        "Accept": "application/json"
    }
    
    all_components = []
    continuation_token = None

    while True:
        if continuation_token:
            params['continuationToken'] = continuation_token

        response = requests.get(url, params=params, headers=headers, auth=(username, password) if username else None)
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            break

        data = response.json()
        for item in data.get('items', []):
            for asset in item.get('assets', []):
                all_components.append({
                    "groupId": item.get("group"),
                    "artifactId": item.get("name"),
                    "version": item.get("version")
                })

        continuation_token = data.get('continuationToken')
        if not continuation_token:
            break

    return all_components

if __name__ == "__main__":
    print("Fetching Maven artifacts from Nexus...")
    artifacts = fetch_maven_components(NEXUS_URL, REPOSITORY, USERNAME, PASSWORD)

    print(f"Found {len(artifacts)} artifacts.")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(artifacts, f, indent=2)

    print(f"Artifacts saved to {OUTPUT_FILE}")
```

---

### 📝 Output

The script writes a list of dictionaries to a JSON file:

```json
[
  {
    "groupId": "org.example",
    "artifactId": "my-lib",
    "version": "1.0.0"
  },
  ...
]
```

---

### 🚀 To Run

```bash
pip install requests
python fetch_nexus_maven_artifacts.py
```

---

Would you like a CSV export instead of JSON?
