import pygame
import random
import math
import time

WIDTH, HEIGHT = 800, 560
FPS = 60
BG = (30, 35, 25)

PLAYER_SPEED = 4

PLAYER_MAX_HP = 3
INVINCIBILITY_TIME = 1000

MAX_AMMO = 12
RELOAD_TIME = 2000

BARREL_COUNT = 4
EXPLOSION_RADIUS = 100
EXPLOSION_DURATION = 300


class Zombie:
    SPEED = 1.5
    HP = 3
    SIZE = 30
    COLOR = (60, 140, 60)

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.color = self.COLOR
        self.hp = self.HP
        self.wobble = random.uniform(0, 6.28)
        self.frame = 0

    def update(self, player_pos):
        px, py = player_pos
        cx, cy = self.rect.center
        dx, dy = px - cx, py - cy
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist:
            self.rect.x += int(dx / dist * self.SPEED)
            self.rect.y += int(dy / dist * self.SPEED)
        self.frame += 1

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        wobble_y = int(math.sin(self.frame * 0.2) * 3)
        draw_rect = self.rect.move(0, wobble_y)
        pygame.draw.rect(screen, self.color, draw_rect, border_radius=5)

        eye_y = draw_rect.y + draw_rect.height // 3
        eye_size = max(2, draw_rect.width // 8)

        pygame.draw.circle(
            screen, (200, 40, 40),
            (draw_rect.x + draw_rect.width // 3, eye_y),
            eye_size
        )
        pygame.draw.circle(
            screen, (200, 40, 40),
            (draw_rect.x + (draw_rect.width * 2) // 3, eye_y),
            eye_size
        )


class FastZombie(Zombie):
    SPEED = 3.0
    HP = 1
    SIZE = 20
    COLOR = (220, 180, 40)


class TankZombie(Zombie):
    SPEED = 0.8
    HP = 6
    SIZE = 45
    COLOR = (150, 60, 150)


def spawn_zombie(width, height, player_rect, zombie_type="standard", margin=120):
    if zombie_type == "fast":
        zombie_class = FastZombie
    elif zombie_type == "tank":
        zombie_class = TankZombie
    else:
        zombie_class = Zombie

    size = zombie_class.SIZE

    while True:
        x = random.randint(0, width - size)
        y = random.randint(0, height - size)
        rect = pygame.Rect(x, y, size, size)

        if not rect.colliderect(player_rect.inflate(margin, margin)):
            return zombie_class(x, y)


class Barrel:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 36)

    def draw(self, screen):
        pygame.draw.rect(
            screen, (170, 90, 35), self.rect, border_radius=5
        )
        pygame.draw.line(
            screen, (80, 45, 20),
            (self.rect.left, self.rect.top + 9),
            (self.rect.right, self.rect.top + 9), 3
        )
        pygame.draw.line(
            screen, (80, 45, 20),
            (self.rect.left, self.rect.bottom - 9),
            (self.rect.right, self.rect.bottom - 9), 3
        )


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (60, 160, 220)
        self.bullets = []
        self.shoot_cooldown = 0

        # Task 1: Health
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.invincible_until = 0

        # Task 2: Ammo
        self.ammo = MAX_AMMO
        self.max_ammo = MAX_AMMO
        self.reload_start = None

    def move(self, keys, width, height):
        dx = dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED

        self.rect.x = max(
            0, min(width - self.rect.width, self.rect.x + dx)
        )
        self.rect.y = max(
            0, min(height - self.rect.height, self.rect.y + dy)
        )

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self, target_pos):
        if self.reload_start is not None:
            return

        if self.ammo <= 0:
            self.start_reload()
            return

        if self.shoot_cooldown > 0:
            return

        cx, cy = self.rect.center
        tx, ty = target_pos
        dx, dy = tx - cx, ty - cy
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist == 0:
            return

        vx, vy = dx / dist * 10, dy / dist * 10
        self.bullets.append([cx - 4, cy - 4, vx, vy])

        self.ammo -= 1
        self.shoot_cooldown = 15

        if self.ammo == 0:
            self.start_reload()

    def start_reload(self):
        if self.reload_start is None:
            self.reload_start = pygame.time.get_ticks()

    def update_reload(self):
        if self.reload_start is None:
            return

        elapsed = pygame.time.get_ticks() - self.reload_start

        if elapsed >= RELOAD_TIME:
            self.ammo = self.max_ammo
            self.reload_start = None

    def get_reload_remaining(self):
        if self.reload_start is None:
            return None

        elapsed = pygame.time.get_ticks() - self.reload_start
        remaining = max(0, RELOAD_TIME - elapsed)
        return remaining / 1000

    def update_bullets(self, width, height):
        live = []

        for b in self.bullets:
            b[0] += b[2]
            b[1] += b[3]

            if 0 <= b[0] <= width and 0 <= b[1] <= height:
                live.append(b)

        self.bullets = live

    def draw(self, screen):
        current_time = pygame.time.get_ticks()

        if current_time < self.invincible_until:
            if (current_time // 100) % 2 == 0:
                pygame.draw.rect(
                    screen, self.color, self.rect, border_radius=6
                )
        else:
            pygame.draw.rect(
                screen, self.color, self.rect, border_radius=6
            )

        for b in self.bullets:
            pygame.draw.circle(
                screen, (255, 220, 60),
                (int(b[0]), int(b[1])), 5
            )


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Escape")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20)
        self.big_font = pygame.font.SysFont("monospace", 44, bold=True)
        self.reset()

    def reset(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)

        # FIX: Spawn enough zombies to complete Wave 1.
        self.wave = 1
        self.kills = 0
        self.kills_to_next = 8

        self.zombies = []

        for _ in range(self.kills_to_next):
            self.zombies.append(
                spawn_zombie(
                    WIDTH, HEIGHT, self.player.rect, "standard"
                )
            )

        self.barrels = []
        self.create_barrels()
        self.explosions = []

        self.score = 0
        self.game_over = False
        self.start_time = time.time()

    def create_barrels(self):
        self.barrels = []
        attempts = 0

        while len(self.barrels) < BARREL_COUNT and attempts < 1000:
            attempts += 1

            x = random.randint(40, WIDTH - 70)
            y = random.randint(70, HEIGHT - 70)

            new_rect = pygame.Rect(x, y, 28, 36)

            if new_rect.colliderect(
                self.player.rect.inflate(150, 150)
            ):
                continue

            overlaps = False

            for barrel in self.barrels:
                if new_rect.colliderect(barrel.rect.inflate(40, 40)):
                    overlaps = True
                    break

            if not overlaps:
                self.barrels.append(Barrel(x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and not self.game_over
                and event.button == 1
            ):
                self.player.shoot(event.pos)

        return True

    def handle_player_damage(self):
        current_time = pygame.time.get_ticks()

        for z in self.zombies:
            if z.rect.colliderect(self.player.rect):
                if current_time >= self.player.invincible_until:
                    self.player.hp -= 1
                    self.player.invincible_until = (
                        current_time + INVINCIBILITY_TIME
                    )

                    if self.player.hp <= 0:
                        self.player.hp = 0
                        self.game_over = True

                    break

    def handle_barrel_collisions(self):
        exploded_barrels = []

        for barrel in self.barrels:
            for bullet in self.player.bullets[:]:
                bx, by = int(bullet[0]), int(bullet[1])

                if barrel.rect.collidepoint(bx, by):
                    exploded_barrels.append(barrel)

                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)

                    break

        for barrel in exploded_barrels:
            if barrel not in self.barrels:
                continue

            explosion_center = barrel.rect.center

            self.explosions.append({
                "center": explosion_center,
                "start": pygame.time.get_ticks()
            })

            dead_zombies = []

            for zombie in self.zombies:
                zx, zy = zombie.rect.center
                dx = zx - explosion_center[0]
                dy = zy - explosion_center[1]
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance <= EXPLOSION_RADIUS:
                    dead_zombies.append(zombie)

            for zombie in dead_zombies:
                if zombie in self.zombies:
                    self.zombies.remove(zombie)
                    self.kills += 1
                    self.score += 10

            self.barrels.remove(barrel)

    def handle_zombie_shooting(self):
        dead = []

        for zombie in self.zombies:
            for bullet in self.player.bullets[:]:
                bx, by = int(bullet[0]), int(bullet[1])

                if zombie.rect.collidepoint(bx, by):
                    if zombie.hit():
                        dead.append(zombie)

                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)

                    break

        for zombie in dead:
            if zombie in self.zombies:
                self.zombies.remove(zombie)
                self.kills += 1
                self.score += 10

    def next_wave(self):
        if self.kills < self.kills_to_next:
            return

        self.kills = 0
        self.wave += 1
        self.kills_to_next = 8 + self.wave * 2

        # FIX: Spawn exactly enough zombies to finish the new wave.
        for _ in range(self.kills_to_next):
            roll = random.random()

            if self.wave >= 2 and roll < 0.20:
                zombie_type = "fast"
            elif self.wave >= 3 and roll < 0.30:
                zombie_type = "tank"
            else:
                zombie_type = "standard"

            self.zombies.append(
                spawn_zombie(
                    WIDTH, HEIGHT, self.player.rect, zombie_type
                )
            )

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()

        self.player.move(keys, WIDTH, HEIGHT)
        self.player.update_bullets(WIDTH, HEIGHT)
        self.player.update_reload()

        self.score = int(time.time() - self.start_time)

        for zombie in self.zombies:
            zombie.update(self.player.rect.center)

        self.handle_player_damage()
        self.handle_barrel_collisions()
        self.handle_zombie_shooting()
        self.next_wave()

        current_time = pygame.time.get_ticks()

        self.explosions = [
            explosion
            for explosion in self.explosions
            if current_time - explosion["start"] < EXPLOSION_DURATION
        ]

    def draw_background(self):
        self.screen.fill(BG)

        for x in range(0, WIDTH, 60):
            pygame.draw.line(
                self.screen, (40, 45, 35),
                (x, 0), (x, HEIGHT), 1
            )

        for y in range(0, HEIGHT, 60):
            pygame.draw.line(
                self.screen, (40, 45, 35),
                (0, y), (WIDTH, y), 1
            )

    def draw_explosions(self):
        current_time = pygame.time.get_ticks()

        for explosion in self.explosions:
            elapsed = current_time - explosion["start"]
            progress = elapsed / EXPLOSION_DURATION

            radius = int(
                20 + (EXPLOSION_RADIUS - 20) * progress
            )

            center = explosion["center"]

            pygame.draw.circle(
                self.screen, (255, 100, 20),
                center, radius, 5
            )

            pygame.draw.circle(
                self.screen, (255, 220, 60),
                center, max(5, radius // 3)
            )

    def draw_hud(self):
        hud_bg = pygame.Rect(0, 0, WIDTH, 55)

        pygame.draw.rect(
            self.screen, (15, 20, 15), hud_bg
        )

        reload_remaining = self.player.get_reload_remaining()

        if reload_remaining is not None:
            reload_text = f"RELOADING {reload_remaining:.1f}s"
        else:
            reload_text = ""

        hud_text = (
            f"HP: {self.player.hp}/{self.player.max_hp}  "
            f"Ammo: {self.player.ammo}/{self.player.max_ammo}  "
            f"Wave: {self.wave}  "
            f"Score: {self.score}  "
            f"Kills: {self.kills}/{self.kills_to_next}"
        )

        hud = self.font.render(
            hud_text,
            True,
            (160, 220, 120)
        )

        self.screen.blit(hud, (8, 5))

        if reload_text:
            reload_surface = self.font.render(
                reload_text,
                True,
                (255, 180, 60)
            )
            self.screen.blit(reload_surface, (8, 30))

    def draw_game_over(self):
        if not self.game_over:
            return

        overlay = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        message = self.big_font.render(
            "DEVOURED!",
            True,
            (180, 40, 40)
        )

        subtitle = self.font.render(
            f"Wave {self.wave} | Score {self.score} | Press R",
            True,
            (200, 200, 200)
        )

        self.screen.blit(
            message,
            (
                WIDTH // 2 - message.get_width() // 2,
                HEIGHT // 2 - 40
            )
        )

        self.screen.blit(
            subtitle,
            (
                WIDTH // 2 - subtitle.get_width() // 2,
                HEIGHT // 2 + 20
            )
        )

    def draw(self):
        self.draw_background()

        for barrel in self.barrels:
            barrel.draw(self.screen)

        for zombie in self.zombies:
            zombie.draw(self.screen)

        self.player.draw(self.screen)
        self.draw_explosions()
        self.draw_hud()
        self.draw_game_over()

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()
