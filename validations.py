# GREEN: se implementó validate_message de forma mínima para que pasen los tests
#       def validate_message(msg):
#           if not msg.strip():
#               return False
#           return True
def validate_message(msg):
    msg = msg.strip()
    
    if not msg:
        return False
# GREEN: se agregó la validación de longitud:
#       if len(msg) > 50:
#           return False
    if len(msg) > 50:
        return False
    return True

# REFACTOR: se limpió el código haciendo el strip una sola vez al principio
#       def validate_message(msg):
#           msg = msg.strip()
#           if not msg:
#               return False
#           if len(msg) > 50:
#               return False
#           return True

def formatted_message(nick,msg):
    return f"{nick}: {msg.strip()}"

# function taht validates if the name is valid
def validate_nickname(nick):
    nick = nick.strip()
    
    if not nick:
        return False

    if len(nick) > 10:
        return False
    return True

# enters the message
def clientMsg(nick):
    msg = input(">")
    if not validate_message(msg):
        return False
    return formatted_message(nick,msg)
        
# obtanines the nickname
def get_nickname():
    while True:
        nick = input("Enter a nickname: ")
        if validate_nickname(nick):
            return nick
 