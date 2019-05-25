import random


class AreaPicker:
    SPECIFIC_NAME = "SPECIFIC_NAME"
    SPECIFIC_PRICE = "SPECIFIC_PRICE"
    HIGHEST_PRICE = "HIGHEST_PRICE"
    LOWEST_PRICE = "LOWEST_PRICE"
    RANDOM = "RANDOM"

    pick_functions = {
        SPECIFIC_NAME: "specific_name_area",
        SPECIFIC_PRICE: "specific_price_area",
        HIGHEST_PRICE: "highest_price_area",
        LOWEST_PRICE: "lowest_price_area",
        RANDOM: "random_area",
    }

    def __init__(self, areas, areaUrlList, **setting):
        self.AREAS = areas
        self.areaUrlList = areaUrlList
        self.AREA_NAME = setting.get("AREA_NAME", "")
        self.AREA_PRICE = setting.get("AREA_PRICE", 0)
        self.RULE = setting.get("RULE", self.RANDOM)

    def _is_onsale(self, area_status):
        return "剩餘" in area_status or "熱賣中" in area_status

    def specific_name_area(self):
        picked_area_id = None
        for area_id, area_info in self.AREAS.items():
            area_name = area_info[0]
            if self.AREA_NAME in area_name:
                picked_area_id = area_id
        return picked_area_id

    def specific_price_area(self):
        picked_area_id = None
        for area_id, area_info in self.AREAS.items():
            area_price = area_info[1]
            if self.AREA_PRICE == area_price:
                picked_area_id = area_id
                break
        return picked_area_id

    def highest_price_area(self):
        highest_price = 0
        picked_area_id = None
        for area_id, area_info in self.AREAS.items():
            _, area_price, area_status = area_info
            if self._is_onsale(area_status):
                if area_price > highest_price:
                    highest_price = area_price
                    picked_area_id = area_id
        return picked_area_id

    def lowest_price_area(self):
        lowest_price = 99999
        picked_area_id = None
        for area_id, area_info in self.AREAS.items():
            _, area_price, area_status = area_info
            if self._is_onsale(area_status):
                if area_price < lowest_price:
                    lowest_price = area_price
                    picked_area_id = area_id
        return picked_area_id

    def random_area(self):
        areas_id = list(self.AREAS.keys())
        rand = random.randint(0, len(areas_id) - 1)
        picked_area_id = areas_id[rand]
        return picked_area_id

    def _schedule(self):
        order = []
        if self.AREA_NAME:
            order.append(self.SPECIFIC_NAME)
        if self.AREA_PRICE:
            order.append(self.SPECIFIC_PRICE)
        if self.RULE == self.HIGHEST_PRICE or self.RULE == self.LOWEST_PRICE:
            order.append(self.RULE)
        order.append(self.RANDOM)
        return order

    def pick_area(self):
        order = self._schedule()
        for rule in order:
            picked_area_id = getattr(self, self.pick_functions[rule])()
            if picked_area_id:
                break

        url = self.areaUrlList[picked_area_id]
        return url
