import telebot
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from keras.api._v2.keras.preprocessing import image

bot = telebot.TeleBot("your_Telebot_ID_here")
global flag
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Привет, чем помочь?")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "/register - зарегаться\n /login - ввести пароль\n /predict - бинарная классификация\n /logout - выйти")

@bot.message_handler(content_types=['text'])
def start(message):
    global flag
    if message.text == '/register':
        bot.send_message(message.from_user.id, "Круто, что ты хочешь зарегаться! Введи новый пароль!")
        bot.register_next_step_handler(message, get_pincode)
    elif message.text == '/login':
        bot.send_message(message.from_user.id, "Чтобы продолжить работу, введи пароль!")
        bot.register_next_step_handler(message, check_pincode)
    elif message.text == '/predict':
        if flag == 0:
            bot.send_message(message.from_user.id, "Отказано в доступе!")
        else:
            bot.send_message(message.from_user.id, "Присылайте вашу картинку!")
            bot.register_next_step_handler(message, predict_image)
    elif message.text == '/logout':
        flag = 0
        bot.send_message(message.from_user.id, "Вы вышли из системы!")
        bot.register_next_step_handler(message, check_pincode)
    else:
        bot.send_message(message.from_user.id, 'Напиши /help')

pincode = ''
def get_pincode(message):
    global pincode
    pincode = message.text
    with open('pincodes.txt', 'a') as f:
        f.write(pincode)
        f.write('\n')
    bot.send_message(message.from_user.id, 'Пароль сохранен!')

def check_pincode(message):
    global pincode
    global flag
    flag = 0
    pincode = message.text
    with open('pincodes.txt', 'r') as f:
        for line in f:
            if pincode in line:
                flag = 1
                break
            else:
                flag = 0
        if flag == 1:
             bot.send_message(message.from_user.id, 'Пароль совпал!')
        else:
             bot.send_message(message.from_user.id, 'Пароль не найден!')

def predict_image(message):
    file_photo = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_photo = bot.download_file(file_photo.file_path)

    new_photo = 'D:/Python_Projects_Univer/lab3_input_file/new_photo/new_photo.jpg'
    with open(new_photo, 'wb') as new_file:
        new_file.write(downloaded_photo)

    model = tf.keras.models.load_model('model.h5')
    img = image.load_img(new_photo, target_size=(200, 200))
    x = image.img_to_array(img)
    plt.imshow(x / 255.)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict(images, batch_size=10)
    print(classes[0])
    if classes[0] < 0.5:
        bot.send_message(message.from_user.id, 'Это коровка!')
    else:
        bot.send_message(message.from_user.id, 'Это человек!')

bot.infinity_polling()
