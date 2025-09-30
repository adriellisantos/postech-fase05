# DATATHON - Fase 5 - Pós Tech Data Analytics - FIAP - RM360405

## Descrição do projeto

Este projeto tem como objetivo construir um sistema de recomendação de candidatos para vagas de emprego utilizando técnicas de processamento de linguagem natural (NLP) e aprendizado de máquina. O sistema analisa informações detalhadas dos candidatos e das vagas, gera embeddings textuais para os perfis e realiza cálculo de similaridade para indicar os candidatos mais adequados para cada vaga.

## Streamlit  
🔗 [Link da aplicação no Streamlit](https://data-analytics-postech-fase05.streamlit.app)

## Youtube  
🎥 [Link do vídeo no Youtube](https://youtu.be/BPD_oQ_02zk)

## Stack utilizada

- Python 3
- Bibliotecas: pandas, numpy, matplotlib, seaborn, re, datetime, warnings
- NLP e embeddings: Sentence-Transformers (`paraphrase-multilingual-MiniLM-L12-v2``)
- Machine Learning: scikit-learn (train_test_split, métricas, cosine_similarity)
- Outras: pickle para serialização, huggingface_hub para autenticação e carregamento de modelos

## Como rodar o app localmente

1. Clone o repositório do projeto.
2. Certifique-se de ter os arquivos JSON de dados (`applicants.json`, `vagas.json`, `prospects.json`) na pasta do projeto.
3. Instale as dependências necessárias com: `pip install -r requirements.txt`
4. Execute o notebook ou o script Python principal que contém o pipeline completo para carregar os dados, processá-los, gerar embeddings, treinar o modelo e realizar recomendações.
5. O sistema irá gerar arquivos de modelo serializados para uso futuro e permitirá testar recomendações para vagas específicas.

## Instruções de instalação

- Instale o Python 3.7 ou superior.
- Instale as bibliotecas necessárias executando: `pip install numpy pandas matplotlib seaborn scikit-learn sentence-transformers`
- Tenha os arquivos JSON de dados necessários no diretório do projeto.

## Como treinar o modelo novamente

1. Prepare os dados JSON dos candidatos, vagas e prospects.
2. Execute o código para carregar e pré-processar os dados (tratamento, limpeza e normalização).
3. Gere embeddings para os perfis dos candidatos e das vagas usando os modelos Sentence-Transformer pré-treinados.
4. Aplique os pesos sobre os embeddings conforme definido para cada grupo de características.
5. Faça o merge dos dados para preparar os pares candidatos-vagas para o treinamento.
6. Treine o modelo utilizando os embeddings processados, calculando a similaridade de cosseno para recomendações.
7. Serialize os dataframes finais com os embeddings para uso futuro, salvando-os em arquivos `.pkl` com `pickle`.

## Arquivos neste diretório do Github  
- **Bases**: Pasta com os arquivos em `.json` utilizados para análise e treinamento
- **Embeddings**: Dataframes finais com os embedding para utilizar na aplicação web
- **Notebook do Machine Learning**: Contém o Notebook utilizado para desenvolvimento do processamento dos dados e treinamento dos embeddings processados.





