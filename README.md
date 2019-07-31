![waxbadges2048](python/waxbadges2048/waxbadges2048/_static/img/2048_splash.png)
# 2048 - WAXBadges Edition
_The classic addictive block game now reborn with WAXBadges achievements! Each achievement you unlock will live forever on the 
WAX blockchain!_

The game's JS code was forked from [gabrielecirulli/2048](https://github.com/gabrielecirulli/2048). All thanks and credit to gabrielecirulli!

twitter: [@WAXBadges](https://twitter.com/WAXBadges)

#### What is WAXBadges?
see the main repo: [https://github.com/kdmukai/waxbadges](https://github.com/kdmukai/waxbadges)


# Overview
_2048 - WAXBadges Edition_ is meant to be a simple demonstration for how the WAXBadges achievement platform can be easily integrated into a game. It's also just a ton of fun!

I augmented the original JS to include Achievement event hooks that talk to a simple Django website running on AWS Lambda and deployed via Zappa. The website processes the incoming Achievement events and talks to the WAXBadges smart contract to issue Achievements to Users.

## Integration steps
As a game developer I would create my game's Achievement ecosystem via the [WAXBadges CREATOR Tool](https://github.com/kdmukai/waxbadges_creator). I can immediately see my new Achievements in the [WAXBadges Explorer](https://explorer.waxbadges.com/ecosys/1).

The game, app, or website then just needs to add some simple smart contract interaction steps. Take a look at `cleos_util.py` here: [python/waxbadges2048/waxbadges2048/cleos_util.py](python/waxbadges2048/waxbadges2048/cleos_util.py). It's basically the beginnings of a very simple python API for some basic data retrieval from the WAXBadges smart contract. It also handles creating new `Users` and granting them `Achievements`. This could easily be re-used for your own project.

The rest is just a fairly vanilla Django website that uses `allauth` to enable Twitter sign-ins. I specified the vars for my particular project in two places:
* `.env--example` for when running the Django site locally
* `zappa_settings--example.json` to set environment variables when deploying to Lambda

Customize each and omit the `--example` to suit your own settings.

