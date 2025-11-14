import json
import os
import time
import urllib.request
import urllib.parse
import uuid
from collections import defaultdict
from datetime import datetime

API_TOKEN = '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'  # Using public API access
REPO_OWNER = 'moment'  
REPO_NAME = 'moment'     
MAX_PRS_TO_FETCH = 500  # Collect all available PR data     

def make_github_request(url):
    """Make a request to GitHub API using urllib"""
    req = urllib.request.Request(url)
    if API_TOKEN:
        req.add_header('Authorization', f'Bearer {API_TOKEN}')
    req.add_header('User-Agent', 'ReviewerDataCollector/1.0')
    req.add_header('Accept', 'application/vnd.github+json')
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error making request to {url}: {e}")
        return None

def get_pr_reviews(pr_number):
    """Get all reviews for a specific PR"""
    reviews_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/reviews"
    reviews_data = make_github_request(reviews_url)
    
    if not reviews_data:
        return []
    
    reviews = []
    for review in reviews_data:
        # Skip reviews where user data is None (deleted/suspended accounts)
        if review.get('user') is None:
            print(f"    Skipping review {review['id']} - user account unavailable")
            continue
            
        review_info = {
            "review_id": review['id'],
            "reviewer_username": review['user']['login'],
            "reviewer_id": review['user']['id'],
            "reviewer_profile_url": review['user']['html_url'],
            "reviewer_avatar_url": review['user']['avatar_url'],
            "reviewer_type": review['user']['type'], 
            "state": review['state'],  
            "body": review.get('body', ''),
            "submitted_at": review['submitted_at'],
            "commit_id": review.get('commit_id', ''),
            "html_url": review.get('html_url', ''),
            "author_association": review.get('author_association', '')  
        }
        reviews.append(review_info)
    
    return reviews

def get_pr_review_comments(pr_number):
    """Get all review comments (line-by-line comments) for a specific PR"""
    comments_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/comments"
    comments_data = make_github_request(comments_url)
    
    if not comments_data:
        return []
    
    comments = []
    for comment in comments_data:
        # Skip comments where user data is None (deleted/suspended accounts)
        if comment.get('user') is None:
            print(f"    Skipping review comment {comment['id']} - user account unavailable")
            continue
            
        comment_info = {
            "comment_id": comment['id'],
            "reviewer_username": comment['user']['login'],
            "reviewer_id": comment['user']['id'],
            "reviewer_profile_url": comment['user']['html_url'],
            "body": comment.get('body', ''),
            "created_at": comment['created_at'],
            "updated_at": comment['updated_at'],
            "path": comment.get('path', ''),
            "line": comment.get('line'),
            "diff_hunk": comment.get('diff_hunk', ''),
            "html_url": comment.get('html_url', ''),
            "author_association": comment.get('author_association', ''),
            "in_reply_to_id": comment.get('in_reply_to_id')
        }
        comments.append(comment_info)
    
    return comments

def get_pr_general_comments(pr_number):
    """Get general discussion comments on the PR"""
    comments_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments"
    comments_data = make_github_request(comments_url)
    
    if not comments_data:
        return []
    
    comments = []
    for comment in comments_data:
        # Skip comments where user data is None (deleted/suspended accounts)
        if comment.get('user') is None:
            print(f"    Skipping general comment {comment['id']} - user account unavailable")
            continue
            
        comment_info = {
            "comment_id": comment['id'],
            "commenter_username": comment['user']['login'],
            "commenter_id": comment['user']['id'],
            "commenter_profile_url": comment['user']['html_url'],
            "body": comment.get('body', ''),
            "created_at": comment['created_at'],
            "updated_at": comment['updated_at'],
            "html_url": comment.get('html_url', ''),
            "author_association": comment.get('author_association', '')
        }
        comments.append(comment_info)
    
    return comments

def fetch_prs_with_reviewer_data():
    """Fetch PRs and collect comprehensive reviewer data"""
    base_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    
    all_reviewer_data = []
    page = 1
    prs_collected = 0
    
    print(f"Starting to collect reviewer data from {REPO_OWNER}/{REPO_NAME}...")
    
    while prs_collected < MAX_PRS_TO_FETCH:
        per_page = min(30, MAX_PRS_TO_FETCH - prs_collected)
        params = f"?state=all&per_page={per_page}&page={page}&sort=updated&direction=desc"
        url = base_url + params
        
        print(f"Fetching page {page} (PRs {prs_collected + 1}-{prs_collected + per_page})...")
        
        prs = make_github_request(url)
        if not prs:
            print("Failed to fetch PRs or no more PRs available")
            break
        
        for pr in prs:
            pr_number = pr['number']
            print(f"  Processing PR #{pr_number}: {pr['title'][:60]}...")
            
            reviews = get_pr_reviews(pr_number)
            review_comments = get_pr_review_comments(pr_number)
            general_comments = get_pr_general_comments(pr_number)
            
            if reviews or review_comments:
                pr_reviewer_data = {
                    "pr_id": str(uuid.uuid4()),
                    "repo_name": f"{REPO_OWNER}/{REPO_NAME}",
                    "pr_number": pr_number,
                    "title": pr['title'],
                    "state": pr['state'],
                    "author": {
                        "username": pr['user']['login'],
                        "id": pr['user']['id'],
                        "profile_url": pr['user']['html_url']
                    },
                    "created_at": pr['created_at'],
                    "updated_at": pr['updated_at'],
                    "merged_at": pr.get('merged_at'),
                    "merged_by": {
                        "username": pr['merged_by']['login'] if pr.get('merged_by') else None,
                        "id": pr['merged_by']['id'] if pr.get('merged_by') else None,
                        "profile_url": pr['merged_by']['html_url'] if pr.get('merged_by') else None
                    } if pr.get('merged_by') else None,
                    "description": pr['body'] or "",
                    "labels": [label['name'] for label in pr.get('labels', [])],
                    "additions": pr.get('additions', 0),
                    "deletions": pr.get('deletions', 0),
                    "changed_files_count": pr.get('changed_files', 0),
                    "is_draft": pr.get('draft', False),
                    
                    # Reviewer-focused data
                    "reviews": reviews,
                    "review_comments": review_comments,
                    "general_comments": general_comments,
                    "reviewer_summary": {
                        "total_reviews": len(reviews),
                        "total_review_comments": len(review_comments),
                        "total_general_comments": len(general_comments),
                        "unique_reviewers": list(set([r['reviewer_username'] for r in reviews] + 
                                                   [c['reviewer_username'] for c in review_comments])),
                        "approval_count": len([r for r in reviews if r['state'] == 'APPROVED']),
                        "changes_requested_count": len([r for r in reviews if r['state'] == 'CHANGES_REQUESTED']),
                        "comment_only_count": len([r for r in reviews if r['state'] == 'COMMENTED'])
                    }
                }
                
                all_reviewer_data.append(pr_reviewer_data)
                reviewer_count = len(pr_reviewer_data['reviewer_summary']['unique_reviewers'])
                print(f"    Found {len(reviews)} reviews, {len(review_comments)} review comments from {reviewer_count} reviewers")
            else:
                print("    No reviewer activity found")
            
            prs_collected += 1
            if prs_collected >= MAX_PRS_TO_FETCH:
                break
            
            # Rate limiting
            time.sleep(0.3)
        
        page += 1
        time.sleep(0.5)  # Additional delay between pages
    
    return all_reviewer_data

def analyze_reviewer_patterns(reviewer_data):
    """Analyze patterns and generate reviewer profiles"""
    reviewer_profiles = defaultdict(lambda: {
        'username': '',
        'profile_url': '',
        'avatar_url': '',
        'user_id': None,
        'total_prs_reviewed': 0,
        'total_formal_reviews': 0,
        'total_review_comments': 0,
        'total_general_comments': 0,
        'review_states': {
            'APPROVED': 0,
            'CHANGES_REQUESTED': 0,
            'COMMENTED': 0,
            'DISMISSED': 0
        },
        'author_associations': defaultdict(int),
        'prs_reviewed': [],
        'review_activity_by_month': defaultdict(int),
        'avg_review_length': 0,
        'repositories_reviewed': set(),
        'collaboration_patterns': {
            'reviews_with_comments': 0,
            'follow_up_comments': 0
        }
    })
    
    for pr_data in reviewer_data:
        repo_name = pr_data['repo_name']
        pr_number = pr_data['pr_number']
        
        # Process formal reviews
        for review in pr_data['reviews']:
            username = review['reviewer_username']
            profile = reviewer_profiles[username]
            
            # Basic info
            profile['username'] = username
            profile['profile_url'] = review['reviewer_profile_url']
            profile['avatar_url'] = review['reviewer_avatar_url']
            profile['user_id'] = review['reviewer_id']
            
            # Counts
            profile['total_formal_reviews'] += 1
            profile['review_states'][review['state']] += 1
            profile['author_associations'][review['author_association']] += 1
            
            if pr_number not in profile['prs_reviewed']:
                profile['prs_reviewed'].append(pr_number)
                profile['total_prs_reviewed'] += 1
            
            profile['repositories_reviewed'].add(repo_name)
            
            # Activity by month
            review_date = datetime.fromisoformat(review['submitted_at'].replace('Z', '+00:00'))
            month_key = review_date.strftime('%Y-%m')
            profile['review_activity_by_month'][month_key] += 1
        
        # Process review comments
        for comment in pr_data['review_comments']:
            username = comment['reviewer_username']
            profile = reviewer_profiles[username]
            
            profile['username'] = username
            profile['profile_url'] = comment['reviewer_profile_url']
            profile['user_id'] = comment['reviewer_id']
            profile['total_review_comments'] += 1
            
            if pr_number not in profile['prs_reviewed']:
                profile['prs_reviewed'].append(pr_number)
                profile['total_prs_reviewed'] += 1
            
            profile['repositories_reviewed'].add(repo_name)
        
        # Process general comments (from reviewers who also did formal reviews)
        reviewer_usernames = set([r['reviewer_username'] for r in pr_data['reviews']] + 
                                [c['reviewer_username'] for c in pr_data['review_comments']])
        
        for comment in pr_data['general_comments']:
            username = comment['commenter_username']
            if username in reviewer_usernames:
                profile = reviewer_profiles[username]
                profile['total_general_comments'] += 1
    
    # Convert sets to lists for JSON serialization
    for profile in reviewer_profiles.values():
        profile['repositories_reviewed'] = list(profile['repositories_reviewed'])
        profile['author_associations'] = dict(profile['author_associations'])
        profile['review_activity_by_month'] = dict(profile['review_activity_by_month'])
    
    return dict(reviewer_profiles)

def main():
    print("="*60)
    print("GITHUB REVIEWER DATA COLLECTOR")
    print("="*60)
    print(f"Target Repository: {REPO_OWNER}/{REPO_NAME}")
    print(f"Max PRs to analyze: {MAX_PRS_TO_FETCH}")
    print()
    
    # Collect reviewer data
    reviewer_data = fetch_prs_with_reviewer_data()
    
    if not reviewer_data:
        print("No reviewer data collected. Exiting.")
        return
    
    print(f"\nCollected data from {len(reviewer_data)} PRs with reviewer activity")
    
    # Analyze reviewer patterns
    print("Analyzing reviewer patterns...")
    reviewer_profiles = analyze_reviewer_patterns(reviewer_data)
    
    # Generate output
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_data = {
        'metadata': {
            'repository': f"{REPO_OWNER}/{REPO_NAME}",
            'collection_date': timestamp,
            'total_prs_analyzed': len(reviewer_data),
            'total_reviewers_found': len(reviewer_profiles),
            'collection_parameters': {
                'max_prs_fetched': MAX_PRS_TO_FETCH,
                'api_token_used': API_TOKEN[:20] + "..." if API_TOKEN else "None"
            }
        },
        'pr_reviewer_data': reviewer_data,
        'reviewer_profiles': reviewer_profiles
    }
    
    # Save to file
    import os
    output_dir = r'D:\PR reviewer Automation\Moment Repo\PR data for Reviewers'
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    output_filename = f'{REPO_OWNER}_{REPO_NAME}_reviewer_data_{timestamp}.json'
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nData saved to: {output_path}")
    
    # Display summary statistics
    print("\n" + "="*60)
    print("COLLECTION SUMMARY")
    print("="*60)
    
    total_reviews = sum(len(pr['reviews']) for pr in reviewer_data)
    total_review_comments = sum(len(pr['review_comments']) for pr in reviewer_data)
    
    print(f"PRs with reviewer activity: {len(reviewer_data)}")
    print(f"Total formal reviews: {total_reviews}")
    print(f"Total review comments: {total_review_comments}")
    print(f"Unique reviewers found: {len(reviewer_profiles)}")
    
    # Top reviewers by activity
    print(f"\nTop 10 Most Active Reviewers:")
    print("-" * 40)
    
    top_reviewers = sorted(reviewer_profiles.items(), 
                          key=lambda x: x[1]['total_formal_reviews'] + x[1]['total_review_comments'], 
                          reverse=True)[:10]
    
    for i, (username, profile) in enumerate(top_reviewers, 1):
        total_activity = profile['total_formal_reviews'] + profile['total_review_comments']
        print(f"{i:2d}. {username:20s} - {total_activity:3d} activities "
              f"({profile['total_formal_reviews']} reviews, {profile['total_review_comments']} comments)")
    
    print(f"\nCollection completed successfully!")
    print(f"Use the generated file to analyze reviewer behavior and patterns.")

if __name__ == "__main__":
    main()