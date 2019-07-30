from django.http import JsonResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView

from . import cleos_util
from . import twitter_util

from allauth.socialaccount.models import SocialAccount

import logging
logger = logging.getLogger(__name__)



class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ecosystem = cleos_util.get_ecosystem()

        achievements = {}
        for category_id, category in enumerate(ecosystem.get('categories')):
            for achievement_id, achievement in enumerate(category.get('achievements')):
                achievements[f"{category_id}_{achievement_id}"] = {
                        "name": achievement.get('name'),
                        "description": achievement.get('description'),
                        "asseturl": f"https://{ecosystem.get('assetbaseurl')}/{achievement.get('assetname')}"
                    }
        context['achievements'] = achievements

        context['is_following'] = False

        if self.request.user.is_authenticated:
            socialaccount = SocialAccount.objects.get(user=self.request.user)
            context['socialaccount'] = socialaccount

            user = twitter_util.get_user(self.request.user.username)
            context['is_following'] = user.following

            # Retrieve user's achievement info from WAXBadges
            context['granted_achievements'] = cleos_util.get_granted_achievements('@' + self.request.user.username, ecosystem=ecosystem)

            user_id = cleos_util.find_user_id("@" + self.request.user.username)
            if user_id is None and user_id != 0:
                # Add user
                twitter_username = self.request.user.username
                avatarurl = twitter_util.get_avatarurl(twitter_username)
                cleos_util.add_user("@" + self.request.user.username, avatarurl)


        return context

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AjaxBaseView(View):
    pass


class GetGrantedAchievementsAjaxView(AjaxBaseView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            granted_achievements = cleos_util.get_granted_achievements('@' + request.user.username)
        else:
            granted_achievements = []
        return JsonResponse({
            "granted_achievements": granted_achievements
        })


class GrantAchievementAjaxView(AjaxBaseView):
    def post(self, request, *args, **kwargs):
        logger.debug(request.POST)

        achievement = request.POST.get('achievement')
        category_id = int(achievement.split('_')[0])
        achievement_id = int(achievement.split('_')[1])

        print(f"category_id:    {category_id}")
        print(f"achievement_id: {achievement_id}")

        ecosystem = cleos_util.get_ecosystem()

        userid = '@' + request.user.username
        user_id = cleos_util.find_user_id(userid, ecosystem=ecosystem)

        print(f"user_id: {user_id}")
        if not user_id and user_id != 0:
            raise Exception(f"User with userid '{userid}' not found")

        resp = cleos_util.grant_achievement(category_id, achievement_id, user_id)
        print(resp)

        achievement_info = cleos_util.get_achievement_info(category_id, achievement_id, ecosystem=ecosystem)
        print(achievement_info)

        url = f"{settings.WAXBADGES_EXPLORER_URL}/poa/{settings.WAXBADGES_ECOSYSTEM_ID}/{category_id}/{achievement_id}/{user_id}"
        msg = f"You earned the \"{achievement_info.get('name')}\" achievement from \"{ecosystem.get('name')}\"!\n\nShare your Proof-of-Achievement!\n{url}"

        print(msg)
        twitter_util.dm_user(username=request.user.username, msg=msg)

        return JsonResponse({
            'success': True,
            'resp': resp
        })


