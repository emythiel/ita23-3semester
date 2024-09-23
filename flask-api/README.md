# Flask API exercise

### Setup:
1. Clone the git repo and move to the correct directory:
```git clone https://github.com/Emythiel/ita23-3semester.git && cd flask-api```
2. Make sure the proper dependencies are installed:
```pip install -r requirements.txt```
3. Create a database and populare it with randomly generated info:
```python app_database_create.py```
4. Launch the app:
```python app.py```

### Usage:
1. You can GET all users with the `/members` endpoint
2. You can GET a specific user with `/members/{id}` where `{id}` is a number
3. You can POST a new member with `/members`
4. You can DELETE a member with `/members/{id}` where `{id}` is a number
5. You can PATCH a member with `/members/{id}` where `{id}` is a number
6. Any changes is saved to the `database.db` file
7. When using GET, it will attempt to fetch the users public GitHub repos:
    - Will notify if the username doesn't exist
    - Will notify if there's no public repositories
    - If a valid Authenticated token is used, will show more information if the token matches a GitHub username
8. All api requests should provide proper HTTP errors and messages in the return json body
