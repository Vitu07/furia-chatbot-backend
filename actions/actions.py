from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.player_info import PlayerInfo
from .next_matches import get_next_furia_match
from .live_match import get_live_furia_match 

class ActionNextMatch(Action):
    def name(self) -> Text:
        return "action_next_match"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        next_match_info = get_next_furia_match()
        dispatcher.utter_message(text=next_match_info, markdown=True)
        return []
    
class ActionLiveMatch(Action):
    def name(self) -> Text:
        return "action_live_match"

    def run(self, dispatcher, tracker, domain):
        match_info = get_live_furia_match()
        
        if match_info:
            dispatcher.utter_message(text=match_info, markdown=True)
        else:
            dispatcher.utter_message(
                text="Nenhuma partida ao vivo da FURIA no momento.\n"
                     "Digite 'próximo jogo' para ver quando será a próxima!",
                markdown=True
            )
        return []

class ActionPlayerSpecific(Action):
    def name(self) -> Text:
        return "action_player_specific"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        player = tracker.get_slot('player')
        player_info = PlayerInfo()

        if not player:
            dispatcher.utter_message(
                text="❌ Não identifiquei o jogador. Você pode tentar:\n"
                     "'FalleN', 'yuurih', 'KSCERATO', 'molodoy' ou 'YEKINDAR'",
                markdown=True
            )
            return []

        jogador_encontrado = player_info.encontrar_jogador(player)

        if jogador_encontrado:
            info = player_info.jogadores_info[jogador_encontrado]
            titulos_formatados = " • " + "\n • ".join(info["titulos"])
            resposta = (
                f"**{info['nome_real']}** ({info['apelido']}) - {info['posicao']}\n\n"
                f"**Idade:** {info.get('idade', 'Não informada')}\n"
                f"**Nacionalidade:** {info.get('nacionalidade', 'Não informada')}\n"
                f"🏆 **Títulos:**\n"
                f"{titulos_formatados}\n\n"
                f"{info['historia']}\n\n"
            )
        else:
            resposta = (
                f"❌ Jogador '{player}' não encontrado.\n\n"
                "🔹 **Elenco Atual da FURIA:**\n"
                "- yuurih (Yuri Santos)\n"
                "- KSCERATO (Kaike Cerato)\n"
                "- FalleN (Gabriel Toledo)\n"
                "- molodoy (Kayke Bertolucci)\n"
                "- YEKINDAR (Mareks Gaļinskis)\n\n"
                "Experimente perguntar por um desses nomes!"
            )

        dispatcher.utter_message(text=resposta, markdown=True)
        return []
