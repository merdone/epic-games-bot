from abc import ABC, abstractmethod
from typing import List, Dict

class BaseParser(ABC):
    @abstractmethod
    def get_discount_games(self) -> list:
        pass

    @abstractmethod
    def get_info_from_game(self, game_data: dict) -> dict | None:
        pass

    def parse(self) -> List[Dict]:
        active_games = self.get_discount_games()
        clean_games = []

        for game_data in active_games:
            game_info = self.get_info_from_game(game_data)
            if game_info:
                clean_games.append(game_info)

        return clean_games