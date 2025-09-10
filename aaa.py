from customtkinter import *
from PIL import Image

class AuthWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title('LoginTalk - Вхід')
        self.resizable(True,False)


        self.left_frame = CTkFrame(self)
        self.left_frame.pack(side = 'left', fill = 'both')

        image_ctk = CTkImage(light_image= Image.open('bg.png'), size=(450,400))
        self.image_label = CTkLabel(self.left_frame, text = 'Welcome', image = image_ctk,
                                    font = ('Helvetica', 60, 'bold'), text_color='white')
        self.image_label.pack()

        main_font = ('Helvetica', 20, 'bold')
        self.right_frame = CTkFrame(self, fg_color='white')
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side = 'right', fill = 'both', expand = 'True')

        CTkLabel(self.right_frame , text = 'LogiTalk' , font = main_font , text_color ='#6753cc').pack(pady =60)
        self.name_entry = CTkEntry(self.right_frame, placeholder_text="--> Ім'я", height=45, font = main_font,
        fg_color="#d7d0fa", border_color="#c3b7fe", text_color="#6753cc", placeholder_text_color="#59527e")
        self.name_entry.pack(fill = 'x', padx= 15)

        
        img_ctk = CTkImage(light_image=Image.open('setting.png'), size=(20, 20))
        self.settings_button = CTkButton(self.right_frame, text='Налаштування', height=45,
                                         corner_radius=25, fg_color='#eae6ff', font=main_font, text_color='#6753cc', image=img_ctk, compound='left')
        self.settings_button.pack(fill='x', padx=10, pady=5)
 
        self.connect_button = CTkButton(self.right_frame, text='УВІЙТИ', height=45,
                                         corner_radius=25, fg_color='#d06fc0', font=main_font, text_color='white')
        self.connect_button.pack(fill='x', padx=50, pady=10)




login_window = AuthWindow()
login_window.mainloop()