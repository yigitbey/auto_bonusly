import requests
import sys

access_token = sys.argv[1]
limit = int(sys.argv[2])
points_per_person = 5
message = "thanks! (automated end-of-month giveaway)"
hashtag = "#be-genuine"

api_base = 'https://bonus.ly/api/v1/' 
access_params = {'access_token': access_token}

bonusly_user = requests.get(api_base + 'users/me', params=access_params).json()['result']
remaining_points = bonusly_user['giving_balance']

if limit: 
  remaining_points = min(limit, remaining_points)
  
user_id = bonusly_user['id']
self_username = '@' + bonusly_user['username']

person_count = int(remaining_points / points_per_person)
remainder = remaining_points - person_count*points_per_person

last_bonuses_given_by = requests.get(api_base + 'users/%s/bonuses'%(user_id), params=access_params).json()['result']

user_names = ['@' + giver['giver']['username'] for giver in last_bonuses_given_by]

user_names = sorted(set(user_names), key=user_names.index)[:person_count]
if self_username in user_names:
  user_names.remove(self_username)

reason = "+%s %s %s %s" % (points_per_person, " ".join(user_names), message, hashtag)
data = {"reason": reason}
given = requests.post(api_base + 'bonuses', params=access_params, data=data).json()

if remainder:
  reason = "+%s %s %s %s" % (remainder, user_names[0], message, hashtag)
  data = {"reason": reason}
  given = requests.post(api_base + 'bonuses', params=access_params, data=data).json()
