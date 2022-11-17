# Crypto-Daily-Update
<h1 align="center">:file_cabinet: Crypto-Daily-Update.md</h1>

## :memo: Descrição
Este projeto tem como objetivo desenvolver um processo de ETL utilizando as ferramentas Apache Airflow e Google Big Query. Isso se dá ao desenvolver uma DAG no Airflow para extrair os dados da API, transformar no formato requerido e inserir as informações no banco de dados no BigQuery. Além disso, essa DAG contem um Crontime para que rode todo dia na hora requisitada. é fornecido também arquivo SQL para queries no Google Big Query que retorne o seguinte resultado:

-name
-snapshot_date
-current_price_usd
-price_delta_current_vs_7d
-price_delta_current_vs_14d
-market_cap_usd
-market_cap_delta_current_vs_7d
-market_cap_current_vs_14d

## :books: Funcionalidades
* <b>Funcionalidades</b>: Funções utilizadas no código
* -transforma(param): Função usada para realizar a transformação de um dataframe para o formato desejado, com colunas com valores( Nome da moeda, Valor, Margem de mercado, data, ...)
* -chamadaAPI(param): Função que define a chamada a API da CoinGecko, retornando um objeto dataframe e um objeto json com os dados recebidos.
* -obter_valor(param): Função que testa o resultado da chamada a API e atribui valor ao xcom
* -carrega_bigquery(param): Função que escreve o dataframe gerado pela chamada a API em table designada no BigQuery

<b>Tasks</b>: Tasks utilizadas no código ((begin >> obter_valores >> carregar_valores >> end))
- Begin: Utiliza DummyOperator para indicar incialização do fluxo
- obter_valor: Utiliza a função obter valores para processo de extração
- carregar_valores: Utiliza função carregar valores para processo de uploading dos dados ao banco localizado em dataset do BigQuery
- End: Utiliza DummyOperator para indicar fim do processo de ETL.

## :rocket: Rodando o projeto
Para rodar o repositório é necessário clonar o mesmo, e no caso de uso windows, configurar Docker para que os containers Airflow rodem apropriadamente. Após configuração do Docker execute o comando, dentro da pasta do projeto, no terminal. é necessário arquivo JSON de credenciais ao BigQuery, que deverá ser colado na pasta do projeto e ter seu caminho indicado em PATH.
```
<linha de comando>
docker-compose up

## :soon: Implementações possíveis
* Para o dado case, foi utilzado apenas uma task apra obtenção dos valores vindos da API, dado tamanho do set de dados e agilidade de conexão vista nos testes. Porém é possível utilizar uma abordagem de uma task por conversão (ex.:bitcoin->real, ethereum->euro), pois assim paralelizamos as tasks, continuando o processo caso alguma requisição falhe. Conforme o projeto é escalado, e mais dados são colhidos por chamada a API, essa abordagem de várias tasks pode se provar mais ágil na obtenção de resultados, demandando porém maior número de containers para rodar. 

