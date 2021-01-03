import json
import re
import urllib
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def get_summoner_id_by_name():

    name = input('Enter account name: ')

    parsed = urllib.parse.quote(name)

    response = urllib.request.urlopen('https://euw.op.gg/summoner/userName=' + parsed).read().decode()

    summoner_id_match = re.search(r'data-summoner-id=\"([0-9]+)', response)

    if summoner_id_match is not None:

        id = int(summoner_id_match.groups(0)[0])
        print ('User Id: ', id)

        games_matches = re.findall(r'GameItem\s(\w+)([^>]+)', response)

        if len(games_matches) > 0:
            print('Last ' + str(len(games_matches)) + ' matches results:')

        for game in games_matches:

            game_id_match = re.search(r'game-id=\"([\d]+)' ,game[1])

            game_info_response = urllib.request.urlopen('https://euw.op.gg/summoner/matches/ajax/detail/gold/gameId=' + game_id_match.groups(0)[0] + '&summonerId=' + summoner_id_match.groups(0)[0] + '&moreLoad=1').read().decode()

            soup = BeautifulSoup(game_info_response, 'html.parser')

            list_items = soup.find_all('li')

            champion_name = ''

            for item in list_items:
                if item.attrs['class'] is not None and 'Active' in item.attrs['class']:
                    img_tag = item.find('img')

                    champion_name = re.search(r'champion/([^.]+)', img_tag.attrs['src']).groups(0)[0]

                    break

            cs_series_part = re.search(r'GraphChampionCS-[\d]+\', {([^)]+)', game_info_response).groups(0)[0]

            cs_series = re.search(r'series: (.+)', cs_series_part).groups(0)[0][:-1]

            data = json.loads(cs_series)

            cs_at_10 = ''

            for entry in data:
                if champion_name in entry['name']:
                    cs_at_10 = entry['data'][10]
                    break;

            print('Result: ' + game[0] + '. ID: ' + game_id_match.groups(0)[0] + '. Champion: ' + champion_name + '. CS @10: ' + str(cs_at_10))



            


    else:
        print('User not found.')
        return

    return (name, parsed, id)


if __name__ == "__main__":

    while True:

        name, parsed, id = get_summoner_id_by_name()



    pass
