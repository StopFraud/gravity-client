import urllib.request, json, os,time,pika
import requests
cred_file="cred.txt"
def _cred(s,u,p):
    fh=open(cred_file,"a",encoding="utf-8")
#    fh=open(logfile,"a")
#    text=str(datetime.datetime.now())+" "+str(message)+"\r\n"
    text=s+","+u+","+p+"\r\n"
#    _log(text)
    fh.write(text)
    fh.close()
    return True

def service_check(pip):
    #2do: add json hostname to dns
    url= urllib.request.urlopen("http://json.stopfraud.cyou:8000")
    data = json.loads(url.read().decode())
    print(data)

    proxies={'https':'http://'+pip}
    print(proxies)


    d={'post_id':119, 'form_id':'62c2bb08', 'queried_id':119, 'form_fields[firstName]':data['name'], 'form_fields[lastName]':data['surname'], 'form_fields[contacts__email]':data['email'], 'form_fields[password]':data['password'], 'form_fields[address__countryCode]':'RU', 'form_fields[contacts__phone]':data['phone_full'], 'form_fields[field_4]':'on', 'form_fields[field_1]':'on','form_fields[field_2]':'on','form_fields[field_3]':'on','form_fields[lang]':'ru','action':'elementor_pro_forms_send_form', 'referrer':'https://clients.gravity-trade.com/ru'} 
#-m 30 '+proxy_str+'  https://clients.gravity-trade.com/wp-admin/admin-ajax.php'


#    d_json=json.dumps(d)
#    print(d_json)
 #   d_json[]['data[name]']=str(data["name"])
#    d_json[]['data[surname]']=str(data["surname"])
    print (d)
    try:
        r1 = requests.post('https://clients.gravity-trade.com/wp-admin/admin-ajax.php',data=d,proxies=proxies, timeout=15)
        print (r1.text)
        print (r1.status_code)
        if 'success":true' in r1.text:
            print('::::::::::Gravity reg OK:::::::::::')
            print(data['email'])
            print(data['password'])
            _cred('gravity',data['email'],data['password'])
    except Exception as e:
        print (e)
        pass
    
#    time.sleep(13)






def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    service_check(body.decode("utf-8"))


RABBITMQ_SERVER=os.getenv("RABBITMQ_SERVER")
RABBITMQ_USER=os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD=os.getenv("RABBITMQ_PASSWORD")



while True:
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(RABBITMQ_SERVER,
                                       5672,
                                       '/',
                                       credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
#        channel.basic_qos(prefetch_count=1, global_qos=False)
        channel.queue_declare(queue='gravity')
        channel.basic_consume(queue='gravity', on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
#    except pika.exceptions.AMQPConnectionError:
#        print ("retry connecting to rabbit")
#        time.sleep(6)
    except Exception as e1:
        print (e1)
        print ("retry connecting to rabbit")
        time.sleep(6)

