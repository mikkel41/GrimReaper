import turtle
import time
import os
import requests
import threading

DARKRED = "\033[38;5;88m"
RESET = "\033[0m"

def intro_animation():
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.setup(width=1.0, height=1.0)
    screen.title("Grim Reaper Webhook KILLER")

    w = screen.window_width()
    h = screen.window_height()

    t = turtle.Turtle()
    t.color("red")
    t.speed(0)
    t.width(3)
    t.hideturtle()

    a = 0
    b = 0
    scale = min(w, h) / 800

    t.penup()
    t.goto(0, h // 2 - 120)
    t.pendown()

    turtle.tracer(0)
    while b < 220:
        t.forward(a * scale)
        t.right(b)
        a += 3
        b += 1
        turtle.update()
        time.sleep(0.01)

    time.sleep(0.5)
    screen.bye()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def send_single(webhook, message):
    try:
        r = requests.post(webhook, json={"content": message})
        if r.status_code in (200, 204):
            print("SENT")
        else:
            print(f"ERROR {r.status_code}")
    except Exception as e:
        print(f"ERROR {e}")

def send_webhooks_fast(webhook, message, amount, ping_everyone):
    if ping_everyone:
        message = "@everyone " + message
    threads = []
    for _ in range(amount):
        t = threading.Thread(target=send_single, args=(webhook, message))
        t.start()
        threads.append(t)
        time.sleep(0.1)  # ~10 messages/sec
    for t in threads:
        t.join()
    print("\nJOB FINISHED")

def terminal_ui():
    clear()
    ascii_text = DARKRED + r"""
   ██████╗ ██████╗ ██╗███╗   ███╗    ██████╗ ███████╗ █████╗ ██████╗ ███████╗██████╗
  ██╔════╝ ██╔══██╗██║████╗ ████║    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗
  ██║  ███╗██████╔╝██║██╔████╔██║    ██████╔╝█████╗  ███████║██████╔╝█████╗  ██████╔╝
  ██║   ██║██╔══██╗██║██║╚██╔╝██║    ██╔══██╗██╔══╝  ██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
  ╚██████╔╝██║  ██║██║██║ ╚═╝ ██║    ██║  ██║███████╗██║  ██║██║     ███████╗██║  ██║
   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
""" + RESET
    print(ascii_text)

    webhook = input(DARKRED + "Webhook URL > " + RESET).strip()
    message = input(DARKRED + "Message > " + RESET).strip()
    amount = int(input(DARKRED + "Amount > " + RESET))
    ping_input = input(DARKRED + "Ping @everyone? (Yes/No) > " + RESET).strip().lower()
    ping_everyone = ping_input in ["yes", "y"]

    print("\nEXECUTING...\n")
    send_webhooks_fast(webhook, message, amount, ping_everyone)

intro_animation()
terminal_ui()
