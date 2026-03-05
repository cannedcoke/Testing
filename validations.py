def validate_message(msg):
    msg = msg.strip()
    
    if not msg:
        return False

    if len(msg) > 50:
        return False
    return True

def formatted_message(nick,msg):
    return f"{nick}: {msg.strip()}"

def validate_nickname(nick):
    nick = nick.strip()
    
    if not nick:
        return False

    if len(nick) > 10:
        return False
    return True
    
def clientMsg(nick):
    msg = input(">")
    if not validate_message(msg):
        return False
    return formatted_message(nick,msg)
        
    
def get_nickname():
    while True:
        nick = input("Enter a nickname: ")
        if validate_nickname(nick):
            return nick
 