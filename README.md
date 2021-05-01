# Github auto pull

This script helps you deploying your code on production server.

When you push your code on the configured branch it will **automatically pull the latest code**, and **execute your bash script** to do whatever need to be done (building, restarting services...).

It uses Github hooks.

The script will run in a docker container, so it will be resilient to crashes.

## Usage

Make sure you have docker and docker-compose installed.

1. Clone the watched repo on your production server. **You must be able to git pull without entering your creds**. You can achieve that by generating a SSH key and upload it to your Github account.

2. Clone this project.

3. Go to your Github repo, then in settings > web hooks, create a new web hook.

   In the payload url field, put **http://your-prod-server:9999/push**.

   In content type, let the default value, **application/x-www-form-urlencode**.

   In the secret field, define a secret that will be used to authenticate requests to your production server.

4. Then you can edit config.json:

```json
{
  "secret": "the secret you defined in your Github hook",
  "branch": "the branch you want to watch",
  "directory": "the absolute path to the repo you cloned",
  "command": "the command to execute after pulling the repo"
}
```



