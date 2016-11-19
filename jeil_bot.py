#-*- coding: utf-8 -*-

import os, time
import MySQLdb, telebot
from telebot import types


API_TOKEN = '293391591:AAF9eEZIu6IAIEAN9DoFKLBK57rc90BozIA'
bot = telebot.TeleBot(API_TOKEN)

user_dict={}

class User:
    def __init__(self, code):
        self.code=code
        self.b_name=""
        self.scno=""
        self.name=""
        self.pwd=""
        self.money=0
        self.m_name=[]
        self.m_var={}
        self.m_num={}
        self.tmp_m_name=""
        self.tmp_m_var=0
        self.tmp_m_num=0
#시작
@bot.message_handler(commands=['start'])
def start_bot(message):
    key=types.ReplyKeyboardHide(selective=False)
    chat_id=message.chat.id
    user_dict[chat_id]=1
    msg=bot.reply_to(message,"안녕하세요. 제일경제 은행 봇입니다.\n할당받으신 부스코드를 입력하시면 시작됩니다.\ndeveloper:yeonho",reply_markup=key)
    bot.register_next_step_handler(msg,insert_booth_code)

def insert_booth_code(message):
    try :
        code=int(message.text)
        key=types.ReplyKeyboardMarkup(row_width=1)
        button_1=types.KeyboardButton(u'확인')
        button_2=types.KeyboardButton(u'다시입력')
        key.add(button_1,button_2)
        db=MySQLdb.connect('db address','id','password','select databases',use_unicode=True,charset="utf8") cursor=db.cursor()
        cursor.execute("set names utf8")

        cursor.execute(u"select name from booth where no=%d" %(code))
        b_name_t=cursor.fetchall()
        if b_name_t:
            chat_id=message.chat.id
            user=User(code)
            b_name=b_name_t[0][0]
            user.b_name=b_name
            user_dict[chat_id]=user
            msg=bot.reply_to(message,u"입력하실 부스명: %s\n맞으시면 확인을 눌러주시고 틀리면 다시입력을 눌러주세요." %(b_name),reply_markup=key)
            db.close()
            bot.register_next_step_handler(msg,insert_boot_code_handle)
        else:
            msg=bot.reply_to(message,u"제대로 입력해주세요.")
            db.close()
            bot.register_next_step_handler(msg,insert_booth_code)
    except:
        msg=bot.reply_to(message,"숫자를 입력하세요..")
        bot.register_next_step_handler(msg,insert_booth_code)
def insert_boot_code_handle(message):
    try:
        if message.text==u"확인":
            key=types.ReplyKeyboardMarkup(row_width=1)
            button_1=types.KeyboardButton(u'구매')
            key.add(button_1)
            msg=bot.reply_to(message,u"부스등록을 하셧습니다!!\n구매 버튼을 누르시면 다음으로 넘어갑니다.",reply_markup=key)
            bot.register_next_step_handler(msg,start_buy)
        elif message.text==u"다시입력":
            key=types.ReplyKeyboardHide(selective=False)
            msg=bot.reply_to(message,u"할당받으신 부스코드를 입력하세요.",reply_markup=key)
            bot.register_next_step_handler(msg,insert_booth_code)
        else:
            msg=bot.reply_to(message,u"error: boot_handler")
    except:
        print "error: booth_handler"

def start_buy(message):
    try:
        if message.text==u"구매":
            key=types.ReplyKeyboardHide(selective=False)
            msg=bot.reply_to(message,u"학번을 입력하세요.",reply_markup=key)
            bot.register_next_step_handler(msg,input_scno)
        else:
            key=types.ReplyKeyboardMarkup(row_width=1)
            key.add(types.KeyboardButton("구매"))
            msg=bot.reply_to(message,u"구매 버튼을 눌러주세요!",reply_markup=key)
            bot.register_next_step_handler(msg,start_buy)
    except:
        print u"error: start_buy"
def input_scno(message):
    chat_id=message.chat.id
    user=user_dict[chat_id]
    user.scno=message.text
    user_dict[chat_id]=user

    msg=bot.reply_to(message,u"이름을 입력하세요")

    bot.register_next_step_handler(msg,input_name)
def input_name(message):
    chat_id=message.chat.id
    user=user_dict[chat_id]
    user.name=message.text
    user_dict[chat_id]=user

    msg=bot.reply_to(message,u"비밀번호를 입력하세요")
    bot.register_next_step_handler(msg,input_pwd)
def input_pwd(message):
    chat_id=message.chat.id
    user=user_dict[chat_id]
    user.pwd=message.text

    db=MySQLdb.connect('db address','id','password','select database',use_unicode=True,charset="utf8")
    cursor=db.cursor()
    cursor.execute("set names utf8")

    cursor.execute('select money from m_list_ where scno="%s" and nick="%s" and password="%s"' %(user.scno,user.name,user.pwd))

    money=cursor.fetchall()

    if money:
        user.money=money[0][0]
        user_dict[chat_id]=user 
        msg=bot.reply_to(message,u"%s님 반갑습니다!!\n구매하실 상품이름을 입력하세요~" %(user.name))
        bot.register_next_step_handler(msg,input_m_name)
    else:
        key=types.ReplyKeyboardMarkup(row_width=1)
        button_1=types.KeyboardButton("구매")
        key.add(button_1)

        msg=bot.reply_to(message,u"학번,이름,비밀번호가 틀렸습니다.",reply_markup=key)
        bot.register_next_step_handler(msg,start_buy)
def input_m_name(message):
    chat_id=message.chat.id
    user=user_dict[chat_id]
    
    db=MySQLdb.connect('db address','id','password','select database',use_unicode=True,charset="utf8")
    cursor=db.cursor()
    cursor.execute("set names utf8")
    
    cursor.execute('select m_var from `booth_%s` where m_name="%s"' %(user.b_name,message.text))
    m_var=cursor.fetchall()

    if m_var:
        db.close()
        user.tmp_m_name=message.text
        user.tmp_m_var=int(m_var[0][0])
        user_dict[chat_id]=user
        
        msg=bot.reply_to(message,u"구매할 물건 갯수를 입력하세요~")
        bot.register_next_step_handler(msg,input_m_num)
    else:
        db.close()
        msg=bot.reply_to(message,u"판매하지 않는 상품입니다. 다시 입력해주세요")
        bot.register_next_step_handler(msg,input_m_name)
        
def input_m_num(message):
    try:
        result_str=""
        chat_id=message.chat.id
        user=user_dict[chat_id]

        tmp_m_num=message.text 
        user.tmp_m_num=int(tmp_m_num)

        result_str+=u"상품명:%s\n개수:%d\n가격:%d" %(user.tmp_m_name,user.tmp_m_num,(user.tmp_m_var*user.tmp_m_num))

        key=types.ReplyKeyboardMarkup(row_width=1)
        button_1=types.KeyboardButton("확인")
        button_2=types.KeyboardButton("다시입력")
        key.add(button_1,button_2)

        msg=bot.reply_to(message,u"입력하신 정보가 맞으세요?\n%s" %(result_str),reply_markup=key)
        bot.register_next_step_handler(msg,buy_handler)

    except:
        msg=bot.reply_to(message,u"숫자를 입력하세요.")
        bot.register_next_step_handler(msg,input_m_num)
def buy_handler(message):
    if message.text==u"확인":
        result_str=""
        total_var=0
        chat_id=message.chat.id
        user=user_dict[chat_id]
        user.m_name.append(user.tmp_m_name)
        user.m_var[user.tmp_m_name]=user.tmp_m_var
        user.m_num[user.tmp_m_name]=user.tmp_m_num
        user_dict[chat_id]=user
        
        key=types.ReplyKeyboardMarkup(row_width=1)
        button_1=types.KeyboardButton(u"추가")
        button_2=types.KeyboardButton(u"계산")
        button_3=types.KeyboardButton(u"구매취소")
        key.add(button_1,button_2,button_3)

        for name in user.m_name:
            result_str+=u"상품명: %s\n갯수: %d\n가격: %d\n\n" %(name,user.m_num[name],(user.m_var[name]*user.m_num[name]))
            total_var+=user.m_var[name]*user.m_num[name]

        msg=bot.reply_to(message,u"장바구니에 추가 되었습니다.!!\n현재 장바구니\n%s\n총금액:%d\n더 구매하시려면 추가버튼을 눌러주세요!!" %(result_str,total_var),reply_markup=key)
        bot.register_next_step_handler(msg,buy_handler)
    elif message.text==u"다시입력" or message.text==u"추가":
        key=types.ReplyKeyboardHide(selective=False)
        msg=bot.reply_to(message,u"상품 이름을 입력하세요.",reply_markup=key)
        bot.register_next_step_handler(msg,input_m_name)
    elif message.text==u"구매취소":
        chat_id=message.chat.id
        user=user_dict[chat_id]
        user.m_name=[]
        user.m_num={}
        user.m_var={}
        user_dict[chat_id]=user

        key=types.ReplyKeyboardMarkup(row_width=1)
        button_1=types.KeyboardButton("구매")
        key.add(button_1)

        msg=bot.reply_to(message,u"구매를 취소하였습니다.",reply_markup=key)
        bot.register_next_step_handler(msg,start_buy)
    elif message.text==u"계산":
        chat_id=message.chat.id
        user=user_dict[chat_id] 
        result_str=""
        total_var=0

        #계산 영역
        #토탈 머니 계산
        for name in user.m_name:
            total_var+=user.m_var[name]*user.m_num[name]
        #잔액부족인지 체크
        if user.money-total_var>=0:
            #여기서부터 DB연동 후 기록 (제일귀찮...)
            db=MySQLdb.connect('db address','id','password','select database',use_unicode=True,charset="utf8")
            cursor=db.cursor()
            cursor.execute("set names utf8")

            #for 문으로 한번에 끝낸다!
            for name in user.m_name:
                #거래내역 추가
                use_money=user.m_num[name]*user.m_var[name]
                user.money=user.money-use_money
                cursor.execute(u'insert into `%s_%s` values("%s","%s",%d,%d,%d,now());'%(user.scno,user.name,user.b_name,name,user.m_num[name],use_money,user.money))
                #회원 잔액 변경
                cursor.execute(u'update m_list_ set money=%d where scno="%s" and nick="%s"'%(user.money,user.scno,user.name))
                #부스 수익 증가 && 현재수익 끌어오기
                cursor.execute(u'select totalmoney from booth where no=%d'%(user.code))
                booth_money=cursor.fetchall()
                booth_money=int(booth_money[0][0])
                cursor.execute(u'update booth set totalmoney=%d where no=%d'%(booth_money+use_money,user.code))

            #db 커밋 && 닫기
            db.commit()
            db.close()
            # 클래스 변수 초기화
            user.m_name=[]
            user.m_var={}
            user.m_num={}
            user_dict[chat_id]=user

            #버튼생성 && 메시지전송
            key=types.ReplyKeyboardMarkup(row_width=1)
            key.add(types.KeyboardButton("구매"))

            msg=bot.reply_to(message,u"성공적으로 구매하였습니다!!\n%s님의 잔액:%d\n%s 부스를 이용해주셔서 감사합니다."%(user.name,user.money,user.b_name),reply_markup=key)
            bot.register_next_step_handler(msg,start_buy)


        else:
            key=types.ReplyKeyboardMarkup(row_width=1)
            button_1=types.KeyboardButton("구매")
            key.add(button_1)
            
            msg=bot.reply_to(message,u"잔액이 부족합니다!!\n잔액: %d" %(user.money),reply_markup=key)

            bot.register_next_step_handler(msg,start_buy)





@bot.message_handler(func=lambda message: message.text!="/start", content_types=['text'])
def reconnect(message):
    try:
        chat_id=message.chat.id
        user_dict[chat_id]
    except:
        chat_id=message.chat.id
        user_dict[chat_id]=1
        key=types.ReplyKeyboardMarkup(row_width=1)
        key.add(types.KeyboardButton("/start"))
        bot.reply_to(message,u"서버와 연결이 끊어졌습니다. 다시 시작해주세요.",reply_markup=key)









try:
    now=time.localtime()
    print 'start %d:%d:%d' %(now.tm_hour,now.tm_min,now.tm_sec)
    bot.polling(none_stop=False)
except Exception as e:
    now=time.localtime()
    print "Error!!!"
    print e
    print 'restart %d:%d:%d' %(now.tm_hour,now.tm_min,now.tm_sec)

    os.system("python ./jeil_bot.py")
#bot.polling(none_stop=False)
