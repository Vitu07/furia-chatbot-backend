import requests
from datetime import datetime, timezone
import pytz
import os

def get_next_furia_match():
    API_TOKEN = os.environ.get('PANDASCORE_API_TOKEN')
    FURIA_ID = 124530
    url = f'https://api.pandascore.co/csgo/matches/upcoming?filter[opponent_id]={FURIA_ID}&token={API_TOKEN}'

    try:
        response = requests.get(url, timeout=10)
        matches = response.json()
    
        if not matches:
            return "Não há partidas futuras programadas. Volte mais tarde!"

        next_match = matches[0]
        
        opponents = next_match.get('opponents', [])
        
        if not opponents:
            return "⚠️ Informações dos times indisponíveis."

        furia_team = opponents[0]['opponent']
        
        if len(opponents) > 1 and opponents[1]['opponent']:
            opponent_team = opponents[1]['opponent']
            opponent_name = opponent_team['name']
        else:
            opponent_name = "Adversário a definir (TBD)"

        begin_at = datetime.fromisoformat(next_match['begin_at'].replace('Z', '+00:00')).replace(tzinfo=timezone.utc)
        match_time = begin_at.astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%d/%m/%Y às %H:%M')

        streams = next_match.get('streams_list', [])
        stream_url = next(
            (s['raw_url'] for s in streams if s.get('main')), 
            streams[0]['raw_url'] if streams else 'Link em breve'
        )

        message = (
            f"**PRÓXIMO JOGO**\n\n"
            f"🏆 **Torneio:** {next_match['league']['name']}\n"
            f"⚔️ **Confronto:** {furia_team['name']} vs {opponent_name}\n"
            f"📅 **Data:** {match_time} (Horário de Brasília)\n"
            f"🔢 **Formato:** Melhor de {next_match.get('number_of_games', 'N')}\n\n"
            f"📺 **Transmissão:** {stream_url}"
        )
        return message

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return "⚠️ Erro ao conectar com o servidor. Tente novamente mais tarde!"
    except Exception as e:
        print(f"Erro inesperado: {type(e).__name__}: {e}")
        return "⚠️ Serviço temporariamente indisponível. Tente novamente mais tarde!"