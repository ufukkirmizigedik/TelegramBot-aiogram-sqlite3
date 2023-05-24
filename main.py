import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
import sqlite3
import datetime
from keyboards import kb_client
from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import time
import aiogram.utils.markdown as md
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
from keyboard2 import kb_client2
from aylar import kb_client4
from send_email import send_me
from aiogram.dispatcher import filters
from admin import kb_client3
import aioschedule
import json
import requests
from bs4 import BeautifulSoup
import emoji
from aiogram.types import ParseMode

storage = MemoryStorage()

API_TOKEN = '5345912328:AAE-MwLrqEakFTMNPePE2696tOHSWUmF13M'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=storage)


base = sqlite3.connect('ops.db')
cur = base.cursor()
if base:
    print('Data base connected')
base.execute('CREATE TABLE IF NOT EXISTS fakt(user_id INTEGER, name TEXT, ems INTEGER, pismo INTEGER, posilka INTEGER, sale INTEGER ,data TEXT)')
base.commit()


base = sqlite3.connect('ops.db')
cur = base.cursor()
if base:
    print('Data base connected')
base.execute('CREATE TABLE IF NOT EXISTS plan(plan_sales INTEGER,  plan_ems INTEGER, plan_pismo INTEGER, plan_posilka INTEGER,data TEXT)')

class Test(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()

class Plan(StatesGroup):
    plan = State()
    plan1 = State()
    plan2 = State()
    plan3 = State()
    plan4 = State()


""" *****************************************    НАЧИНАЕМ   ******************************************"""
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Добрый день! Я бот. Я помогу тебе отправить отчет, покажу результат дня и наглядный отчет твоей работы за месяц. Раздел Admin создан для руководителей, поэтому работай, стремись и у тебя тоже будет доступ :) ", reply_markup=kb_client)
"""   """

@dp.message_handler(commands="Лучшее_сотрудники_месяца")
async def best(message: types.Message):
    base = sqlite3.connect('ops.db')
    cur = base.cursor()
    best = cur.execute("SELECT name,MAX(totalsale) FROM (SELECT name,SUM(sale) as totalsale FROM fakt GROUP BY name)").fetchone()
    bist = cur.execute("SELECT name,MAX(totalems) FROM (SELECT name,SUM(ems) as totalems FROM fakt GROUP BY name)").fetchone()
    base.commit()
    await bot.send_message(message.chat.id,
                           md.text(
                           md.text('Лучшее продаж : ', md.bold(best[0],best[1],'руб')),'\n',
                           md.text('Лучшее емс    :     ',md.bold(bist[0],bist[1],'шт'))))




"""  *****************************************   СОБИРАЕМ ПЛАН   **************************************    """
@dp.message_handler(commands = "План_месяц")
async def send_plan(message: types.Message):
    await message.answer('План в розничных продажах на месяц?')
    await Plan.plan.set()

@dp.message_handler(state=Plan.plan)
async def plan_sale(message: types.Message,state:FSMContext):
    async with state.proxy() as pla :
        pla['plan'] = message.text
        time.sleep(1)
        await Plan.next()
        await message.answer('План емс на месяц?')

@dp.message_handler(state=Plan.plan1)
async def plan_ems(message: types.Message,state:FSMContext):
    async with state.proxy() as pla :
        pla['plan1'] = message.text
        time.sleep(1)
        await Plan.next()
        await message.answer('План по количеству писем 1 класса на месяц?')

@dp.message_handler(state=Plan.plan2)
async def plan_pismo(message: types.Message,state:FSMContext):
    async with state.proxy() as pla :
        pla['plan2'] = message.text
        time.sleep(1)
        await Plan.next()
        await message.answer('План по количеству посылок 1 класса на месяц?')

@dp.message_handler(state=Plan.plan3)
async def plan_posilok(message: types.Message,state:FSMContext):
    async with state.proxy() as pla :
        pla['plan3'] = message.text
        time.sleep(1)
        await Plan.next()
        await message.answer('Какой месяц ?',reply_markup=kb_client4)

@dp.message_handler(state=Plan.plan4)
async def plan_plans(message: types.Message,state:FSMContext):
    async with state.proxy() as pla :
        pla['plan4'] = message.text
        time.sleep(1)
        sqlite3.connect('ops.db')
        psales = pla['plan']
        pems = pla['plan1']
        ppismo = pla['plan2']
        pposilka =pla['plan3']
        data = pla['plan4']
        base = sqlite3.connect('ops.db')
        cur = base.cursor()
        cur.execute("INSERT INTO plan VALUES (?,?,?,?,?)",(psales,pems,ppismo,pposilka,data))
        base.commit()
        await bot.send_message(
            message.chat.id,
            md.text(
            md.text('План на месяц : ', md.bold(pla['plan4'])),
            md.text('План на розничных продажа:', pla['plan']),
            md.text('План ЕМС:',pla['plan1']),
            md.text('План 1кл письмо:',pla['plan2']),
            md.text('План 1кл посылок :', pla['plan3']), sep='\n'),reply_markup=kb_client)
        await state.finish()



"""" ******************************************     ОТПРАВЛЯЕМ ОТЧЕТ   ******************************************"""
@dp.message_handler(commands= "Отправить_отчет")
async def question1(message: types.Message):
    await message.answer('Как вас зовут?')
    await Test.Q1.set()

@dp.message_handler(state=Test.Q1)
async  def answer1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Q1'] = message.text
        time.sleep(1)
    await Test.next()
    await message.answer("Сколько ЕМС приняли?",reply_markup=kb_client2)


@dp.message_handler(state = Test.Q2)
async  def answer2(message:types.Message,state:FSMContext):
    async  with state.proxy() as data:
        data['Q2'] = message.text
        time.sleep(1)
        await Test.next()
        await message.answer("Сколько писем 1 класса без О/Ц приняли?",reply_markup=kb_client2)

@dp.message_handler(state = Test.Q3)
async  def answer3(message: types.Message,state:FSMContext):
    async  with state.proxy() as data:
        data['Q3'] = message.text
        time.sleep(1)

    await Test.next()
    await message.answer("Сколько не предзаполненных посылок 1 класса приняли?",reply_markup=kb_client2)

@dp.message_handler(state = Test.Q4)
async  def answer4(message:types.Message,state:FSMContext):
    async  with state.proxy() as data:
        data['Q4'] = message.text
        time.sleep(1)

    await Test.next()
    await message.answer("Сколько розничных продаж сделали?",reply_markup=kb_client)

@dp.message_handler(state = Test.Q5)
async def answer5(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['Q5'] = message.text
        time.sleep(1)
        base = sqlite3.connect('ops.db')
        id = message.from_user.id
        name = data['Q1']
        ems = data['Q2']
        pismo = data['Q3']
        posilka =data['Q4']
        sale = data['Q5']
        vremia = datetime.date.today()
        base = sqlite3.connect('ops.db')
        cur = base.cursor()
        cur.execute("INSERT INTO fakt VALUES (?,?,?,?,?,?,?)" , (id,name,ems,pismo,posilka,sale,vremia))
        base.commit()

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Спасибо за отчет', md.bold(data['Q1'])),
                md.text('Емс:', data['Q2']),
                md.text('1кл_письмо:',data['Q3']),
                md.text('1кл_посылка:',data['Q4']),
                md.text('Продажа:', data['Q5']),md.text('Дата:',vremia), sep='\n'))
        await state.finish()

"""""*****************************************      ОТЧЕТ ДНЯ     **********************************************"""

@dp.message_handler(commands= "Отчет_дня")
async def report_of_day(message: types.Message):
    bugun = datetime.date.today()
    base = sqlite3.connect('ops.db')
    cur = base.cursor()
    sales = cur.execute("SELECT SUM(sale) FROM fakt WHERE data == ?",(bugun,)).fetchone()
    emss = cur.execute("SELECT SUM(ems)FROM fakt WHERE data == ?",(bugun,)).fetchone()
    klasspk = cur.execute("SELECT SUM(pismo) FROM fakt WHERE data== ? ",(bugun,)).fetchone()
    poss = cur.execute("SELECT SUM(posilka) FROM fakt WHERE data == ?",(bugun,)).fetchone()
    base.commit()

    await bot.send_message(

        message.chat.id,
        md.text(md.bold('Дневной отчет ОПС 117513 '),
            md.text('Продажа:',sales,'руб'),
            md.text('Емс:', emss,'шт'),
            md.text('1 класс письмо:', klasspk,'шт'),
            md.text('1 класс посылка:', poss,'шт'), sep='\n'))


""" **********************************************  ОТЧЕТ МЕСЯЦА ******************************************* """

@dp.message_handler(commands= "Отчет_месяца")
async def report_of_month(message: types.Message):
    base = sqlite3.connect('ops.db')
    cur = base.cursor()
    sales = cur.execute("SELECT SUM(sale) FROM fakt").fetchone()
    emss = cur.execute("SELECT SUM(ems)FROM fakt").fetchone()
    klasspk = cur.execute("SELECT SUM(pismo) FROM fakt").fetchone()
    poss = cur.execute("SELECT SUM(posilka) FROM fakt").fetchone()
    plan_poss = cur.execute("SELECT plan_posilka FROM plan").fetchone()
    plan_emss = cur.execute("SELECT plan_ems FROM plan").fetchone()
    plan_saless = cur.execute("SELECT plan_sales FROM plan").fetchone()
    plan_piss = cur.execute("SELECT plan_pismo FROM plan").fetchone()
    yuzde_sales= (sales[0] / plan_saless[0] ) * 100
    yuzde_ems = (emss[0] / plan_emss[0]) * 100
    yuzde_klasspk = (klasspk[0] / plan_piss[0]) * 100
    yuzde_poss = (poss[0] /plan_poss[0])*100


    base.commit()
    await bot.send_message(

        message.chat.id,
        md.text(md.bold('Отчет месячний ОПС 117513'),
            md.text('Продажа:',sales[0],'руб',',','выполнение: ',"%",int(yuzde_sales)),
            md.text('Емс:', emss[0],'шт',',','выполнение: ','%',int(yuzde_ems)),
            md.text('1кл письмо:', klasspk[0],'шт',',','выполнение: ','%',int(yuzde_klasspk)),
            md.text('1кл посылка:', poss[0],'шт',',','выполнение: ','%',int(yuzde_poss)), sep='\n'))



""""  ********************************** Отправить Почту ************************************* """
@dp.message_handler(filters.IDFilter(user_id=1353075505),commands= "Email")
async def report_of_month(message: types.Message):
    send_me()
    await message.answer("Отчет на почту отправлено")


"""""  ********************************************  ДАТА ВИЗУАЛИЗАЦИЯ  ***************************************** """

@dp.message_handler(commands= "Дата_визуализация")
async def data_visualition(message:types.Message):
    dat = sqlite3.connect('ops.db')
    query = dat. execute("SELECT * From fakt")
    cols = [column[0] for column in query. description]
    results= pd.DataFrame.from_records(data = query. fetchall(), columns = cols)
    df = results.groupby('name').sum()
    df.reset_index(inplace=True)
    print(df)
    x1 = seaborn.barplot(x='name',y='sale',data=df,color="b",label="продажа")
    plt.savefig('sales.png')
    x2 = seaborn.relplot(x='name',y='ems',hue='name',data=results,palette = "muted")
    plt.savefig('ems.jpg')
    x3 = seaborn.relplot(x='ems',y = 'pismo',hue = 'name',kind="line",data=results)
    plt.savefig('pismo.png')
    x4 = seaborn.stripplot(x='ems',y='sale',hue='name',data=results)
    plt.savefig('posilka.jpg')
    photo = open('/app/sales.png','rb')
    photo1 = open('/app/ems.jpg','rb')
    foto = open('/app/pismo.png','rb')
    fato = open('/app/posilka.jpg','rb')

    await bot.send_photo(chat_id= message.chat.id,photo=photo)
    await bot.send_photo(chat_id= message.chat.id,photo=photo1)
    await bot.send_photo(chat_id= message.chat.id,photo=foto)
    await bot.send_photo(chat_id= message.chat.id,photo=fato)

""""" ***************************************   ПЛАН  ****************************************** """
@dp.message_handler(commands="План")
async def show_plan(message:types.Message):
    base = sqlite3.connect('ops.db')
    cur = base.cursor()
    planss = cur.execute("SELECT plan_sales FROM plan").fetchone()
    plansems = cur.execute("SELECT plan_ems FROM plan").fetchone()
    planspismo = cur.execute("SELECT plan_pismo FROM plan").fetchone()
    plansposilok = cur.execute("SELECT plan_posilka FROM plan").fetchone()
    plan_month = cur.execute("SELECT data FROM plan").fetchone()
    base.commit()
    await bot.send_message(

        message.chat.id,
        md.text(md.bold('План месяца ОПС 117513'),'\n',
                md.text('Месяц:',plan_month),'\n',
                md.text('План розничный продажа:', planss,'руб'),'\n',
                md.text('План ЕМС :', plansems,'шт'),'\n',
                md.text('План 1 класс письмо:', planspismo,'шт'),'\n',
                md.text('План 1 класс посылок :',plansposilok,'шт')))


""""" *************************** УДАЛЯЕМ ВСЕ **************************** """

@dp.message_handler(commands= "Delete_all")
async def report_of_month(message: types.Message):
    base = sqlite3.connect('ops.db')
    cur = base.cursor()
    cur.execute("DELETE FROM fakt").fetchall()
    cur.execute("DELETE FROM plan").fetchall()
    base.commit()

    await message.answer('Bсё данные из таблицы факт удалины, Можете начать снова!! ')

"""" ******************** Только Админ ******************************* """

@dp.message_handler(filters.IDFilter(user_id=1353075505),commands = "Admin")
async def admin_panel(message:types.Message):
    await message.answer('Добрый день, Admin! Что хотели бы сделать? Обращаю Ваше внимание , что для создания нового плана на месяц или для его корректировки, необходимо удалить введенные ранее данные с помощью /Delete_all', reply_markup=kb_client3)



"""" ********************************** Отчет Ваш *************************************** """

@dp.message_handler(commands= "Отчет_ваш")
async def report_of_month(message: types.Message):
        base = sqlite3.connect('ops.db')
        cur = base.cursor()
        prodaj = cur.execute("SELECT sum(sale) FROM fakt WHERE user_id == ? " ,(message.from_user.id,)).fetchone()
        emss = cur.execute("SELECT sum(ems) FROM fakt WHERE user_id == ?",(message.from_user.id,)).fetchone()
        pismos = cur.execute("SELECT sum(pismo) FROM fakt WHERE user_id == ?" ,(message.from_user.id,)).fetchone()
        posilkas = cur.execute("SELECT sum(posilka) FROM fakt WHERE user_id == ?" ,(message.from_user.id,)).fetchone()
        imya = cur.execute("SELECT name FROM fakt WHERE user_id == ?",(message.from_user.id,)).fetchone()
        base.commit()
        await bot.send_message(

            message.chat.id,
            md.text(md.bold('Отчет ваш на месяц'),'\n',
                    md.text('Сотрудник:',imya),'\n',
                    md.text('Итого роз. продажа:', prodaj,'руб'),'\n',
                    md.text('Итого ЕМС :', emss,'шт'),'\n',
                    md.text('Итого 1 класс письмо:', pismos,'шт'),'\n',
                    md.text('Итого 1 класс посылок :',posilkas,'шт')))


"""" ********* Главное ************ """

@dp.message_handler(commands= "Главное")
async def report_of_month(message: types.Message):
    await message.answer('Что вы хотите сделать?',reply_markup=kb_client)




async def parse():

    url = requests.get('https://www.pochta.ru/news')
    soup = BeautifulSoup(url.text,'html.parser')


    title = soup.find('a',class_='Linkstyles__LinkStyled-sc-1xo7cu-0 fSeBPp').text
    paragraph = soup.find('div',class_='Paragraph-sc-10hckd4-0 jcFakn').text
    tarih = soup.find('span',class_='Font-sc-le1wax-0 eLmwWf').text
    img_url = 'https://www.iphones.ru/wp-content/uploads/2017/06/pochta_featured-1240x580.jpg'
    text = md.text(
        md.text('Новости дня ' + emoji.emojize(":newspaper:")),'\n','\n',
        md.text(title),'\n',
        md.text(paragraph),'\n',
        md.text(tarih))
    await bot.send_message(-1001809364709, f'{text}<a href="{img_url}">.</a>', parse_mode=ParseMode.HTML)







def quiz():
    question = 'Сколько стоит отправить простое письмо до 20г по России?'
    chat_id = '-1001809364709'
    type_ = "quiz"
    correct_option_id = 2
    _TELEGRAM_BOT_TOKEN="5527521010:AAGkz20GIqmvoQigQNQzQ-u9ZLNUL139huE"

    options = ['50', '100', '25','75']
    uri = f'https://api.telegram.org/bot{_TELEGRAM_BOT_TOKEN}/sendPoll?chat_id={chat_id}&' \
          f'question={question}&options={json.dumps(options)}&type={type_}&correct_option_id={correct_option_id}' \
          f'&is_anonymous=True'
    requests.get(uri)
    return bot.send_message(chat_id=1927913960, text='спасибо')


async def report(message: types.Message):
    bugun = datetime.date.today()
    base = sqlite3.connect('ops.db')
    cur = base.cursor()
    sales = cur.execute("SELECT SUM(sale) FROM fakt WHERE data == ?",(bugun,)).fetchone()
    emss = cur.execute("SELECT SUM(ems)FROM fakt WHERE data == ?",(bugun,)).fetchone()
    klasspk = cur.execute("SELECT SUM(pismo) FROM fakt WHERE data== ? ",(bugun,)).fetchone()
    poss = cur.execute("SELECT SUM(posilka) FROM fakt WHERE data == ?",(bugun,)).fetchone()
    base.commit()

    await bot.send_message(

        message.chat.id,
        md.text(md.bold('Дневной отчет ОПС 117513 '),
                md.text('Продажа:',sales,'руб'),
                md.text('Емс:', emss,'шт'),
                md.text('1 класс письмо:', klasspk,'шт'),
                md.text('1 класс посылка:', poss,'шт'), sep='\n'))


async def remember():
    await bot.send_message(chat_id=(-1001809364709),text='коллеги отчет')

async def scheduler():
    aioschedule.every().monday.at("17:00").do(remember)
    aioschedule.every().tuesday.at("17:00").do(remember)
    aioschedule.every().wednesday.at("17:00").do(remember)
    aioschedule.every().thursday.at("17:00").do(remember)
    aioschedule.every().friday.at("17:00").do(remember)
    aioschedule.every().saturday.at("15:00").do(remember)

    aioschedule.every().monday.at("12:00").do(parse)
    aioschedule.every().tuesday.at("12:00").do(parse)
    aioschedule.every().wednesday.at("12:00").do(parse)
    aioschedule.every().thursday.at("12:00").do(parse)
    aioschedule.every().friday.at("12:00").do(parse)

    aioschedule.every().monday.at("13:00").do(quiz)
    aioschedule.every().tuesday.at("13:00").do(quiz)
    aioschedule.every().wednesday.at("13:00").do(quiz)
    aioschedule.every().thursday.at("13:00").do(quiz)
    aioschedule.every().friday.at("13:00").do(quiz)


    aioschedule.every().monday.at("18:00").do(report)
    aioschedule.every().tuesday.at("18:00").do(report)
    aioschedule.every().wednesday.at("18:00").do(report)
    aioschedule.every().thursday.at("18:00").do(report)
    aioschedule.every().friday.at("18:00").do(report)
    aioschedule.every().saturday.at("16:00").do(report)












    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
async def on_startup(_):
    asyncio.create_task(scheduler())






@dp.message_handler(commands= "Результат_Сотрудников")
async def report_of_month(message: types.Message):
    base = sqlite3.connect('ops.db')
    cur = base.cursor()
    Marina_sale = cur.execute("SELECT SUM(sale) FROM fakt WHERE name== ('Марина')").fetchone()
    Marina_ems = cur.execute("SELECT SUM(ems) FROM fakt WHERE name== ('Марина')").fetchone()
    Olga_sale = cur.execute("SELECT SUM(sale) FROM fakt WHERE name== ('Ольга')").fetchone()
    Olga_ems = cur.execute("SELECT SUM(ems) FROM fakt WHERE name== ('Ольга')").fetchone()
    Irina_sale = cur.execute("SELECT SUM(sale) FROM fakt WHERE name== ('Ирина')").fetchone()
    Irina_ems = cur.execute("SELECT SUM(ems) FROM fakt WHERE name== ('Ирина')").fetchone()
    Oksana_sale = cur.execute("SELECT SUM(sale) FROM fakt WHERE name== ('Оксана')").fetchone()
    Oksana_ems = cur.execute("SELECT SUM(ems) FROM fakt WHERE name== ('Оксана')").fetchone()
    Yulia_sale = cur.execute("SELECT SUM(sale) FROM fakt WHERE name== ('Юллия')").fetchone()
    Yulia_ems = cur.execute("SELECT SUM(ems) FROM fakt WHERE name== ('Юллия')").fetchone()
    Katya_sale = cur.execute("SELECT SUM(sale) FROM fakt WHERE name== ('Катя')").fetchone()
    Katya_ems = cur.execute("SELECT SUM(ems) FROM fakt WHERE name== ('Катя')").fetchone()
    Plan_sale = cur.execute("SELECT plan_sales FROM plan").fetchone()
    Plan_ems = cur.execute("SELECT plan_ems FROM plan").fetchone()
    print(Plan_ems)
    Plan_sales = Plan_sale[0] / 6
    Plan_emss = Plan_ems[0] / 6
    Marina_yuzde_sale = (Marina_sale[0] / Plan_sales) * 100
    Marina_yuzde_ems = (Marina_ems[0] / Plan_emss) * 100
    Olga_yuzde_sale = (Olga_sale[0] / Plan_sales) * 100
    Olga_yuzde_ems = (Olga_ems[0] / Plan_emss) * 100
    Irina_yuzde_sale = (Irina_sale[0] / Plan_sales) * 100
    Irina_yuzde_ems = (Irina_ems[0] / Plan_emss ) * 100
    Oksana_yuzde_sale = (Oksana_sale[0] / Plan_sales ) * 100
    Oksana_yuzde_ems = (Oksana_ems[0] / Plan_emss ) * 100
    Yulia_yuzde_sale = (Yulia_sale[0] / Plan_sales ) * 100
    Yulia_yuzde_ems = (Yulia_ems[0] / Plan_emss ) * 100
    Katya_yuzde_sale = (Katya_sale[0] / Plan_sales ) * 100
    Katya_yuzde_ems = (Katya_ems[0] / Plan_emss ) * 100

    await bot.send_message(
        message.chat.id,
        md.text(md.bold('Результат Сотрудников на месяц'),'\n',

                md.text('Продажа Марина:',Marina_sale[0],'руб'),
                md.text('Марина Емс:', Marina_ems[0],'шт'),
                md.text('Выпольнено план продажа:','%',int(Marina_yuzde_sale)),
                md.text('Выпольнено план емс:','%',int(Marina_yuzde_ems)),'\n',

                md.text('Продажа Ольга:',Olga_sale[0],'руб'),
                md.text('Марина Емс:', Olga_ems[0],'шт'),
                md.text('Выпольнено план продажа:','%',int(Olga_yuzde_sale)),
                md.text('Выпольнено план емс:','%',int(Olga_yuzde_ems)),'\n',

                md.text('Продажа Ирина:',Irina_sale[0],'руб'),
                md.text('Марина Емс:', Irina_ems[0],'шт'),
                md.text('Выпольнено план продажа:','%',int(Irina_yuzde_sale)),
                md.text('Выпольнено план емс:','%',int(Irina_yuzde_ems)),'\n',

                md.text('Продажа Оксана:',Oksana_sale[0],'руб'),
                md.text('Оксана Емс:', Oksana_ems[0],'шт'),
                md.text('Выпольнено план продажа:','%',int(Oksana_yuzde_sale)),
                md.text('Выпольнено план емс:','%',int(Oksana_yuzde_ems)),'\n',

                md.text('Продажа Юллия:',Yulia_sale[0],'руб'),
                md.text('Юллия Емс:', Yulia_ems[0],'шт'),
                md.text('Выпольнено план продажа:','%',int(Yulia_yuzde_sale)),
                md.text('Выпольнено план емс:','%',int(Yulia_yuzde_ems)),'\n',

                md.text('Продажа Катя:',Katya_sale[0],'руб'),
                md.text('Катя Емс:', Katya_ems[0],'шт'),
                md.text('Выпольнено план продажа:','%',int(Katya_yuzde_sale)),
                md.text('Выпольнено план емс:','%',int(Katya_yuzde_ems)),'\n',







                 sep='\n'))










if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)