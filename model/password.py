from datetime import datetime
from pathlib import Path
class BaseModel:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'
    def save(self):
        table_path = Path(self.DB_DIR / f'{self.__class__.__name__}.txt')
        
        if not table_path.exists():
            table_path.touch() #cria o arquivo table_touch caso ele não exista
        
        with open(table_path, 'a') as arq:
           arq.write("|".join(list(map(str, self.__dict__.values()))))
           arq.write('\n')
           
    @classmethod
    def get(cls):
        table_path = Path(cls.DB_DIR / f'{cls.__name__}.txt')
    
        if not table_path.exists():
            table_path.touch()
    
        with open(table_path, 'r') as arq: #separa o texto pela barra de navegação
            x = arq.readlines() 
            
        results = []
        
        atributes = vars(cls())
        print(atributes)
        
        for i in x:
            split_v = i.split('|')
            tmp_dict = dict(zip(atributes, split_v))
            results.append(tmp_dict)

        return results

class Password(BaseModel):
    def __init__(self, domain=None, password=None, expire=False):
        self.domain = domain
        self.password = password
        self.create_at = datetime.now().isoformat()

p1 = Password(domain='Youtube', password='abc')
Password.get()




# print("|".join(list(map(str, self.__dict__.values())))) # - percorre todos os valores dentro dessa lista

# print(self.__dict__.values())
       
    # with open(table_path, 'a')    
        # w -> escreve no arquivo
        # a -> escreve + o que já tinha no arquivo
        # r -> apenas lê o arquivo
