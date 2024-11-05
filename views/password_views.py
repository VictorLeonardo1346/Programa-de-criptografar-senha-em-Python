import string, secrets
import hashlib
import base64
from pathlib import Path #biblioteca do python que auxilia a gerenciar diretórios no programa. o path serve para passar o caminho de um arquivo para outro diretório
from cryptography.fernet import Fernet, InvalidToken 

class FernetHasher:         # o nome FernetHaser é utilizado pois é o nome do algoritmo que será utilizado para criar a criptografia
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase  #irá mostrar todos os caracteres em minúsculo e maiúsculo
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / 'keys' #diretório onde a chave criptografada será enviada
    
    def __init__(self, key): #metodo chamado quando é instanciado uma nova classe
        if not isinstance(key, bytes):
            key = key.encode()

        self.fernet = Fernet(key)

    @classmethod
    def _get_random_string(cls, length=25): # o cls informa ao programa que é um metodo de uma classe
        string = ''
        for i in range(length):
            string = string + secrets.choice(cls.RANDOM_STRING_CHARS)
           
        return string

    @classmethod
    def create_key(cls, archive=False):
        value = cls._get_random_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest() #codifica o valor string em byte #sha256 é uma hash #converte o valor em criptografia. A criptografia hash é apenas one way
        key = base64.b64encode(hasher)
        if archive:
            return key, cls.archive_key(key)
        return key, None

    @classmethod
    def archive_key(cls, key):
        file = 'key.key'
        while Path(cls.KEY_DIR / file).exists():
            file = f'key_{cls._get_random_string(length=5)}.key'

        with open(cls.KEY_DIR / file, 'wb') as arq:
            arq.write(key)

        return cls.KEY_DIR / file


    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.encrypt(value)

    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        
        try:
            return self.fernet.decrypt(value).decode()
        except InvalidToken as e:
            return 'Token inválido'
       
    




