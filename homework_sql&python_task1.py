import psycopg2

def delete_db(cur):
    """Удаление таблиц"""
    cur.execute("""
        DROP TABLE phones;
        DROP TABLE abonent;
    """)

def create_db(cur):
    """Создание таблиц в базе данных"""
    cur.execute("""
        CREATE TABLE IF NOT EXISTS abonent(
            id_abonent SERIAL PRIMARY KEY,
            name VARCHAR(60) NOT NULL,
            surname VARCHAR(60) NOT NULL,
            e_mail TEXT 
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id_phone SERIAL PRIMARY KEY,
            phone VARCHAR(20) NULL,
            id_abonent int REFERENCES abonent(id_abonent)
        );
    """)
    print('База данных создана')


def insert_abonent(cur, name = None, surname = None, e_mail = None, phone = None):
    """Добавление абонента"""
    cur.execute("""
        INSERT INTO abonent(name,surname,e_mail)
        VALUES(%s,%s,%s)
    """, (name, surname, e_mail))
    cur.execute("""
        SELECT id_abonent FROM abonent
        ORDER BY id_abonent DESC
        LIMIT 1
    """)
    print(f'Абонент {name, surname} добавлен')
    id_abonent = cur.fetchone()[0]
    if phone is not None:    
        insert_number(cur, phone, id_abonent)
        return id_abonent


def insert_number(cur, phone, id_abonent):
    """Добавление номера телефона"""
    cur.execute("""
        INSERT INTO phones(phone,id_abonent)
        VALUES(%s,%s)
    """,(phone,id_abonent))
    print(f'Номер {phone} для абонента {id_abonent} добавлен')


def update_abonent(cur,id_abonent, name = None, surname = None, e_mail = None, phone = None):
    """Обновление данных абонента"""
    if name is not None:
        cur.execute("""
            UPDATE abonent
            SET name = %s
            WHERE id_abonent = %s AND name <> %s
        """,(name,id_abonent,name))
        print(f'Имя абонента {id_abonent} изменено на {name}')       
    elif surname is not None:
        cur.execute("""
            UPDATE abonent
            SET surname = %s
            WHERE id_abonent = %s AND surname <> %s
        """,(surname,id_abonent,surname))
        print(f'Фамилия абонента {id_abonent}изменена на {surname}')
    elif e_mail is not None:
        cur.execute("""
            UPDATE abonent
            SET e_mail = %s
            WHERE id_abonent = %s AND e_mail <> %s
        """,(e_mail,id_abonent,e_mail))
        print(f'E-mail абонента {id_abonent} изменен на {e_mail}')
    elif phone is not None:
        cur.execute("""
            UPDATE phones
            SET phone = %s
            WHERE id_abonent = %s AND phone <> %s
        """,(phone,id_abonent, phone))
        print(f'Телефон абонента {id_abonent} изменен на {phone} ')
   

def delete_phone(cur, id_abonent,phone):
    """Удаление телефона"""
    cur.execute("""
        DELETE FROM phones
        WHERE id_abonent = %s AND phone = %s
    """,(id_abonent,phone))
    print(f'Телефон {phone} удален')


def delete_abonent(cur,id_abonent):
    """Удаление абонента"""
    cur.execute("""
        DELETE FROM phones
        WHERE id_abonent = %s
    """,[id_abonent])      
    cur.execute("""
        DELETE FROM abonent CASCADE
        WHERE id_abonent =%s
    """,[id_abonent])
    print(f'Абонент Id {id_abonent} удален')


def find_abonent(cur, name = None, surname = None, e_mail = None, phone = None):
    """Поиск всех данных абонента"""
    if phone is not None:
        cur.execute(""" 
            SELECT * FROM abonent a
            LEFT JOIN phones p ON a.id_abonent = p.id_abonent
            WHERE a.name LIKE %s OR a.surname LIKE %s 
            OR a.e_mail LIKE %s OR p.phone LIKE %s
        """,(name, surname, e_mail, phone))
    else:
         cur.execute(""" 
            SELECT * FROM abonent a
            LEFT JOIN phones p ON a.id_abonent = p.id_abonent
            WHERE a.name LIKE %s OR a.surname LIKE %s 
            OR a.e_mail LIKE %s 
        """,(name, surname, e_mail))  
    print(cur.fetchall())   


if __name__ =='__main__':
    name_database = ''
    user = ''
    password = ''
    with psycopg2.connect(database = name_database, user = user, password = password) as conn:    
        with conn.cursor() as cur:

            delete_db(cur)

            create_db(cur)

            insert_abonent(cur, 'Ivan','Ivanov','ivan@gmail.com','89111111122')
            insert_abonent(cur,'Marina','Marinina','marina@gmail.com','89991112233')
            insert_abonent(cur,'Vasya','Vasiliev','vasya@gmail.com','89992223344')
            insert_abonent(cur,'Peter','Petrov','peter@gmail.com','89993334455')
            insert_abonent(cur,'Ivan','Vasiliev','ivan_v@gmail.com','89994445566')

            insert_number(cur, '89223334455',1)
            insert_number(cur, '89335556677',4)
            insert_number(cur, '89224445566',2)
            
            update_abonent(cur, 4, 'Maria')

            delete_phone(cur,1,'89223334455')
            
            delete_abonent(cur,1)

            find_abonent(cur,None,'Vasiliev')



