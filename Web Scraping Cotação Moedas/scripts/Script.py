class cotacao():
    
    def __init__(self):
        self.leitura_base()
        self.raspagem()
        self.transforma_tabela()
        
    def leitura_base(self):
        #Importação do metodo da lib
        from pandas import read_csv
        
        #Caminho do Arquivo
        path = '../database/moedas.csv'
        
        #Leitura do DF
        df = read_csv(path, sep=';', encoding='latin-1')

        #Criação da Lista
        lista = []
        for indice, linha in df.iterrows():
            lista.append(linha['moeda'])
    
        #Salvando a Lista em um escopo Global
        self.dados_moedas = lista
        
    def raspagem(self):
        from bs4 import BeautifulSoup
        import requests
        import urllib.parse
        
        #Web Service usado por mim
        headers = {
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'}
        
        #Listas Vázias pra inserção de dados
        lista_data = []
        lista_nomes = []
        
        #Criação de uma estrutura de repetição que vai inserir o Nome da moeda e o Valor dela em 2 listas
        i = 0
        while i < len(self.dados_moedas):
            
            #Formatando as moedas Tirando (' ')
            moeda_formatada = urllib.parse.quote(self.dados_moedas[i])
            
            #Link dos htmls que vamos usar composto por: https://www.google.com/search?q=cotacao + Moeda que queremos
            link = f'https://www.google.com/search?q=cotacao+{moeda_formatada}'

            #Requisição por meio de protocolo HTTP
            requisicao = requests.get(link, headers=headers)
            
            #Dados do Site (Html)
            html = BeautifulSoup(requisicao.text, "html.parser")
            
            #Buscando a span pela Classe 
            cotacao_moeda = html.find('span', class_='DFlfde SwHCTb')
            titulo_moeda = html.find('span', class_='vLqKYe')
            
            # Adicionar o dicionário à lista de dados
            lista_data.append(cotacao_moeda.get_text())
            lista_nomes.append(titulo_moeda.get_text())
           
            i += 1
            
        #Passando as listas para um Escopo Global
        self.lista_data = lista_data
        self.lista_nomes = lista_nomes
            
    def transforma_tabela(self):
        #Crianção do Dicionário:
        dic = {
            'moeda':self.lista_nomes,
            'valor R$':self.lista_data
        }
        
        #Importação do metodo da lib
        from pandas import DataFrame
        
        #Criação do DataFrame
        df_moeda = DataFrame(dic)
        
        #Salvando o Dataframe em um arquivo .xlsx
        df_moeda.to_excel('../database/Moedas.xlsx', index=False)
            