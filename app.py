import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

#Define o título da página
st.set_page_config(
    page_title="Recomendações Inteligente",
    page_icon="🔍",
    layout="wide",
)

#Carregando os modelos  para gerar a compartibilidade
def carregar_dados():
    df_candidatos = pd.read_pickle("embeddings/df_finalcandidatos.pkl")
    df_vagas = pd.read_pickle("embeddings/df_finalvagas.pkl")
    df_applicants = pd.read_pickle("embeddings/df_applicants.pkl")
    df_vagas_additional = pd.read_pickle("embeddings/df_vagas.pkl")
    return df_vagas, df_candidatos, df_applicants, df_vagas_additional

    #Função para carregar os candidados, considerando apenas os 5 mais compativeis
def recomendar_candidatos_cosine(
    codigo_vaga_input, df_candidatos_final, df_vagas_final, df_applicants, top_n=5
):
    vaga_embed = df_vagas_final[df_vagas_final['codigo_vaga'] == codigo_vaga_input]
    if vaga_embed.empty:
        return pd.DataFrame()

    #Selecionando todas as colunas do df de vagas cujo nome contém a embedding
    embedding_cols_vaga = [c for c in df_vagas_final.columns if 'embedding' in c]
    embedding_cols_candidatos = [c for c in df_candidatos_final.columns if 'embedding' in c]

    # Extraindo os valores numéricos dos embeddings da vaga em questão
    vaga_vector = vaga_embed[embedding_cols_vaga].values
    candidatos_vectors = df_candidatos_final[embedding_cols_candidatos].values

    #Calculando a similaridade de cosseno entre o vetor da vaga e os vetores de todos os candidatos
    sim_scores = cosine_similarity(candidatos_vectors, vaga_vector).flatten()

    #Adicionando ao df de candidatos a coluna com o score de similaridade (cosseno)
    df_candidatos_final['score_cosine'] = sim_scores

    #Criando uma coluna com o score em formato percentual arredondado para duas casas decimais
    df_candidatos_final['score_cosine_percentual'] = (
        (df_candidatos_final['score_cosine'] * 100).round(2).astype(str) + '%'
    )
    #Garantindo que o código do profissional em df_applicants seja do tipo inteiro
    df_applicants['codigo_profissional'] = df_applicants['codigo_profissional'].astype(int)
    candidatos_com_info = df_candidatos_final.merge(
        df_applicants[['codigo_profissional', 'objetivo_profissional']],
        on='codigo_profissional',
        how='left'
    )
    #Renomeando a coluna score_cosine_percentual para Compatibilidade
    candidatos_com_info.rename(columns={'score_cosine_percentual': 'Compatibilidade'}, inplace=True)

    #Retornando apenas as colunas de interesse ordenadas pelo score de compatibilidade
    return (
        candidatos_com_info
        .sort_values('score_cosine', ascending=False)
        .head(top_n)[['codigo_profissional', 'objetivo_profissional', 'Compatibilidade']]
    )

df_vagas, df_candidatos, df_applicants, df_vagas_additional = carregar_dados()

#Ajustando o layout da página
st.markdown(
    """
    <style>
    .big-title {
        font-size: 2.2em;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 0.4em;
    }
    .description {
        font-size: 1.1em;
        text-align: center;
        color: #555;
        margin-bottom: 2em;
    }
    </style>
    <div class="big-title">🔍 Recomendações Inteligente</div>
    <div class="description">
        Este sistema utiliza <b>Inteligência Artificial</b> para recomendar os candidatos mais compatíveis
        com cada vaga disponível.  
        Escolha uma vaga e visualize os profissionais com maior afinidade de perfil.
    </div>
    """,
    unsafe_allow_html=True
)

#Criando duas abas
tab_vagas, tab_recomendacao = st.tabs(["📋 Vagas Disponíveis", "🤝 Recomendação de Candidatos"])

with tab_vagas:
     #Exibindo apenas as 10 primeiras colunas do DataFrame df_vagas_additional em uma tabela
    st.markdown("### Vagas em Aberto")
    colunas_para_mostrar = df_vagas_additional.columns[:10]
    st.dataframe(df_vagas_additional[colunas_para_mostrar], use_container_width=True)

with tab_recomendacao:
    st.markdown("### Top 5 Candidatos Recomendados")
    # Criando um selectbox com todos os códigos de vaga disponíveis
    codigo_vagas = df_vagas['codigo_vaga'].unique()
    codigo_vaga_input = st.selectbox("💼 Selecione o código da vaga:", codigo_vagas)

    if st.button("🚀 Recomendar Candidatos", type="primary"):
       #Chamando a função que calcula a compatibilidade para a vaga selecionada.
        resultado = recomendar_candidatos_cosine(
            codigo_vaga_input, df_candidatos.copy(), df_vagas, df_applicants
        )

        if resultado.empty:
            st.warning("⚠️ Nenhum candidato encontrado para esta vaga.")
        else:
             #Converte o código do profissional para string
            resultado['codigo_profissional'] = resultado['codigo_profissional'].astype(str)
            st.success("✅ Candidatos recomendados com sucesso!")
             # Exibe a lista dos candidatos recomendados em uma tabela ajustada a largura da página
            st.dataframe(resultado, use_container_width=True)
