# Github auto pull

This script helps you deploying your code on production server.

When you push your code on the configured branch it will **automatically pull the latest code**, and **execute your bash script** to do whatever need to be done (building, restarting services...).

It uses Github hooks.

The script will run in a docker container, so it will be resilient to crashes.

## Usage

1. Clone the watched repo on your production server. **You must be able to git pull without entering your creds**. You can achieve that by generating a SSH key and upload it to your Github account.

2. Clone this project.

3. Go to your Github repo, then in settings > web hooks, create a new web hook.

   In the payload url field, put **http://your-prod-server:9999/push**.

   In content type, select **application/json**.

   In the secret field, define a secret that will be used to authenticate requests to your production server.

4. Then you can edit config.json:

```json
{
    "repos": [
        {
            "repo": "t0mm4rx/test_repo", // Full name of the repo -> gh_user/repo_name
            "secret": "dummy", // Secret you put when creating the hook
            "branch": "main", // The branch you want to pull
            "directory": "/root/test_repo", // The full path of the repo on your production server
            "command": "/bin/bash /root/restart_services.sh" // The command to execute when the repo is pulled
        }
    ]
}
```

You can have multiple repos to watch.