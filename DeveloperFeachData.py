import requests
import json
import uuid
import os
API_TOKEN = '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' #change the API token


base_repo_url = "https://api.github.com/repos/lodash/lodash/pulls" #change the repo link
headers = {
    'Authorization': API_TOKEN
}

def transform_pr_data(raw_pr):
    transformed_pr = {
        "pr_id": str(uuid.uuid4()),
        "repo_name": f"{raw_pr['base']['repo']['owner']['login']}/{raw_pr['base']['repo']['name']}",
        "pr_number": raw_pr['number'],
        "title": raw_pr['title'],
        "state": raw_pr['state'],
        "author": {
            "username": raw_pr['user']['login'],
            "id": raw_pr['user']['id'],
            "profile_url": raw_pr['user']['html_url']
        },
        "created_at": raw_pr['created_at'],
        "updated_at": raw_pr['updated_at'],
        "merged_at": raw_pr.get('merged_at'),
        "merged_by": {
            "username": raw_pr['merged_by']['login'] if raw_pr.get('merged_by') else None,
            "id": raw_pr['merged_by']['id'] if raw_pr.get('merged_by') else None,
            "profile_url": raw_pr['merged_by']['html_url'] if raw_pr.get('merged_by') else None
        } if raw_pr.get('merged_by') else None,
        "description": raw_pr['body'] or "",
        "labels": [label['name'] for label in raw_pr.get('labels', [])],
        "comments_count": raw_pr.get('comments', 0),
        "review_comments_count": raw_pr.get('review_comments', 0),
        "commits_count": raw_pr.get('commits', 0),
        "additions": raw_pr.get('additions', 0),
        "deletions": raw_pr.get('deletions', 0),
        "changed_files_count": raw_pr.get('changed_files', 0),
        "changed_files": [],
        "diff_url": raw_pr['diff_url'],
        "patch_url": raw_pr['patch_url'],
        "language_stats": {},
        "is_draft": raw_pr.get('draft', False)
    }
    return transformed_pr

def get_pr_files(pr_number):
    files_url = f"https://api.github.com/repos/lodash/lodash/pulls/{pr_number}/files" #change the repo link
    try:
        response = requests.get(files_url, headers=headers)
        if response.status_code == 200:
            files_data = response.json()
            return [
                {
                    "filename": file_info['filename'],
                    "status": file_info['status'],
                    "additions": file_info['additions'],
                    "deletions": file_info['deletions']
                }
                for file_info in files_data
            ]
    except Exception as e:
        print(f"Error fetching files for PR {pr_number}: {e}")
    return []

def fetch_all_prs_by_state(state='all', per_page=100):
    all_prs = []
    page = 1
    
    while True:
        params = {
            'state': state,
            'per_page': per_page,
            'page': page,
            'sort': 'updated',
            'direction': 'desc'
        }
        
        if page % 5 == 1:
            print(f"Fetching page {page}...")
        
        response = requests.get(base_repo_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error on page {page}: Status {response.status_code}")
            break
            
        page_prs = response.json()
        if not page_prs:
            break
            
        all_prs.extend(page_prs)
        
        import time
        time.sleep(0.3)
        page += 1
        
        if page > 100:
            print("Reached page limit")
            break
    
    return all_prs



print("Collecting PR data...")
all_raw_pr_data = fetch_all_prs_by_state(state='all')

states_count = {}
merged_count = 0
for pr in all_raw_pr_data:
    state = pr['state']
    states_count[state] = states_count.get(state, 0) + 1
    if pr.get('merged_at'):
        merged_count += 1

print(f"Collected {len(all_raw_pr_data)} PRs")
print(f"Open: {states_count.get('open', 0)}, Closed: {states_count.get('closed', 0)}, Merged: {merged_count}")


print("Processing data...")
transformed_prs = []
for i, raw_pr in enumerate(all_raw_pr_data):
    transformed_pr = transform_pr_data(raw_pr)
    transformed_prs.append(transformed_pr)

# Create the output directory if it doesn't exist
output_dir = os.path.join("PR data for Developers")
os.makedirs(output_dir, exist_ok=True)

output_filename = os.path.join(output_dir, 'lodash_all_pr_data.json')
with open(output_filename, 'w') as json_file:
    json.dump(transformed_prs, json_file, indent=2)

print(f"Saved {len(transformed_prs)} PRs to {output_filename}")
print("Done!")