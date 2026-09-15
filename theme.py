"""Central color palette fot he game - synthwave neon theme"""

BACKGROUND_COLOR = "#0A0015"
STAR_COLORS = ("#FFFFFF", "#B8F1FF", "#FFD6F5", "#D9B8FF")

PLAYER_COLOR = "#FFF500"
BULLET_COLOR = "#FF2EC4"
ALIEN_BULLET_COLOR = "#39FF14"
BARRIER_COLOR = "#8A2BE2"

TEXT_COLOR = "#00FFF2"
GAME_OVER_COLOR = "#FF2EC4"
FONT = ("Courier", 16, "normal")
GAME_OVER_FONT = ("Courier", 24, "bold")

ALIEN_TIER_COLORS = [
    "#FF2EC4",
    "#C400FF",
    "#C400FF",
    "#00FFF2",
    "#00FFF2",
]

def alien_color_for_row(row_index):
    if row_index < len(ALIEN_TIER_COLORS):
        return ALIEN_TIER_COLORS[row_index]
    return ALIEN_TIER_COLORS[-1]

