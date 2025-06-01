from typing import Optional
import random
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

# --- Helper Functions ---

def distance(A: Position, B: Position):
    return abs(A.x - B.x) + abs(A.y - B.y)

def distanceWithTeleporter(near_teleporter: int, Destination: Position, far_teleporter: Position):
    return near_teleporter + distance(Destination, far_teleporter)

def goToBase(distance_base: int, distance_with_tele: int, base: Position, teleporter: Position, current_position: Position):
    if distance_base <= distance_with_tele:
        delta_x, delta_y = get_direction(current_position.x, current_position.y, base.x, base.y)
    else:
        delta_x, delta_y = get_direction(current_position.x, current_position.y, teleporter.x, teleporter.y)

    if delta_x == delta_y:
        delta_x = 0
        delta_y = pow(-1, random.randint(0, 1))

    return delta_x, delta_y

# --- Efficient Greedy Algorithm ---

def efficientGreedyAlgorithm(diamonds, teleporter, redButton, base, current_position, props, near_teleporter, last_goal):
    min_dist = 1000
    goal = None
    jumlahDiamond = 0

    # Caching: kalau goal sebelumnya masih valid → teruskan
    if last_goal is not None:
        goal = last_goal

    # Pilih target baru kalau belum ada goal
    if goal is None:
        for diamond in diamonds:
            jumlahDiamond += 1
            if not (diamond.properties.points == 2 and props.diamonds >= 4):
                dist = distance(current_position, diamond.position)
                dist_with_tele = distanceWithTeleporter(near_teleporter, diamond.position, teleporter[1].position)

                if dist < min_dist:
                    if dist <= dist_with_tele:
                        goal = diamond.position
                        min_dist = dist
                    else:
                        goal = teleporter[0].position
                        min_dist = dist_with_tele
                elif dist_with_tele < min_dist:
                    goal = teleporter[0].position
                    min_dist = dist_with_tele

    # Cek red button
    positionRedButton = redButton.position
    distRedButton = distance(current_position, positionRedButton)
    distRedButtonTeleport = distanceWithTeleporter(near_teleporter, positionRedButton, teleporter[1].position)

    if distRedButtonTeleport <= distRedButton:
        positionRedButton = teleporter[1].position
        distRedButton = distRedButtonTeleport

    if (jumlahDiamond <= 6 and distRedButton <= min_dist):
        goal = positionRedButton

    # Fallback: kalau tidak ada goal (diamond habis)
    if goal is None:
        goal = base

    # Reset goal jika sudah sampai
    if goal == current_position:
        goal = None
    
    # Gerakan ke goal
    delta_x, delta_y = get_direction(current_position.x, current_position.y, goal.x, goal.y)

    if delta_x == delta_y:
        delta_x = 0
        delta_y = pow(-1, random.randint(0, 1))

    # Optional: Logging buat laporan
    print(f"[INFO] Current Target: ({goal.x}, {goal.y})")

    return delta_x, delta_y, goal

# --- Main Logic Class ---

class divaRacing(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        base = board_bot.properties.base
        diamonds = []
        bots = []
        teleporter = []

        for object in board.game_objects:
            if object.type == "DiamondGameObject":
                diamonds.append(object)
            elif object.type == "BotGameObject":
                bots.append(object)
            elif object.type == "TeleportGameObject":
                teleporter.append(object)
            elif object.type == "DiamondButtonGameObject":
                redButton = object

        teleporter_distance = [distance(d.position, current_position) for d in teleporter]
        if teleporter_distance[0] > teleporter_distance[1]:
            near_teleporter = teleporter_distance[1]
            teleporter[0], teleporter[1] = teleporter[1], teleporter[0]
        else:
            near_teleporter = teleporter_distance[0]

        dist_base = distance(current_position, base)
        dist_base_teleport = distanceWithTeleporter(near_teleporter, base, teleporter[1].position)

        # --- PRIORITY HANDLING ---

        # ⿡ Pulang ke base kalau waktu sekarat
        if props.diamonds > 0 and board_bot.properties.milliseconds_left < 10000:
            print("[INFO] Emergency Return to Base")
            return goToBase(dist_base, dist_base_teleport, base, teleporter[0].position, current_position)

        # ⿢ Bunuh bot lawan (greedy tackle)
        for bot in bots:
            if bot.properties.name != board_bot.properties.name:
                dist_to_bot = distance(current_position, bot.position)
                if (dist_to_bot < 3 and bot.properties.diamonds > 2) or dist_to_bot == 1:
                    print(f"[INFO] ATTACK Target: ({bot.position.x}, {bot.position.y})")
                    return get_direction(current_position.x, current_position.y, bot.position.x, bot.position.y)

        # ⿣ Pulang ke base kalau inventory penuh
        if props.diamonds == 5 or (props.diamonds > 2 and dist_base < 2):
            print("[INFO] Return to Base (Inventory Full)")
            return goToBase(dist_base, dist_base_teleport, base, teleporter[0].position, current_position)

        # ⿤ Else: Efficient Greedy
        delta_x, delta_y, new_goal = efficientGreedyAlgorithm(
            diamonds, teleporter, redButton, base, current_position, props, near_teleporter, self.goal_position
        )

        # Update caching goal
        self.goal_position = new_goal
        return delta_x,delta_y
