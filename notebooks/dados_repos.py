import requests
import pandas as pd

#  classe engloba a extração e transformação dos dados
class DadosRepositorios:

    # Construtor da  Classe para criação objetos e métodos
    def __init__(self, owner):
        # nome do dono da conta do github
        self.owner = owner        
        self.api_base_url = 'https://api.github.com'
        self.access_token='tokenGeradoGitHub'
        # cabeçalho com as informações completas para requisição
        self.headers = {'Authorization': 'Bearer ' + self.access_token,
                    'X-GitHub-Api-Version': '2022-11-28'}
    
    # Método para extração de dados de todos os repositórios
    # A ideia é que a classe seja a mais genérica possível, pois pode haver repositórios com mais de  6 páginas
    def lista_repositorios (self):
        repos_list = []
        for page_num in range(1, 20):
            try:
                    url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                    response = requests.get(url, headers=self.headers)
                    repos_list.append(response.json())
            except:
                    repos_list.append(None)                    
        return repos_list
    
    # Método para extração dos nomes dos repositórios
    def nomes_repos (self, repos_list): 
            repo_names=[] 
            for page in repos_list:
                    for repo in page:
                            try:
                                repo_names.append(repo['name'])
                            except: 
                                    pass
            return repo_names
    
    # Método para extração dos nomes das linguagens dentro do repositório
    def nomes_linguagens (self, repos_list):
        repo_languages=[]
        for page in repos_list:
            for repo in page:
                    try:
                            repo_languages.append(repo ['language'])
                    except:
                            pass
            return repo_languages
        
    # Transforma, junta as 2 listas (repositório e linguagens) em uma tabela (dataframe)   
    def cria_df_linguagens (self):
        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos (repositorios)
        linguagens = self.nomes_linguagens (repositorios)
        dados = pd.DataFrame()
        dados['repository_name'] = nomes
        dados['language'] = linguagens
        return dados
    
        
        
