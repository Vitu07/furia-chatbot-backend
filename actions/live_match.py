import requests
from datetime import datetime
import pytz
import os

def get_live_furia_match():    
    API_TOKEN = os.environ.get('PANDASCORE_API_TOKEN')
    FURIA_ID = 124530
    url = f'https://api.pandascore.co/csgo/matches/running?token={API_TOKEN}'

    try:
        response = requests.get(url, timeout=10)
        matches = response.json()

        if not matches:
            return "Nenhuma partida ao vivo encontrada para a FURIA no momento."

        for match in matches:
            furia_playing = any(opp['opponent']['id'] == FURIA_ID 
                          for opp in match['opponents'])
            
            if not furia_playing:
                continue

            team1 = match['opponents'][0]['opponent']
            team2 = match['opponents'][1]['opponent']
            
            furia_team = team1 if team1['id'] == FURIA_ID else team2
            opponent_team = team2 if team1['id'] == FURIA_ID else team1

            score_furia = next((r['score'] for r in match['results'] 
                              if r['team_id'] == FURIA_ID), 0)
            score_opponent = next((r['score'] for r in match['results'] 
                                if r['team_id'] != FURIA_ID), 0)

            current_map = next(
                (f"Mapa {game['position']}" for game in match['games'] 
                 if game['status'] == 'running'),
                "Mapa em andamento"
            )

            stream_url = match['streams_list'][0]['raw_url'] if match.get('streams_list') else 'Link não disponível'

            message = (
                f"🔴 *PARTIDA AO VIVO - {furia_team['name']}*\n\n"
                f"⚔️ *Confronto:* {furia_team['name']} vs {opponent_team['name']}\n"
                f"🏆 *Torneio:* {match['league']['name']}\n"
                f"📊 *Placar:* {furia_team['acronym']} {score_furia}-{score_opponent} {opponent_team['acronym']}\n"
                f"🗺️ *Mapa Atual:* {current_map}\n\n"
                f"📺 *Assistir:* {stream_url}\n"
                f"⏱️ *Atualizado:* {datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M')}"     
            )
            return message

        return None

    except requests.exceptions.RequestException as e:
        print(f"Erro na API: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None