class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id
        self.score = 0
        damaged_points = 0
        gained_points = 0
        self.role = ""

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score,
            "dpoints": self.damaged_points,
            "gpoints": self.gained_points,
        }

    def damaged_points(self, points):
        self.damaged_points = points

    def gained_points(self, points):
        self.gained_points = points

    def update_score(self, points):
        self.score += points

    def set_role(self, role):
        self.role = role

    def __str__(self):
        return f"Player: {self.name} (ID: {self.player_id}), Role: {self.role}, Score: {self.score}"
