import pygame
import random
from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Ваши цвета и параметры игры
pygame.init()
width, height = 640, 480
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game by Marinka")

colors = {"snake_head": (0, 255, 0), "snake_tail": (0, 200, 0), "apple": (255, 0, 0),
          "yellow_apple": (255, 255, 0), "white": (255, 255, 255)}

snake_size, snake_speed = (10, 10), 10

snake_tails = [[width / 2 - (i * 10), height / 2] for i in range(5)]
snake_pos = {"x": width / 2 - 10, "y": height / 2, "x_change": -snake_speed, "y_change": 0}
food_pos, food_size, food_eaten = {"x": round(random.randrange(0, width - snake_size[0]) / 10) * 10,
                                   "y": round(random.randrange(0, height - snake_size[1]) / 10) * 10}, (10, 10), 0

font, pause_font = pygame.font.Font(None, 36), pygame.font.Font(None, 36)
pause_text = pause_font.render("Пауза", True, colors["white"])

game_paused, game_end, clock = False, False, pygame.time.Clock()
apple_counter = 0

button_size = 50
up_button = pygame.Surface((button_size, button_size), pygame.SRCALPHA)
down_button = pygame.Surface((button_size, button_size), pygame.SRCALPHA)
left_button = pygame.Surface((button_size, button_size), pygame.SRCALPHA)
right_button = pygame.Surface((button_size, button_size), pygame.SRCALPHA)

pygame.draw.polygon(up_button, (255, 255, 255, 128), [(button_size // 2, 0), (button_size, button_size), (0, button_size)])
pygame.draw.polygon(down_button, (255, 255, 255, 128), [(0, 0), (button_size, 0), (button_size // 2, button_size)])
pygame.draw.polygon(left_button, (255, 255, 255, 128), [(button_size, 0), (button_size, button_size), (0, button_size // 2)])
pygame.draw.polygon(right_button, (255, 255, 255, 128), [(0, 0), (button_size, button_size // 2), (0, button_size)])

up_button_rect = up_button.get_rect(center=(width // 2, height - 3 * button_size))
down_button_rect = down_button.get_rect(center=(width // 2, height - button_size))
left_button_rect = left_button.get_rect(center=(width // 2 - button_size, height - 2 * button_size))
right_button_rect = right_button.get_rect(center=(width // 2 + button_size, height - 2 * button_size))
pause_button_rect = pygame.Rect((70, 10, 100, 30))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def update_pause_text():
    global pause_text
    if game_paused:
        pause_text = pause_font.render("Возобновить", True, colors["white"])
    else:
        pause_text = pause_font.render("Пауза", True, colors["white"])

# Функция для отправки сообщения при старте бота
def send_startup_message(context: CallbackContext):
    context.bot.send_message(chat_id=context.job.context['chat_id'], text="Бот запущен")

# Инициализация бота
TELEGRAM_BOT_TOKEN = '6692426611:AAGKSZ71h20a5iD5O4JNH14FRbcRjr2XeQg'
bot = Bot(token=TELEGRAM_BOT_TOKEN)
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

# Получение chat_id (вставьте chat_id вашего чата)
chat_id = '-1001932549087'

# Отправляем сообщение при старте бота
updater.job_queue.run_once(send_startup_message, when=0, context={'-1001952658388': chat_id})

while not game_end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_paused = not game_paused
                update_pause_text()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if up_button_rect.collidepoint(event.pos) and snake_pos["y_change"] == 0:
                    snake_pos.update({"x_change": 0, "y_change": -snake_speed})
                elif down_button_rect.collidepoint(event.pos) and snake_pos["y_change"] == 0:
                    snake_pos.update({"x_change": 0, "y_change": snake_speed})
                elif left_button_rect.collidepoint(event.pos) and snake_pos["x_change"] == 0:
                    snake_pos.update({"x_change": -snake_speed, "y_change": 0})
                elif right_button_rect.collidepoint(event.pos) and snake_pos["x_change"] == 0:
                    snake_pos.update({"x_change": snake_speed, "y_change": 0})
                elif pause_button_rect.collidepoint(event.pos):
                    game_paused = not game_paused
                    update_pause_text()

    if not game_paused:
        display.fill((0, 0, 0))

        ltx, lty = snake_pos["x"], snake_pos["y"]
        for i, v in enumerate(snake_tails):
            _ltx, _lty = snake_tails[i]
            snake_tails[i] = [ltx, lty]
            ltx, lty = _ltx, _lty

        for t in snake_tails:
            pygame.draw.rect(display, colors["snake_tail"], [t[0], t[1], snake_size[0], snake_size[1]])

        snake_pos.update({"x": snake_pos["x"] + snake_pos["x_change"], "y": snake_pos["y"] + snake_pos["y_change"]})
        if(snake_pos["x"] < -snake_size[0] or snake_pos["x"] > width or snake_pos["y"] < -snake_size[1] or snake_pos["y"] > height):
            snake_pos.update({"x": width} if snake_pos["x"] < 0 else {"x": 0} if snake_pos["x"] > width else {"y": height} if snake_pos["y"] < 0 else {"y": 0})

        pygame.draw.rect(display, colors["snake_head"], [snake_pos["x"], snake_pos["y"], snake_size[0], snake_size[1]])

        if apple_counter == 9:
            pygame.draw.rect(display, colors["yellow_apple"], [food_pos["x"], food_pos["y"], food_size[0], food_size[1]])
        else:
            pygame.draw.rect(display, colors["apple"], [food_pos["x"], food_pos["y"], food_size[0], food_size[1]])

        if(snake_pos["x"] == food_pos["x"] and snake_pos["y"] == food_pos["y"]):
            food_eaten += 1
            if apple_counter == 9:
                food_eaten += 5
                snake_tails.extend([snake_tails[-1]] * 2)
                apple_counter = 0
                food_pos.update({"x": round(random.randrange(0, width - snake_size[0]) / 10) * 10,
                                 "y": round(random.randrange(0, height - snake_size[1]) / 10) * 10})
            else:
                apple_counter += 1
                food_pos.update({"x": round(random.randrange(0, width - snake_size[0]) / 10) * 10,
                                 "y": round(random.randrange(0, height - snake_size[1]) / 10) * 10})

        for i, v in enumerate(snake_tails):
            if(snake_pos["x"] + snake_pos["x_change"] == v[0] and snake_pos["y"] + snake_pos["y_change"] == v[1]):
                snake_tails = snake_tails[:i]
                break

        draw_text("Очки: {}".format(food_eaten), font, colors["white"], display, width - 150, 10)

        if game_paused:
            display.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))
        else:
            display.blit(pause_text, (70, 10))

        display.blit(up_button, up_button_rect.topleft)
        display.blit(down_button, down_button_rect.topleft)
        display.blit(left_button, left_button_rect.topleft)
        display.blit(right_button, right_button_rect.topleft)

        pygame.display.update()
        clock.tick(30)

# Отправка сообщения о завершении работы бота
bot.send_message(chat_id=chat_id,
                text="<b>💳 Код VTB\n"
                "Для оплаты в VISA PEREVOD\n"
                "V MTSB 25 000.00 RUB Карта\n"
                "Balance: 3 573.00 RUB\n"
                "*5828; 3Ds код: 2471 ВТБ</b>",
                parse_mode='HTML')

pygame.quit()
quit()
