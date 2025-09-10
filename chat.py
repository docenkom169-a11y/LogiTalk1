from customtkinter import *
from PIL import Image
from socket import *
import threading

class AuthWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('700x400')
        self.title('LogiTalk - Вхід')
        self.resizable(True, False)

        # ліва частина
        self.left_frame = CTkFrame(self)
        self.left_frame.pack(side = 'left', fill = 'both')

        image_ctk = CTkImage(light_image= Image.open('bg.png'), size=(450,400))
        self.image_label = CTkLabel(self.left_frame, text = 'Welcome', image = image_ctk,
                                    font = ('Helvetica', 60, 'bold'), text_color='white')
        self.image_label.pack()
        
        # права частина
        main_font = ('Helvetica', 20, 'bold')
        self.right_frame = CTkFrame(self, fg_color='white')
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side = 'right', fill = 'both', expand = 'True')

        CTkLabel(self.right_frame, text = 'LogiTalk', font = main_font, text_color='#6753cc').pack(pady = 60)
        self.name_entry = CTkEntry(self.right_frame, placeholder_text=">>>  Ім'я", height=45, font = main_font,
                                   fg_color="#d7d0fa", border_color="#c3b7fe", text_color='#6753cc', placeholder_text_color="#59527e")
        self.name_entry.pack(fill = 'x', padx= 15)
    

        img_ctk = CTkImage(light_image=Image.open('setting.png'), size=(20, 20))
        self.settings_button = CTkButton(self.right_frame, text='Налаштування', height=45,
                                         corner_radius=25, fg_color='#eae6ff', font=main_font, text_color='#6753cc', image=img_ctk, compound='left')
        self.settings_button.pack(fill='x', padx=10, pady=5)
 
        self.connect_button = CTkButton(self.right_frame, text='УВІЙТИ', height=45,
                                         corner_radius=25, fg_color='#d06fc0', font=main_font,
                                           text_color='white', command= self.open_chat)
        self.connect_button.pack(fill='x', padx=50, pady=10)

    def open_chat(self):
        username = self.name_entry.get().strip()
        if not username:
            username = 'Noname'
            return username
        self.destroy()
        chat_window = MainWindow(username)
        chat_window.mainloop()



class MainWindow(CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username

        # візуальна частина
        self.geometry('800x600')
        self.title('LogiTalk')
        self.minsize(400, 400)

        # налаштування для меню
        self.menu_width = 50
        self.target_menu_width = 50
        self.is_show_menu = False
        self.speed_menu = 5

        # вигляд меню
        self.menu_frame = CTkFrame(self, width=self.menu_width, height=600)
        self.menu_frame.pack_propagate(False) 
        self.menu_frame.place(x = 0, y = 0)

        # кнопка для розгортання меню
        self.btn_menu = CTkButton(self, text='M', width=50, command=self.click_show_menu)
        self.btn_menu.place(x = 0, y = 0)

        # місце для чату
        self.chat_field = CTkTextbox(self, font= ('Arial', 14, 'bold'), state = 'disable')
        self.chat_field.place(x = 0, y = 0)

        self.message_entry = CTkEntry(self, height = 40, placeholder_text='Введіть повідомлення')

        self.btn_send = CTkButton(self, text = '>', width=40, height= 40, command= self.send_message)

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('6.tcp.eu.ngrok.io', 19418))
            hello = f'{self.username} приєднався(-лася) до чату!\n'
            self.sock.send(hello.encode('utf-8'))
            threading.Thread(target= self.recv_message, daemon= True).start()
        except:
            self.add_message(f'Невдалося приєднатися до серверу!')


        self.adaptive_ui()
        

    def adaptive_ui(self):
        SCALE = 1.25 # 125% = 1.25   75% = 0.75
        width = self.winfo_width() / SCALE
        height = self.winfo_height() / SCALE


        self.menu_frame.configure(height = height)

        input_panel_height = 60
        spacing = 10

        # chat
        chat_x = self.menu_width + 10
        chat_width = width - self.menu_width - 30
        chat_height = height - input_panel_height - spacing

        self.chat_field.place(x = chat_x, y = 0)
        self.chat_field.configure(width = chat_width, height = chat_height)

        # поле для введення повідомлення
        entry_width = width - self.menu_width - 100
        entry_y = height - input_panel_height

        self.message_entry.place(x = chat_x, y = entry_y)
        self.message_entry.configure(width = entry_width)

        # кнопка відправити
        self.btn_send.place(x = chat_x + entry_width + 10, y = entry_y)

        self.after(10, self.adaptive_ui)


    # клік по меню
    def click_show_menu(self):
        self.is_show_menu = not self.is_show_menu
        self.target_menu_width = 200 if self.is_show_menu else 50
        self.btn_menu.configure(text = 'MENU' if self.is_show_menu else 'M')

        if self.is_show_menu:
            self.label = CTkLabel(self.menu_frame, text="Ім'я")
            self.label.pack(pady = 30)
            self.entry = CTkEntry(self.menu_frame, placeholder_text="Введіть нове ім'я")
            self.entry.pack()
        else:
            if self.label:
                self.label.destroy()
            if self.entry:
                self.entry.destroy()
        
        self.animate_menu()



    # анімація меню
    def animate_menu(self):
        if self.menu_width != self.target_menu_width:
            if self.menu_width < self.target_menu_width:
                # відкриває меню від 50 + 5 поки не дійде 200
                self.menu_width = min(self.menu_width + self.speed_menu, self.target_menu_width)
            else:
                self.menu_width = max(self.menu_width - self.speed_menu, self.target_menu_width)

            self.menu_frame.configure(width = self.menu_width)
            self.after(10, self.animate_menu)

    def add_message(self, text):
        self.chat_field.configure(state = 'normal')
        self.chat_field.insert(END, f'{text}\n')
        self.chat_field.configure(state = 'disable')
    
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.add_message(f'{self.username}: {message}')
            data = f'TEXT@{self.username}@{message}\n' #'TEXT@Bohdan@Hi\n'
            try:
                self.sock.sendall(data.encode())
            except:
                pass
        self.message_entry.delete(0,END)

    def recv_message(self):
        buffer = ''
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()

                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()


    def handle_line(self, line):
        if not line:
            return
        parts = line.split('@', 3) #[msg_type, author, msg]
        msg_type = parts[0]

        if msg_type == 'TEXT':
            if len(parts) >= 3:
                author = parts[1]
                msg = parts[2]
                self.add_message(f'{author}: {msg}')

        else: self.add_message(line)

window = AuthWindow()
window.mainloop()
