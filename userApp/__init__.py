# -*- coding: utf-8 -*-
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine


def create_app(db_url):
    # Инициализация Flask приложения
    usApp = Flask(__name__)
    # Указание конфигурации Flask-SQLAlchemy для работы с БД
    usApp.config['SQLALCHEMY_DATABASE_URI'] = db_url
    usApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    usApp.config['UPLOAD_FOLDER'] = 'C:/Users/kysya/Desktop/l7new/userApp/templates/static/imgs'
    usApp.config['TEMPLATES'] = 'C:/Users/kysya/PycharmProjects/pythonProject2/userApp/templates'
    return usApp


userApp = create_app('postgresql://postgres:klotorol159@127.0.0.1:5432/mos_rf')

#userApp = create_app('postgresql://maria:Q17hqPE249sRwtsf@127.0.0.1:5432/moss')


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# Создание сессии для БД
db = SQLAlchemy(userApp)
# Инициализация классов БД
from userApp.database import *

# Создание таблиц БД в соответствии с описанными классами
#with userApp.app_context():
 #   db.create_all()

# Инициализация интерфейсов
from userApp.interfaces import *

# Указание конфигурации Flask приложения
userApp.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)


def get_private(x):
    if x == 'Частная организация' or x=='Частная':
        return True
    return False


def database_set():
    data = pd.read_excel('C:\\Users\\kysya\\PycharmProjects\\pythonProject2\\full_clinic.xlsx')
    data.drop_duplicates()
    data = data.fillna('')
    for el in data['Регион'].unique():
        reg = Region(region_name=el)
        try:
            with userApp.app_context():
                db.session.add(reg)
                db.session.commit()
        except:
            print('Mistake regions')
    print('regions done')
    # Занесение в базу данных клиник
    regions = {}
    with userApp.app_context():
        r = Region.query.all()
    for i in range(90):
        regions[r[i].region_name] = r[i].id
    for index, row in data.iterrows():
        clinic = Clinic(name=row['Юридическое наименование'], short_name=row['Наименование'], is_private=get_private(row['Тип']), clinic_region=regions[row['Регион']],
                     clinic_legal_address= row['Юридический адрес'], inn = row['ИНН'], phone_numbers = row['Телефон'], leader = row['Руководитель'],
                     mail = row['E-mail'], nets = row['Сайт'], specialization = row['Специализация'])
        #try:
        with userApp.app_context():
            db.session.add(clinic)
            db.session.commit()
        #except:
    print('clinics done')

    # Занесение в базу данных министров здравоохранения по региону, их заместителей,
    # главных внештатных онкологов и оториноларингологов, руководителей региональных онкоцентров
    data = pd.read_excel('C:\\Users\\kysya\\PycharmProjects\\pythonProject2\\lpr.xlsx')
    data.drop_duplicates()
    data = data.fillna('')
    for index, row in data.iterrows():
        lpr = DecisionMaker(name=row['ФИО'], position=row['Должность'], dm_region=regions[row['Регион']], dm_phone= row['Телефон'],
                            dm_site = row['Сайт'], dm_mail = row['Мыло'], dm_tg = row['ТГ'], dm_ok = row['Одноклассники'],
                            dm_vk = row['ВК'], dm_facebook = row['FaceBook'])
        try:
            with userApp.app_context():
                db.session.add(lpr)
                db.session.commit()
        except:
            print('Mistake decizhon doers')

    print('lprs done')

#database_set()