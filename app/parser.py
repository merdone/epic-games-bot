import requests
from datetime import datetime

URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"


def get_discount_games() -> list:
    free_games = []

    try:
        request_result = requests.get(URL, timeout=10)
        request_result.raise_for_status()
        request_dict = request_result.json()
    except (requests.RequestException, ValueError):
        return []

    data = request_dict.get('data', {})
    if not data:
        return []

    catalog = data.get('Catalog', {})
    search_store = catalog.get('searchStore', {})
    elements = search_store.get('elements', [])

    if not elements:
        return []

    for element in elements:
        try:
            price_info = element.get("price", {}).get("totalPrice", {})
            discount_price = price_info.get("discountPrice")

            if discount_price is None or discount_price != 0:
                continue

            promotions = element.get("promotions")
            if not promotions:
                continue

            active_promos = promotions.get("promotionalOffers", [])
            if not active_promos or len(active_promos) == 0:
                continue

            offer_group = active_promos[0].get("promotionalOffers", [])
            if not offer_group or len(offer_group) == 0:
                continue

            discount_setting = offer_group[0].get("discountSetting", {})
            discount_percentage = discount_setting.get("discountPercentage")

            if discount_percentage == 0:
                free_games.append(element)

        except (KeyError, IndexError, TypeError, AttributeError):
            continue

    return free_games


def get_info_from_game(game_data: dict) -> dict | None:
    try:
        result = {}

        title = game_data.get("title")
        if not title:
            return None
        result["name"] = title

        description = game_data.get("description")
        if not description:
            return None
        result["description"] = description

        slug = game_data.get('productSlug')

        if not slug:
            mappings = game_data.get('catalogNs', {}).get('mappings', [])
            if mappings and isinstance(mappings, list) and len(mappings) > 0:
                slug = mappings[0].get('pageSlug')

        if not slug:
            offer_mappings = game_data.get('offerMappings', [])
            if offer_mappings and isinstance(offer_mappings, list) and len(offer_mappings) > 0:
                slug = offer_mappings[0].get('pageSlug')

        if not slug:
            return None

        result["link"] = f"https://store.epicgames.com/en-US/p/{slug}"

        game_id = game_data.get("id", -1)
        if game_id == -1:
            return None
        result["game_id"] = game_id

        promotions = game_data.get("promotions")
        if not promotions:
            return None

        promotional_offers = promotions.get("promotionalOffers")
        if not promotional_offers or len(promotional_offers) == 0:
            return None

        offer_block = promotional_offers[0].get("promotionalOffers")
        if not offer_block or len(offer_block) == 0:
            return None

        start_date_str = offer_block[0].get("startDate")
        end_date_str = offer_block[0].get("endDate")

        if start_date_str:
            try:
                dt_start = datetime.fromisoformat(start_date_str)
                if not dt_start:
                    return None
                result["start_date"] = dt_start
            except ValueError:
                return None

        if end_date_str:
            try:
                dt_end = datetime.fromisoformat(end_date_str)
                if not dt_end:
                    return None
                result["end_date"] = dt_end
            except ValueError:
                return None

        key_images = game_data.get("keyImages")
        if key_images and len(key_images) > 0:
            image_url = key_images[0].get("url")
            result["image_url"] = image_url
        else:
            return None

        return result

    except (KeyError, IndexError, TypeError, AttributeError):
        return None
