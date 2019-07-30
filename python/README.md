## Overall system architecture

**Django**: Does very light duty as an Ajax endpoint for the JS front end code to interact with. It only manages invoices and the leaderboard.

**AWS Lambda**: Runs Django serverless. Running within ethtweetme's account to leverage existing infrastructure and amortize costs across micro projects. _Cost note: external API access from within Lambda requires a NAT gateway running as a micro instance in the AWS free tier. But this will soon incur a small monthly fee._

**AWS RDS**: Also sharing ethtweetme's RDS instance to amortize one of the few 24/7 costs. Will explore serverless Postgres when it's rolled out on RDS.

**JS front end**: The game itself and all of its UI is served as static content via html and JS.

**NodeJS**: Manages JS dependencies, transpiles, minifies, and builds the JS source code into a single `app.js` resource along with static files.

**AWS S3 & Cloudfront**: Hosts the site's static html, JS, and image files.

**AWS Route53**: Controls the EscapeQR domain name and DNS entries.



## Postgres/RDS setup
Create the DB role for remote and local DB
```
createuser --createdb -P waxbadges2048_app
createuser --createdb -P waxbadges2048_app -h some_rds_endpoint.us-east-1.rds.amazonaws.com -U rds_admin_username
```

Create the empty remote and local DB, set `waxbadges2048_app` role as owner
```
createdb waxbadges2048 -O waxbadges2048_app
createdb waxbadges2048 -O waxbadges2048_app -h some_rds_endpoint.us-east-1.rds.amazonaws.com -U waxbadges2048_app
```


## macOS Setup
Target Python 3.7
```
brew tap sashkab/python
brew install sashkab/python/python37
```


## Zappa integration with AWS Lambda
Note that Zappa needs to use the AWS cli config to talk to AWS. If launching within an existing AWS account, be sure that `profile_name` in `zappa_settings.json` references that config (see configs in `~/.aws/config`).

Create the new Zappa environment (run from `waxbadges2048/waxbadges2048`):
```
zappa deploy production
```
names 'staging' and 'production'._

Update zappa, migrate db, etc:
```
zappa update production
zappa manage production migrate
zappa manage production collectstatic
```

Monitor logs:
```
zappa tail waxbadges2048_production
```


