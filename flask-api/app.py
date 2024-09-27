import requests
from flask import Flask, request, Response
from data_dict import random_users
from app_database import db_read_all, db_read_one, db_create_entry, db_delete_entry, db_update_entry
import json

app = Flask(__name__)

# List of fields that the api accepts
ALLOWED_FIELDS = ['first_name', 'last_name', 'birth_date', 'gender', 'email', 'phonenumber', 'address', 'nationality', 'active', 'github_username']

# Function to fetch authenticated username
def fetch_authenticated_username(token):
    url = 'https://api.github.com/user'
    headers = {'Authorization': f'token {token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return user_info['login'].lower() # Return GitHub username
    else:
        return None # Token is invalid

# Function to get GitHub repositories
def fetch_github_repos(username, token=None, fetch_private=False):
    if fetch_private:
        url = 'https://api.github.com/user/repos'
    else:
        url = f'https://api.github.com/users/{username}/repos'

    headers = {}
    # Check if an auth token is supplied
    if token:
        headers['Authorization'] = f'token {token}'

    try:
        response = requests.get(url, headers=headers)

        print(f'url: {url}')

        # Handle 404 response if GitHub user doesn't exist
        if response.status_code == 404:
            return 'Username invalid'
        # Handle other responses for general API errors
        if response.status_code == 401:
            return f'Unauthorized: {response.json().get("message", "no message provided")}'
        if response.status_code != 200:
            return 'GitHub API error'

        repos = response.json()

        # If user exists but no public repos
        if not repos:
            return 'No public repositories found'

        # Return a simplified list of repositories
        return [{'name': repo['name'], 'visibility': repo['visibility']} for repo in repos]

    except requests.exceptions.RequestException as e:
        return f'Error fetching GitHub repositories: {str(e)}'

# Show results function, properly sorted by column order
def show_result(data, status=200):
    return Response(json.dumps(data, sort_keys=False), status=status, mimetype='application/json')

# Routes

# Get list of all members or specific member based on ID
@app.route('/members', defaults={'id': None})
@app.route('/members/<int:id>')
def read_all(id):
    # Get GitHub auth token from headers
    token = request.headers.get('Authorization')

    # If no ID given, return all members
    if id is None:
        members = db_read_all()

        # Fetch GitHub repos for each member
        for member in members:
            # Check if token matches the member's GitHub username
            if token:
                auth_username = fetch_authenticated_username(token.split()[1])
                if auth_username == member['github_username']:
                    github_repos = fetch_github_repos(member['github_username'], token.split()[1], fetch_private=True)
                else:
                    github_repos = fetch_github_repos(member['github_username'], token.split()[1])
            else:
                github_repos = fetch_github_repos(member['github_username'])

            member['github_repos'] = github_repos

        return show_result(members)

    # If ID given return member or error if id not found
    else:
        member = db_read_one(id)

        if member:
        # Check if token matches the member's GitHub username
            if token:
                auth_username = fetch_authenticated_username(token.split()[1])
                if auth_username == member['github_username']:
                    github_repos = fetch_github_repos(member['github_username'], token.split()[1], fetch_private=True)
                else:
                    github_repos = fetch_github_repos(member['github_username'], token.split()[1])
            else:
                github_repos = fetch_github_repos(member['github_username'])

             # Add GitHub repos to the member dictionary
            member['github_repos'] = github_repos

            return show_result([member])
        else:
            return show_result({'error': 'Member ID not found'}, status=404)


# Add new member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()

    # Validate that all fields are present
    missing_fields = [field for field in ALLOWED_FIELDS if field not in data]
    if missing_fields:
        return show_result({'error': f'Missing field(s): {", ".join(missing_fields)}'}, status=400)

    # Validate no additional fields are provided:
    invalid_fields = [field for field in data if field not in ALLOWED_FIELDS]
    if invalid_fields:
        return show_result({'error': f'Invalid field(s): {", ".join(invalid_fields)}'}, status=400)

    try:
        db_create_entry(data)
        return show_result({'success': 'Member created successfully'}, status=201)
    except Exception as e:
        return show_result({'error': 'Error creating member', 'details': str(e)}, status=500)


# Delete a member based on ID
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    # Retrieve the member to see if they exist
    member = db_read_one(id)
    if not member:
        return show_result({'error': 'Member ID not found'}, status=404)

    try:
        db_delete_entry(id)
        return show_result({'success': f'Member {id} ({member["first_name", "last_name"]}) deleted successfully'}, status=200)
    except Exception as e:
        return show_result({'error': 'Error deleting member', 'details': str(e)}, status=500)


# Update a member based on ID
@app.route('/members/<int:id>', methods=['PATCH'])
def update_member(id):
    # Retrieve the member to see if they exist
    member = db_read_one(id)
    if not member:
        return Response(json.dumps({'error': 'Member ID not found'}), status=404, mimetype='application/json')

    # Get data from request body
    data = request.get_json()

    # Validate that all fields in the request are allowed
    invalid_fields = [field for field in data if field not in ALLOWED_FIELDS]
    if invalid_fields:
        return Response(json.dumps({'error': f'Invalid field(s): {', '.join(invalid_fields)}'}), status=400, mimetype='application/json')

    # Update the entry in the database
    db_update_entry(id, data)

    # Return the updated member
    updated_member = db_read_one(id)
    return show_result(updated_member)


app.run(host="0.0.0.0")
