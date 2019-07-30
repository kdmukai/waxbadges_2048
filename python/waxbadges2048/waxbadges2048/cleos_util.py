import eospy
import json
import datetime as dt
import math
import pytz
import time

from eospy.cleos import Cleos

from django.conf import settings


def get_ecosystem():
    cleos = Cleos(url=settings.WAX_URL)
    ecosystems = cleos.get_table(
        code=settings.WAX_CONTRACT,
        scope=settings.WAX_CONTRACT,
        table='ecosystems',
        lower_bound=settings.WAXBADGES_ECOSYSTEM_ID,
        upper_bound=settings.WAXBADGES_ECOSYSTEM_ID,
        limit=1,
        timeout=30
    )
    return ecosystems.get('rows', [])[0]


def get_userachievements(userid, ecosystem=None):
    if not ecosystem:
        ecosystem = get_ecosystem()

    try:
        users = [u for u in ecosystem.get('users') if u.get('userid') == userid]
        if len(users) == 0: 
            return None

        return users[0].get('userachievements')
    except Exception as e:
        print(e)
        return None


def get_granted_achievements(userid, ecosystem=None):
    userachievements = get_userachievements(userid, ecosystem)
    granted_achievements = []
    if userachievements:
        for userachievement in userachievements:
            granted_achievements.append(f"{userachievement.get('category_id')}_{userachievement.get('achievement_id')}");
    return granted_achievements


def get_achievement_info(category_id, achievement_id, ecosystem=None):
    if not ecosystem:
        ecosystem = get_ecosystem()

    return ecosystem.get('categories')[category_id].get('achievements')[achievement_id]


def find_user_id(userid, ecosystem=None):
    if not ecosystem:
        ecosystem = get_ecosystem()

    for user_id, user in enumerate(ecosystem.get('users')):
        if user.get('userid') == userid:
            return user_id

    return None


def add_user(userid, avatarurl):
    cleos = Cleos(url=settings.WAX_URL)

    # void adduser(name ecosystem_owner, uint32_t ecosystem_id, string user_name, string userid, string avatarurl)
    arguments = {
        "ecosystem_owner": settings.WAX_ACCOUNT_NAME,
        "ecosystem_id": settings.WAXBADGES_ECOSYSTEM_ID,
        "user_name": userid,
        "userid": userid,
        "avatarurl": avatarurl
    }
    payload = {
        "account": settings.WAX_CONTRACT,
        "name": "adduser",
        "authorization": [{
            "actor": settings.WAX_ACCOUNT_NAME,
            "permission": "active",
        }],
    }

    #Converting payload to binary
    data = cleos.abi_json_to_bin(payload['account'],payload['name'],arguments)

    #Inserting payload binary form as "data" field in original payload
    payload['data']=data['binargs']

    #final transaction formed
    trx = {"actions": [payload]}
    trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))

    key = eospy.keys.EOSKey(settings.WAX_PRIVATE_KEY)
    resp = cleos.push_transaction(trx, key, broadcast=True)

    return resp



def grant_achievement(category_id, achievement_id, user_id):
    cleos = Cleos(url=settings.WAX_URL)

    # void grantach(name ecosystem_owner, uint32_t ecosystem_id, uint32_t user_id, uint32_t category_id, uint32_t achievement_id, uint32_t timestamp)
    arguments = {
        "ecosystem_owner": settings.WAX_ACCOUNT_NAME,
        "ecosystem_id": settings.WAXBADGES_ECOSYSTEM_ID,
        "user_id": user_id,
        "category_id": category_id,
        "achievement_id": achievement_id,
        "timestamp": math.trunc(time.time())
    }
    payload = {
        "account": settings.WAX_CONTRACT,
        "name": "grantach",
        "authorization": [{
            "actor": settings.WAX_ACCOUNT_NAME,
            "permission": "active",
        }],
    }

    #Converting payload to binary
    data = cleos.abi_json_to_bin(payload['account'],payload['name'],arguments)

    #Inserting payload binary form as "data" field in original payload
    payload['data']=data['binargs']

    #final transaction formed
    trx = {"actions": [payload]}
    trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))

    key = eospy.keys.EOSKey(settings.WAX_PRIVATE_KEY)
    resp = cleos.push_transaction(trx, key, broadcast=True)

    return resp
